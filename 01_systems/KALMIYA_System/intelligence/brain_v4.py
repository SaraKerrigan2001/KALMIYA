"""
brain_v4.py — Cerebro Modernizado de KALMIYA usando LangChain
===================================================================
Versión 2.0: Utiliza conectores oficiales de LangChain para enrutamiento
de LLMs locales y en la nube.
"""

import os
import sys
from typing import Any, List
from decouple import config

# Apuntar a la raíz de KALMIYA_System para poder importar database, os_ops, etc.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import log_command, save_thought
from _logging import get_logger
try:
    from kalmiya_tools_schema import OPENAI_TOOLS
except ImportError:
    from kalmiya.kalmiya_tools_schema import OPENAI_TOOLS

logger = get_logger(__name__)

# Dependencias de LangChain
try:
    from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
    from langchain_ollama import ChatOllama
    from langchain_openai import ChatOpenAI
    LANGCHAIN_OK = True
except ImportError as e:
    LANGCHAIN_OK = False
    SystemMessage = HumanMessage = AIMessage = None  # type: ignore
    ChatOllama = ChatOpenAI = None  # type: ignore
    logger.warning(f"[BRAIN v4] Faltan dependencias de LangChain: {e}")

# Configuración básica (API Keys y Modelos)
def _clean_key(key: object) -> str:
    key_str = str(key or "").strip()
    if key_str.startswith('TU_') and key_str.endswith('_AQUI'):
        return ''
    if key_str == 'TU_API_KEY_AQUI':
        return ''
    return key_str

AI_MODEL           = str(config('AI_MODEL',           default='llama3.2'))
GEMINI_KEY         = _clean_key(str(config('GEMINI_API_KEY',      default='')))
CLAUDE_KEY         = _clean_key(str(config('CLAUDE_API_KEY',      default='')))
CLAUDE_MODEL       = str(config('CLAUDE_MODEL',        default='claude-opus-4-8'))
GROQ_KEY           = _clean_key(str(config('GROQ_API_KEY',        default='')))
GROQ_MODEL         = str(config('GROQ_MODEL',          default='llama-3.3-70b-versatile'))
OPENROUTER_KEY     = _clean_key(str(config('OPENROUTER_API_KEY',  default='')))
OPENROUTER_MODEL   = str(config('OPENROUTER_MODEL',    default='meta-llama/llama-3.3-70b-instruct:free'))
COHERE_KEY         = _clean_key(str(config('COHERE_API_KEY',      default='')))
COHERE_MODEL       = str(config('COHERE_MODEL',        default='command-r-plus'))
AI_MODE            = str(config('AI_MODE',             default='auto'))
BOTNAME            = str(config('BOTNAME',             default='KALMIYA'))
USERNAME           = str(config('USER',                default='Sara'))

_conversation_history: list[dict] = []
MAX_HISTORY = 10  # Reducido para ahorrar memoria
_active_engine = "ninguno"
_pending_questions: list[str] = []

def _build_system_prompt(extra_context: str = '') -> str:
    """Reutiliza el prompt original del sistema de la personalidad de KALMIYA."""
    try:
        from intelligence.brain import _build_system_prompt as build_classic_prompt
        return build_classic_prompt(extra_context)
    except Exception:
        return f"Eres {BOTNAME}, un asistente inteligente creado por {USERNAME}."

def _convert_history_to_langchain(user_input: str, system_prompt: str) -> List[Any]:
    """Convierte el historial de KALMIYA al formato de mensajes de LangChain."""
    if not LANGCHAIN_OK or SystemMessage is None or HumanMessage is None or AIMessage is None:
        return []

    messages: List[Any] = [SystemMessage(content=system_prompt)]
    for msg in _conversation_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
            
    if not _conversation_history or _conversation_history[-1]["content"] != user_input:
        messages.append(HumanMessage(content=user_input))
        
    return messages

def _get_langchain_model(engine: str) -> Any:
    """Retorna la instancia del modelo de LangChain correspondiente."""
    if not LANGCHAIN_OK:
        return None

    if engine == 'ollama' and ChatOllama is not None:
        return ChatOllama(model=AI_MODEL)
        
    elif engine == 'gemini' and ChatOpenAI is not None:
        if not GEMINI_KEY:
            return None
        return ChatOpenAI(
            model="gemini-1.5-flash",
            api_key=GEMINI_KEY,  # type: ignore
            base_url="https://generativelanguage.googleapis.com/v1beta/openai"
        )
        
    elif engine == 'groq' and ChatOpenAI is not None:
        if not GROQ_KEY:
            return None
        return ChatOpenAI(
            model=GROQ_MODEL,
            api_key=GROQ_KEY,  # type: ignore
            base_url="https://api.groq.com/openai/v1"
        )
        
    elif engine == 'openrouter' and ChatOpenAI is not None:
        if not OPENROUTER_KEY:
            return None
        return ChatOpenAI(
            model=OPENROUTER_MODEL,
            api_key=OPENROUTER_KEY,  # type: ignore
            base_url="https://openrouter.ai/api/v1"
        )
        
    return None

def _route_to_engine_langchain(user_input: str, engine: str, extra_context: str = '') -> str:
    """Invoca el LLM correspondiente usando la abstracción de LangChain."""
    global _active_engine
    
    if not LANGCHAIN_OK:
        return "LangChain no está configurado."
        
    model = _get_langchain_model(engine)
    if not model:
        try:
            from intelligence.brain import _build_local_reasoning_response
            return _build_local_reasoning_response(user_input, extra_context)
        except Exception:
            return "El motor seleccionado no está disponible y el fallback falló."
            
    _active_engine = f"{engine.upper()} (LangChain)"
    
    # 1. Construir prompt y mensajes
    sys_prompt = _build_system_prompt(extra_context)
    messages = _convert_history_to_langchain(user_input, sys_prompt)
    
    # 2. Vincular herramientas (Tool Calling)
    if OPENAI_TOOLS and engine in ('gemini', 'groq', 'openrouter'):
        try:
            model = model.bind_tools(OPENAI_TOOLS)
        except Exception as e:
            logger.warning(f"[BRAIN v4] No se pudieron vincular herramientas a {engine}: {e}")
            
    # 3. Invocar con Agent Loop (Max 3 interacciones)
    from langchain_core.messages import ToolMessage
    from intelligence.tools_executor import execute_tool
    
    max_steps = 3
    current_step = 0
    while current_step < max_steps:
        try:
            response = model.invoke(messages)
            messages.append(response)
            
            # 4. Procesar llamadas a herramientas nativas
            if hasattr(response, 'tool_calls') and response.tool_calls:
                for tool_call in response.tool_calls:
                    func_name = tool_call.get('name')
                    func_args = tool_call.get('args', {})
                    tool_id = tool_call.get('id')
                    
                    try:
                        logger.info(f"[TOOL_CALL] {func_name} {func_args}")
                        tool_result = execute_tool(func_name, func_args)
                        messages.append(ToolMessage(content=tool_result, tool_call_id=tool_id))
                    except Exception as e:
                        messages.append(ToolMessage(content=f"Error: {e}", tool_call_id=tool_id))
                current_step += 1
                continue
            
            result = response.content
            if isinstance(result, list):
                return ' '.join(str(part) for part in result).strip()
            return str(result).strip()
            
        except Exception as e:
            logger.error(f"[BRAIN v4] Error invocando modelo: {e}")
            break
            
    return "Error: Superado el maximo de pasos de herramientas o el modelo falló."


def ask_kalmiya(user_input: str, force_engine: str = '') -> str:
    """Función principal del cerebro v4 compatible con la v1."""
    global _conversation_history
    
    _conversation_history.append({"role": "user", "content": user_input})
    if len(_conversation_history) > MAX_HISTORY:
        _conversation_history = _conversation_history[-MAX_HISTORY:]
        
    engine = str(force_engine).lower() if force_engine else str(AI_MODE).lower()
    
    if engine == 'auto':
        try:
            import requests
            r = requests.get("http://localhost:11434/api/tags", timeout=1)
            ollama_ok = (r.status_code == 200)
        except Exception:
            ollama_ok = False
            
        if ollama_ok:
            engine = 'ollama'
        elif GEMINI_KEY:
            engine = 'gemini'
        elif GROQ_KEY:
            engine = 'groq'
        else:
            engine = 'local'
            
    if engine == 'local':
        try:
            from intelligence.brain import _build_local_reasoning_response
            raw_response = _build_local_reasoning_response(user_input)
        except Exception:
            raw_response = "Modo de respaldo local falló."
    else:
        raw_response = _route_to_engine_langchain(user_input, engine)
        
    try:
        from intelligence.brain import _extract_question, _blockchain_ledger
        clean_response, question = _extract_question(raw_response)
        if question:
            _pending_questions.append(question)
        
        _conversation_history.append({"role": "assistant", "content": clean_response})
        _blockchain_ledger.record({"user": user_input, "assistant": clean_response, "engine": _active_engine})
        log_command(user_input, clean_response, source=f'ai-v4-{_active_engine}')
        save_thought(f"[v4-{_active_engine}] {clean_response[:100]}...")
        return clean_response
    except Exception:
        _conversation_history.append({"role": "assistant", "content": raw_response})
        return raw_response

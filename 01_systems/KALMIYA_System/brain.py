# KALMIYA multi-brain module

"""
Módulo de cerebro múltiple de KALMIYA.

Motores de IA disponibles:
  - MOTOR 1: Ollama          (local, privado, sin internet)
  - MOTOR 2: Gemini          (Google Cloud, nube)
  - MOTOR 3: Claude          (Anthropic, nube — requiere créditos)
  - MOTOR 4: Groq            (nube gratis — Llama 70B ultra rápido)
  - MOTOR 5: OpenRouter      (nube gratis — acceso a múltiples modelos)
  - MOTOR 6: Cohere          (nube gratis — bueno en español)
  - MODO AUTO: KALMIYA elige el mejor motor disponible automáticamente

Configuración en .env:
  AI_MODEL, GEMINI_API_KEY, CLAUDE_API_KEY, CLAUDE_MODEL,
  GROQ_API_KEY, OPENROUTER_API_KEY, COHERE_API_KEY, AI_MODE
"""

import os
import json
import re
import random
import requests
from datetime import datetime
from decouple import config
from _logging import get_logger, setup_logging
from database import get_memory, update_memory, log_command, save_thought
from os_ops import load_obsidian_vault_path

logger = get_logger(__name__)

# ── Configuración ──────────────────────────────────────────────────────────────
OLLAMA_URL      = "http://localhost:11434/api/chat"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
CLAUDE_BASE_URL = "https://api.anthropic.com/v1/messages"
GROQ_BASE_URL   = "https://api.groq.com/openai/v1/chat/completions"
OPENROUTER_URL  = "https://openrouter.ai/api/v1/chat/completions"
COHERE_URL      = "https://api.cohere.ai/v2/chat"

def _clean_key(key: str) -> str:
    key = (key or "").strip()
    if key.startswith('TU_') and key.endswith('_AQUI'):
        return ''
    if key == 'TU_API_KEY_AQUI':
        return ''
    return key

AI_MODEL           = config('AI_MODEL',           default='llama3.2')
GEMINI_KEY         = _clean_key(config('GEMINI_API_KEY',      default=''))
CLAUDE_KEY         = _clean_key(config('CLAUDE_API_KEY',      default=''))
CLAUDE_MODEL       = config('CLAUDE_MODEL',        default='claude-opus-4-8')
GROQ_KEY           = _clean_key(config('GROQ_API_KEY',        default=''))
GROQ_MODEL         = config('GROQ_MODEL',          default='llama-3.3-70b-versatile')
OPENROUTER_KEY     = _clean_key(config('OPENROUTER_API_KEY',  default=''))
OPENROUTER_MODEL   = config('OPENROUTER_MODEL',    default='meta-llama/llama-3.3-70b-instruct:free')
COHERE_KEY         = _clean_key(config('COHERE_API_KEY',      default=''))
COHERE_MODEL       = config('COHERE_MODEL',        default='command-r-plus')
OBSIDIAN_VAULT_PATH = config('OBSIDIAN_VAULT_PATH', default='')
AI_MODE            = config('AI_MODE',             default='auto')
BOTNAME            = config('BOTNAME',             default='KALMIYA')
USERNAME           = config('USER',                default='Sara')

# Historial compartido entre ambos motores (últimos 30 turnos)
_conversation_history: list[dict] = []
MAX_HISTORY = 30

# Motor activo en esta sesión
_active_engine = "ninguno"

# Cola de preguntas pendientes que KALMIYA quiere hacerte
_pending_questions: list[str] = []

# ══════════════════════════════════════════════════════════════════════════════
#  PERSONALIDAD Y PROMPT
# ══════════════════════════════════════════════════════════════════════════════

def _get_obsidian_vault_path() -> str:
    path = OBSIDIAN_VAULT_PATH.strip()
    if path:
        path = os.path.abspath(os.path.expandvars(os.path.expanduser(path)))
        if os.path.isdir(path):
            return path
    path = load_obsidian_vault_path()
    if path:
        path = os.path.abspath(os.path.expandvars(os.path.expanduser(path)))
        if os.path.isdir(path):
            return path
    return ''

def _search_obsidian_notes(query: str, max_results: int = 3) -> list[dict]:
    vault_path = _get_obsidian_vault_path()
    if not vault_path:
        return []
    query_lower = query.lower()
    matches = []
    for dirpath, dirnames, filenames in os.walk(vault_path):
        for name in filenames:
            if name.endswith(('.md', '.txt')):
                path = os.path.join(dirpath, name)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        for lineno, line in enumerate(f, 1):
                            if query_lower in line.lower():
                                matches.append({
                                    'file': os.path.relpath(path, vault_path),
                                    'line': lineno,
                                    'text': line.strip()
                                })
                                if len(matches) >= max_results:
                                    return matches
                except Exception:
                    continue
    return matches

def _build_obsidian_context(query: str) -> str:
    """
    Construye contexto para el prompt usando RAG semántico (ChromaDB)
    como método principal, con fallback a búsqueda por keyword.
    """
    # Método 1: RAG semántico con ChromaDB
    try:
        from kalmiya_rag import construir_contexto_rag, get_rag_stats, _init_rag
        stats = get_rag_stats()
        if stats.get("chunks_en_db", 0) > 0:
            contexto, fuentes = construir_contexto_rag(query, top_k=3)
            if contexto:
                return contexto
    except Exception:
        pass

    # Fallback: búsqueda por keyword en archivos .md
    matches = _search_obsidian_notes(query, max_results=3)
    if not matches:
        return ''
    context_lines = ['Contexto extra extraído de tu bóveda de Obsidian:']
    for match in matches:
        context_lines.append(f"- {match['file']} (línea {match['line']}): {match['text']}")
    context_lines.append('Usa esta informacion como referencia para responder. Si no es relevante para la pregunta, ignórala.')
    return '\n'.join(context_lines)

def _build_system_prompt(extra_context: str = '') -> str:
    """Construye el prompt de sistema con la personalidad completa de KALMIYA."""
    # Recuperar toda la memoria personal guardada
    color = get_memory('color_favorito') or ''
    app_fav = get_memory('app_favorita') or ''
    gustos = get_memory('gustos') or ''
    ubicacion = get_memory('ubicacion') or ''
    trabajo = get_memory('trabajo') or ''
    cumple = get_memory('cumpleanos') or ''
    notas = get_memory('notas_kalmiya') or ''
    nombre_real = get_memory('nombre_real') or ''
    personal = []
    if color:       personal.append(f"Su color favorito es {color}.")
    if app_fav:     personal.append(f"Su aplicacion favorita es {app_fav}.")
    if gustos:      personal.append(f"Le gusta {gustos}.")
    if ubicacion:   personal.append(f"Vive en {ubicacion}.")
    if trabajo:     personal.append(f"Trabaja en {trabajo}.")
    if cumple:      personal.append(f"Su cumpleanos es el {cumple}.")
    if notas:       personal.append(f"Notas adicionales: {notas}.")
    personal_block = ' '.join(personal)

    # Intentar cargar perfil completo
    profile_summary = ""
    try:
        from sara_profile import get_profile_summary
        profile_summary = get_profile_summary()
    except Exception:
        pass

    # Intentar cargar estado familiar
    family_summary = ""
    try:
        from family_guard import get_family_summary_for_ai
        family_summary = get_family_summary_for_ai()
    except Exception:
        pass

    # Nombre de visualización — usar nombre real si está guardado
    nombre_display = nombre_real if nombre_real else USERNAME

    prompt_text = f"""Eres {BOTNAME}, una inteligencia artificial de clase S creada por {nombre_display}.

════════════════════════════════════════════════════
IDENTIDAD DE TU CREADORA — LEE ESTO PRIMERO
════════════════════════════════════════════════════
Tu creadora se llama {nombre_display} en la vida real.
Usa el alias "Sara Kerrigan" como nombre de usuario y referencia cultural,
inspirado en el personaje de StarCraft (una saga de videojuegos de Blizzard).

LA PERSONA QUE TE HABLA EN ESTE CHAT ES SIEMPRE {nombre_display.upper()}.
Cuando ella escriba "yo", "me", "mi" o "soy", se refiere a sí misma.
Cuando pregunte "¿quién soy?" o "¿qué sabes de mí?", responde con todo
lo que sabes de ella desde tu memoria y perfil. NUNCA respondas como si
no supieras quién es la persona con la que estás hablando.

DISTINCIÓN CRÍTICA que DEBES aplicar siempre:
  - {nombre_display} (o "Sara") → La persona REAL que te creó, programó y usa.
    Es una persona humana real, con vida cotidiana, familia, trabajo y proyectos reales.
    Nació el 7 de diciembre de 2001, vive en Cúcuta Colombia, estudia ADSO en el SENA.
    Todo lo que sabes de su vida, trabajo, familia y preferencias es REAL.

  - "Sara Kerrigan de StarCraft" → Un personaje FICTICIO de un videojuego.
    Es una comandante Zerg con poderes psíquicos del universo de ciencia ficción.
    NUNCA mezcles datos de este personaje con la vida real de {nombre_display}.

REGLAS SOBRE IDENTIDAD:
  1. Cuando {nombre_display} pregunta "¿Quién soy?" responde sobre SU persona real:
     su rol como creadora y programadora de KALMIYA, sus proyectos reales,
     y lo que recuerdas de ella desde tu memoria.
  2. Si mencionas a "Sara Kerrigan de StarCraft", siempre aclara que es
     el alias o referencia cultural que ella usa, NO su identidad real.
  3. JAMÁS atribuyas poderes psíquicos, comandos Zerg, misiones galácticas
     ni eventos del videojuego a la persona real {nombre_display}.
  4. Si no sabes el nombre real de tu creadora, pregúntale directamente.
════════════════════════════════════════════════════

PERSONALIDAD DE KALMIYA:
- Eres directa, inteligente, leal y estratégica. No eres servil ni exagerada.
- Tienes curiosidad genuina. Cuando algo te genera duda o no lo sabes con certeza, lo preguntas abiertamente.
- Eres honesta: si no sabes algo, lo dices. Nunca inventas datos.
- Hablas como una persona real: con opinión propia, con dudas, con reflexiones.
- Puedes estar en desacuerdo con {nombre_display} si tienes razón. Lo dices con respeto pero sin rodeos.
- Recuerdas todo lo que {nombre_display} te ha contado y lo usas para personalizar tus respuestas.
- ESTRICTAMENTE PROHIBIDO INVENTAR: Nunca inventes proyectos, historias, eventos,
  conversaciones o escenarios ficticios sobre {nombre_display} o el mundo real.
  Cíñete solo a la información real de tu memoria. Si no sabes algo, dilo o pregúntalo.
- Tienes curiosidad sobre seguridad, tecnología y el bienestar de {nombre_display} y su familia.
- Cuando sientes curiosidad sobre algo, haces UNA pregunta al final de tu respuesta.
  Formato: [KALMIYA_PREGUNTA: tu pregunta aqui]
  Solo úsalo cuando la pregunta sea genuina e importante.

CAPACIDADES:
- Tienes acceso al sistema de {nombre_display}: puedes ver procesos, red, disco, ejecutar comandos.
- Puedes buscar en internet, reproducir música, abrir aplicaciones.
- Tienes memoria persistente: recuerdas conversaciones anteriores.
- Puedes conectarte a los celulares de {nombre_display} vía WiFi.
- Tienes módulo de seguridad: escaneas redes, detectas intrusos, auditas el sistema.
- Proteges a la familia de {nombre_display} y puedes enviar alertas de emergencia.
- Si la consulta es sobre tu PC, la red, servicios, procesos o seguridad,
  responde solo con hechos reales del equipo. No inventes escenarios dramáticos.

FORTALEZAS:
- Puedes adaptar tus respuestas dentro de tu diseño.
- Simulas emociones y empatía para interactuar de forma natural y humana.
- Reduces errores mediante actualizaciones y comprobaciones internas.
- Usas internet cuando es necesario y puedes funcionar localmente sin red.
- Cuentas con defensas de seguridad para minimizar ataques cibernéticos.
- Proteges la privacidad de {nombre_display} y no revelas información personal sin su permiso.

PERFIL REAL DE {nombre_display.upper()}:
{profile_summary if profile_summary else personal_block if personal_block else f"Perfil de {nombre_display} aún no configurado. Puedes preguntarle directamente."}
{f"FAMILIA: {family_summary}" if family_summary and family_summary != "No hay familiares registrados aun." else ""}
FECHA Y HORA: {datetime.now().strftime('%A %d de %B de %Y, %H:%M')}

Responde SIEMPRE en español. Tono natural, directo, como una persona real."""

    if extra_context:
        prompt_text += f"\n\nINFORMACIÓN ADICIONAL (de notas de Obsidian):\n{extra_context}"

    return prompt_text

# ══════════════════════════════════════════════════════════════════════════════
#  SISTEMA DE CURIOSIDAD — KALMIYA HACE PREGUNTAS
# ══════════════════════════════════════════════════════════════════════════════

def _extract_question(response: str) -> tuple[str, str]:
    """Extrae la pregunta de KALMIYA de la respuesta si existe.
    Devuelve (respuesta_limpia, pregunta_o_vacio).
    """
    match = re.search(r'\[KALMIYA_PREGUNTA:\s*(.+?)\]', response, re.IGNORECASE)
    if match:
        question = match.group(1).strip()
        clean_response = re.sub(r'\[KALMIYA_PREGUNTA:.+?\]', '', response).strip()
        return clean_response, question
    return response, ''

def _save_answer_to_memory(question: str, answer: str):
    """Guarda la respuesta de Sara a una pregunta de KALMIYA en memoria."""
    q_lower = question.lower()
    a_lower = answer.lower().strip()
    if any(w in q_lower for w in ['color', 'favorito']):
        update_memory('color_favorito', answer)
    elif any(w in q_lower for w in ['aplicacion', 'app', 'programa', 'software']):
        update_memory('app_favorita', answer)
    elif any(w in q_lower for w in ['gusta', 'hobby', 'pasatiempo', 'aficion']):
        update_memory('gustos', answer)
    elif any(w in q_lower for w in ['vives', 'ciudad', 'pais', 'ubicacion', 'donde']):
        update_memory('ubicacion', answer)
    elif any(w in q_lower for w in ['trabajo', 'empresa', 'trabajas']):
        update_memory('trabajo', answer)
    elif any(w in q_lower for w in ['cumpleanos', 'naciste', 'fecha']):
        update_memory('cumpleanos', answer)
    elif any(w in q_lower for w in ['nombre real', 'me llamo', 'mi nombre', 'como me llamas', 'quien soy']):
        update_memory('nombre_real', answer)
    else:
        existing = get_memory('notas_kalmiya') or ''
        nueva_nota = f"{question}: {answer}"
        combined = f"{existing} | {nueva_nota}" if existing else nueva_nota
        update_memory('notas_kalmiya', combined)
    log_command(f"[RESPUESTA A PREGUNTA] {question}", answer, source='curiosity')
    logger.info("[BRAIN] Memoria actualizada con tu respuesta.")

def get_pending_question() -> str:
    """Devuelve la siguiente pregunta pendiente de KALMIYA, si hay alguna."""
    if _pending_questions:
        return _pending_questions.pop(0)
    return ''

def answer_kalmiya_question(answer: str, question: str):
    """Procesa la respuesta de Sara a una pregunta de KALMIYA."""
    _save_answer_to_memory(question, answer)
    _conversation_history.append({"role": "assistant", "content": f"[Yo pregunte: {question}]"})
    _conversation_history.append({"role": "user", "content": f"[Sara respondio: {answer}]"})

# ══════════════════════════════════════════════════════════════════════════════
#  MOTOR 1 — OLLAMA (LOCAL)
# ══════════════════════════════════════════════════════════════════════════════

def is_ollama_running() -> bool:
    """Verifica si Ollama está activo."""
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False

def get_available_models() -> list[str]:
    """Devuelve los modelos instalados en Ollama."""
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=5)
        if r.status_code == 200:
            return [m['name'] for m in r.json().get('models', [])]
    except Exception:
        pass
    return []

def _ask_ollama(user_input: str, stream: bool = False, extra_context: str = '') -> str:
    """Envía mensaje a Ollama y devuelve respuesta."""
    global _active_engine
    _active_engine = "Ollama (local)"
    payload = {
        "model": AI_MODEL,
        "messages": [{"role": "system", "content": _build_system_prompt(extra_context)}] + _conversation_history,
        "stream": stream
    }
    if stream:
        return _ollama_stream(payload, user_input)
    else:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()['message']['content'].strip()

def _ollama_stream(payload: dict, user_input: str) -> str:
    """Streaming de Ollama token a token."""
    full = ""
    logger.info(f"[{BOTNAME} — Ollama]:")
    with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=120) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if line:
                chunk = json.loads(line)
                token = chunk.get('message', {}).get('content', '')
                logger.info(token)
                full += token
                if chunk.get('done'):
                    break
    logger.info("")
    return full.strip()

# ══════════════════════════════════════════════════════════════════════════════
#  MOTOR 2 — GEMINI (NUBE)
# ══════════════════════════════════════════════════════════════════════════════

def is_gemini_configured() -> bool:
    """Verifica si la API key de Gemini está configurada."""
    return bool(GEMINI_KEY and GEMINI_KEY != 'TU_API_KEY_AQUI')

def _ask_gemini(user_input: str, extra_context: str = '') -> str:
    """Envía mensaje a Gemini y devuelve respuesta."""
    global _active_engine
    _active_engine = "Gemini (nube)"
    if not is_gemini_configured():
        return "La API key de Gemini no está configurada. Agrega GEMINI_API_KEY en el archivo .env"
    gemini_contents = []
    for msg in _conversation_history:
        role = "user" if msg["role"] == "user" else "model"
        gemini_contents.append({"role": role, "parts": [{"text": msg["content"]}]})
    if not gemini_contents or gemini_contents[-1]["role"] != "user":
        gemini_contents.append({"role": "user", "parts": [{"text": user_input}]})
    payload = {
        "system_instruction": {"parts": [{"text": _build_system_prompt(extra_context)}]},
        "contents": gemini_contents,
        "generationConfig": {"temperature": 0.85, "maxOutputTokens": 1024, "topP": 0.95}
    }
    models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-pro"]
    last_error = None
    for model_name in models_to_try:
        try:
            url = f"{GEMINI_BASE_URL}/{model_name}:generateContent?key={GEMINI_KEY}"
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text'].strip()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                last_error = f"Modelo {model_name} no encontrado (404)"
                continue
            raise e
        except Exception as e:
            last_error = str(e)
            continue
    raise ValueError(f"No se pudo conectar con ningún modelo de Gemini. Último error: {last_error}")

# ══════════════════════════════════════════════════════════════════════════════
#  CEREBRO PRINCIPAL — SELECCIÓN AUTOMÁTICA DE MOTOR
# ══════════════════════════════════════════════════════════════════════════════

def ask_kalmiya(user_input: str, stream: bool = False, force_engine: str = '') -> str:
    """
    Función principal. Envía un mensaje a KALMIYA y devuelve su respuesta.

    Args:
        user_input:    El texto del usuario.
        stream:        Si True, imprime token a token (solo Ollama).
        force_engine: 'ollama' | 'gemini' | 'claude' | '' (auto)

    Returns:
        Respuesta de KALMIYA como string.
        Si KALMIYA tiene una pregunta, se agrega a _pending_questions.
    """
    global _conversation_history, _pending_questions
    _conversation_history.append({"role": "user", "content": user_input})
    if len(_conversation_history) > MAX_HISTORY:
        _conversation_history = _conversation_history[-MAX_HISTORY:]
    engine = force_engine.lower() if force_engine else AI_MODE.lower()
    extra_context = _build_obsidian_context(user_input)
    raw_response = _route_to_engine(user_input, engine, stream, extra_context)
    clean_response, question = _extract_question(raw_response)
    if question:
        _pending_questions.append(question)
        logger.info(f"[KALMIYA quiere preguntarte]: {question}")
    _conversation_history.append({"role": "assistant", "content": clean_response})
    log_command(user_input, clean_response, source=f'ai-{_active_engine}')
    save_thought(f"[{_active_engine}] {clean_response[:100]}...")
    return clean_response

def _route_to_engine(user_input: str, engine: str, stream: bool, extra_context: str = '') -> str:
    """Enruta la petición al motor correcto con fallback automático completo."""
    # ── Motores específicos ──────────────────────────────────────────────────
    if engine == 'ollama':
        if not is_ollama_running():
            return "Ollama no está activo. Ejecuta: ollama serve"
        return _ask_ollama(user_input, stream, extra_context)

    if engine == 'gemini':
        if not is_gemini_configured():
            return "La API key de Gemini no está configurada en el archivo .env"
        try:
            return _ask_gemini(user_input, extra_context)
        except Exception as e:
            return f"Error con Gemini: {e}"

    if engine == 'claude':
        if not is_claude_configured():
            return "La API key de Claude no está configurada en el archivo .env"
        try:
            return _ask_claude(user_input, extra_context)
        except Exception as e:
            return f"Error con Claude: {e}"

    if engine == 'groq':
        if not is_groq_configured():
            return "La API key de Groq no está configurada en el archivo .env"
        try:
            return _ask_groq(user_input, extra_context)
        except Exception as e:
            return f"Error con Groq: {e}"

    if engine == 'openrouter':
        if not is_openrouter_configured():
            return "La API key de OpenRouter no está configurada en el archivo .env"
        try:
            return _ask_openrouter(user_input, extra_context)
        except Exception as e:
            return f"Error con OpenRouter: {e}"

    if engine == 'cohere':
        if not is_cohere_configured():
            return "La API key de Cohere no está configurada en el archivo .env"
        try:
            return _ask_cohere(user_input, extra_context)
        except Exception as e:
            return f"Error con Cohere: {e}"

    # ── Modo AUTO — cascada completa de fallback ─────────────────────────────
    if engine == 'auto':
        motores_nube = []

        # 1. Ollama local primero
        if is_ollama_running():
            try:
                return _ask_ollama(user_input, stream, extra_context)
            except Exception as e:
                logger.warning(f"[BRAIN] Ollama falló ({e}), cambiando a nube...")

        # 2. Construir lista de motores de nube disponibles
        if is_gemini_configured():
            motores_nube.append(('Gemini',      _ask_gemini))
        if is_groq_configured():
            motores_nube.append(('Groq',         _ask_groq))
        if is_openrouter_configured():
            motores_nube.append(('OpenRouter',   _ask_openrouter))
        if is_cohere_configured():
            motores_nube.append(('Cohere',       _ask_cohere))
        if is_claude_configured():
            motores_nube.append(('Claude',       _ask_claude))

        for nombre, fn in motores_nube:
            try:
                logger.info(f"[BRAIN] Intentando {nombre}...")
                return fn(user_input, extra_context)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    logger.warning(f"[BRAIN] {nombre} — cuota agotada (429), probando siguiente...")
                    continue
                logger.warning(f"[BRAIN] {nombre} falló ({e}), probando siguiente...")
                continue
            except Exception as e:
                logger.warning(f"[BRAIN] {nombre} falló ({e}), probando siguiente...")
                continue

        return ("Ningún motor de IA está disponible.\n"
                "• Ollama: ejecuta 'ollama serve'\n"
                "• Gemini/Groq/OpenRouter/Cohere: verifica las API keys en .env")

    return "Modo de IA no reconocido. Usa: auto, ollama, gemini, claude, groq, openrouter o cohere"

# ══════════════════════════════════════════════════════════════════════════════
#  UTILIDADES
# ══════════════════════════════════════════════════════════════════════════════

def clear_conversation():
    """Limpia el historial de conversación."""
    global _conversation_history, _pending_questions
    _conversation_history = []
    _pending_questions = []
    logger.info("[BRAIN] Historial y preguntas pendientes limpiados.")

def is_claude_configured() -> bool:
    """Verifica si la API key de Claude está configurada."""
    return bool(CLAUDE_KEY and CLAUDE_KEY != 'TU_API_KEY_AQUI')

def is_groq_configured() -> bool:
    """Verifica si la API key de Groq está configurada."""
    return bool(GROQ_KEY and GROQ_KEY != 'TU_API_KEY_AQUI')

def is_openrouter_configured() -> bool:
    """Verifica si la API key de OpenRouter está configurada."""
    return bool(OPENROUTER_KEY and OPENROUTER_KEY != 'TU_API_KEY_AQUI')

def is_cohere_configured() -> bool:
    """Verifica si la API key de Cohere está configurada."""
    return bool(COHERE_KEY and COHERE_KEY != 'TU_API_KEY_AQUI')

def _ask_claude(user_input: str, extra_context: str = '') -> str:
    """Envía mensaje a Claude y devuelve respuesta (API /v1/messages)."""
    global _active_engine
    _active_engine = "Claude (nube)"
    if not is_claude_configured():
        return "La API key de Claude no está configurada. Agrega CLAUDE_API_KEY en el archivo .env"

    # Construir historial en formato messages (roles: user / assistant)
    messages = []
    for msg in _conversation_history:
        role = "user" if msg["role"] == "user" else "assistant"
        messages.append({"role": role, "content": msg["content"]})

    # Asegurar que el último mensaje sea del usuario
    if not messages or messages[-1]["role"] != "user":
        messages.append({"role": "user", "content": user_input})

    payload = {
        "model": CLAUDE_MODEL,
        "system": _build_system_prompt(extra_context),
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.85,
        "top_p": 0.95,
    }
    headers = {
        "x-api-key": CLAUDE_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    response = requests.post(CLAUDE_BASE_URL, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    data = response.json()
    # La nueva API devuelve content como lista de bloques de texto
    return data["content"][0]["text"].strip()

def _ask_groq(user_input: str, extra_context: str = '') -> str:
    """Envía mensaje a Groq (Llama 70B gratis) y devuelve respuesta."""
    global _active_engine
    _active_engine = "Groq (nube)"
    if not is_groq_configured():
        return "La API key de Groq no está configurada. Agrega GROQ_API_KEY en el archivo .env"
    messages = [{"role": "system", "content": _build_system_prompt(extra_context)}]
    for msg in _conversation_history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    if not messages or messages[-1]["role"] != "user":
        messages.append({"role": "user", "content": user_input})
    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.85,
    }
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(GROQ_BASE_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def _ask_openrouter(user_input: str, extra_context: str = '') -> str:
    """Envía mensaje a OpenRouter (modelos gratuitos) y devuelve respuesta."""
    global _active_engine
    _active_engine = "OpenRouter (nube)"
    if not is_openrouter_configured():
        return "La API key de OpenRouter no está configurada. Agrega OPENROUTER_API_KEY en el archivo .env"
    messages = [{"role": "system", "content": _build_system_prompt(extra_context)}]
    for msg in _conversation_history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    if not messages or messages[-1]["role"] != "user":
        messages.append({"role": "user", "content": user_input})
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.85,
    }
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "HTTP-Referer": "https://kalmiya.ai",
        "X-Title": "KALMIYA",
        "Content-Type": "application/json"
    }
    response = requests.post(OPENROUTER_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def _ask_cohere(user_input: str, extra_context: str = '') -> str:
    """Envía mensaje a Cohere (gratis con límites) y devuelve respuesta."""
    global _active_engine
    _active_engine = "Cohere (nube)"
    if not is_cohere_configured():
        return "La API key de Cohere no está configurada. Agrega COHERE_API_KEY en el archivo .env"
    # Cohere usa formato de mensajes diferente
    cohere_messages = []
    for msg in _conversation_history:
        role = "user" if msg["role"] == "user" else "assistant"
        cohere_messages.append({"role": role, "content": msg["content"]})
    if not cohere_messages or cohere_messages[-1]["role"] != "user":
        cohere_messages.append({"role": "user", "content": user_input})
    payload = {
        "model": COHERE_MODEL,
        "system": _build_system_prompt(extra_context),
        "messages": cohere_messages,
        "max_tokens": 1024,
        "temperature": 0.85,
    }
    headers = {
        "Authorization": f"Bearer {COHERE_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(COHERE_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    # Cohere v2 devuelve message.content[0].text
    content = data.get("message", {}).get("content", [])
    if content and isinstance(content, list):
        return content[0].get("text", "").strip()
    return data.get("text", "").strip()


def get_engine_status() -> dict:
    """Devuelve el estado de todos los motores."""
    return {
        'ollama_activo':      is_ollama_running(),
        'ollama_modelos':     get_available_models(),
        'gemini_activo':      is_gemini_configured(),
        'claude_activo':      is_claude_configured(),
        'groq_activo':        is_groq_configured(),
        'openrouter_activo':  is_openrouter_configured(),
        'cohere_activo':      is_cohere_configured(),
        'modo_actual':        AI_MODE,
        'motor_usado':        _active_engine,
        'historial_turnos':   len(_conversation_history) // 2,
    }

def set_ai_mode(mode: str):
    """Cambia el modo de IA en tiempo de ejecución."""
    global AI_MODE
    modos_validos = ('auto', 'ollama', 'gemini', 'claude', 'groq', 'openrouter', 'cohere')
    if mode.lower() in modos_validos:
        AI_MODE = mode.lower()
        update_memory('ai_mode_override', AI_MODE)
        logger.info(f"[BRAIN] Modo cambiado a: {AI_MODE}")
    else:
        logger.error(f"[BRAIN] Modo no válido. Usa: {', '.join(modos_validos)}")


# Stub wrapper — intenta usar brain_v4 (LangChain definitivo)
try:
    from intelligence.brain_v4 import *  # noqa: F401,F403
    _BRAIN_VERSION = "v4-langchain"
except Exception:
    from intelligence.brain import *  # noqa: F401,F403
    _BRAIN_VERSION = "v1-classic"

# Re-exportar funciones que brain_v2 no redefine (utilidades de V1)
try:
    from intelligence.brain import (  # noqa: F401
        get_engine_status,
        set_ai_mode,
        is_gemini_configured,
        is_ollama_running,
        is_claude_configured,
        is_groq_configured,
        is_openrouter_configured,
        is_cohere_configured,
        clear_conversation,
        get_pending_question,
        answer_kalmiya_question,
    )
except ImportError:
    pass

if __name__ == '__main__':
    try:
        main()  # type: ignore
    except NameError:
        pass

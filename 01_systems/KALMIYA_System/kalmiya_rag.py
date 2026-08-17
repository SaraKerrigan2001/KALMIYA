
# Stub wrapper — intenta usar kalmiya_rag_v4 (LangChain), fallback a V1.
try:
    from intelligence.kalmiya_rag_v4 import *  # noqa: F401,F403
    _RAG_VERSION = "v4-langchain"
except Exception:
    from intelligence.kalmiya_rag import *  # noqa: F401,F403
    _RAG_VERSION = "v1-classic"

# Re-exportar funciones de V1 que V2 no redefine
try:
    from intelligence.kalmiya_rag import (  # noqa: F401
        indexar_vault,
        indexar_url,
        get_rag_stats,
        limpiar_base_vectorial,
        buscar_rag_manual,
        responder_con_rag,
        imprimir_rag_stats,
    )
except ImportError:
    pass

if __name__ == '__main__':
    try:
        main()  # type: ignore
    except NameError:
        pass

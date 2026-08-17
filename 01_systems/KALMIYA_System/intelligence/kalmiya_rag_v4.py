"""
kalmiya_rag_v4.py — RAG Modernizado con LangChain para KALMIYA
===================================================================
Versión 2.0: Utiliza LangChain para ingestión, chunking y vector store.
"""

import os
import sys
import hashlib
from pathlib import Path

os.environ["HF_HUB_OFFLINE"] = "1"
# Apuntar a la raíz de KALMIYA_System para poder importar database y _logging
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import update_memory, get_memory  # noqa: E402
from _logging import get_logger  # noqa: E402

logger = get_logger(__name__)

# Dependencias de LangChain
try:
    from langchain_chroma import Chroma
    from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.document_loaders import (
        PyPDFLoader, 
        TextLoader, 
        UnstructuredMarkdownLoader,
        CSVLoader,
        Docx2txtLoader
    )
    LANGCHAIN_OK = True
except ImportError as e:
    LANGCHAIN_OK = False
    logger.warning(f"[RAG v4] Faltan dependencias de LangChain: {e}")

# Configuración
RAG_DIR = Path(__file__).parent / "rag_db_v4"
VAULT_PATH = Path(r"c:\Users\maria\env")
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

EXTENSIONES_SOPORTADAS = {
    ".md": UnstructuredMarkdownLoader,
    ".txt": TextLoader,
    ".py": TextLoader,
    ".js": TextLoader,
    ".pdf": PyPDFLoader,
    ".csv": CSVLoader,
    ".docx": Docx2txtLoader
}

EXCLUIR_CARPETAS = {
    ".obsidian", "__pycache__", ".git", "node_modules",
    "02_infrastructure", "site-packages", "_BACKUPS",
    "rag_db", "rag_db_v4", "temp_audio", ".pytest_cache"
}

_vectorstore = None

def _init_rag() -> bool:
    """Inicializa la base vectorial de LangChain (Chroma)."""
    global _vectorstore
    if not LANGCHAIN_OK:
        return False
        
    try:
        # Usamos la misma función de embedding local pero a través de LangChain
        embedding_function = SentenceTransformerEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v4"
        )
        
        _vectorstore = Chroma(
            collection_name="kalmiya_langchain",
            persist_directory=str(RAG_DIR),
            embedding_function=embedding_function
        )
        logger.info("[RAG v4] ChromaDB iniciado vía LangChain")
        return True
    except Exception as e:
        logger.error(f"[RAG v4] Error iniciando ChromaDB v4: {e}")
        return False

def indexar_documento(ruta: Path, forzar: bool = False) -> int:
    """Indexa un documento usando los Loaders de LangChain."""
    if not _vectorstore and not _init_rag():
        return 0
        
    ext = ruta.suffix.lower()
    if ext not in EXTENSIONES_SOPORTADAS:
        return 0
        
    fuente = str(ruta.relative_to(VAULT_PATH)) if ruta.is_relative_to(VAULT_PATH) else ruta.name
    
    try:
        # Generar hash simple para saber si cambió
        mtime = ruta.stat().st_mtime
        file_hash = hashlib.md5(f"{fuente}_{mtime}".encode()).hexdigest()
        sanitized = fuente.replace('/', '_').replace('.', '_').replace(' ', '_')
        hash_key = f"rag_v4_hash_{sanitized}"
        
        if get_memory(hash_key) == file_hash and not forzar:
            return 0 # Sin cambios
            
        # 1. Cargar el documento usando el loader específico
        LoaderClass = EXTENSIONES_SOPORTADAS[ext]
        try:
            loader = LoaderClass(str(ruta))
            docs = loader.load()
        except Exception as load_err:
            logger.warning(f"[RAG v4] Error cargando {ruta} con {LoaderClass.__name__}: {load_err}")
            # Fallback a TextLoader si falla
            loader = TextLoader(str(ruta), autodetect_encoding=True)
            docs = loader.load()
            
        # 2. Dividir usando el splitter de LangChain
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", r"(?<=\. )", " ", ""]
        )
        splits = text_splitter.split_documents(docs)
        
        # 3. Enriquecer metadatos
        for i, split in enumerate(splits):
            split.metadata["fuente"] = fuente
            split.metadata["tipo"] = ext
            split.metadata["indice"] = i
            
        # 4. Guardar en VectorStore
        # LangChain Chroma maneja automáticamente la eliminación si pasamos IDs repetidos, 
        # pero es más seguro generar IDs únicos por chunk
        ids = [f"{hash_key}_{i}" for i in range(len(splits))]
        
        # Intentar eliminar versiones viejas (LangChain no tiene un delete_by_metadata fácil nativo,
        # así que iteramos eliminando los IDs si existían)
        try:
            _vectorstore.delete(ids)
        except Exception:
            pass
            
        _vectorstore.add_documents(documents=splits, ids=ids)
        update_memory(hash_key, file_hash)
        
        logger.debug(f"[RAG v4] Indexado: {fuente} — {len(splits)} chunks")
        return len(splits)
        
    except Exception as e:
        logger.warning(f"[RAG v4] Error indexando {ruta}: {e}")
        return 0

def buscar_rag(query: str, top_k: int = 5) -> list[dict]:
    """Busca contexto usando LangChain Retriever."""
    if not _vectorstore and not _init_rag():
        return []
        
    try:
        # LangChain hace la búsqueda vectorial pura muy fácil
        # Pasamos a devolver un formato compatible con el antiguo para no romper el resto del sistema
        resultados_langchain = _vectorstore.similarity_search_with_score(query, k=top_k)
        
        chunks_compatibles = []
        for doc, score in resultados_langchain:
            # En Chroma, menor distance = mayor score. A veces LangChain devuelve distancias.
            # Convertimos la distancia a un "score" de similitud para retrocompatibilidad
            similitud = max(0.0, 1.0 - score) if score < 1.0 else 0.5
            
            chunks_compatibles.append({
                "texto": doc.page_content,
                "fuente": doc.metadata.get("fuente", "?"),
                "tipo": doc.metadata.get("tipo", "?"),
                "similitud": round(similitud, 3),
                "score_final": round(similitud, 3) # Asignamos directamente
            })
            
        return chunks_compatibles
    except Exception as e:
        logger.warning(f"[RAG v4] Error en búsqueda LangChain: {e}")
        return []

def construir_contexto_rag(query: str, top_k: int = 5) -> tuple:
    """Construye el bloque de contexto igual que la v1 pero usa la db v4."""
    chunks = buscar_rag(query, top_k=top_k)
    if not chunks:
        return "", []

    lineas = [
        "CONTEXTO DE TUS DOCUMENTOS PERSONALES:",
        "(Usa esta información para responder. Cita la fuente cuando sea relevante.)"
    ]
    fuentes_vistas = set()
    fuentes_lista = []

    for chunk in chunks:
        fuente = chunk["fuente"]
        score = chunk.get("score_final", chunk["similitud"])
        if fuente not in fuentes_vistas:
            fuentes_vistas.add(fuente)
            fuentes_lista.append({"fuente": fuente, "score": score, "tipo": chunk["tipo"]})
            lineas.append(f"\n📄 Fuente: {fuente} (relevancia: {score})")
        lineas.append(chunk["texto"])

    lineas.append("\n--- Fin del contexto ---")
    lineas.append("Responde basándote en este contexto.")

    return "\n".join(lineas), fuentes_lista

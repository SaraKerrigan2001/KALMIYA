"""
KALMIYA Vector Store v3.6
Sistema de memoria a largo plazo con embeddings y búsqueda semántica
Utiliza ChromaDB local para almacenar y recuperar conocimiento del vault
"""

import chromadb
from chromadb.config import Settings
from pathlib import Path
import hashlib
import json
from datetime import datetime
from typing import List, Dict, Optional
import re

class KalmiyaVectorStore:
    """
    Vector store para memoria semántica de KALMIYA
    Indexa y recupera información del vault de Obsidian
    """
    
    def __init__(self, vault_path: str, collection_name: str = "kalmiya_memory"):
        """
        Inicializa el vector store
        
        Args:
            vault_path: Ruta al vault de Obsidian
            collection_name: Nombre de la colección en ChromaDB
        """
        self.vault_path = Path(vault_path)
        self.wiki_path = self.vault_path / "wiki"
        
        # Inicializar ChromaDB en modo local
        chroma_path = Path(__file__).parent.parent / "data" / "chroma_db"
        chroma_path.mkdir(parents=True, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=str(chroma_path),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Crear o obtener colección
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Usar distancia coseno
        )
        
        print(f"✅ Vector Store inicializado: {collection_name}")
        print(f"📁 Vault path: {self.vault_path}")
        print(f"💾 ChromaDB path: {chroma_path}")
    
    def index_vault(self, force_reindex: bool = False):
        """
        Indexa todo el contenido del vault
        
        Args:
            force_reindex: Si True, reindexar todos los archivos
        """
        print("\n🔄 Indexando vault de Obsidian...")
        
        markdown_files = list(self.wiki_path.rglob("*.md"))
        indexed_count = 0
        skipped_count = 0
        
        for md_file in markdown_files:
            try:
                # Leer contenido
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Generar ID único basado en path
                file_id = self._generate_file_id(md_file)
                
                # Verificar si ya está indexado
                if not force_reindex:
                    existing = self.collection.get(ids=[file_id])
                    if existing['ids']:
                        skipped_count += 1
                        continue
                
                # Extraer metadatos
                metadata = self._extract_metadata(content, md_file)
                
                # Dividir en chunks si es muy largo
                chunks = self._split_content(content)
                
                for i, chunk in enumerate(chunks):
                    chunk_id = f"{file_id}_chunk_{i}"
                    
                    # Agregar a ChromaDB
                    self.collection.add(
                        documents=[chunk],
                        ids=[chunk_id],
                        metadatas=[{
                            **metadata,
                            'chunk_index': i,
                            'total_chunks': len(chunks)
                        }]
                    )
                
                indexed_count += 1
                
                if indexed_count % 10 == 0:
                    print(f"   Indexados: {indexed_count} archivos...")
                
            except Exception as e:
                print(f"⚠️  Error indexando {md_file.name}: {e}")
        
        print(f"\n✅ Indexación completada:")
        print(f"   📝 Archivos indexados: {indexed_count}")
        print(f"   ⏩ Archivos omitidos: {skipped_count}")
        print(f"   📊 Total documentos: {self.collection.count()}")
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Busca en el vault usando búsqueda semántica
        
        Args:
            query: Pregunta o búsqueda
            n_results: Número de resultados a devolver
            
        Returns:
            Lista de documentos relevantes con metadata
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        formatted_results = []
        
        for i in range(len(results['ids'][0])):
            formatted_results.append({
                'document': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            })
        
        return formatted_results
    
    def ask(self, question: str, context_window: int = 3) -> str:
        """
        Hace una pregunta y obtiene respuesta con contexto del vault
        
        Args:
            question: Pregunta del usuario
            context_window: Número de documentos de contexto
            
        Returns:
            Respuesta generada con contexto
        """
        # Buscar documentos relevantes
        results = self.search(question, n_results=context_window)
        
        if not results:
            return "No encontré información relevante en la bóveda."
        
        # Construir contexto
        context = "\n\n".join([
            f"**{r['metadata']['title']}**\n{r['document']}"
            for r in results
        ])
        
        # Construir respuesta
        response = f"""
📚 **Información encontrada en la bóveda:**

{context}

📂 **Fuentes consultadas:**
{', '.join([r['metadata']['file_name'] for r in results])}

💡 **Sugerencia:** Revisa estos documentos para más detalles.
        """
        
        return response.strip()
    
    def _generate_file_id(self, file_path: Path) -> str:
        """Genera ID único para un archivo"""
        relative_path = file_path.relative_to(self.wiki_path)
        return hashlib.md5(str(relative_path).encode()).hexdigest()
    
    def _extract_metadata(self, content: str, file_path: Path) -> Dict:
        """Extrae metadatos del contenido markdown"""
        metadata = {
            'file_name': file_path.name,
            'file_path': str(file_path.relative_to(self.vault_path)),
            'indexed_at': datetime.now().isoformat()
        }
        
        # Extraer frontmatter YAML
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            try:
                frontmatter = frontmatter_match.group(1)
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip()
            except:
                pass
        
        # Extraer título del primer heading
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            metadata['title'] = title_match.group(1)
        else:
            metadata['title'] = file_path.stem
        
        return metadata
    
    def _split_content(self, content: str, max_chunk_size: int = 1000) -> List[str]:
        """
        Divide contenido largo en chunks manejables
        
        Args:
            content: Contenido a dividir
            max_chunk_size: Tamaño máximo de cada chunk en caracteres
            
        Returns:
            Lista de chunks
        """
        # Remover frontmatter
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
        
        # Si es corto, devolver tal cual
        if len(content) <= max_chunk_size:
            return [content]
        
        # Dividir por párrafos
        paragraphs = content.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) + 2 <= max_chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [content]
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas del vector store"""
        return {
            'total_documents': self.collection.count(),
            'collection_name': self.collection.name,
            'vault_path': str(self.vault_path),
            'last_updated': datetime.now().isoformat()
        }
    
    def clear(self):
        """Limpia toda la colección (usar con cuidado)"""
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.create_collection(
            name=self.collection.name,
            metadata={"hnsw:space": "cosine"}
        )
        print("⚠️  Colección limpiada")


# Funciones de utilidad para usar desde otros módulos

def initialize_memory(vault_path: str = None) -> KalmiyaVectorStore:
    """
    Inicializa el sistema de memoria vectorial
    
    Args:
        vault_path: Ruta al vault (None para usar default)
        
    Returns:
        Instancia de KalmiyaVectorStore
    """
    if vault_path is None:
        vault_path = Path(__file__).parent.parent.parent / "KALMIYA"
    
    store = KalmiyaVectorStore(str(vault_path))
    return store


def search_memory(query: str, vault_path: str = None) -> List[Dict]:
    """
    Búsqueda rápida en memoria
    
    Args:
        query: Pregunta o búsqueda
        vault_path: Ruta al vault (None para usar default)
        
    Returns:
        Lista de resultados
    """
    store = initialize_memory(vault_path)
    return store.search(query)


if __name__ == '__main__':
    # Demo de uso
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         KALMIYA VECTOR STORE v3.6 - DEMO                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Inicializar
    vault_path = Path(__file__).parent.parent.parent / "KALMIYA"
    store = KalmiyaVectorStore(str(vault_path))
    
    # Indexar vault
    store.index_vault()
    
    # Mostrar estadísticas
    stats = store.get_stats()
    print(f"\n📊 Estadísticas:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Ejemplo de búsqueda
    print("\n🔍 Ejemplo de búsqueda:")
    query = "¿Qué es KALMIYA?"
    results = store.search(query, n_results=3)
    
    print(f"\nPregunta: {query}")
    print(f"Resultados encontrados: {len(results)}\n")
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['metadata']['title']}")
        print(f"   📄 {result['metadata']['file_name']}")
        print(f"   📝 {result['document'][:150]}...\n")

# pyrefly: ignore [missing-import]
import chromadb
from datetime import datetime

class EpisodicMemory:
    """
    Gestor de Memoria Episódica para KALMIYA usando ChromaDB.
    Guarda el contexto a largo plazo de todas las interacciones.
    """
    def __init__(self, db_path="./kalmiya_memory_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="episodic_memory")

    def remember(self, user_input: str, ai_response: str):
        """Guarda un recuerdo de la interacción."""
        timestamp = datetime.now().isoformat()
        memory_id = f"mem_{timestamp.replace(':', '').replace('.', '')}"
        
        document = f"User: {user_input}\nKALMIYA: {ai_response}"
        metadata = {"timestamp": timestamp, "type": "conversation"}
        
        self.collection.add(
            documents=[document],
            metadatas=[metadata],
            ids=[memory_id]
        )
        print(f"[EpisodicMemory] Recuerdo guardado ({memory_id})")

    def recall(self, query: str, n_results: int = 3):
        """Recupera recuerdos pasados relevantes."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results['documents'][0] if results['documents'] else []

if __name__ == "__main__":
    memory = EpisodicMemory()
    memory.remember("Me gusta el color azul y la ciencia ficción.", "¡Anotado! Lo tendré en cuenta.")
    print("Recuerdos sobre gustos:", memory.recall("¿Qué cosas me gustan?"))

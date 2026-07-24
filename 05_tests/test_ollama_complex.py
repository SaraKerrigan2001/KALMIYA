import os
import sys

# Asegurar que el directorio actual está en el path
sys.path.append(os.getcwd())

from brain import ask_kalmiya, get_engine_status

def test_ollama_brain():
    print("=== TEST DE CEREBRO LOCAL (OLLAMA) ===")
    
    # Verificar estado inicial
    status = get_engine_status()
    print(f"Estado inicial: {status['motor_usado']} (Ollama activo: {status['ollama_activo']})")
    
    # Pregunta compleja
    query = "¿Cómo podrías ayudarme a optimizar el rendimiento de mi PC basándote en que tengo una RTX 3050 y 32GB de RAM? Sé específica y técnica."
    
    print(f"\nPregunta: {query}")
    print("\n[KALMIYA pensando con Ollama...]\n")
    
    try:
        # Forzamos Ollama para el test
        response = ask_kalmiya(query, force_engine='ollama')
        print(f"Respuesta de KALMIYA:\n{'-'*40}\n{response}\n{'-'*40}")
        
        # Verificar estado final
        status = get_engine_status()
        print(f"\nMotor final utilizado: {status['motor_usado']}")
        
    except Exception as e:
        print(f"Error en el test: {e}")

if __name__ == "__main__":
    test_ollama_brain()

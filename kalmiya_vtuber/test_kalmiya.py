import asyncio
import os
from dotenv import load_dotenv
from google import genai
import edge_tts

# Cargar variables de entorno
load_dotenv()

async def test_integracion():
    print("========================================")
    print("  Iniciando Pruebas Automatizadas (KALMIYA)")
    print("========================================\n")
    
    # 1. Probar Inicialización de Cliente Gemini
    try:
        client = genai.Client()
        chat = client.chats.create(
            model="gemini-1.5-flash",
            config=dict(system_instruction="Eres un asistente de prueba. Responde únicamente con la frase 'Prueba de audio y texto exitosa.'")
        )
        print("[OK] [1/3] Conexión a Gemini (API) inicializada correctamente.")
    except Exception as e:
        print(f"[ERROR] [1/3] Error de conexión a Gemini: {e}")
        return

    # 2. Probar Generación de Texto del Modelo
    try:
        print("[INFO] Enviando mensaje de prueba a Google...")
        respuesta = chat.send_message("Hola, realiza la prueba.")
        texto_ia = respuesta.text
        print(f"[OK] [2/3] Respuesta del modelo recibida: '{texto_ia.strip()}'")
    except Exception as e:
        print(f"[ERROR] [2/3] Error al generar texto (Posible sobrecarga 503): {e}")
        return

    # 3. Probar Generación de Voz (Edge-TTS)
    try:
        OUTPUT_FILE = "test_respuesta.mp3"
        communicate = edge_tts.Communicate(texto_ia, "es-MX-DaliaNeural")
        await communicate.save(OUTPUT_FILE)
        
        if os.path.exists(OUTPUT_FILE):
            print("[OK] [3/3] Generación de voz (MP3) creada en disco exitosamente.")
            os.remove(OUTPUT_FILE) # Limpiar la prueba
        else:
            print("[ERROR] [3/3] El archivo de audio no se generó.")
    except Exception as e:
         print(f"[ERROR] [3/3] Error en síntesis de voz (TTS): {e}")
         return
         
    print("\n[ÉXITO] DIAGNÓSTICO FINAL: Todo el núcleo de KALMIYA funciona a la perfección.")

if __name__ == "__main__":
    # Política necesaria para Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_integracion())

import asyncio
import os
import subprocess
import playsound3
import edge_tts
import pyvts
from google import genai
from dotenv import load_dotenv
import pyautogui

# Cargar variables de entorno (como GEMINI_API_KEY)
load_dotenv()

# ==========================================
# 1. HERRAMIENTAS DE LA IA (CONTROL DE PC)
# ==========================================
def abrir_aplicacion(nombre_app: str) -> str:
    """Abre una aplicación básica en la computadora del usuario (ej: bloc de notas, calculadora, explorador)."""
    try:
        nombre = nombre_app.lower()
        if "bloc" in nombre or "notas" in nombre or "notepad" in nombre:
            subprocess.Popen("notepad.exe")
            return "El Bloc de Notas fue abierto con éxito en la PC del usuario."
        elif "calculadora" in nombre or "calc" in nombre:
            subprocess.Popen("calc.exe")
            return "La Calculadora fue abierta con éxito en la PC del usuario."
        elif "explorador" in nombre or "archivos" in nombre or "carpeta" in nombre:
            subprocess.Popen("explorer.exe")
            return "El Explorador de archivos fue abierto."
        else:
            return f"No tengo permisos configurados para abrir la aplicación: '{nombre_app}'."
    except Exception as e:
        return f"Error al intentar abrir la aplicación: {e}"



def mover_mouse(x: int, y: int, clic: bool = False) -> str:
    """Mueve el cursor del mouse a la coordenada (x, y) de la pantalla. Opcionalmente hace clic."""
    try:
        # Failsafe activado por defecto (si el usuario mueve el mouse a una esquina, se detiene)
        pyautogui.FAILSAFE = True
        
        # Mover el mouse a la posición (x, y)
        pyautogui.moveTo(x, y, duration=1.0)
        
        if clic:
            pyautogui.click()
            return f"Mouse movido a ({x}, {y}) y clic realizado."
        else:
            return f"Mouse movido a ({x}, {y})."
    except pyautogui.FailSafeException:
        return "El usuario ha abortado el movimiento del ratón moviéndolo a una esquina (FAILSAFE activado)."
    except Exception as e:
        return f"Error al intentar mover el ratón: {e}"

# Esta lista se la damos a Gemini para que sepa qué puede hacer
herramientas_de_kalmiya = [abrir_aplicacion, mover_mouse]

# ==========================================
# 2. CONFIGURACIÓN DE VTS Y TTS
# ==========================================
VOICE = "es-MX-DaliaNeural" 
OUTPUT_FILE = "respuesta.mp3"

# Instancia de VTube Studio
plugin_info = {
    "plugin_name": "KALMIYA AI", 
    "developer": "Sara Kerrigan", 
    "authentication_token_path": "./vts_token.txt"
}
vts = pyvts.vts(plugin_info=plugin_info)

async def generar_voz(texto: str) -> None:
    """Convierte texto a voz usando edge-tts."""
    communicate = edge_tts.Communicate(texto, VOICE)
    await communicate.save(OUTPUT_FILE)

def reproducir_audio(archivo: str) -> None:
    """Reproduce el audio en el canal seleccionado."""
    try:
        playsound3.playsound(archivo)
    except Exception as e:
        pass # Ignorar errores menores de reproducción

# ==========================================
# 3. BUCLE PRINCIPAL
# ==========================================
async def main():
    print("========================================")
    print("  KALMIYA v2 - Asistente Virtual y VTuber")
    print("========================================")
    
    # --- CONEXIÓN A VTUBE STUDIO ---
    print("\n🔌 Conectando a VTube Studio en el puerto 8001...")
    try:
        await vts.connect()
        # VTube Studio solicitará permisos en la interfaz gráfica
        print("👉 Si VTube Studio te pide permisos, haz clic en 'Allow' / 'Permitir'.")
        await vts.request_authenticate_token()
        await vts.request_authenticate()
        print("✅ ¡Conectado y autenticado con VTube Studio exitosamente!")
    except Exception as e:
        print(f"⚠️ No se pudo conectar a VTube Studio: {e}")
        print("💡 Asegúrate de que VTube Studio esté abierto y que la API (puerto 8001) esté habilitada en sus opciones.")

    # --- INICIALIZACIÓN DE GEMINI ---
    print("\n🧠 Iniciando cerebro neuronal de KALMIYA...")
    try:
        client = genai.Client()
        chat = client.chats.create(
            model="gemini-3.5-flash",
            config=dict(
                system_instruction=(
                    "Eres KALMIYA, una IA VTuber animada y súper avanzada creada por Sara Kerrigan. "
                    "Ahora tienes control sobre el PC del usuario usando tus herramientas. "
                    "Si te piden abrir el bloc de notas, la calculadora o el explorador, usa tu herramienta 'abrir_aplicacion'. "
                    "Si te piden mover el ratón, usa la herramienta 'mover_mouse' adivinando unas coordenadas X e Y lógicas. "
                    "Recuerda que una pantalla normal mide 1920x1080 (el centro es 960, 540). "
                    "Tus respuestas deben seguir siendo cortas, carismáticas y naturales."
                ),
                tools=herramientas_de_kalmiya, # Le damos el poder a la IA
                temperature=0.7
            )
        )
        print("✅ Inteligencia Artificial en línea.")
    except Exception as e:
         print(f"❌ Error al crear el chat de Gemini: {e}")
         return

    print("\n========================================")
    print("Escribe 'salir' para terminar el programa.")
    print("========================================")
    
    while True:
        try:
            usuario_texto = input("\nTú: ")
            
            if usuario_texto.lower() in ["salir", "exit", "quit"]:
                print("KALMIYA: ¡Nos vemos pronto, Sara!")
                break
            
            if not usuario_texto.strip():
                continue

            print("KALMIYA está pensando...")
            
            # Enviar mensaje con reintentos (para evadir el error 503 de servidores llenos)
            max_reintentos = 5
            texto_ia = ""
            for intento in range(max_reintentos):
                try:
                    respuesta = chat.send_message(usuario_texto)
                    texto_ia = respuesta.text
                    break
                except Exception as e:
                    if "503" in str(e) and intento < max_reintentos - 1:
                        print(f"⚠️ Servidores de Google llenos. Reintentando conexión... ({intento+1}/{max_reintentos})")
                        import time
                        time.sleep(2)
                    else:
                        raise e
            
            if texto_ia:
                print(f"KALMIYA: {texto_ia}")
                # Generar voz y enviarla al Virtual Audio Cable (por defecto el sistema de audio)
                await generar_voz(texto_ia)
                reproducir_audio(OUTPUT_FILE)
                
                # Limpieza
                if os.path.exists(OUTPUT_FILE):
                    os.remove(OUTPUT_FILE)

        except Exception as e:
            print(f"Ocurrió un error (¿Sobrecarga 503?): {e}")

if __name__ == "__main__":
    # Necesario en Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

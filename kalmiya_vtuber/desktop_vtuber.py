import asyncio
import os
import sys
import threading
import requests
import playsound3
import edge_tts
import pyvts
from twitchio.ext import commands
from dotenv import load_dotenv

# ==========================================
# 1. CONFIGURACIÓN DEL SISTEMA KALMIYA
# ==========================================
load_dotenv()

# Añadir la ruta del sistema principal
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
system_dir = os.path.join(root_dir, "01_systems", "KALMIYA_System")

if system_dir not in sys.path:
    sys.path.insert(0, system_dir)

# Añadir subcarpetas necesarias del sistema principal al final de sys.path (fallback)
for sub in ['services', 'core', 'audio', 'intelligence', 'kalmiya', 'modules']:
    sub_path = os.path.join(system_dir, sub)
    if sub_path not in sys.path:
        sys.path.append(sub_path)

try:
    from intelligence.brain_v4 import ask_kalmiya
    BRAIN_OK = True
except ImportError as e:
    print(f"❌ Error al importar el cerebro principal: {e}")
    BRAIN_OK = False

# ==========================================
# 2. CONFIGURACIÓN DE VTS, TTS Y AUDIO
# ==========================================
OUTPUT_FILE = "respuesta.mp3"
VOICE_EDGE = "es-MX-DaliaNeural"

# Fish Audio Config
FISH_AUDIO_API_KEY = os.getenv("FISH_AUDIO_API_KEY", "")
FISH_AUDIO_MODEL_ID = os.getenv("FISH_AUDIO_MODEL_ID", "")

# Twitch Config
TWITCH_TOKEN = os.getenv("TWITCH_TOKEN", "")
TWITCH_CHANNEL = os.getenv("TWITCH_CHANNEL", "")


plugin_info = {
    "plugin_name": "KALMIYA AI Desktop", 
    "developer": "Sara Kerrigan", 
    "authentication_token_path": "./vts_token.txt"
}
vts = pyvts.vts(plugin_info=plugin_info)

# Cola de tareas para evitar colisiones en respuestas (limitado a 5)
message_queue = asyncio.Queue(maxsize=5)

async def generar_voz_fish(texto: str) -> bool:
    """Intenta generar voz con Fish Audio API."""
    if not FISH_AUDIO_API_KEY or not FISH_AUDIO_MODEL_ID or FISH_AUDIO_API_KEY.startswith("tu_"):
        return False
        
    try:
        url = "https://api.fish.audio/v1/tts"
        headers = {
            "Authorization": f"Bearer {FISH_AUDIO_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "text": texto,
            "reference_id": FISH_AUDIO_MODEL_ID,
            "format": "mp3"
        }
        response = requests.post(url, headers=headers, json=data, timeout=15)
        
        if response.status_code == 200:
            with open(OUTPUT_FILE, "wb") as f:
                f.write(response.content)
            return True
        else:
            print(f"⚠️ Error Fish Audio ({response.status_code}): {response.text}")
            return False
    except Exception as e:
        print(f"⚠️ Excepción al contactar Fish Audio: {e}")
        return False

async def generar_voz(texto: str) -> None:
    """Generador de voz principal con fallback a Edge-TTS."""
    # 1. Intentar Fish Audio
    exito = await generar_voz_fish(texto)
    
    # 2. Fallback a Edge TTS si Fish Audio falla o no está configurado
    if not exito:
        communicate = edge_tts.Communicate(texto, VOICE_EDGE)
        await communicate.save(OUTPUT_FILE)

def reproducir_audio(archivo: str) -> None:
    """Reproduce el audio.
    
    Para sincronización labial (VoiceMeeter):
    Configura tu salida de audio predeterminada de Windows a 'VoiceMeeter Input'.
    Luego en VTube Studio, en la sección de Micrófono, selecciona 'VoiceMeeter Output'.
    """
    try:
        playsound3.playsound(archivo)
    except Exception as e:
        print(f"⚠️ Error al reproducir el audio: {e}")
    finally:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
            except Exception as e:
                print(f"⚠️ Error al eliminar archivo temporal de audio: {e}")

# ==========================================
# 3. BOT DE TWITCH
# ==========================================
class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(token=TWITCH_TOKEN, prefix='!', initial_channels=[TWITCH_CHANNEL])

    async def event_ready(self):
        print(f"🟣 Conectado a Twitch como | {self.nick}")
        print(f"🟣 Escuchando el canal | {TWITCH_CHANNEL}")

    async def event_message(self, message):
        if message.echo:
            return
            
        print(f"\n[Twitch] {message.author.name}: {message.content}")
        
        # Poner mensaje en la cola de procesamiento
        await message_queue.put({
            "source": f"Twitch ({message.author.name})",
            "content": f"{message.author.name} dice: {message.content}"
        })

# ==========================================
# 4. ENTRADA DE CONSOLA (Hilo separado)
# ==========================================
def console_input_loop(loop):
    """Permite seguir escribiendo en la terminal sin bloquear a Twitch."""
    while True:
        try:
            texto = input()
            if not texto.strip():
                continue
                
            if texto.lower() in ["salir", "exit", "quit"]:
                asyncio.run_coroutine_threadsafe(message_queue.put({"source": "system", "content": "QUIT"}), loop)
                break
                
            asyncio.run_coroutine_threadsafe(message_queue.put({
                "source": "Terminal",
                "content": texto
            }), loop)
        except EOFError:
            break
        except Exception as e:
            print(f"⚠️ Error en consola: {e}")

# ==========================================
# 5. PROCESADOR CENTRAL
# ==========================================
async def procesar_cola():
    """Consume mensajes de Twitch o Terminal en orden."""
    while True:
        item = await message_queue.get()
        
        if item["content"] == "QUIT":
            print("KALMIYA: ¡Nos vemos pronto, Sara!")
            os._exit(0)
            
        print(f"\n⚡ KALMIYA pensando en el mensaje de {item['source']}...")
        
        # Llamar al cerebro en un thread (ask_kalmiya es bloqueante)
        try:
            texto_ia = await asyncio.to_thread(ask_kalmiya, item["content"])
            
            if texto_ia:
                print(f"KALMIYA: {texto_ia}")
                await generar_voz(texto_ia)
                
                # Reproducir en un thread (playsound es bloqueante)
                await asyncio.to_thread(reproducir_audio, OUTPUT_FILE)
        except Exception as e:
            print(f"❌ Error procesando mensaje: {e}")
            
        message_queue.task_done()
        print("\n> Esperando nuevos mensajes...")

# ==========================================
# 6. BUCLE PRINCIPAL
# ==========================================
async def main():
    print("========================================")
    print("  KALMIYA - Desktop VTuber Avanzado V4")
    print("  + Integración Twitch + Fish Audio")
    print("========================================")
    
    if not BRAIN_OK:
        print("No se puede iniciar sin el cerebro. Saliendo...")
        return
        
    # --- CONEXIÓN A VTUBE STUDIO ---
    print("\n🔌 Conectando a VTube Studio...")
    try:
        await vts.connect()
        await vts.request_authenticate_token()
        await vts.request_authenticate()
        print("✅ ¡Conectado a VTube Studio exitosamente!")
    except Exception as e:
        print("⚠️ No se pudo conectar a VTube Studio. ¿Está abierto y la API habilitada?")

    # --- INICIAR TWITCH BOT ---
    bot = None
    if TWITCH_TOKEN and not TWITCH_TOKEN.startswith("oauth:tu_") and TWITCH_CHANNEL and not TWITCH_CHANNEL.startswith("tu_"):
        bot = TwitchBot()
        asyncio.create_task(bot.start())
    else:
        print("⚠️ Twitch no configurado en .env. Saltando conexión a Twitch.")

    # --- INICIAR CONSUMIDOR DE COLA ---
    asyncio.create_task(procesar_cola())

    # --- INICIAR CONSOLA DE TERMINAL ---
    print("\n✅ Inteligencia Artificial (Cerebro Completo) en línea.")
    print("Escribe tus mensajes aquí (o en Twitch) y presiona Enter.")
    print("Escribe 'salir' para terminar el programa.")
    print("========================================")
    print("\n> Esperando nuevos mensajes...")
    
    loop = asyncio.get_running_loop()
    thread = threading.Thread(target=console_input_loop, args=(loop,), daemon=True)
    thread.start()
    
    # Mantener el programa vivo
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(main())

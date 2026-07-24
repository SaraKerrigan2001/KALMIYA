import os
import re
import asyncio
import subprocess
import pyttsx3
import uuid
import threading
import time as _time
from decouple import config
from database import get_memory

# Configuración básica
USERNAME = config('USER', default='Usuario')
BOTNAME = config('BOTNAME', default='Asistente')

# Configuración de voz neuronal (Microsoft Edge)
# Voces recomendadas: es-ES-AlvaroNeural (Hombre), es-ES-ElviraNeural (Mujer)
NEURAL_VOICE = "es-ES-ElviraNeural"  # Usar voz femenina

# Directorio temporal para audios
import tempfile
TEMP_DIR = tempfile.gettempdir()

# Lock para evitar que dos hilos hablen al mismo tiempo (anti-eco)
_speak_lock = threading.Lock()
# Timestamp del último momento en que terminó de hablar
LAST_SPEECH_END = 0.0

def _init_pyttsx3():
    """Inicializa el motor offline como respaldo."""
    try:
        engine = pyttsx3.init('sapi5')
        engine.setProperty('rate', 145)
        engine.setProperty('volume', 0.50)
        voices = engine.getProperty('voices')
        spanish_voice = next((v.id for v in voices if 'spanish' in v.name.lower() or 'helena' in v.name.lower()), None)
        if spanish_voice:
            engine.setProperty('voice', spanish_voice)
        return engine
    except:
        return None

offline_engine = _init_pyttsx3()

async def _generate_neural_audio(text, output_path):
    """Genera audio neuronal usando Edge TTS."""
    try:
        import edge_tts
        communicate = edge_tts.Communicate(text, NEURAL_VOICE, volume="-40%", rate="-10%")
        await communicate.save(output_path)
        return True
    except Exception as e:
        print(f"Error generando audio neuronal: {e}")
        return False

def _play_audio_windows(file_path):
    """Reproduce audio en Windows usando .NET (sin librerías externas) con un timeout de 3s."""
    try:
        abspath = os.path.abspath(file_path)
        # Script con timeout de 3 segundos (60 * 50ms) para evitar bloqueos infinitos en servidores headless
        powershell_cmd = (
            f"Add-Type -AssemblyName PresentationCore; "
            f"$p = New-Object System.Windows.Media.MediaPlayer; "
            f"$p.Open('{abspath}'); "
            f"$timeout = 60; "
            f"while ($p.NaturalDuration.HasTimeSpan -eq $false -and $timeout -gt 0) {{ "
            f"    Start-Sleep -m 50; "
            f"    $timeout--; "
            f"}}; "
            f"if ($p.NaturalDuration.HasTimeSpan -eq $true) {{ "
            f"    $p.Play(); "
            f"    Start-Sleep -s ($p.NaturalDuration.TimeSpan.TotalSeconds + 0.5); "
            f"}}; "
            f"$p.Close();"
        )
        subprocess.run(["powershell", "-Command", powershell_cmd], 
                       creationflags=subprocess.CREATE_NO_WINDOW,
                       capture_output=True)
        return True
    except Exception as e:
        print(f"Error reproduciendo audio: {e}")
        return False

def speak(text):
    """
    Convierte texto a voz. Activa KALMIYA_SPEAKING para pausar
    la escucha del microfono y evitar el eco.
    Usa un lock para que solo una voz se reproduzca a la vez.
    """
    global LAST_SPEECH_END

    if not text:
        return

    voice_setting = get_memory('voice_enabled')
    if voice_setting == "false":
        print(f"[{BOTNAME} - MUDO]: {text}")
        return

    # Adquirir lock — si otro hilo ya esta hablando, esperar
    with _speak_lock:
        text = re.sub(r'\b(pero|porque|aunque|cuando|si|entonces)\b', r', \1', text)
        text = text.replace(', ,', ',')
        print(f"[{BOTNAME}]: {text}")

        # Pausar escucha para evitar eco
        try:
            import kalmiya_core as _core
            _core.KALMIYA_SPEAKING = True
            _core.WAS_SPEAKING = True
        except Exception:
            pass

        try:
            temp_file = os.path.join(TEMP_DIR, f"speech_{uuid.uuid4()}.mp3")
            try:
                success = asyncio.run(_generate_neural_audio(text, temp_file))
                if success:
                    _play_audio_windows(temp_file)
                    try:
                        os.remove(temp_file)
                    except Exception:
                        pass
                    return
            except Exception:
                pass

            if offline_engine:
                try:
                    offline_engine.say(text)
                    offline_engine.runAndWait()
                except Exception as e:
                    print(f"Error en voz offline: {e}")
        finally:
            # Pausa mas larga antes de reanudar escucha (evita eco residual)
            _time.sleep(1.5)
            LAST_SPEECH_END = _time.time()
            try:
                import kalmiya_core as _core
                _core.KALMIYA_SPEAKING = False
            except Exception:
                pass


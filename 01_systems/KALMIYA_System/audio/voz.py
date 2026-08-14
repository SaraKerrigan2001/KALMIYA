import os
import re
import asyncio
import subprocess
import uuid
import threading
import time as _time
from decouple import config
from database import get_memory, update_memory

try:
    import pyttsx3
except ModuleNotFoundError:  # pragma: no cover - optional runtime dependency
    pyttsx3 = None

# Configuración básica
USERNAME = config('USER', default='Usuario')
BOTNAME = config('BOTNAME', default='Asistente')

# Configuración de voz neuronal (Microsoft Edge)
# Voces recomendadas: es-ES-AlvaroNeural (Hombre), es-ES-ElviraNeural (Mujer)
# O usa un identificador configurable desde .env o memoria interna.
DEFAULT_NEURAL_VOICE = config('NEURAL_VOICE', default='es-ES-ElviraNeural')

# Directorio temporal para audios
import tempfile
TEMP_DIR = tempfile.gettempdir()

# Lock para evitar que dos hilos hablen al mismo tiempo (anti-eco)
_speak_lock = threading.Lock()
# Timestamp del último momento en que terminó de hablar
LAST_SPEECH_END = 0.0

def _init_pyttsx3():
    """Inicializa el motor offline como respaldo."""
    if pyttsx3 is None:
        return None
    try:
        engine = pyttsx3.init('sapi5')
        engine.setProperty('rate', 145)
        engine.setProperty('volume', 0.50)
        voices = engine.getProperty('voices')
        spanish_voice = next((v.id for v in voices if 'spanish' in v.name.lower() or 'helena' in v.name.lower()), None)
        if spanish_voice:
            engine.setProperty('voice', spanish_voice)
        return engine
    except Exception:
        return None

offline_engine = _init_pyttsx3()

# Integración opcional con Azure Speech (Custom Neural Voice)
_azure_available = False
try:
    import azure.cognitiveservices.speech as speechsdk
    _azure_available = True
except Exception:
    _azure_available = False

def _generate_azure_audio(text, output_path):
    """Genera audio vía Azure Speech SDK si está configurado.

    Requiere variables de entorno o .env: AZ_SPEECH_KEY, AZ_SPEECH_REGION, AZ_SPEECH_VOICE
    """
    if not _azure_available:
        return False
    key = os.environ.get('AZ_SPEECH_KEY') or config('AZ_SPEECH_KEY', default=None)
    region = os.environ.get('AZ_SPEECH_REGION') or config('AZ_SPEECH_REGION', default=None)
    voice = os.environ.get('AZ_SPEECH_VOICE') or config('AZ_SPEECH_VOICE', default=None)
    if not key or not region or not voice:
        return False
    try:
        cfg = speechsdk.SpeechConfig(subscription=key, region=region)
        cfg.speech_synthesis_voice_name = voice
        audio_cfg = speechsdk.audio.AudioOutputConfig(filename=output_path)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=cfg, audio_config=audio_cfg)
        result = synthesizer.speak_text_async(text).get()
        return getattr(result, 'reason', None) == speechsdk.ResultReason.SynthesizingAudioCompleted
    except Exception as e:
        print(f"Azure TTS error: {e}")
        return False

def _resolve_voice_alias(voice_id: str) -> str:
    """Resuelve alias conocidos de voz a un identificador real."""
    if not isinstance(voice_id, str) or not voice_id.strip():
        return DEFAULT_NEURAL_VOICE

    voice_key = voice_id.strip().lower()
    if voice_key in {
        'cortana', 'halo cortana', 'cortana latino', 'cortana halo', 'cortana español',
        'cortana latinoamericano', 'cortana latinoam', 'cortana latinoamérica'
    }:
        azure_cortana = os.environ.get('AZ_SPEECH_CORTANA') or config('AZ_SPEECH_CORTANA', default=None)
        if azure_cortana:
            return azure_cortana
        return DEFAULT_NEURAL_VOICE

    return voice_id.strip()


def get_neural_voice() -> str:
    """Devuelve el identificador de voz neuronal configurado."""
    voice_override = get_memory('neural_voice')
    if voice_override:
        return _resolve_voice_alias(voice_override)
    return DEFAULT_NEURAL_VOICE


def get_neural_voice_info() -> dict[str, str | bool]:
    """Devuelve información del estado actual de la voz neuronal."""
    voice_override = get_memory('neural_voice')
    alias_used = False
    requested = DEFAULT_NEURAL_VOICE
    if voice_override:
        requested = voice_override.strip()
        alias_used = requested.lower() in {
            'cortana', 'halo cortana', 'cortana latino', 'cortana halo',
            'cortana español', 'cortana latinoamericano', 'cortana latinoam',
            'cortana latinoamérica'
        }
    resolved = _resolve_voice_alias(requested)
    fallback = alias_used and resolved == DEFAULT_NEURAL_VOICE
    return {
        'requested': requested,
        'resolved': resolved,
        'alias': alias_used,
        'fallback': fallback,
    }


def set_neural_voice(voice_id: str) -> bool:
    """Configura el identificador de voz neuronal en la memoria interna."""
    if not isinstance(voice_id, str) or not voice_id.strip():
        return False
    voice_id = voice_id.strip()
    update_memory('neural_voice', voice_id)
    return True


async def _generate_neural_audio(text, output_path):
    """Genera audio neuronal usando Edge TTS."""
    try:
        import edge_tts
        voice = get_neural_voice()
        communicate = edge_tts.Communicate(text, voice, volume="-40%", rate="-10%")
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
                success = False
                if _generate_azure_audio(text, temp_file):
                    success = True
                else:
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


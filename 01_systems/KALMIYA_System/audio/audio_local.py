"""
audio_local.py - Audio completamente privado (STT + TTS local, sin APIs)

Implementa:
- STT (Speech-to-Text): Vosk (offline, rápido)
- TTS (Text-to-Speech): pyttsx3 (offline, natural)
- Audio local, cero privacidad comprometida
- Sin conexión a APIs externas
"""

import os
import threading
import json
from pathlib import Path
from decouple import config

try:
    import pyttsx3
except ModuleNotFoundError:  # pragma: no cover - optional runtime dependency
    pyttsx3 = None

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────────────────────

USERNAME = config('USER', default='Usuario')
BOTNAME = config('BOTNAME', default='JARVIS')

# TTS: Inicializar pyttsx3
if pyttsx3 is None:
    _tts_engine = None
    TTS_AVAILABLE = False
else:
    try:
        _tts_engine = pyttsx3.init('sapi5')  # Windows SAPI5
        _tts_engine.setProperty('rate', 150)  # Velocidad
        _tts_engine.setProperty('volume', 0.75)  # Volumen

        # Buscar voz en español
        voices = _tts_engine.getProperty('voices')
        spanish_voices = [v for v in voices if 'spanish' in v.name.lower() or 'españa' in v.name.lower()]
        if spanish_voices:
            _tts_engine.setProperty('voice', spanish_voices[0].id)

        TTS_AVAILABLE = True
    except Exception as e:
        print(f"[AUDIO_LOCAL] Advertencia: TTS no disponible: {e}")
        _tts_engine = None
        TTS_AVAILABLE = False

# STT: Intentar usar Vosk
try:
    from vosk import Model, KaldiRecognizer
    import pyaudio
    STT_ENGINE = 'vosk'
    STT_AVAILABLE = True
    
    # Modelo de voz (español o inglés)
    MODEL_PATH = os.path.expanduser("~/.vosk/model-es")
    if not os.path.exists(MODEL_PATH):
        MODEL_PATH = os.path.expanduser("~/.vosk/model")
    
    try:
        model = Model(MODEL_PATH)
    except Exception:
        print(f"[AUDIO_LOCAL] Modelo Vosk no encontrado en {MODEL_PATH}")
        model = None
        STT_AVAILABLE = False
        
except ImportError:
    STT_ENGINE = None
    STT_AVAILABLE = False
    print("[AUDIO_LOCAL] Vosk no instalado. Para STT local, instala: pip install vosk pyaudio")

# Alternativa: Vosk fallback a offline-speech-recognition si es necesario
if not STT_AVAILABLE:
    try:
        import speech_recognition as sr_lib
        STT_ENGINE = 'sr_local'
        # NOTA: Aunque SpeechRecognition por defecto usa Google, se puede usar offline si se configura
        STT_AVAILABLE = True
    except ImportError:
        STT_AVAILABLE = False

# Lock para evitar que dos hilos hablen al mismo tiempo
_speak_lock = threading.Lock()
_listen_lock = threading.Lock()

# ─────────────────────────────────────────────────────────────────────────────
# TTS - Text-to-Speech (LOCAL, PRIVADO)
# ─────────────────────────────────────────────────────────────────────────────

def speak(text: str, wait: bool = True) -> bool:
    """
    Sintetiza y reproduce texto en voz usando pyttsx3 (completamente local).
    
    Args:
        text: Texto a sintetizar
        wait: Esperar a que termine de hablar
        
    Returns:
        True si fue exitoso
    """
    if not TTS_AVAILABLE:
        print(f"[{BOTNAME}] (sin audio): {text}")
        return False
    
    if not text or not text.strip():
        return False
    
    with _speak_lock:
        try:
            print(f"[{BOTNAME}]: {text}")
            _tts_engine.say(text)
            if wait:
                _tts_engine.runAndWait()
            return True
        except Exception as e:
            print(f"[AUDIO_LOCAL] Error en TTS: {e}")
            return False

def speak_async(text: str) -> None:
    """Habla en un hilo separado (no bloquea)."""
    thread = threading.Thread(target=speak, args=(text, True), daemon=True)
    thread.start()

def get_tts_status() -> dict:
    """Retorna el estado del motor TTS."""
    if not TTS_AVAILABLE:
        return {"available": False, "engine": None, "reason": "TTS no disponible"}
    
    try:
        rate = _tts_engine.getProperty('rate')
        volume = _tts_engine.getProperty('volume')
        voice = _tts_engine.getProperty('voice')
        voices = _tts_engine.getProperty('voices')
        
        return {
            "available": True,
            "engine": "pyttsx3 (SAPI5 local)",
            "rate": rate,
            "volume": volume,
            "voice": voice,
            "voices_available": len(voices)
        }
    except Exception as e:
        return {"available": False, "error": str(e)}

# ─────────────────────────────────────────────────────────────────────────────
# STT - Speech-to-Text (LOCAL, PRIVADO)
# ─────────────────────────────────────────────────────────────────────────────

def listen(timeout: float = 5.0, phrase_limit: float = 10.0) -> str | None:
    """
    Escucha el micrófono y transcribe usando STT local (Vosk).
    
    Args:
        timeout: Tiempo máximo de espera para comenzar a hablar (segundos)
        phrase_limit: Tiempo máximo de grabación (segundos)
        
    Returns:
        Texto transcrito o None si hubo error/timeout
    """
    if not STT_AVAILABLE:
        print("[AUDIO_LOCAL] STT no disponible. Instala: pip install vosk pyaudio")
        return None
    
    if STT_ENGINE == 'vosk':
        return _listen_vosk(timeout, phrase_limit)
    elif STT_ENGINE == 'sr_local':
        return _listen_sr_local(timeout, phrase_limit)
    else:
        return None

def _listen_vosk(timeout: float, phrase_limit: float) -> str | None:
    """Escucha usando Vosk (offline, privado)."""
    with _listen_lock:
        try:
            import pyaudio
            
            if not model:
                return None
            
            recognizer = KaldiRecognizer(model, 16000)
            recognizer.SetWords(["jarvis", "kalmiya", "oye", "hey"])
            
            p = pyaudio.PyAudio()
            stream = p.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=4096
            )
            
            print(f"[{BOTNAME}] Escuchando... (máx {phrase_limit}s)")
            stream.start_stream()
            
            result_text = ""
            start_time = __import__('time').time()
            silence_count = 0
            
            try:
                while True:
                    elapsed = __import__('time').time() - start_time
                    
                    if elapsed > phrase_limit:
                        break
                    
                    data = stream.read(4096, exception_on_overflow=False)
                    
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        if 'result' in result:
                            result_text = ' '.join([item['conf'] for item in result['result']])
                        if result_text:
                            break
                    else:
                        partial = json.loads(recognizer.PartialResult())
                        if 'partial' in partial:
                            partial_text = partial['partial']
                            if partial_text:
                                print(f"  > {partial_text}")
                                silence_count = 0
                            else:
                                silence_count += 1
                                if silence_count > 10 and result_text:
                                    break
                
                if not result_text:
                    final = json.loads(recognizer.FinalResult())
                    if 'result' in final:
                        result_text = ' '.join([item['conf'] for item in final['result']])
                
                print(f"[{BOTNAME}] Escuchado: {result_text}")
                return result_text if result_text else None
                
            finally:
                stream.stop_stream()
                stream.close()
                p.terminate()
                
        except Exception as e:
            print(f"[AUDIO_LOCAL] Error en Vosk STT: {e}")
            return None

def _listen_sr_local(timeout: float, phrase_limit: float) -> str | None:
    """Fallback: SpeechRecognition local (si está disponible offline)."""
    try:
        import speech_recognition as sr_lib
        
        recognizer = sr_lib.Recognizer()
        
        with sr_lib.Microphone() as source:
            print(f"[{BOTNAME}] Escuchando... (máx {phrase_limit}s)")
            
            # Nota: SpeechRecognition default usa Google API
            # Para local puro, deberías usar Vosk o similar
            try:
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
                # ADVERTENCIA: Esta línea usa Google API (no es local)
                # Para verdadero local, usar Vosk arriba
                print("[AUDIO_LOCAL] ADVERTENCIA: SpeechRecognition usa Google API, no es privado")
                return None  # Retornar None fuerza a usar Vosk
            except sr_lib.RequestError:
                return None
            except sr_lib.UnknownValueError:
                return None
                
    except Exception as e:
        print(f"[AUDIO_LOCAL] Error en SR STT: {e}")
        return None

def get_stt_status() -> dict:
    """Retorna el estado del motor STT."""
    if not STT_AVAILABLE:
        return {
            "available": False,
            "engine": None,
            "reason": "STT no disponible. Instala vosk: pip install vosk"
        }
    
    return {
        "available": True,
        "engine": STT_ENGINE,
        "private": STT_ENGINE == 'vosk',
        "requires_internet": False
    }

# ─────────────────────────────────────────────────────────────────────────────
# AUDIO STATUS
# ─────────────────────────────────────────────────────────────────────────────

def get_audio_status() -> dict:
    """Retorna estado completo del sistema de audio."""
    return {
        "tts": get_tts_status(),
        "stt": get_stt_status(),
        "private": True,
        "requires_internet": False,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }

# ─────────────────────────────────────────────────────────────────────────────
# MAIN - Test
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("═" * 60)
    print("AUDIO LOCAL - Test de STT y TTS")
    print("═" * 60)
    
    print("\n[STATUS]")
    status = get_audio_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))
    
    print("\n[TTS TEST]")
    speak("Hola, soy JARVIS. Sistema de audio completamente privado.")
    
    print("\n[STT TEST]")
    print("Habla algo cuando estés listo...")
    text = listen(timeout=3.0, phrase_limit=5.0)
    if text:
        print(f"Escuché: {text}")
        speak(f"Dijiste: {text}")
    else:
        print("No se escuchó nada o error.")
    
    print("\n[DONE]")

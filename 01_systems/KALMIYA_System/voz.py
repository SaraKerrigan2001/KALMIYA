
# Wrapper que prioriza audio_local (privado) sobre audio.voz (APIs)
# JARVIS OS: Completamente local y privado

try:
    # Primario: Audio local (STT/TTS privado, sin APIs)
    from audio.audio_local import *
    print("[VOZ] Audio local activado (privado, sin APIs)")
except ImportError:
    # Fallback: Audio con APIs (si audio_local no está disponible)
    try:
        from audio.voz import *
        print("[VOZ] Audio con APIs (fallback)")
    except ImportError:
        print("[VOZ] ERROR: Ningún módulo de audio disponible")
        raise

if __name__ == '__main__':
    try:
        main()
    except NameError:
        pass

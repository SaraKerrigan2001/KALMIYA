import subprocess as sp
from voz import speak

def open_camera():
    """Abre la aplicación de cámara de Windows."""
    try:
        sp.run('start microsoft.windows.camera:', shell=True)
        speak("Abriendo cámara")
        return True
    except Exception as e:
        speak(f"Error al abrir la cámara: {str(e)}")
        return False
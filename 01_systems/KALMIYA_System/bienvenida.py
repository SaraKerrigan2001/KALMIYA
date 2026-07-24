from datetime import datetime
from voz import speak, USERNAME, BOTNAME
from online_ops import get_location_info
from database import update_memory

def greet_user():
    """Saluda al usuario con hora, ubicación e idioma."""
    try:
        # Asegurar que la voz esté encendida al iniciar el PC
        update_memory('voice_enabled', 'true')
        now = datetime.now()
        # Formato de hora amigable
        hour_str = now.strftime("%H y %M minutos")
        
        # Obtener ubicación
        location = get_location_info()
        location_msg = ""
        if location:
            location_msg = f" desde {location['city']}, {location['country']}"
        
        hour = now.hour
        if 6 <= hour < 12:
            greeting = f"Buenos días {USERNAME}."
        elif 12 <= hour < 18:
            greeting = f"Buenas tardes {USERNAME}."
        else:
            greeting = f"Buenas noches {USERNAME}."
        
        # Construir mensaje completo
        full_intro = (
            f"Son las {hour_str}. "
            f"Te saludo{location_msg}. "
            f"Mi idioma actual es el español y estoy lista para asistirte."
        )
        
        speak(greeting)
        speak(full_intro)
    except Exception as e:
        print(f"Error en saludo: {e}")
        speak("Hola, bienvenida. Estoy lista para ayudarte.")

def daily_routine():
    """Ejecuta la rutina diaria de KALMIYA."""
    try:
        from modules.daily_activities import DailyActivities
        import os
        
        speak("Iniciando mi rutina diaria. Verificando tus módulos de productividad.")
        
        # Iniciar monitoreo de actividades silencioso si no está activo
        monitor = DailyActivities()
        res = monitor.start_monitoring()
        if res.get("status") == "success":
            speak("Monitoreo de actividades diarias activado en segundo plano.")
            
        speak("Rutina completada. El sistema está optimizado para tu sesión.")
    except Exception as e:
        print(f"Error en rutina diaria: {e}")
        speak("Hubo un problema al iniciar mi rutina diaria, pero sigo operativa.")
"""
push_to_talk.py - Sistema global de Push-to-Talk para JARVIS

Implementa:
- Hotkey global (Ctrl+Alt+M o configurable)
- Presiona para hablar, suelta para procesar
- Respuesta inmediata en voz
- Completamente privado (sin APIs)
- Compatible con Windows
"""

import threading
import keyboard  # pip install keyboard
import time
from datetime import datetime
from decouple import config

# Importar audio local
try:
    from audio.audio_local import listen, speak
except ImportError:
    print("[PTT] ADVERTENCIA: audio_local no disponible")
    listen = None
    speak = None

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────────────────────

HOTKEY = config('PTT_HOTKEY', default='ctrl+alt+m')  # Hotkey global
BOTNAME = config('BOTNAME', default='JARVIS')

# Estado global
_ptt_active = False
_listening = False
_ptt_thread = None

# ─────────────────────────────────────────────────────────────────────────────
# PUSH-TO-TALK
# ─────────────────────────────────────────────────────────────────────────────

def on_hotkey_press():
    """Se ejecuta cuando se presiona el hotkey."""
    global _listening
    
    if not listen or not speak:
        print("[PTT] Audio no disponible")
        return
    
    if _listening:
        return  # Ya está escuchando
    
    _listening = True
    print(f"[{BOTNAME}] 🎤 Escuchando... (suelta para procesar)")
    
    # Indicador visual: beep corto
    try:
        import winsound
        winsound.Beep(800, 100)  # Frecuencia 800Hz, duración 100ms
    except:
        pass

def on_hotkey_release():
    """Se ejecuta cuando se suelta el hotkey."""
    global _listening
    
    if not listen or not speak:
        return
    
    if not _listening:
        return
    
    _listening = False
    
    # Indicador visual: dos beeps
    try:
        import winsound
        winsound.Beep(1000, 100)
        time.sleep(0.1)
        winsound.Beep(1000, 100)
    except:
        pass
    
    print(f"[{BOTNAME}] ✓ Transcribiendo...")
    
    # Ejecutar escucha en hilo separado
    thread = threading.Thread(target=_process_ptt, daemon=True)
    thread.start()

def _process_ptt():
    """Procesa el audio capturado."""
    try:
        # Escuchar (máximo 8 segundos)
        text = listen(timeout=1.0, phrase_limit=8.0)
        
        if text:
            print(f"[{BOTNAME}] Dijiste: {text}")
            
            # Importar aquí para evitar circular imports
            try:
                from brain import ask_kalmiya
                response = ask_kalmiya(text)
                
                if response:
                    print(f"[{BOTNAME}] Respondiendo...")
                    speak(response)
                else:
                    print(f"[{BOTNAME}] No pude generar respuesta")
            except Exception as e:
                print(f"[PTT] Error procesando: {e}")
        else:
            print(f"[{BOTNAME}] No se escuchó nada")
            
    except Exception as e:
        print(f"[PTT] Error: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# INICIALIZACIÓN
# ─────────────────────────────────────────────────────────────────────────────

def init_ptt():
    """Inicializa el sistema de Push-to-Talk."""
    global _ptt_active
    
    if _ptt_active:
        print("[PTT] Ya está inicializado")
        return True
    
    try:
        # Registrar hotkey
        # keyboard.on_press_key() y on_release_key() funcionan con teclas individuales
        # Para combinaciones, usamos keyboard.add_hotkey()
        
        keyboard.add_hotkey(HOTKEY, on_hotkey_press)
        
        # Para la liberación, necesitamos un callback más complejo
        # Usamos un hook a nivel bajo
        def _on_key_event(event):
            if event.event_type == 'down' and event.name in ['ctrl', 'alt', 'm']:
                return
            if event.event_type == 'up':
                # Verificar si se liberó la combinación
                if not _listening:
                    return
                # Simular liberación cuando detectamos que se soltó
                on_hotkey_release()
        
        # Alternativa: Monitoreo periódico de estado del hotkey
        _monitor_ptt()
        
        _ptt_active = True
        print(f"[PTT] ✓ Sistema Push-to-Talk activado")
        print(f"[PTT] Hotkey: {HOTKEY} (presiona y habla)")
        
        return True
        
    except Exception as e:
        print(f"[PTT] ERROR al inicializar: {e}")
        print(f"[PTT] Asegúrate de instalar: pip install keyboard")
        return False

def _monitor_ptt():
    """Monitorea el estado del hotkey de forma periódica."""
    global _ptt_active, _listening
    
    def _monitor():
        import keyboard as kb
        while _ptt_active:
            try:
                # Verificar si el hotkey está presionado
                keys_pressed = kb.is_pressed(HOTKEY) if hasattr(kb, 'is_pressed') else False
                
                if keys_pressed and not _listening:
                    on_hotkey_press()
                elif not keys_pressed and _listening:
                    on_hotkey_release()
                
                time.sleep(0.05)  # Monitorear cada 50ms
            except Exception:
                pass
    
    thread = threading.Thread(target=_monitor, daemon=True)
    thread.start()

def stop_ptt():
    """Detiene el sistema Push-to-Talk."""
    global _ptt_active, _listening
    
    _ppt_active = False
    _listening = False
    
    try:
        keyboard.remove_hotkey(HOTKEY)
    except:
        pass
    
    print("[PTT] ✓ Push-to-Talk detenido")

def get_ptt_status() -> dict:
    """Retorna estado del sistema PTT."""
    return {
        "active": _ptt_active,
        "listening": _listening,
        "hotkey": HOTKEY,
        "timestamp": datetime.now().isoformat()
    }

# ─────────────────────────────────────────────────────────────────────────────
# MAIN - Test
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("═" * 60)
    print("PUSH-TO-TALK - Sistema de voz global")
    print("═" * 60)
    print(f"\nHotkey: {HOTKEY}")
    print("Presiona el hotkey y habla para interactuar con JARVIS")
    print("Presiona Ctrl+C para salir\n")
    
    if init_ptt():
        try:
            # Mantener el programa corriendo
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n[PTT] Saliendo...")
            stop_ptt()
    else:
        print("[PTT] No se pudo inicializar Push-to-Talk")

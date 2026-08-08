"""
family_guard.py - Sistema de proteccion familiar de KALMIYA
============================================================
KALMIYA vigila y protege a la familia de Sara:
  - Registro de contactos familiares
  - Alertas de emergencia por WhatsApp/SMS
  - Monitoreo de estado (check-in)
  - Notificaciones cuando un familiar se conecta
  - Mensajes automaticos de seguridad
  - KALMIYA aprende sobre cada familiar
"""

import threading
import time
import json
import os
from datetime import datetime, timedelta
from database import log_command, update_memory, get_memory
from voz import speak

try:
    import requests
    REQUESTS_OK = True
except Exception:
    REQUESTS_OK = False

try:
    import pywhatkit
    WHATSAPP_OK = True
except Exception:
    WHATSAPP_OK = False


FAMILY_STATE_FILE = os.path.join(os.path.dirname(__file__), "family_state.json")

# Estado en memoria de la familia
_family_state: dict = {}
_monitoring_active = False
_check_in_intervals: dict[str, int] = {}  # nombre -> minutos entre check-ins


# ── Carga y guardado de estado ─────────────────────────────────────────────────

def _load_state() -> dict:
    if os.path.exists(FAMILY_STATE_FILE):
        try:
            with open(FAMILY_STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _save_state():
    try:
        with open(FAMILY_STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(_family_state, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[FAMILY] Error guardando estado: {e}")


# ── Registro de familia ────────────────────────────────────────────────────────

def register_family_member(nombre: str, relacion: str, telefono: str,
                            check_in_minutes: int = 0) -> bool:
    """
    Registra un miembro de la familia en el sistema de proteccion.
    
    Args:
        nombre:            Nombre del familiar.
        relacion:          Relacion (madre, padre, hermano, etc.)
        telefono:          Numero de telefono con codigo de pais (ej: +57300...)
        check_in_minutes:  Cada cuantos minutos debe hacer check-in (0 = desactivado)
    """
    global _family_state
    _family_state = _load_state()

    _family_state[nombre] = {
        'relacion': relacion,
        'telefono': telefono,
        'estado': 'desconocido',
        'ultimo_contacto': None,
        'check_in_interval': check_in_minutes,
        'alertas_activas': True,
        'notas': [],
        'registrado': datetime.now().isoformat()
    }

    if check_in_minutes > 0:
        _check_in_intervals[nombre] = check_in_minutes

    _save_state()
    speak(f"He registrado a {nombre} como tu {relacion} en mi sistema de proteccion familiar.")
    log_command(f"[FAMILIA] Registrado: {nombre}", relacion, source='family')
    return True


def update_family_status(nombre: str, estado: str, notas: str = ""):
    """Actualiza el estado de un familiar."""
    global _family_state
    _family_state = _load_state()

    if nombre in _family_state:
        _family_state[nombre]['estado'] = estado
        _family_state[nombre]['ultimo_contacto'] = datetime.now().isoformat()
        if notas:
            _family_state[nombre]['notas'].append({
                'nota': notas,
                'fecha': datetime.now().isoformat()
            })
        _save_state()
        speak(f"Estado de {nombre} actualizado: {estado}")
        return True
    return False


def get_family_status() -> dict:
    """Devuelve el estado actual de todos los familiares."""
    return _load_state()


# ── Sistema de alertas ─────────────────────────────────────────────────────────

def send_family_alert(nombre: str, mensaje: str, urgente: bool = False):
    """
    Envia una alerta a un familiar via WhatsApp.
    
    Args:
        nombre:   Nombre del familiar registrado.
        mensaje:  Mensaje a enviar.
        urgente:  Si True, KALMIYA tambien habla el mensaje en voz alta.
    """
    state = _load_state()
    if nombre not in state:
        speak(f"No tengo registrado a {nombre} en el sistema familiar.")
        return False

    telefono = state[nombre].get('telefono', '')
    if not telefono:
        speak(f"No tengo el telefono de {nombre}.")
        return False

    if urgente:
        speak(f"Alerta urgente para {nombre}: {mensaje}")

    # Enviar por WhatsApp si esta disponible
    if WHATSAPP_OK:
        try:
            # Limpiar numero (quitar +, espacios)
            numero = telefono.replace('+', '').replace(' ', '').replace('-', '')
            now = datetime.now()
            # pywhatkit necesita hora futura
            hora = now.hour
            minuto = now.minute + 2
            if minuto >= 60:
                minuto -= 60
                hora += 1

            pywhatkit.sendwhatmsg(f"+{numero}", f"[KALMIYA] {mensaje}", hora, minuto,
                                  wait_time=15, tab_close=True)
            speak(f"Mensaje enviado a {nombre} por WhatsApp.")
            log_command(f"[FAMILIA] Alerta enviada a {nombre}", mensaje, source='family')
            return True
        except Exception as e:
            print(f"[FAMILY] Error enviando WhatsApp: {e}")

    speak(f"No pude enviar el mensaje a {nombre}. Verifica la configuracion de WhatsApp.")
    return False


def send_emergency_alert(mensaje: str = ""):
    """
    Envia una alerta de emergencia a TODOS los familiares registrados.
    """
    if not mensaje:
        mensaje = f"ALERTA DE EMERGENCIA de Sara Kerrigan. {datetime.now().strftime('%H:%M del %d/%m/%Y')}"

    speak(f"Enviando alerta de emergencia a toda la familia.")
    state = _load_state()

    if not state:
        speak("No hay familiares registrados en el sistema.")
        return

    for nombre, data in state.items():
        if data.get('alertas_activas', True):
            threading.Thread(
                target=send_family_alert,
                args=(nombre, mensaje, False),
                daemon=True
            ).start()
            time.sleep(1)  # Pequena pausa entre mensajes

    log_command("[FAMILIA] ALERTA DE EMERGENCIA", mensaje, source='family')


# ── Check-in automatico ────────────────────────────────────────────────────────

def family_check_in(nombre: str):
    """
    Registra que un familiar hizo check-in (esta bien).
    Puede ser llamado manualmente o desde el puente movil.
    """
    update_family_status(nombre, 'bien', 'Check-in automatico')
    speak(f"Check-in de {nombre} registrado. Esta bien.")


def _check_overdue_checkins():
    """Verifica si algun familiar no ha hecho check-in a tiempo."""
    state = _load_state()
    now = datetime.now()

    for nombre, data in state.items():
        interval = data.get('check_in_interval', 0)
        if interval <= 0:
            continue

        ultimo = data.get('ultimo_contacto')
        if not ultimo:
            continue

        try:
            ultimo_dt = datetime.fromisoformat(ultimo)
            diferencia = (now - ultimo_dt).total_seconds() / 60  # en minutos

            if diferencia > interval * 1.5:  # 50% de margen
                speak(f"Sara, {nombre} no ha hecho check-in en {int(diferencia)} minutos. "
                      f"Deberia haber contactado hace {interval} minutos.")
                log_command(f"[FAMILIA] Check-in tardio: {nombre}",
                            f"{int(diferencia)} minutos sin contacto", source='family')
        except Exception:
            pass


# ── Monitor familiar ───────────────────────────────────────────────────────────

def start_family_monitor():
    """Inicia el monitor de proteccion familiar en segundo plano."""
    global _monitoring_active
    _monitoring_active = True
    speak("Sistema de proteccion familiar activado. Vigilando a tu familia, Sara.")

    def _monitor():
        while _monitoring_active:
            try:
                _check_overdue_checkins()
            except Exception as e:
                print(f"[FAMILY] Error en monitor: {e}")
            time.sleep(300)  # Verificar cada 5 minutos

    t = threading.Thread(target=_monitor, daemon=True, name="family-monitor")
    t.start()
    return t


def stop_family_monitor():
    """Detiene el monitor familiar."""
    global _monitoring_active
    _monitoring_active = False
    speak("Monitor familiar desactivado.")


# ── Informacion familiar para KALMIYA ─────────────────────────────────────────

def get_family_summary_for_ai() -> str:
    """Genera un resumen de la familia para el contexto de IA."""
    state = _load_state()
    if not state:
        return "No hay familiares registrados aun."

    lines = []
    for nombre, data in state.items():
        estado = data.get('estado', 'desconocido')
        relacion = data.get('relacion', '')
        ultimo = data.get('ultimo_contacto', 'nunca')
        if ultimo and ultimo != 'nunca':
            try:
                dt = datetime.fromisoformat(ultimo)
                ultimo = dt.strftime('%d/%m %H:%M')
            except Exception:
                pass
        lines.append(f"{nombre} ({relacion}): {estado}, ultimo contacto: {ultimo}")

    return "Familia de Sara:\n" + "\n".join(lines)


# ── Aprender sobre la familia ──────────────────────────────────────────────────

def learn_about_family_member(nombre: str, info: str):
    """
    KALMIYA aprende informacion nueva sobre un familiar.
    Guarda notas autonomas sobre cada persona.
    """
    state = _load_state()
    if nombre not in state:
        speak(f"No tengo registrado a {nombre}. Primero registralo en el sistema.")
        return False

    state[nombre]['notas'].append({
        'nota': info,
        'fecha': datetime.now().isoformat(),
        'fuente': 'KALMIYA_aprendizaje'
    })

    # Guardar en memoria de base de datos tambien
    update_memory(f'familia_{nombre}_info', info)
    _family_state.update(state)
    _save_state()

    speak(f"He aprendido algo nuevo sobre {nombre} y lo he guardado en mi memoria.")
    return True


# ── Interfaz interactiva ───────────────────────────────────────────────────────

def setup_family_interactive():
    """Guia para configurar el sistema familiar."""
    speak("Vamos a configurar el sistema de proteccion familiar, Sara.")
    print("\n=== CONFIGURACION FAMILIAR ===\n")

    while True:
        nombre = input("Nombre del familiar (Enter para terminar): ").strip()
        if not nombre:
            break

        relacion = input(f"  Relacion con {nombre}: ").strip()
        telefono = input(f"  Telefono de {nombre} (con codigo de pais, ej: +57300...): ").strip()
        checkin = input(f"  Check-in cada cuantos minutos? (0 para desactivar): ").strip()
        checkin_min = int(checkin) if checkin.isdigit() else 0

        register_family_member(nombre, relacion, telefono, checkin_min)

    speak("Sistema familiar configurado. Estoy lista para proteger a tu familia.")
    print("\n[FAMILIA] Configuracion guardada.")


if __name__ == "__main__":
    setup_family_interactive()

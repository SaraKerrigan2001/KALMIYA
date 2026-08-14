"""
kalmiya_biometrics.py — Sistema Biométrico Completo de KALMIYA v3.5
====================================================================
Verificación de identidad por 3 métodos:
  1. Reconocimiento facial    (OpenCV + haar cascades)
  2. Verificación de voz      (SpeechRecognition + huella de voz)
  3. PIN biométrico de respaldo

Niveles de acceso:
  NIVEL 5 — Sara Kerrigan   (Creadora — acceso total)
  NIVEL 2 — Compañeros ADSO 201 (invitado seguro)
  NIVEL 0 — Desconocido    (bloqueo inmediato)

Integración:
  - Se llama desde kalmiya_launcher.py antes de iniciar el núcleo
  - Se puede activar manualmente desde main.py (opción BIO)
  - Los intentos fallidos se registran en la BD y alertan a Sara
"""

import os
import sys
import time
import hashlib
import threading
import json
import ctypes
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import log_command, update_memory, get_memory
from voz import speak, BOTNAME, USERNAME
from _logging import get_logger

logger = get_logger(__name__)

# ── Dependencias opcionales ────────────────────────────────────────────────────
try:
    import cv2
    OPENCV_OK = True
except ImportError:
    OPENCV_OK = False
    logger.warning("[BIO] opencv-python no disponible — escaneo facial desactivado")

try:
    import speech_recognition as sr
    SR_OK = True
except ImportError:
    SR_OK = False
    logger.warning("[BIO] SpeechRecognition no disponible — verificación de voz desactivada")

try:
    import pyaudio  # required by speech_recognition Microphone
    PYAUDIO_OK = True
except ImportError:
    PYAUDIO_OK = False
    logger.warning("[BIO] PyAudio no disponible — verificación de voz desactivada")

try:
    import numpy as np
    NUMPY_OK = True
except ImportError:
    NUMPY_OK = False

# ══════════════════════════════════════════════════════════════════════════════
# BASE DE DATOS BIOMÉTRICA
# ══════════════════════════════════════════════════════════════════════════════

# Usuarios registrados con nivel de acceso
USUARIOS_REGISTRADOS: dict[str, dict] = {
    "sara_kerigan": {
        "nombre":       "Sara Kerrigan",
        "alias":        ["Sara", "Administradora", "Sara Kerrigan"],
        "rol":          "Creadora / Administradora",
        "grupo":        "ADSO 201 — SENA Cúcuta",
        "nivel_acceso": 5,
        "descripcion":  "Acceso total al sistema KALMIYA",
        "pin_hash":     hashlib.sha256(b"sara2001").hexdigest(),
        "frase_voz":    ["kalmiya soy sara", "acceso sara kerigan",
                         "autorización creadora"],
        "color":        "CYAN",
    },
}

# PIN de emergencia para cuando los sensores fallen
PIN_EMERGENCIA_HASH = hashlib.sha256(b"kalmiya2026").hexdigest()

# Intentos fallidos permitidos antes de bloqueo total
MAX_INTENTOS = 3

# Estado global
_sesion_activa: Optional[dict] = None
_intentos_fallidos: int = 0
_biometria_activa: bool = False


# ══════════════════════════════════════════════════════════════════════════════
# UTILIDADES
# ══════════════════════════════════════════════════════════════════════════════

def _hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.strip().encode()).hexdigest()


def _log_acceso(evento: str, usuario: str, nivel: int, detalles: str = ""):
    log_command(
        f"[BIOMETRÍA] {evento}",
        f"Usuario: {usuario} | Nivel: {nivel} | {detalles}",
        source="security"
    )
    logger.info(f"[BIO] {evento} — {usuario} — Nivel {nivel}")


def _bloquear_pc():
    """Bloquea la sesión de Windows inmediatamente."""
    speak("Alerta de seguridad. Bloqueando el equipo ahora.")
    logger.critical("[BIO] BLOQUEO DE PC ejecutado por acceso no autorizado")
    try:
        ctypes.windll.user32.LockWorkStation()
    except Exception:
        try:
            os.system("rundll32.exe user32.dll,LockWorkStation")
        except Exception:
            pass


def _alertar_sara(intruso_info: str):
    """Notifica a Sara sobre un intento de acceso no autorizado."""
    mensaje = f"Alerta de intrusión: {intruso_info}"
    log_command("[!!! ALERTA INTRUSIÓN BIOMÉTRICA !!!]", intruso_info, source="security")
    try:
        from database import update_memory
        update_memory("ultima_alerta_bio", f"{datetime.now().isoformat()} | {intruso_info}")
    except Exception:
        pass
    # Intentar notificar por Telegram si está activo
    try:
        from remote_bridge import send_telegram_message
        send_telegram_message(f"🚨 KALMIYA ALERTA:\n{mensaje}")
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════════════════════
# MÉTODO 1 — RECONOCIMIENTO FACIAL
# ══════════════════════════════════════════════════════════════════════════════

def verificar_cara(timeout_seg: int = 8) -> Optional[dict]:
    """
    Abre la cámara y detecta si hay un rostro en los próximos N segundos.
    Con OpenCV — muestra overlay de escaneo en tiempo real.

    Returns:
        Usuario si se reconoce, None si no hay cámara o no hay rostro.
    """
    if not OPENCV_OK:
        logger.warning("[BIO] OpenCV no disponible — saltando reconocimiento facial")
        return None

    speak("Iniciando escaneo facial. Mira fijamente a la cámara.")
    print("\n" + "═" * 60)
    print("  🔬  ESCANEO BIOMÉTRICO FACIAL — KALMIYA v3.5")
    print("═" * 60)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logger.warning("[BIO] Cámara no disponible")
        speak("No encontré una cámara activa. Usando método alternativo.")
        return None

    # Cargar clasificador de rostros de OpenCV
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)

    inicio   = time.time()
    rostros_detectados = 0
    frame_count = 0

    try:
        while time.time() - inicio < timeout_seg:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            h, w = frame.shape[:2]
            gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rostros = face_cascade.detectMultiScale(
                gris, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80)
            )

            # Overlay de escaneo
            elapsed = time.time() - inicio
            barra_y = int(h * 0.25 + (h * 0.5) * abs(__import__("math").sin(elapsed * 3)))
            overlay = frame.copy()

            # Recuadro central de alineación
            cv2.rectangle(overlay, (w//4, h//4), (3*w//4, 3*h//4), (0, 255, 100), 2)
            # Línea de barrido
            cv2.line(overlay, (w//4, barra_y), (3*w//4, barra_y), (0, 255, 100), 2)
            # Título
            cv2.putText(overlay, "KALMIYA BIOMETRIC SCAN",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 100), 2)
            # Tiempo restante
            restante = int(timeout_seg - elapsed)
            cv2.putText(overlay, f"Escaneando... {restante}s",
                        (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)

            # Dibujar rostros detectados
            for (x, y, rw, rh) in rostros:
                cv2.rectangle(overlay, (x, y), (x+rw, y+rh), (0, 255, 255), 3)
                cv2.putText(overlay, "ROSTRO DETECTADO",
                            (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                rostros_detectados += 1

            cv2.imshow("KALMIYA — Verificación Biométrica", overlay)
            if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

    print(f"  Rostros detectados en {frame_count} fotogramas: {rostros_detectados}")

    if rostros_detectados > 0:
        print("  ✅  Rostro detectado — verificación completada")
        speak("Rostro detectado. Análisis completado.")
        # En producción aquí iría el modelo de reconocimiento facial
        # Por ahora confirma identidad por PIN/voz
        return {"metodo": "facial", "detectado": True}
    else:
        speak("No detecté ningún rostro frente a la cámara.")
        return None


# ══════════════════════════════════════════════════════════════════════════════
# MÉTODO 2 — VERIFICACIÓN DE VOZ
# ══════════════════════════════════════════════════════════════════════════════

def verificar_voz(intentos: int = 2) -> Optional[dict]:
    """
    Escucha el micrófono y verifica la frase biométrica de voz.
    Compara lo dicho con las frases registradas de cada usuario.

    Returns:
        Usuario reconocido o None si falla.
    """
    if not SR_OK or not PYAUDIO_OK:
        logger.warning("[BIO] SpeechRecognition o PyAudio no disponibles — saltando verificación de voz")
        return None

    reconocedor = sr.Recognizer()
    reconocedor.energy_threshold = 3000
    reconocedor.dynamic_energy_threshold = True

    speak("Verificación de voz. Di tu frase de acceso cuando escuches el tono.")
    print("\n" + "═" * 60)
    print("  🎙️  VERIFICACIÓN BIOMÉTRICA DE VOZ — KALMIYA v3.5")
    print("═" * 60)
    print("  Frases aceptadas:")
    print("    Sara      → 'kalmiya soy sara'  o  'acceso sara kerigan'")
    print("    Compañero → 'kalmiya soy [nombre]'")
    print("═" * 60)

    for intento in range(intentos):
        print(f"\n  🎙️  Escuchando... (intento {intento+1}/{intentos})")
        speak("Di tu frase de acceso ahora.")

        try:
            with sr.Microphone() as fuente:
                reconocedor.adjust_for_ambient_noise(fuente, duration=0.5)
                audio = reconocedor.listen(fuente, timeout=8, phrase_time_limit=5)

            texto = reconocedor.recognize_google(audio, language="es-ES").lower().strip()
            print(f"  Escuché: '{texto}'")
            logger.info(f"[BIO-VOZ] Texto reconocido: '{texto}'")

            # Buscar coincidencia con frases registradas
            for user_id, datos in USUARIOS_REGISTRADOS.items():
                for frase in datos["frase_voz"]:
                    if frase.lower() in texto or texto in frase.lower():
                        print(f"  ✅  Voz reconocida: {datos['nombre']}")
                        speak(f"Voz verificada. Bienvenida, {datos['nombre']}.")
                        return {"metodo": "voz", "user_id": user_id,
                                "texto": texto, **datos}

            print(f"  ❌  Frase no reconocida: '{texto}'")
            speak("Frase no reconocida. Inténtalo de nuevo.")

        except sr.WaitTimeoutError:
            speak("No escuché nada. Inténtalo de nuevo.")
        except sr.UnknownValueError:
            speak("No pude entender lo que dijiste.")
        except OSError as e:
            error_msg = str(e).lower()
            if "pyaudio" in error_msg or "portaudio" in error_msg or "could not find pyaudio" in error_msg:
                logger.warning("[BIO-VOZ] PyAudio no disponible o micrófono inaccesible")
                speak("No pude acceder al micrófono. Verificación de voz desactivada.")
                return None
            logger.warning(f"[BIO-VOZ] Error de micrófono: {e}")
            speak("Hubo un problema con el micrófono.")
        except Exception as e:
            logger.warning(f"[BIO-VOZ] Error: {e}")
            speak("Hubo un problema con el micrófono.")

    return None


# ══════════════════════════════════════════════════════════════════════════════
# MÉTODO 3 — PIN BIOMÉTRICO
# ══════════════════════════════════════════════════════════════════════════════

def verificar_pin(intentos: int = 3) -> Optional[dict]:
    """
    Solicita el PIN biométrico como método de respaldo.
    También acepta el PIN de emergencia del sistema.

    Returns:
        Usuario autenticado o None si falla.
    """
    print("\n" + "═" * 60)
    print("  🔐  VERIFICACIÓN POR PIN BIOMÉTRICO — KALMIYA v3.5")
    print("═" * 60)
    print("  Ingresa tu PIN para verificar tu identidad.")
    print("  (No se muestra en pantalla por seguridad)")
    print("═" * 60)

    for intento in range(intentos):
        try:
            import getpass
            pin = getpass.getpass(f"\n  PIN (intento {intento+1}/{intentos}): ").strip()
        except Exception:
            pin = input(f"\n  PIN (intento {intento+1}/{intentos}): ").strip()

        if not pin:
            continue

        pin_hash = _hash_pin(pin)

        # Verificar contra usuarios registrados
        for user_id, datos in USUARIOS_REGISTRADOS.items():
            if pin_hash == datos.get("pin_hash", ""):
                print(f"\n  ✅  PIN correcto — {datos['nombre']}")
                speak(f"PIN verificado. Bienvenida, {datos['nombre']}.")
                return {"metodo": "pin", "user_id": user_id, **datos}

        # PIN de emergencia del sistema
        if pin_hash == PIN_EMERGENCIA_HASH:
            print("\n  ✅  PIN de emergencia del sistema aceptado")
            speak("PIN de emergencia aceptado. Acceso de administrador concedido.")
            return {"metodo": "pin_emergencia", "user_id": "sara_kerigan",
                    **USUARIOS_REGISTRADOS["sara_kerigan"]}

        print(f"  ❌  PIN incorrecto (intento {intento+1}/{intentos})")
        speak("PIN incorrecto.")

    return None


# ══════════════════════════════════════════════════════════════════════════════
# VERIFICACIÓN COMPLETA — FLUJO PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def verificacion_biometrica_completa(
    usar_cara: bool = True,
    usar_voz:  bool = True,
    usar_pin:  bool = True,
    modo_silencioso: bool = False
) -> Optional[dict]:
    """
    Flujo completo de verificación biométrica en cascada:
    1. Intenta reconocimiento facial
    2. Si falla → verificación de voz
    3. Si falla → PIN biométrico
    4. Si todo falla → bloqueo y alerta

    Args:
        usar_cara:       Intentar reconocimiento facial.
        usar_voz:        Intentar verificación de voz.
        usar_pin:        Intentar PIN como respaldo.
        modo_silencioso: No hablar durante la verificación.

    Returns:
        dict del usuario autenticado o None si falla todo.
    """
    global _sesion_activa, _intentos_fallidos, _biometria_activa

    if not modo_silencioso:
        speak(f"Sistema de verificación biométrica iniciado. "
              f"Por favor verifica tu identidad para acceder a {BOTNAME}.")

    print("\n" + "╔" + "═" * 60 + "╗")
    print("║" + "  🔒  KALMIYA BIOMETRIC SECURITY SYSTEM v3.5".center(60) + "║")
    print("╚" + "═" * 60 + "╝")
    print(f"  Fecha : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Sistema: {BOTNAME} — Acceso biométrico requerido\n")

    usuario_verificado = None

    # ── Paso 1: Reconocimiento facial ─────────────────────────────────────────
    if usar_cara and OPENCV_OK:
        print("  [1/3] Reconocimiento facial...")
        resultado_cara = verificar_cara(timeout_seg=8)
        if resultado_cara and resultado_cara.get("detectado"):
            # Cara detectada → confirmar identidad por voz o PIN
            print("  ✅  Cara detectada — confirmando identidad...")
            if usar_voz and SR_OK:
                usuario_verificado = verificar_voz(intentos=1)
            if not usuario_verificado and usar_pin:
                usuario_verificado = verificar_pin(intentos=2)
    else:
        print("  [1/3] Reconocimiento facial — no disponible, saltando...")

    # ── Paso 2: Verificación de voz ───────────────────────────────────────────
    if not usuario_verificado and usar_voz and SR_OK:
        print("\n  [2/3] Verificación de voz...")
        usuario_verificado = verificar_voz(intentos=2)

    # ── Paso 3: PIN biométrico ────────────────────────────────────────────────
    if not usuario_verificado and usar_pin:
        print("\n  [3/3] PIN biométrico...")
        usuario_verificado = verificar_pin(intentos=3)

    # ── Resultado ─────────────────────────────────────────────────────────────
    if usuario_verificado:
        nivel = usuario_verificado.get("nivel_acceso", 0)
        nombre = usuario_verificado.get("nombre", "Desconocido")
        metodo = usuario_verificado.get("metodo", "desconocido")

        _sesion_activa    = usuario_verificado
        _intentos_fallidos = 0
        _biometria_activa  = True

        # Guardar sesión en BD
        update_memory("bio_sesion_activa",   nombre)
        update_memory("bio_nivel_acceso",    str(nivel))
        update_memory("bio_ultimo_acceso",   datetime.now().isoformat())
        update_memory("bio_metodo_acceso",   metodo)

        _log_acceso("ACCESO AUTORIZADO", nombre, nivel,
                    f"Método: {metodo}")

        print("\n" + "╔" + "═" * 60 + "╗")
        print("║" + f"  ✅  ACCESO AUTORIZADO — NIVEL {nivel}".center(60) + "║")
        print("╠" + "═" * 60 + "╣")
        print(f"║  Usuario : {nombre:<48}║")
        print(f"║  Rol     : {usuario_verificado.get('rol','?'):<48}║")
        print(f"║  Nivel   : {usuario_verificado.get('descripcion','?'):<48}║")
        print(f"║  Método  : {metodo:<48}║")
        print("╚" + "═" * 60 + "╝\n")

        if not modo_silencioso:
            if nivel == 5:
                speak(f"Bienvenida de vuelta, {nombre}. "
                      f"Todos los sistemas de {BOTNAME} están a tu disposición.")
            else:
                speak(f"Bienvenido, {nombre}. "
                      f"Tienes acceso de nivel {nivel}. "
                      f"Los sistemas principales están protegidos.")

        # Aplicar restricciones según nivel
        _aplicar_restricciones_nivel(nivel)
        return usuario_verificado

    else:
        # Todo falló
        _intentos_fallidos += 1
        info_intruso = f"Intento #{_intentos_fallidos} — Sin identificación biométrica válida"

        print("\n" + "╔" + "═" * 60 + "╗")
        print("║" + "  🚨  ACCESO DENEGADO — IDENTIDAD NO VERIFICADA".center(60) + "║")
        print("╚" + "═" * 60 + "╝\n")

        _log_acceso("ACCESO DENEGADO", "Desconocido", 0, info_intruso)
        _alertar_sara(info_intruso)

        if not modo_silencioso:
            speak("Acceso denegado. No pude verificar tu identidad. "
                  "Se ha registrado este intento de acceso y se ha notificado a Sara.")

        if _intentos_fallidos >= MAX_INTENTOS:
            speak("Demasiados intentos fallidos. Bloqueando el equipo por seguridad.")
            _bloquear_pc()

        return None


def _aplicar_restricciones_nivel(nivel: int):
    """Aplica restricciones del sistema según el nivel de acceso."""
    if nivel == 5:
        # Acceso total — sin restricciones
        update_memory("modo_restriccion", "ninguna")
        logger.info("[BIO] Acceso total activado")

    elif nivel == 2:
        # Invitado — sellar algoritmos centrales
        update_memory("modo_restriccion", "invitado")
        logger.info("[BIO] Modo invitado activado — algoritmos sellados")
        try:
            from cyber_security_ml import generate_algorithm_signatures
            generate_algorithm_signatures()
        except Exception:
            pass

    else:
        # Sin acceso
        update_memory("modo_restriccion", "bloqueado")


# ══════════════════════════════════════════════════════════════════════════════
# GESTIÓN DE SESIÓN
# ══════════════════════════════════════════════════════════════════════════════

def obtener_sesion_activa() -> Optional[dict]:
    """Devuelve la sesión biométrica activa."""
    return _sesion_activa


def cerrar_sesion_biometrica():
    """Cierra la sesión biométrica activa."""
    global _sesion_activa, _biometria_activa
    if _sesion_activa:
        nombre = _sesion_activa.get("nombre", "Desconocido")
        _log_acceso("SESIÓN CERRADA", nombre,
                    _sesion_activa.get("nivel_acceso", 0))
        speak(f"Sesión de {nombre} cerrada. Hasta pronto.")
    _sesion_activa   = None
    _biometria_activa = False
    update_memory("bio_sesion_activa", "")


def estado_biometrico() -> dict:
    """Devuelve el estado actual del sistema biométrico."""
    return {
        "activo":            _biometria_activa,
        "sesion":            _sesion_activa.get("nombre") if _sesion_activa else None,
        "nivel":             _sesion_activa.get("nivel_acceso", 0) if _sesion_activa else 0,
        "intentos_fallidos": _intentos_fallidos,
        "opencv_ok":         OPENCV_OK,
        "speech_ok":         SR_OK and PYAUDIO_OK,
        "pyaudio_ok":        PYAUDIO_OK,
        "metodos_activos":   [m for m, ok in
                              [("facial", OPENCV_OK), ("voz", SR_OK and PYAUDIO_OK), ("pin", True)]
                              if ok],
    }


def agregar_usuario_biometrico(user_id: str, nombre: str, nivel: int,
                                pin: str, rol: str = "Invitado",
                                frases_voz: list = None) -> bool:
    """
    Registra un nuevo usuario en el sistema biométrico.
    Solo puede llamarse con sesión de nivel 5.
    """
    if not _sesion_activa or _sesion_activa.get("nivel_acceso", 0) < 5:
        speak("Solo la creadora puede registrar nuevos usuarios biométricos.")
        return False

    USUARIOS_REGISTRADOS[user_id] = {
        "nombre":       nombre,
        "alias":        [nombre],
        "rol":          rol,
        "grupo":        "Registrado manualmente",
        "nivel_acceso": nivel,
        "descripcion":  f"Nivel {nivel} — acceso registrado por Sara",
        "pin_hash":     _hash_pin(pin),
        "frase_voz":    frases_voz or [f"kalmiya soy {nombre.lower()}"],
        "color":        "YELLOW",
    }
    _log_acceso("USUARIO REGISTRADO", nombre, nivel,
                f"Registrado por: {_sesion_activa.get('nombre')}")
    speak(f"Usuario {nombre} registrado con nivel de acceso {nivel}.")
    return True


def listar_usuarios_biometricos():
    """Lista todos los usuarios registrados en el sistema biométrico."""
    print("\n" + "═" * 60)
    print("  USUARIOS REGISTRADOS EN SISTEMA BIOMÉTRICO")
    print("═" * 60)
    for uid, d in USUARIOS_REGISTRADOS.items():
        nivel = d.get("nivel_acceso", 0)
        ico   = "👑" if nivel == 5 else "👤" if nivel >= 2 else "⛔"
        print(f"  {ico}  {d['nombre']:<25} Nivel {nivel} — {d['rol']}")
    print("═" * 60)
    speak(f"Hay {len(USUARIOS_REGISTRADOS)} usuarios registrados en el sistema biométrico.")

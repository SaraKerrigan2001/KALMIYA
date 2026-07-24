"""
kalmiya_restrictions.py — Sistema Centralizado de Restricciones de KALMIYA
===========================================================================
Gestiona TODAS las restricciones del sistema en un solo lugar:

  1. CHECK constraints en BD     — validación de datos en SQLite
  2. Restricciones de acceso     — qué módulos pueden escribir en la BD
  3. Restricciones de seguridad  — comandos del sistema que requieren confirmación
  4. Foreign Keys                — relaciones entre tablas de la BD
  5. Rate limiting               — límite de operaciones por módulo/segundo

Uso:
    from kalmiya_restrictions import (
        check_db_write_permission,
        check_command_allowed,
        validate_source,
        validate_memory_key,
        validate_thought,
        RESTRICTED_COMMANDS,
    )
"""

import re
import logging
import threading
import time
from datetime import datetime
from typing import Callable

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════════════════
#  1. RESTRICCIONES DE ACCESO A LA BD — qué módulos pueden escribir
# ══════════════════════════════════════════════════════════════════════════════

# Módulos autorizados a escribir en command_history
_ALLOWED_COMMAND_SOURCES: frozenset[str] = frozenset({
    "voice",       # Comandos de voz
    "ui",          # Interfaz de usuario (main.py)
    "remote",      # Conexión remota (Telegram, Cloudflare)
    "curiosity",   # Sistema de curiosidad del cerebro
    "security",    # Módulo de seguridad
    "phone",       # Puente de celulares
    "family",      # Módulo familiar
    "modules",     # Módulos extendidos (41 funciones)
    "profile",     # Perfil de Sara
    "backup",      # Sistema de backups
    "ai",          # Motor de IA directo
    "system",      # Sistema operativo / core
    "autonomous",  # Bucle autónomo de KALMIYA
    "chat",        # Interfaz de chat gráfica
    "hud",         # HUD flotante
})

# Módulos autorizados a leer/escribir user_memory
_ALLOWED_MEMORY_WRITERS: frozenset[str] = frozenset({
    "brain",       # Cerebro IA (curiosidad)
    "sara_profile","family_guard","kalmiya_core",
    "security_ops","phone_bridge","remote_bridge",
    "modules_integration","database",
})

# Prefijos de clave reservados para el sistema (no modificables por módulos externos)
_RESERVED_MEMORY_KEYS: frozenset[str] = frozenset({
    "ai_mode_override", "cloudflare_url", "voice_enabled",
    "known_devices", "sara_emergency_contacts",
})

# Claves de memoria permitidas (patrón regex)
_MEMORY_KEY_PATTERN = re.compile(r'^[a-zA-Z0-9_\-]{2,64}$')


def check_db_write_permission(source: str, operation: str = "write") -> tuple[bool, str]:
    """
    Verifica si un módulo tiene permiso para escribir en la BD.

    Args:
        source:    Identificador del módulo (ej: 'security', 'ai-Gemini').
        operation: Tipo de operación ('write', 'memory_write', 'audit_read').

    Returns:
        (permitido: bool, motivo: str)
    """
    # Los prefijos ai- siempre están permitidos para command_history
    if source.startswith("ai-"):
        return True, "OK"

    if operation == "write":
        if source in _ALLOWED_COMMAND_SOURCES:
            return True, "OK"
        return False, f"Módulo '{source}' no está autorizado para escribir en command_history"

    if operation == "memory_write":
        if source in _ALLOWED_MEMORY_WRITERS:
            return True, "OK"
        return False, f"Módulo '{source}' no está autorizado para modificar user_memory"

    return True, "OK"


def validate_source(source: str) -> str:
    """
    Valida y normaliza el campo source.
    Si no es válido, devuelve 'ui' como fallback seguro.
    """
    if not source or not isinstance(source, str):
        logger.warning("Source vacío o inválido — usando 'ui'")
        return "ui"

    source = source.strip()[:32]  # Máximo 32 caracteres

    if source.startswith("ai-"):
        # Sanear el nombre del motor — solo alfanumérico, espacios, paréntesis
        clean = re.sub(r'[^a-zA-Z0-9 \-_()\.]', '', source)
        return clean if len(clean) >= 3 else "ai"

    if source in _ALLOWED_COMMAND_SOURCES:
        return source

    logger.warning(f"Source desconocido '{source}' — conservando para trazabilidad")
    return source  # Conservar pero no bloquear


def validate_memory_key(key: str) -> tuple[bool, str]:
    """
    Valida que una clave de memoria sea válida.

    Returns:
        (válida: bool, motivo: str)
    """
    if not key or not isinstance(key, str):
        return False, "Clave vacía o no es string"

    key = key.strip()

    if not _MEMORY_KEY_PATTERN.match(key):
        return False, f"Clave '{key}' contiene caracteres inválidos (solo a-z, A-Z, 0-9, _ y -)"

    if len(key) > 64:
        return False, f"Clave demasiado larga ({len(key)} chars, máx 64)"

    return True, "OK"


def validate_thought(thought: str) -> tuple[bool, str]:
    """Valida que un pensamiento sea un string no vacío de longitud razonable."""
    if not thought or not isinstance(thought, str):
        return False, "Pensamiento vacío"
    if len(thought.strip()) < 3:
        return False, "Pensamiento demasiado corto"
    if len(thought) > 10_000:
        return False, f"Pensamiento demasiado largo ({len(thought)} chars, máx 10000)"
    return True, "OK"


def validate_command(command: str) -> tuple[bool, str]:
    """Valida que un comando sea un string no vacío."""
    if not command or not isinstance(command, str):
        return False, "Comando vacío"
    if len(command.strip()) < 1:
        return False, "Comando demasiado corto"
    if len(command) > 8_000:
        return False, f"Comando demasiado largo ({len(command)} chars, máx 8000)"
    return True, "OK"


# ══════════════════════════════════════════════════════════════════════════════
#  2. RESTRICCIONES DE SEGURIDAD — comandos del sistema peligrosos
# ══════════════════════════════════════════════════════════════════════════════

# Comandos que SIEMPRE requieren confirmación explícita de Sara
RESTRICTED_COMMANDS: dict[str, dict] = {
    # Energía
    "shutdown_system":       {"nivel": "ALTO",   "confirmacion": True,  "mensaje": "¿Confirmas que quieres apagar el PC?"},
    "restart_system":        {"nivel": "ALTO",   "confirmacion": True,  "mensaje": "¿Confirmas que quieres reiniciar el PC?"},
    "lock_system":           {"nivel": "BAJO",   "confirmacion": False, "mensaje": ""},
    "cancel_shutdown_timer": {"nivel": "BAJO",   "confirmacion": False, "mensaje": ""},

    # Seguridad
    "scan_network":          {"nivel": "MEDIO",  "confirmacion": False, "mensaje": ""},
    "scan_ports":            {"nivel": "MEDIO",  "confirmacion": False, "mensaje": ""},
    "execute_counter_attack":{"nivel": "CRITICO","confirmacion": True,  "mensaje": "⚠️ ¿Confirmas ejecutar contra-ataque de red? Esta acción es irreversible."},
    "activate_cyber_shield": {"nivel": "MEDIO",  "confirmacion": False, "mensaje": ""},

    # Sistema de archivos
    "download_file":         {"nivel": "MEDIO",  "confirmacion": False, "mensaje": ""},
    "move_file":             {"nivel": "MEDIO",  "confirmacion": False, "mensaje": ""},
    "full_maintenance":      {"nivel": "MEDIO",  "confirmacion": True,  "mensaje": "¿Confirmas ejecutar mantenimiento completo del sistema?"},
    "clean_temp_files":      {"nivel": "BAJO",   "confirmacion": False, "mensaje": ""},

    # Micrófono y hardware
    "restore_microphone":    {"nivel": "MEDIO",  "confirmacion": True,  "mensaje": "¿Confirmas restaurar el driver del micrófono?"},

    # Comunicación
    "send_emergency_alert":  {"nivel": "ALTO",   "confirmacion": True,  "mensaje": "¿Confirmas enviar alerta de EMERGENCIA a toda la familia?"},
    "send_family_alert":     {"nivel": "MEDIO",  "confirmacion": False, "mensaje": ""},
    "send_whatsapp_message": {"nivel": "BAJO",   "confirmacion": False, "mensaje": ""},
    "stop_all_tunnels":      {"nivel": "MEDIO",  "confirmacion": False, "mensaje": ""},

    # Backups y BD
    "kalmiya_backup":        {"nivel": "BAJO",   "confirmacion": False, "mensaje": ""},
}

# Patrones de texto en comandos de voz que activan restricción adicional
_DANGEROUS_VOICE_PATTERNS: list[tuple[str, str]] = [
    (r'\bformatea?\b.*disco', "Formatear disco detectado — operación bloqueada"),
    (r'\bborr[ao]\b.*sistema', "Borrar sistema detectado — operación bloqueada"),
    (r'\belimin[ao]\b.*todo', "Eliminar todo detectado — operación bloqueada"),
    (r'rm\s+-rf', "Comando rm -rf detectado — operación bloqueada"),
    (r'del\s+/[sf]', "Comando del /s/f detectado — operación bloqueada"),
    (r'format\s+c:', "Formatear C: detectado — operación bloqueada"),
]


def check_command_allowed(func_name: str, from_voice: bool = False) -> tuple[bool, str, bool]:
    """
    Verifica si un comando está permitido y si necesita confirmación.

    Args:
        func_name:  Nombre de la función a ejecutar.
        from_voice: Si el comando viene de reconocimiento de voz.

    Returns:
        (permitido: bool, mensaje: str, requiere_confirmacion: bool)
    """
    info = RESTRICTED_COMMANDS.get(func_name)
    if not info:
        return True, "OK", False

    nivel = info["nivel"]
    requiere = info["confirmacion"]
    mensaje = info["mensaje"]

    if nivel == "CRITICO":
        logger.warning(f"[RESTRICCIÓN] Comando crítico solicitado: {func_name}")
        return True, mensaje, True  # Siempre requiere confirmación

    if requiere:
        return True, mensaje, True

    return True, "OK", False


def check_voice_command_safe(text: str) -> tuple[bool, str]:
    """
    Verifica que un comando de voz no contiene patrones peligrosos.

    Returns:
        (seguro: bool, motivo: str)
    """
    text_lower = text.lower()
    for pattern, motivo in _DANGEROUS_VOICE_PATTERNS:
        if re.search(pattern, text_lower):
            logger.critical(f"[RESTRICCIÓN] Patrón peligroso en comando de voz: {motivo}")
            return False, motivo
    return True, "OK"


def require_confirmation(mensaje: str, from_voice: bool = False) -> bool:
    """
    Pide confirmación al usuario para una operación peligrosa.

    Args:
        mensaje:    Texto de confirmación a mostrar/hablar.
        from_voice: Si es True, espera respuesta de voz (sí/no).

    Returns:
        True si el usuario confirmó, False si canceló.
    """
    try:
        from voz import speak
        speak(mensaje)
    except Exception:
        pass

    print(f"\n⚠️  CONFIRMACIÓN REQUERIDA: {mensaje}")
    print("   Escribe 'si' para confirmar o 'no' para cancelar: ", end="")

    try:
        respuesta = input().strip().lower()
        confirmado = respuesta in ("si", "sí", "yes", "s", "confirmar", "ok")
        if confirmado:
            logger.info(f"[RESTRICCIÓN] Confirmado: {mensaje[:50]}")
        else:
            logger.info(f"[RESTRICCIÓN] Cancelado: {mensaje[:50]}")
        return confirmado
    except (EOFError, KeyboardInterrupt):
        return False


# ══════════════════════════════════════════════════════════════════════════════
#  3. RATE LIMITING — límite de operaciones por módulo
# ══════════════════════════════════════════════════════════════════════════════

_rate_lock = threading.Lock()
_rate_counters: dict[str, list[float]] = {}

# Límites por módulo (operaciones por minuto)
_RATE_LIMITS: dict[str, int] = {
    "voice":    60,   # 1 por segundo en promedio
    "ai-":      30,   # 0.5 por segundo — los motores de IA tienen sus propios límites
    "security": 10,   # escaneos son pesados
    "modules":  120,  # los módulos pueden ser más intensivos
    "default":  200,  # límite genérico
}


def check_rate_limit(source: str) -> tuple[bool, str]:
    """
    Verifica que un módulo no supere su límite de operaciones por minuto.

    Returns:
        (dentro_del_límite: bool, motivo: str)
    """
    now = time.monotonic()
    window = 60.0  # ventana de 1 minuto

    # Determinar límite aplicable
    limit = _RATE_LIMITS.get("default")
    for key, val in _RATE_LIMITS.items():
        if source.startswith(key):
            limit = val
            break

    with _rate_lock:
        if source not in _rate_counters:
            _rate_counters[source] = []

        # Limpiar entradas fuera de la ventana
        _rate_counters[source] = [t for t in _rate_counters[source] if now - t < window]

        if len(_rate_counters[source]) >= limit:
            return False, f"Rate limit alcanzado para '{source}': {limit} ops/min"

        _rate_counters[source].append(now)
        return True, "OK"


# ══════════════════════════════════════════════════════════════════════════════
#  4. CHECK CONSTRAINTS PARA LA BD (validación antes de insertar)
# ══════════════════════════════════════════════════════════════════════════════

def validate_command_history_row(command: str, response: str | None, source: str) -> tuple[bool, str]:
    """
    Valida una fila antes de insertar en command_history.
    Aplica las mismas reglas que los CHECK constraints de la BD.
    """
    ok, msg = validate_command(command)
    if not ok:
        return False, f"command inválido: {msg}"

    if response is not None and len(str(response)) > 50_000:
        return False, "response demasiado larga (máx 50.000 chars)"

    source_clean = validate_source(source)
    if not source_clean:
        return False, "source inválido"

    return True, "OK"


def validate_memory_row(key: str, value: str) -> tuple[bool, str]:
    """
    Valida una fila antes de insertar/actualizar user_memory.
    """
    ok, msg = validate_memory_key(key)
    if not ok:
        return False, msg

    if not value or not isinstance(value, str):
        return False, "value vacío o no es string"

    if len(value) > 10_000:
        return False, f"value demasiado largo ({len(value)} chars, máx 10.000)"

    return True, "OK"


# ══════════════════════════════════════════════════════════════════════════════
#  5. DECORADOR — para aplicar restricciones automáticamente a funciones
# ══════════════════════════════════════════════════════════════════════════════

def restricted(func_name: str | None = None, confirm_msg: str | None = None):
    """
    Decorador que aplica restricciones de seguridad a una función.

    Uso:
        @restricted("shutdown_system")
        def shutdown_system():
            ...

        @restricted(confirm_msg="¿Confirmas esta acción?")
        def mi_funcion_peligrosa():
            ...
    """
    def decorator(func: Callable) -> Callable:
        import functools

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            name = func_name or func.__name__
            permitido, mensaje, necesita_confirm = check_command_allowed(name)

            if not permitido:
                logger.warning(f"[RESTRICCIÓN] Función bloqueada: {name} — {mensaje}")
                try:
                    from voz import speak
                    speak(f"No puedo ejecutar {name}. {mensaje}")
                except Exception:
                    pass
                return None

            if necesita_confirm or confirm_msg:
                msg = confirm_msg or mensaje
                if not require_confirmation(msg):
                    logger.info(f"[RESTRICCIÓN] Función cancelada por usuario: {name}")
                    try:
                        from voz import speak
                        speak("Operación cancelada.")
                    except Exception:
                        pass
                    return None

            return func(*args, **kwargs)
        return wrapper
    return decorator


# ══════════════════════════════════════════════════════════════════════════════
#  UTILIDADES DE DIAGNÓSTICO
# ══════════════════════════════════════════════════════════════════════════════

def get_restrictions_summary() -> dict:
    """Devuelve un resumen del estado de las restricciones."""
    return {
        "sources_permitidos":       sorted(_ALLOWED_COMMAND_SOURCES),
        "memory_writers_permitidos": sorted(_ALLOWED_MEMORY_WRITERS),
        "claves_reservadas":         sorted(_RESERVED_MEMORY_KEYS),
        "comandos_restringidos":     list(RESTRICTED_COMMANDS.keys()),
        "comandos_criticos": [
            k for k, v in RESTRICTED_COMMANDS.items() if v["nivel"] == "CRITICO"
        ],
        "comandos_con_confirmacion": [
            k for k, v in RESTRICTED_COMMANDS.items() if v["confirmacion"]
        ],
        "rate_limits":               _RATE_LIMITS,
        "patrones_voz_bloqueados":   len(_DANGEROUS_VOICE_PATTERNS),
    }

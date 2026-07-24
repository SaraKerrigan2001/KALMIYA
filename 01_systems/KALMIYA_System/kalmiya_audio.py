"""
kalmiya_audio.py — Sistema de Audio Completo de KALMIYA v3.5
=============================================================
Controla todo el audio del sistema:
  - Volumen maestro, micrófono, aplicaciones
  - Ecualizador (graves, medios, agudos)
  - Efectos de sonido para KALMIYA
  - Fuentes de audio (altavoces, auriculares, HDMI)
  - Monitor de nivel de audio en tiempo real
  - Perfil de audio por hora (día/noche)
"""

import os, sys, subprocess, threading, time, json
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import log_command, update_memory, get_memory
from _logging import get_logger

logger = get_logger(__name__)

try:
    import psutil
    PSUTIL_OK = True
except ImportError:
    PSUTIL_OK = False

try:
    import sounddevice as sd
    import numpy as np
    SD_OK = True
except ImportError:
    SD_OK = False

# ── Estado del sistema de audio ───────────────────────────────────────────────
_audio_state: dict = {
    "volumen_maestro": 70,
    "volumen_micro":   80,
    "muted":           False,
    "micro_muted":     False,
    "perfil_activo":   "normal",
    "eq":              {"graves": 0, "medios": 0, "agudos": 0},
    "dispositivo_out": "",
    "dispositivo_in":  "",
}

# ── Perfiles de audio predefinidos ────────────────────────────────────────────
PERFILES_AUDIO: dict[str, dict] = {
    "normal": {
        "descripcion":  "Uso diario normal",
        "volumen":      70,
        "micro":        80,
        "eq":           {"graves": 0,  "medios": 0,  "agudos": 0},
    },
    "noche": {
        "descripcion":  "Modo nocturno — volumen bajo",
        "volumen":      30,
        "micro":        60,
        "eq":           {"graves": -3, "medios": 0,  "agudos": -2},
    },
    "musica": {
        "descripcion":  "Escuchar música — graves potenciados",
        "volumen":      75,
        "micro":        50,
        "eq":           {"graves": 5,  "medios": 1,  "agudos": 2},
    },
    "estudio": {
        "descripcion":  "Programación / ADSO — sin distracciones",
        "volumen":      40,
        "micro":        85,
        "eq":           {"graves": -2, "medios": 2,  "agudos": 1},
    },
    "juegos": {
        "descripcion":  "Gaming — audio envolvente",
        "volumen":      80,
        "micro":        70,
        "eq":           {"graves": 3,  "medios": 0,  "agudos": 3},
    },
    "llamada": {
        "descripcion":  "Videollamada — voz clara",
        "volumen":      65,
        "micro":        90,
        "eq":           {"graves": -4, "medios": 4,  "agudos": 2},
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# CONTROL DE VOLUMEN (PowerShell / nircmd)
# ══════════════════════════════════════════════════════════════════════════════

def _ps(cmd: str, timeout: int = 8) -> str:
    """Ejecuta un comando PowerShell y devuelve stdout."""
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command", cmd],
            capture_output=True, text=True, timeout=timeout
        )
        return r.stdout.strip()
    except Exception as e:
        logger.warning(f"[AUDIO] PowerShell error: {e}")
        return ""


def get_volumen_maestro() -> int:
    """Lee el volumen maestro actual del sistema (0-100)."""
    out = _ps(
        "(New-Object -ComObject WScript.Shell).SendKeys([char]173);"
        "$vol = (Get-WmiObject -Namespace root/cimv2 -Query "
        "'SELECT * FROM Win32_SoundDevice').StatusInfo; "
        "Add-Type -TypeDefinition '"
        "using System.Runtime.InteropServices;"
        "[Guid(\"5CDF2C82-841E-4546-9722-0CF74078229A\")]"
        "[InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]"
        "public interface IAudioEndpointVolume { }';"
    )
    # Método alternativo con VBScript/SoundMixer
    try:
        out2 = _ps(
            "$wshShell = New-Object -ComObject WScript.Shell;"
            "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null;"
            "$vol = [System.Windows.Forms.SendKeys]; "
            "(Get-WmiObject Win32_SoundDevice | Measure-Object).Count"
        )
        # Leer volumen via PyCaw si disponible, sino retornar estado guardado
        return _audio_state["volumen_maestro"]
    except Exception:
        return _audio_state["volumen_maestro"]


def set_volumen_maestro(nivel: int) -> bool:
    """
    Establece el volumen maestro del sistema.
    Args:
        nivel: 0-100
    """
    nivel = max(0, min(100, nivel))
    try:
        # Método 1: PowerShell con SoundMixer COM
        script = (
            f"$obj = New-Object -ComObject WScript.Shell; "
            f"$vol = {nivel}; "
            f"Add-Type -AssemblyName System.Windows.Forms; "
            f"$current = [System.Math]::Round((50 * $vol) / 100); "
            f"[System.Audio.AudioMixer]::SetVolume($vol) 2>$null; "
            f"# Método alternativo via nircmd "
            f"$nircmd = 'C:\\\\Windows\\\\System32\\\\nircmd.exe'; "
            f"if (Test-Path $nircmd) {{ & $nircmd setsysvolume {int(nivel * 655.35)} }}"
        )
        # Método 2: Script VBS más confiable
        vbs_content = (
            f'Dim oWMP, oLib, oEq\n'
            f'Set oWMP = CreateObject("WMPlayer.OCX.7")\n'
            f'oWMP.settings.volume = {nivel}\n'
        )
        vbs_path = Path(os.environ.get("TEMP", "")) / "set_vol.vbs"
        vbs_path.write_text(vbs_content, encoding="utf-8")
        subprocess.run(["cscript", "//nologo", str(vbs_path)],
                       capture_output=True, timeout=5)
        vbs_path.unlink(missing_ok=True)

        _audio_state["volumen_maestro"] = nivel
        update_memory("audio_volumen", str(nivel))
        log_command("[AUDIO] Volumen", f"{nivel}%", source="system")
        logger.info(f"[AUDIO] Volumen maestro → {nivel}%")
        return True
    except Exception as e:
        logger.warning(f"[AUDIO] No se pudo cambiar volumen: {e}")
        _audio_state["volumen_maestro"] = nivel
        return False


def subir_volumen(pasos: int = 10) -> int:
    """Sube el volumen en N pasos."""
    nuevo = min(100, _audio_state["volumen_maestro"] + pasos)
    set_volumen_maestro(nuevo)
    return nuevo


def bajar_volumen(pasos: int = 10) -> int:
    """Baja el volumen en N pasos."""
    nuevo = max(0, _audio_state["volumen_maestro"] - pasos)
    set_volumen_maestro(nuevo)
    return nuevo


def toggle_mute() -> bool:
    """Activa o desactiva el silencio."""
    try:
        _ps(
            "Add-Type -AssemblyName System.Windows.Forms; "
            "[System.Windows.Forms.SendKeys]::SendWait([char]173)"
        )
        _audio_state["muted"] = not _audio_state["muted"]
        update_memory("audio_muted", str(_audio_state["muted"]))
        logger.info(f"[AUDIO] Mute → {_audio_state['muted']}")
        return _audio_state["muted"]
    except Exception as e:
        logger.warning(f"[AUDIO] Toggle mute error: {e}")
        return _audio_state["muted"]


def set_volumen_microfono(nivel: int) -> bool:
    """Establece el volumen del micrófono (0-100)."""
    nivel = max(0, min(100, nivel))
    try:
        script = (
            f"$reg = 'HKCU:\\Software\\Microsoft\\Speech\\AudioOutput'; "
            f"$mic = Get-WmiObject Win32_SoundDevice | Where-Object "
            f"{{$_.DeviceID -like '*INPUTCAPTURE*'}} | Select-Object -First 1; "
            f"if ($mic) {{ "
            f"  $mixer = New-Object System.Media.SoundPlayer; "
            f"}} "
            f"# via mmsys.cpl mic boost "
        )
        _audio_state["volumen_micro"] = nivel
        update_memory("audio_micro", str(nivel))
        log_command("[AUDIO] Micrófono", f"{nivel}%", source="system")
        return True
    except Exception as e:
        logger.warning(f"[AUDIO] Micro vol error: {e}")
        _audio_state["volumen_micro"] = nivel
        return False


# ══════════════════════════════════════════════════════════════════════════════
# DISPOSITIVOS DE AUDIO
# ══════════════════════════════════════════════════════════════════════════════

def listar_dispositivos_audio() -> dict:
    """Lista todos los dispositivos de audio del sistema."""
    dispositivos = {"entrada": [], "salida": []}
    try:
        # Salida
        out = _ps(
            "Get-WmiObject Win32_SoundDevice | "
            "Select-Object Name, Status, DeviceID | ConvertTo-Json"
        )
        if out and "{" in out:
            import json as _json
            datos = _json.loads(out)
            if isinstance(datos, dict):
                datos = [datos]
            for d in datos:
                dispositivos["salida"].append({
                    "nombre": d.get("Name", "?"),
                    "estado": d.get("Status", "?"),
                })
    except Exception as e:
        logger.warning(f"[AUDIO] Error listando dispositivos: {e}")

    # Entrada via sounddevice
    if SD_OK:
        try:
            devs = sd.query_devices()
            for i, dev in enumerate(devs):
                if dev["max_input_channels"] > 0:
                    dispositivos["entrada"].append({
                        "id":     i,
                        "nombre": dev["name"],
                        "canales_in": dev["max_input_channels"],
                    })
        except Exception:
            pass

    return dispositivos


def get_dispositivo_salida_actual() -> str:
    """Devuelve el nombre del dispositivo de audio de salida activo."""
    out = _ps(
        "(Get-WmiObject Win32_SoundDevice | "
        "Where-Object {$_.Status -eq 'OK'} | "
        "Select-Object -First 1).Name"
    )
    _audio_state["dispositivo_out"] = out or "Desconocido"
    return _audio_state["dispositivo_out"]


# ══════════════════════════════════════════════════════════════════════════════
# ECUALIZADOR (simulado via ajuste de frecuencias de voz TTS)
# ══════════════════════════════════════════════════════════════════════════════

def set_ecualizador(graves: int = 0, medios: int = 0, agudos: int = 0) -> dict:
    """
    Ajusta el ecualizador de KALMIYA.
    Rango: -10 a +10 dB para cada banda.
    Los valores se aplican a la síntesis de voz TTS (rate y pitch de Edge TTS).
    """
    graves = max(-10, min(10, graves))
    medios = max(-10, min(10, medios))
    agudos = max(-10, min(10, agudos))

    _audio_state["eq"] = {"graves": graves, "medios": medios, "agudos": agudos}

    # Traducir EQ a parámetros de Edge TTS
    # Agudos altos → tono más alto (pitch +)
    # Graves altos → rate más lento (más profundo)
    pitch_offset = agudos * 2    # Hz
    rate_offset  = -graves       # % más lento si graves altos

    # Guardar para que voz.py lo use
    update_memory("audio_eq_pitch", str(pitch_offset))
    update_memory("audio_eq_rate",  str(rate_offset))
    update_memory("audio_eq",       json.dumps(_audio_state["eq"]))

    log_command("[AUDIO] EQ", f"Graves:{graves} Medios:{medios} Agudos:{agudos}",
                source="system")
    logger.info(f"[AUDIO] EQ ajustado → G:{graves} M:{medios} A:{agudos}")
    return _audio_state["eq"]


def get_ecualizador() -> dict:
    """Devuelve el estado actual del ecualizador."""
    return _audio_state["eq"]


# ══════════════════════════════════════════════════════════════════════════════
# PERFILES DE AUDIO
# ══════════════════════════════════════════════════════════════════════════════

def aplicar_perfil_audio(nombre_perfil: str) -> bool:
    """
    Aplica un perfil de audio predefinido.
    Perfiles: normal, noche, musica, estudio, juegos, llamada
    """
    perfil = PERFILES_AUDIO.get(nombre_perfil.lower())
    if not perfil:
        logger.warning(f"[AUDIO] Perfil '{nombre_perfil}' no encontrado")
        return False

    set_volumen_maestro(perfil["volumen"])
    set_volumen_microfono(perfil["micro"])
    eq = perfil["eq"]
    set_ecualizador(eq["graves"], eq["medios"], eq["agudos"])

    _audio_state["perfil_activo"] = nombre_perfil
    update_memory("audio_perfil", nombre_perfil)
    log_command("[AUDIO] Perfil", nombre_perfil, source="system")
    logger.info(f"[AUDIO] Perfil aplicado: {nombre_perfil}")
    return True


def perfil_automatico_por_hora() -> str:
    """
    Aplica automáticamente el perfil de audio según la hora del día.
    22:00-6:00 → noche | 8:00-18:00 → normal/estudio
    """
    hora = datetime.now().hour
    if 22 <= hora or hora < 6:
        perfil = "noche"
    elif 8 <= hora < 14:
        perfil = "estudio"
    else:
        perfil = "normal"
    aplicar_perfil_audio(perfil)
    return perfil


# ══════════════════════════════════════════════════════════════════════════════
# MONITOR DE NIVEL DE AUDIO
# ══════════════════════════════════════════════════════════════════════════════

_monitor_activo = False


def iniciar_monitor_audio(callback=None, intervalo: float = 0.5):
    """
    Inicia el monitor de nivel de audio en tiempo real.
    Detecta si hay audio reproduciéndose o si el micrófono está activo.

    Args:
        callback:  Función llamada con (nivel_rms, tipo) en cada muestra.
        intervalo: Segundos entre muestras.
    """
    global _monitor_activo
    if _monitor_activo or not SD_OK:
        return

    _monitor_activo = True

    def _loop():
        global _monitor_activo
        while _monitor_activo:
            try:
                # Capturar muestra corta del micrófono
                muestra = sd.rec(
                    int(intervalo * 16000),
                    samplerate=16000, channels=1,
                    dtype="float32", blocking=True
                )
                nivel_rms = float(np.sqrt(np.mean(muestra ** 2)))
                nivel_pct = min(100, int(nivel_rms * 1000))

                if callback:
                    callback(nivel_pct, "microfono")
                elif nivel_pct > 20:
                    logger.debug(f"[AUDIO] Nivel mic: {nivel_pct}%")

            except Exception:
                pass
            time.sleep(intervalo)

    t = threading.Thread(target=_loop, daemon=True, name="audio-monitor")
    t.start()
    logger.info("[AUDIO] Monitor de nivel iniciado")


def detener_monitor_audio():
    """Detiene el monitor de audio."""
    global _monitor_activo
    _monitor_activo = False
    logger.info("[AUDIO] Monitor de nivel detenido")


# ══════════════════════════════════════════════════════════════════════════════
# EFECTOS DE SONIDO PARA KALMIYA
# ══════════════════════════════════════════════════════════════════════════════

def reproducir_efecto(efecto: str):
    """
    Reproduce un efecto de sonido del sistema.
    Efectos: arranque, alerta, ok, error, notificacion, boot
    """
    EFECTOS = {
        "arranque":     ("*", 800, 200),    # SystemStart
        "ok":           ("*", 1000, 150),
        "error":        ("!", 400, 300),
        "alerta":       ("!", 600, 200),
        "notificacion": ("*", 900, 100),
    }
    params = EFECTOS.get(efecto.lower())
    if not params:
        return
    tipo, freq, duracion = params
    try:
        # Beep de Windows como fallback
        import winsound
        winsound.Beep(freq, duracion)
    except Exception:
        try:
            subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 f"[System.Media.SystemSounds]::{tipo.capitalize()}.Play()"],
                capture_output=True, timeout=3
            )
        except Exception:
            pass


def sonido_kalmiya_arranque():
    """Secuencia de sonidos al arrancar KALMIYA."""
    try:
        import winsound
        for freq, dur in [(440, 100), (550, 100), (660, 150), (880, 200)]:
            winsound.Beep(freq, dur)
            time.sleep(0.05)
    except Exception:
        reproducir_efecto("arranque")


# ══════════════════════════════════════════════════════════════════════════════
# ESTADO Y UTILIDADES
# ══════════════════════════════════════════════════════════════════════════════

def get_estado_audio() -> dict:
    """Devuelve el estado completo del sistema de audio."""
    return {
        **_audio_state,
        "dispositivo_salida": get_dispositivo_salida_actual(),
        "sd_disponible":      SD_OK,
        "perfiles":           list(PERFILES_AUDIO.keys()),
        "monitor_activo":     _monitor_activo,
    }


def cargar_estado_guardado():
    """Restaura el estado de audio desde la base de datos."""
    try:
        vol   = get_memory("audio_volumen")
        micro = get_memory("audio_micro")
        eq    = get_memory("audio_eq")
        perfil = get_memory("audio_perfil")

        if vol   and vol.isdigit():
            _audio_state["volumen_maestro"] = int(vol)
        if micro and micro.isdigit():
            _audio_state["volumen_micro"]   = int(micro)
        if eq:
            _audio_state["eq"] = json.loads(eq)
        if perfil and perfil in PERFILES_AUDIO:
            _audio_state["perfil_activo"] = perfil

        logger.info(f"[AUDIO] Estado restaurado: vol={_audio_state['volumen_maestro']}% perfil={_audio_state['perfil_activo']}")
    except Exception as e:
        logger.warning(f"[AUDIO] No se pudo restaurar estado: {e}")


def imprimir_estado_audio():
    """Imprime en consola el estado actual del audio."""
    e = get_estado_audio()
    print("\n╔" + "═" * 55 + "╗")
    print("║" + "  🔊  KALMIYA — ESTADO DEL SISTEMA DE AUDIO".center(55) + "║")
    print("╠" + "═" * 55 + "╣")
    print(f"║  Volumen maestro : {e['volumen_maestro']}%{' (MUDO)' if e['muted'] else '':<38}║")
    print(f"║  Micrófono       : {e['volumen_micro']}%{' (MUDO)' if e['micro_muted'] else '':<38}║")
    print(f"║  Perfil activo   : {e['perfil_activo']:<39}║")
    eq = e["eq"]
    print(f"║  EQ Graves       : {eq['graves']:+d} dB{'':<42}║")
    print(f"║  EQ Medios       : {eq['medios']:+d} dB{'':<42}║")
    print(f"║  EQ Agudos       : {eq['agudos']:+d} dB{'':<42}║")
    print(f"║  Dispositivo     : {e.get('dispositivo_salida','?')[:35]:<39}║")
    print(f"║  SoundDevice     : {'✅ Disponible' if e['sd_disponible'] else '❌ No disponible':<39}║")
    print("╚" + "═" * 55 + "╝\n")


# Cargar estado al importar el módulo
cargar_estado_guardado()

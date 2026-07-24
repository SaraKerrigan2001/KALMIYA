import os
import shutil
import subprocess as sp
from voz import speak

# Obtener el directorio del usuario actual
current_user = os.getenv('USERNAME', 'Usuario')
appdata_path = os.getenv('APPDATA', os.path.join(r'C:\Users', current_user, 'AppData', 'Roaming'))

# Rutas de aplicaciones
local_appdata = os.getenv('LOCALAPPDATA', os.path.join(r'C:\Users', current_user, 'AppData', 'Local'))
default_obsidian_path = os.path.join(local_appdata, 'Programs', 'Obsidian', 'Obsidian.exe')
program_files_obsidian_path = os.path.join(r'C:\Program Files', 'Obsidian', 'Obsidian.exe')
obsidian_path = os.getenv('OBSIDIAN_EXECUTABLE_PATH', default_obsidian_path)
if not os.path.isfile(obsidian_path) and os.path.isfile(program_files_obsidian_path):
    obsidian_path = program_files_obsidian_path

paths = {
    'notepad': r"C:\Program Files\Notepad++\notepad++.exe",
    'discord': os.path.join(local_appdata, r"Discord\app-1.0.9015\Discord.exe"),
    'calculator': r"C:\Windows\System32\calc.exe",
    'obsidian': obsidian_path
}

obsidian_vault_path = os.getenv('OBSIDIAN_VAULT_PATH', '')

def open_application(app_name):
    """Abre una aplicación basada en su nombre clave."""
    try:
        if app_name in paths and paths[app_name]:
            sp.Popen(paths[app_name])
            speak(f"Abriendo {app_name}")
            return True
        else:
            speak(f"La aplicación {app_name} no está en mi base de datos de rutas.")
            return False
    except Exception as e:
        speak(f"Error al abrir {app_name}: {e}")
        return False


def find_obsidian_executable():
    """Busca el ejecutable de Obsidian en el sistema."""
    if shutil.which('obsidian'):
        return shutil.which('obsidian')
    if os.path.isfile(paths.get('obsidian', '')):
        return paths.get('obsidian')
    return None


def open_obsidian_vault(vault_path=None):
    """Abre Obsidian y, si está configurado, abre directamente la bóveda indicada."""
    try:
        executable = find_obsidian_executable()
        if vault_path:
            vault_path = os.path.abspath(os.path.expandvars(os.path.expanduser(vault_path)))
        elif obsidian_vault_path:
            vault_path = os.path.abspath(obsidian_vault_path)

        if executable:
            if vault_path and os.path.isdir(vault_path):
                sp.Popen([executable, vault_path])
                speak("Abriendo Obsidian con la bóveda configurada.")
                return True
            sp.Popen([executable])
            speak("Abriendo Obsidian.")
            return True

        if vault_path and os.path.isdir(vault_path):
            os.startfile(vault_path)
            speak("Abriendo carpeta local de la bóveda. Si Obsidian está instalado, debería activarse automáticamente.")
            return True

        speak("No encontré Obsidian instalado ni una ruta válida de bóveda.")
        return False
    except Exception as e:
        speak(f"Error al abrir Obsidian: {e}")
        return False


def load_obsidian_vault_path():
    """Devuelve la ruta válida de la bóveda de Obsidian si está configurada."""
    # Intentar primero con python-decouple (lee el .env del proyecto)
    try:
        from decouple import config as _dconfig
        path = _dconfig('OBSIDIAN_VAULT_PATH', default='').strip()
    except Exception:
        path = os.getenv('OBSIDIAN_VAULT_PATH', '').strip()

    if path:
        path = os.path.abspath(os.path.expandvars(os.path.expanduser(path)))
        if os.path.isdir(path):
            return path
    return ''


def shutdown_system(minutes=0):
    """Programa el apagado del sistema."""
    from kalmiya_restrictions import check_command_allowed, require_confirmation
    _, mensaje, necesita = check_command_allowed("shutdown_system")
    if necesita and not require_confirmation(mensaje):
        speak("Apagado cancelado.")
        return False
    try:
        seconds = int(minutes) * 60
        os.system(f"shutdown /s /t {seconds}")
        if minutes > 0:
            speak(f"Sistema programado para apagarse en {minutes} minutos.")
        else:
            speak("Iniciando secuencia de apagado inmediato.")
        return True
    except Exception as e:
        speak(f"Error al programar apagado: {e}")
        return False

def restart_system():
    """Reinicia el sistema."""
    from kalmiya_restrictions import check_command_allowed, require_confirmation
    _, mensaje, necesita = check_command_allowed("restart_system")
    if necesita and not require_confirmation(mensaje):
        speak("Reinicio cancelado.")
        return False
    try:
        os.system("shutdown /r /t 0")
        speak("Reiniciando el sistema.")
        return True
    except Exception as e:
        speak(f"Error al reiniciar: {e}")
        return False

def lock_system():
    """Bloquea la sesión actual (Apartar PC)."""
    try:
        import ctypes
        ctypes.windll.user32.LockWorkStation()
        speak("Sistema bloqueado. Protocolo 'Apartar' activado.")
        return True
    except Exception as e:
        speak(f"Error al bloquear el sistema: {e}")
        return False

def cancel_shutdown_timer():
    """Cancela un apagado programado."""
    try:
        # En Windows shutdown /a devuelve 0 si tiene éxito
        result = os.system("shutdown /a")
        if result == 0:
            speak("Secuencia de apagado cancelada.")
            return True
        else:
            speak("No hay ninguna secuencia de apagado activa para cancelar.")
            return False
    except Exception:
        return False

# ==================== CONTROLES DE HARDWARE (KALMIYA v3.5) ====================

def set_volume(action):
    """Controla el volumen del sistema."""
    if action == "up":
        cmd = "(New-Object -ComObject WScript.Shell).SendKeys([char]175)"
    elif action == "down":
        cmd = "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"
    elif action == "mute":
        cmd = "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"
    else:
        # Acción no reconocida, no ejecutamos comando
        return f"Acción de volumen no soportada: {action}"

    sp.run(["powershell", "-Command", cmd], capture_output=True)
    return f"Volumen: {action}"

def media_control(action):
    """Controla la reproducción multimedia."""
    codes = {"play": 179, "next": 176, "prev": 177}
    if action in codes:
        cmd = f"(New-Object -ComObject WScript.Shell).SendKeys([char]{codes[action]})"
        sp.run(["powershell", "-Command", cmd], capture_output=True)
    return f"Multimedia: {action}"

def take_screenshot():
    """Captura la pantalla usando PowerShell (sin dependencias)."""
    if not os.path.exists("static"): os.makedirs("static")
    script = """
    [Reflection.Assembly]::LoadWithPartialName('System.Drawing') | Out-Null
    [Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null
    $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bmp = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bmp)
    $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
    $bmp.Save('static/screen.jpg', [System.Drawing.Imaging.ImageFormat]::Jpeg)
    $graphics.Dispose()
    $bmp.Dispose()
    """
    sp.run(["powershell", "-Command", script], capture_output=True)
    return "/static/screen.jpg"

def type_text(text):
    """Escribe texto en la ventana activa de la PC."""
    if not text: return "Texto vacío."
    
    # Escapar caracteres especiales de SendKeys: +, ^, %, ~, (, ), {, }
    special_chars = ['+', '^', '%', '~', '(', ')', '{', '}']
    escaped_text = ""
    for char in text:
        if char in special_chars:
            escaped_text += "{" + char + "}"
        else:
            escaped_text += char
            
    # Escapar comillas para PowerShell
    safe_text = escaped_text.replace("'", "''").replace('"', '\"')
    cmd = f"(New-Object -ComObject WScript.Shell).SendKeys('{safe_text}')"
    sp.run(["powershell", "-Command", cmd], capture_output=True)
    speak(f"Tecleando {text[:20]}...")
    return f"Texto enviado: {text}"

def press_key(key):
    """Presiona una tecla especial (enter, esc, alt-f4)."""
    keys = {
        "enter": "~",
        "esc": "{ESC}",
        "tab": "{TAB}",
        "backspace": "{BACKSPACE}",
        "alt_f4": "%{F4}",
        "space": " "
    }
    if key in keys:
        cmd = f"(New-Object -ComObject WScript.Shell).SendKeys('{keys[key]}')"
        sp.run(["powershell", "-Command", cmd], capture_output=True)
        return f"Tecla {key} presionada."
    return "Tecla no soportada."


# ==================== INFORMACIÓN COMPLETA DEL SISTEMA (KALMIYA v3.5) ====================

def get_full_system_info() -> dict:
    """
    Recopila información completa del sistema operativo y hardware del PC.

    Incluye:
      - OS: nombre, versión, build, arquitectura, edición
      - CPU: nombre, núcleos físicos/lógicos, frecuencia
      - RAM: total, disponible, uso
      - Disco: unidades, espacio total/libre/usado
      - Pantalla: resolución y DPI
      - Red: hostname, IP local, MAC
      - BIOS: fabricante, versión, fecha
      - GPU: nombre y VRAM (si está disponible)
      - Placa base: fabricante y modelo
      - Usuario actual y nombre del equipo

    Returns:
        dict con toda la información. Cada clave puede ser None si no está disponible.
    """
    import platform
    import socket
    import uuid

    try:
        import psutil
        PSUTIL_OK = True
    except ImportError:
        PSUTIL_OK = False

    info = {}

    # ── Sistema Operativo ──────────────────────────────────────────────────────
    try:
        info['os_nombre']       = platform.system()
        info['os_version']      = platform.version()
        info['os_release']      = platform.release()
        info['os_arquitectura'] = platform.machine()
        info['os_plataforma']   = platform.platform()
        info['os_bits']         = '64-bit' if platform.machine().endswith('64') else '32-bit'
    except Exception:
        info['os_nombre'] = 'Desconocido'

    # Edición de Windows (Home/Pro/Enterprise)
    try:
        result = sp.run(
            ['powershell', '-NoProfile', '-Command',
             '(Get-WmiObject Win32_OperatingSystem).Caption'],
            capture_output=True, text=True, timeout=10
        )
        info['os_edicion'] = result.stdout.strip() or 'Desconocido'
    except Exception:
        info['os_edicion'] = 'Desconocido'

    # Build de Windows
    try:
        result = sp.run(
            ['powershell', '-NoProfile', '-Command',
             '(Get-WmiObject Win32_OperatingSystem).BuildNumber'],
            capture_output=True, text=True, timeout=10
        )
        info['os_build'] = result.stdout.strip() or 'Desconocido'
    except Exception:
        info['os_build'] = 'Desconocido'

    # Fecha de instalación del SO
    try:
        result = sp.run(
            ['powershell', '-NoProfile', '-Command',
             '(Get-WmiObject Win32_OperatingSystem).InstallDate'],
            capture_output=True, text=True, timeout=10
        )
        info['os_instalacion'] = result.stdout.strip()[:8] or 'Desconocido'
    except Exception:
        info['os_instalacion'] = 'Desconocido'

    # ── CPU ───────────────────────────────────────────────────────────────────
    try:
        info['cpu_nombre'] = platform.processor()
    except Exception:
        info['cpu_nombre'] = 'Desconocido'

    try:
        result = sp.run(
            ['powershell', '-NoProfile', '-Command',
             '(Get-WmiObject Win32_Processor).Name'],
            capture_output=True, text=True, timeout=10
        )
        nombre = result.stdout.strip()
        if nombre:
            info['cpu_nombre'] = nombre
    except Exception:
        pass

    if PSUTIL_OK:
        try:
            info['cpu_nucleos_fisicos'] = psutil.cpu_count(logical=False)
            info['cpu_nucleos_logicos'] = psutil.cpu_count(logical=True)
            freq = psutil.cpu_freq()
            info['cpu_frecuencia_mhz'] = round(freq.current) if freq else None
            info['cpu_frecuencia_max_mhz'] = round(freq.max) if freq else None
            info['cpu_uso_pct'] = psutil.cpu_percent(interval=1)
        except Exception:
            pass

    # ── RAM ───────────────────────────────────────────────────────────────────
    if PSUTIL_OK:
        try:
            mem = psutil.virtual_memory()
            info['ram_total_gb']     = round(mem.total / (1024 ** 3), 2)
            info['ram_disponible_gb'] = round(mem.available / (1024 ** 3), 2)
            info['ram_uso_pct']      = mem.percent
            info['ram_usada_gb']     = round(mem.used / (1024 ** 3), 2)
        except Exception:
            pass

    # Tipo de RAM (DDR4, DDR5, etc.) — usar SMBIOSMemoryType que es más fiable
    try:
        result = sp.run(
            ['powershell', '-NoProfile', '-Command',
             '(Get-WmiObject Win32_PhysicalMemory | Select-Object -First 1).SMBIOSMemoryType'],
            capture_output=True, text=True, timeout=10
        )
        tipos = {
            20: 'DDR', 21: 'DDR2', 22: 'DDR2 FB-DIMM',
            24: 'DDR3', 26: 'DDR4', 27: 'LPDDR', 28: 'LPDDR2',
            29: 'LPDDR3', 30: 'LPDDR4', 34: 'DDR5', 35: 'LPDDR5'
        }
        tipo_num = result.stdout.strip()
        info['ram_tipo'] = tipos.get(int(tipo_num), 'DDR4') if tipo_num.isdigit() else 'DDR4'
    except Exception:
        info['ram_tipo'] = 'Desconocido'

    # Velocidad de RAM
    try:
        result = sp.run(
            ['powershell', '-NoProfile', '-Command',
             '(Get-WmiObject Win32_PhysicalMemory | Select-Object -First 1).Speed'],
            capture_output=True, text=True, timeout=10
        )
        info['ram_velocidad_mhz'] = result.stdout.strip() or 'Desconocido'
    except Exception:
        info['ram_velocidad_mhz'] = 'Desconocido'

    # ── DISCO ─────────────────────────────────────────────────────────────────
    if PSUTIL_OK:
        try:
            discos = []
            for particion in psutil.disk_partitions():
                try:
                    uso = psutil.disk_usage(particion.mountpoint)
                    discos.append({
                        'unidad':      particion.mountpoint,
                        'tipo':        particion.fstype,
                        'total_gb':    round(uso.total  / (1024 ** 3), 2),
                        'usado_gb':    round(uso.used   / (1024 ** 3), 2),
                        'libre_gb':    round(uso.free   / (1024 ** 3), 2),
                        'uso_pct':     uso.percent
                    })
                except PermissionError:
                    continue
            info['discos'] = discos
        except Exception:
            info['discos'] = []

    # Modelo de disco (SSD/HDD)
    try:
        result = sp.run(
            ['powershell', '-NoProfile', '-Command',
             'Get-PhysicalDisk | Select-Object FriendlyName,MediaType,Size | ConvertTo-Json'],
            capture_output=True, text=True, timeout=15
        )
        import json as _json
        raw = result.stdout.strip()
        if raw:
            datos = _json.loads(raw)
            if isinstance(datos, dict):
                datos = [datos]
            info['discos_fisicos'] = [
                {
                    'nombre': d.get('FriendlyName', 'Desconocido'),
                    'tipo':   d.get('MediaType', 'Desconocido'),
                    'size_gb': round(int(d.get('Size', 0)) / (1024 ** 3), 2) if d.get('Size') else 0
                }
                for d in datos
            ]
    except Exception:
        info['discos_fisicos'] = []

    # ── GPU ───────────────────────────────────────────────────────────────────
    try:
        result = sp.run(
            ['powershell', '-NoProfile', '-Command',
             'Get-WmiObject Win32_VideoController | Select-Object Name,AdapterRAM | ConvertTo-Json'],
            capture_output=True, text=True, timeout=15
        )
        import json as _json
        raw = result.stdout.strip()
        if raw:
            datos = _json.loads(raw)
            if isinstance(datos, dict):
                datos = [datos]
            info['gpus'] = [
                {
                    'nombre': d.get('Name', 'Desconocido'),
                    'vram_gb': round(int(d.get('AdapterRAM', 0)) / (1024 ** 3), 2) if d.get('AdapterRAM') else 0
                }
                for d in datos
            ]
    except Exception:
        info['gpus'] = []

    # ── PLACA BASE ────────────────────────────────────────────────────────────
    try:
        result = sp.run(
            ['powershell', '-NoProfile', '-Command',
             '(Get-WmiObject Win32_BaseBoard).Manufacturer + " | " + (Get-WmiObject Win32_BaseBoard).Product'],
            capture_output=True, text=True, timeout=10
        )
        info['placa_base'] = result.stdout.strip() or 'Desconocido'
    except Exception:
        info['placa_base'] = 'Desconocido'

    # ── BIOS ──────────────────────────────────────────────────────────────────
    try:
        result = sp.run(
            ['powershell', '-NoProfile', '-Command',
             '(Get-WmiObject Win32_BIOS).SMBIOSBIOSVersion + " | " + (Get-WmiObject Win32_BIOS).Manufacturer'],
            capture_output=True, text=True, timeout=10
        )
        info['bios'] = result.stdout.strip() or 'Desconocido'
    except Exception:
        info['bios'] = 'Desconocido'

    # ── RED ───────────────────────────────────────────────────────────────────
    try:
        info['hostname'] = socket.gethostname()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        info['ip_local'] = s.getsockname()[0]
        s.close()
    except Exception:
        info['hostname'] = 'Desconocido'
        info['ip_local'] = 'Desconocido'

    try:
        info['mac'] = ':'.join(
            ['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 48, 8)][::-1]
        )
    except Exception:
        info['mac'] = 'Desconocido'

    # ── USUARIO Y EQUIPO ──────────────────────────────────────────────────────
    info['usuario']      = os.getenv('USERNAME', 'Desconocido')
    info['nombre_equipo'] = os.getenv('COMPUTERNAME', 'Desconocido')

    # ── PANTALLA ──────────────────────────────────────────────────────────────
    try:
        # Intentar con Win32_VideoController primero
        result = sp.run(
            ['powershell', '-NoProfile', '-Command',
             '$s = (Get-WmiObject Win32_VideoController | Where-Object {$_.CurrentHorizontalResolution -gt 0} | Select-Object -First 1);'
             'if ($s) { "$($s.CurrentHorizontalResolution)x$($s.CurrentVerticalResolution)" }'
             'else {'
             '  $m = (Get-WmiObject Win32_DesktopMonitor | Select-Object -First 1);'
             '  if ($m -and $m.ScreenWidth) { "$($m.ScreenWidth)x$($m.ScreenHeight)" }'
             '  else {'
             '    Add-Type -AssemblyName System.Windows.Forms;'
             '    $b = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds;'
             '    "$($b.Width)x$($b.Height)"'
             '  }'
             '}'],
            capture_output=True, text=True, timeout=12
        )
        res = result.stdout.strip()
        info['resolucion'] = res if (res and 'x' in res and res != 'x') else 'Desconocido'
    except Exception:
        info['resolucion'] = 'Desconocido'

    return info


def print_full_system_info() -> str:
    """
    Muestra en consola y devuelve como string la información completa del sistema.
    También habla un resumen por voz.
    """
    data = get_full_system_info()

    lineas = [
        "",
        "╔══════════════════════════════════════════════════════╗",
        "║        KALMIYA — INFORMACIÓN COMPLETA DEL SISTEMA    ║",
        "╚══════════════════════════════════════════════════════╝",
        "",
        f"  EQUIPO       : {data.get('nombre_equipo')}",
        f"  USUARIO      : {data.get('usuario')}",
        "",
        "── SISTEMA OPERATIVO ──────────────────────────────────",
        f"  Edición      : {data.get('os_edicion')}",
        f"  Versión      : {data.get('os_release')} (Build {data.get('os_build')})",
        f"  Arquitectura : {data.get('os_arquitectura')} {data.get('os_bits')}",
        f"  Instalado    : {data.get('os_instalacion')}",
        "",
        "── PROCESADOR ─────────────────────────────────────────",
        f"  CPU          : {data.get('cpu_nombre')}",
        f"  Núcleos      : {data.get('cpu_nucleos_fisicos')} físicos / {data.get('cpu_nucleos_logicos')} lógicos",
        f"  Frecuencia   : {data.get('cpu_frecuencia_mhz')} MHz (máx {data.get('cpu_frecuencia_max_mhz')} MHz)",
        f"  Uso actual   : {data.get('cpu_uso_pct')} %",
        "",
        "── MEMORIA RAM ────────────────────────────────────────",
        f"  Total        : {data.get('ram_total_gb')} GB ({data.get('ram_tipo')} {data.get('ram_velocidad_mhz')} MHz)",
        f"  Usada        : {data.get('ram_usada_gb')} GB ({data.get('ram_uso_pct')} %)",
        f"  Disponible   : {data.get('ram_disponible_gb')} GB",
        "",
        "── ALMACENAMIENTO ─────────────────────────────────────",
    ]

    for disco in data.get('discos_fisicos', []):
        lineas.append(f"  Disco        : {disco['nombre']} ({disco['tipo']}) — {disco['size_gb']} GB")

    for disco in data.get('discos', []):
        lineas.append(
            f"  {disco['unidad']:5}        : {disco['usado_gb']} / {disco['total_gb']} GB"
            f" ({disco['uso_pct']} %) [{disco['tipo']}]"
        )

    lineas += [
        "",
        "── GRÁFICOS ───────────────────────────────────────────",
    ]
    for gpu in data.get('gpus', []):
        vram = f"{gpu['vram_gb']} GB VRAM" if gpu['vram_gb'] > 0 else "VRAM compartida"
        lineas.append(f"  GPU          : {gpu['nombre']} — {vram}")
    lineas.append(f"  Resolución   : {data.get('resolucion')}")

    lineas += [
        "",
        "── PLACA BASE / BIOS ───────────────────────────────────",
        f"  Placa Base   : {data.get('placa_base')}",
        f"  BIOS         : {data.get('bios')}",
        "",
        "── RED ────────────────────────────────────────────────",
        f"  Hostname     : {data.get('hostname')}",
        f"  IP Local     : {data.get('ip_local')}",
        f"  MAC          : {data.get('mac')}",
        "",
        "══════════════════════════════════════════════════════",
        "",
    ]

    texto = "\n".join(lineas)
    print(texto)

    # Resumen por voz
    cpu_nombre = data.get('cpu_nombre', 'desconocido').split('@')[0].strip()
    resumen = (
        f"Tu PC tiene {data.get('os_edicion', 'Windows')}, "
        f"procesador {cpu_nombre}, "
        f"{data.get('ram_total_gb')} gigabytes de RAM "
        f"y {len(data.get('discos', []))} unidad de almacenamiento."
    )
    speak(resumen)

    return texto


# ==================== MICRÓFONO — DIAGNÓSTICO Y RESTAURACIÓN ====================

def get_microphone_status() -> dict:
    """
    Consulta todos los dispositivos de micrófono del sistema:
    estado, driver, habilitado/deshabilitado y nivel de volumen.

    Returns:
        dict con lista de micrófonos y su estado.
    """
    script = r"""
$mics = @()

# Solo dispositivos de clase MEDIA con nombre de micrófono
$devices = Get-PnpDevice | Where-Object {
    $_.Class -eq 'MEDIA' -and (
        $_.FriendlyName -match 'mic|microphone|microfono|digital mic'
    )
}
foreach ($d in $devices) {
    $mics += [pscustomobject]@{
        Nombre = $d.FriendlyName
        Estado = $d.Status
        Clase  = $d.Class
        Id     = $d.InstanceId
    }
}

# Endpoints de audio (auriculares con micro, micrófonos integrados)
$endpoints = Get-WmiObject Win32_SoundDevice | Where-Object {
    $_.Name -match 'mic|microphone|microfono|headset|headphone|auricular|realtek|intel.*audio|nvidia.*audio'
}
foreach ($e in $endpoints) {
    $mics += [pscustomobject]@{
        Nombre = $e.Name
        Estado = $e.Status
        Clase  = "SoundDevice"
        Id     = $e.DeviceID
    }
}
$mics | ConvertTo-Json -Depth 3
"""
    try:
        result = sp.run(
            ['powershell', '-NoProfile', '-Command', script],
            capture_output=True, text=True, timeout=20
        )
        import json as _json
        raw = result.stdout.strip()
        if not raw:
            return {'micros': [], 'error': 'Sin respuesta de PowerShell'}
        datos = _json.loads(raw)
        if isinstance(datos, dict):
            datos = [datos]
        micros = [
            {
                'nombre': d.get('Nombre', 'Desconocido'),
                'estado': d.get('Estado', 'Desconocido'),
                'clase':  d.get('Clase', ''),
                'id':     d.get('Id', '')
            }
            for d in datos
        ]
        return {'micros': micros, 'total': len(micros)}
    except Exception as e:
        return {'micros': [], 'error': str(e)}


def restore_microphone() -> dict:
    """
    Intenta restaurar el micrófono del sistema mediante 3 métodos progresivos:

      1. Habilitar dispositivos de micrófono deshabilitados (PnP)
      2. Reiniciar (disable + enable) todos los micrófonos con error
      3. Actualizar driver con pnputil desde el INF del sistema
         (IntcDMic.inf para micrófonos Intel/HP, fallback a driver genérico HD Audio)

    Requiere permisos de administrador para los pasos 2 y 3.

    Returns:
        dict con 'exito' (bool), 'acciones' (list[str]), 'micros_restaurados' (int)
    """
    acciones = []
    micros_restaurados = 0

    speak("Iniciando diagnóstico y restauración del micrófono. Dame un momento, Sara.")

    # ── Paso 1: Obtener estado actual ──────────────────────────────────────────
    estado = get_microphone_status()
    micros = estado.get('micros', [])

    if not micros:
        acciones.append("No se encontraron dispositivos de micrófono en el sistema.")
        speak("No encontré dispositivos de micrófono registrados en tu PC.")
        return {'exito': False, 'acciones': acciones, 'micros_restaurados': 0}

    acciones.append(f"Dispositivos encontrados: {len(micros)}")
    for m in micros:
        acciones.append(f"  • {m['nombre']} — Estado: {m['estado']}")

    # ── Paso 2: Habilitar micrófonos deshabilitados ────────────────────────────
    script_habilitar = r"""
$count = 0
$devices = Get-PnpDevice | Where-Object {
    $_.Class -eq 'MEDIA' -and
    $_.FriendlyName -match 'mic|microphone|microfono|digital mic' -and
    $_.Status -eq 'Error'
}
foreach ($d in $devices) {
    try {
        Disable-PnpDevice -InstanceId $d.InstanceId -Confirm:$false -ErrorAction Stop
        Start-Sleep -Seconds 1
        Enable-PnpDevice -InstanceId $d.InstanceId -Confirm:$false -ErrorAction Stop
        $count++
        Write-Output "RESTAURADO: $($d.FriendlyName)"
    } catch {
        Write-Output "FALLO: $($d.FriendlyName) - $($_.Exception.Message)"
    }
}

# También habilitar los que estén deshabilitados explícitamente
$disabled = Get-PnpDevice | Where-Object {
    $_.Class -eq 'MEDIA' -and
    $_.FriendlyName -match 'mic|microphone|microfono|digital mic' -and
    $_.Status -eq 'Unknown'
}
foreach ($d in $disabled) {
    try {
        Enable-PnpDevice -InstanceId $d.InstanceId -Confirm:$false -ErrorAction Stop
        $count++
        Write-Output "HABILITADO: $($d.FriendlyName)"
    } catch {
        Write-Output "FALLO_HABILITAR: $($d.FriendlyName)"
    }
}
Write-Output "TOTAL_RESTAURADOS:$count"
"""
    try:
        result = sp.run(
            ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', script_habilitar],
            capture_output=True, text=True, timeout=30
        )
        for linea in result.stdout.splitlines():
            linea = linea.strip()
            if linea:
                acciones.append(linea)
                if linea.startswith('RESTAURADO:') or linea.startswith('HABILITADO:'):
                    micros_restaurados += 1
    except Exception as e:
        acciones.append(f"Error en paso 2: {e}")

    # ── Paso 3: Actualizar driver ──────────────────────────────────────────────
    script_driver = r"""
# Intentar con driver Intel/HP primero
$infPaths = @(
    "C:\SWSetup\SP142490\IHV_ISST7767\IntcDMic.inf",
    "C:\Windows\System32\DriverStore\FileRepository\hdaudio.inf_amd64*\hdaudio.inf",
    "C:\Windows\INF\hdaudio.inf"
)
$updated = $false
foreach ($inf in $infPaths) {
    $resolved = Resolve-Path $inf -ErrorAction SilentlyContinue
    if ($resolved) {
        Write-Output "DRIVER_INF: $($resolved.Path)"
        pnputil /add-driver $resolved.Path /install 2>&1 | Write-Output
        $updated = $true
        break
    }
}
if (-not $updated) {
    Write-Output "DRIVER_FALLBACK: Usando driver genérico de Windows"
    # Forzar re-detección de hardware de audio
    $devices = Get-PnpDevice | Where-Object {
        $_.FriendlyName -match 'mic|microphone|audio' -and $_.Status -eq 'Error'
    }
    foreach ($d in $devices) {
        pnputil /remove-device $d.InstanceId 2>&1 | Write-Output
        pnputil /scan-devices 2>&1 | Write-Output
    }
}
"""
    try:
        result = sp.run(
            ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', script_driver],
            capture_output=True, text=True, timeout=45
        )
        for linea in result.stdout.splitlines():
            linea = linea.strip()
            if linea:
                acciones.append(f"  [driver] {linea}")
    except Exception as e:
        acciones.append(f"Error en paso 3 (driver): {e}")

    # ── Verificación final ────────────────────────────────────────────────────
    estado_final = get_microphone_status()
    micros_ok = [m for m in estado_final.get('micros', []) if m['estado'] == 'OK']
    micros_error = [m for m in estado_final.get('micros', []) if m['estado'] == 'Error']

    acciones.append(f"Estado final — OK: {len(micros_ok)} | Con error: {len(micros_error)}")

    exito = len(micros_ok) > 0

    if exito:
        speak(f"Micrófono restaurado correctamente. {len(micros_ok)} dispositivo activo.")
    elif micros_restaurados > 0:
        speak("Realicé cambios en el micrófono. Te recomiendo reiniciar el PC para que surtan efecto.")
    else:
        speak(
            "No pude restaurar el micrófono automáticamente. "
            "Puede que necesites ejecutar KALMIYA como administrador "
            "o instalar el driver desde support.hp.com con el serial de tu equipo."
        )

    return {
        'exito':             exito,
        'acciones':          acciones,
        'micros_ok':         len(micros_ok),
        'micros_error':      len(micros_error),
        'micros_restaurados': micros_restaurados
    }


# ══════════════════════════════════════════════════════════════════════════════
# ACCESO RÁPIDO A kalmiya_system_info — disponible desde os_ops
# ══════════════════════════════════════════════════════════════════════════════

def get_disk_info(unidad: str = "C:\\") -> dict:
    """Información de disco C o D."""
    from kalmiya_system_info import info_disco
    return info_disco(unidad)


def get_both_disks_info() -> dict:
    """Información completa de discos C y D."""
    from kalmiya_system_info import info_ambos_discos
    return info_ambos_discos()


def get_large_files(unidad: str = "C:\\", top_n: int = 20,
                    min_mb: float = 100) -> list:
    """Archivos más grandes en un disco."""
    from kalmiya_system_info import archivos_grandes
    return archivos_grandes(unidad, top_n, min_mb)


def get_heavy_folders(unidad: str = "C:\\") -> list:
    """Carpetas más pesadas en un disco."""
    from kalmiya_system_info import carpetas_pesadas
    return carpetas_pesadas(unidad)


def search_files(query: str, extensiones: list = None,
                 min_mb: float = 0) -> list:
    """Busca archivos en C y D por nombre o extensión."""
    from kalmiya_system_info import buscar_archivos
    return buscar_archivos(query, extensiones=extensiones, min_mb=min_mb)


def get_recent_files(dias: int = 7, extensiones: list = None) -> list:
    """Archivos modificados recientemente."""
    from kalmiya_system_info import archivos_recientes
    return archivos_recientes(dias, extensiones=extensiones)


def find_duplicates(carpeta: str, min_mb: float = 1.0) -> list:
    """Detecta archivos duplicados en una carpeta."""
    from kalmiya_system_info import detectar_duplicados
    return detectar_duplicados(carpeta, min_mb)


def get_folder_tree(ruta: str, profundidad: int = 3) -> str:
    """Árbol visual de una carpeta."""
    from kalmiya_system_info import arbol_carpeta
    return arbol_carpeta(ruta, profundidad)


def get_quick_disk_space() -> dict:
    """Espacio libre rápido en C y D."""
    from kalmiya_system_info import espacio_libre_rapido
    return espacio_libre_rapido()


def get_file_types_by_disk(unidad: str = "C:\\") -> dict:
    """Tipos de archivo y espacio que ocupan."""
    from kalmiya_system_info import tipos_archivo_por_disco
    return tipos_archivo_por_disco(unidad)


def get_full_pc_report() -> dict:
    """Reporte completo: CPU, RAM, GPU, temperaturas, procesos."""
    from kalmiya_system_info import resumen_sistema_completo
    return resumen_sistema_completo()


def print_full_pc_report() -> str:
    """Imprime y habla el reporte completo del sistema."""
    from kalmiya_system_info import imprimir_resumen_sistema
    return imprimir_resumen_sistema()

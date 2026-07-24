"""
kalmiya_system_info.py — Información Completa del Sistema para KALMIYA
=======================================================================
Le da a KALMIYA acceso total al PC:
  - Sistema operativo completo (CPU, RAM, GPU, BIOS, placa base)
  - Discos C y D: espacio, archivos grandes, duplicados, carpetas pesadas
  - Procesos activos y consumo de recursos
  - Temperatura del hardware
  - Archivos recientes y más usados
  - Árbol de carpetas de un directorio
  - Búsqueda de archivos por nombre, extensión o tamaño
"""

import os, sys, json, hashlib, subprocess as sp
from pathlib import Path
from datetime import datetime
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voz import speak, USERNAME
from database import log_command, update_memory
from _logging import get_logger

logger = get_logger(__name__)

try:
    import psutil
    PSUTIL_OK = True
except ImportError:
    PSUTIL_OK = False


# ══════════════════════════════════════════════════════════════════════════════
# 1. INFORMACIÓN COMPLETA DEL PC
# ══════════════════════════════════════════════════════════════════════════════

def info_cpu() -> dict:
    """CPU: nombre, núcleos, frecuencia, uso actual y por núcleo."""
    import platform
    data = {"nombre": platform.processor()}
    try:
        r = sp.run(["powershell", "-NoProfile", "-Command",
                    "(Get-WmiObject Win32_Processor).Name"],
                   capture_output=True, text=True, timeout=8)
        if r.stdout.strip():
            data["nombre"] = r.stdout.strip()
    except Exception:
        pass
    if PSUTIL_OK:
        try:
            freq = psutil.cpu_freq()
            data["nucleos_fisicos"]  = psutil.cpu_count(logical=False)
            data["nucleos_logicos"]  = psutil.cpu_count(logical=True)
            data["frecuencia_mhz"]   = round(freq.current) if freq else None
            data["frecuencia_max"]   = round(freq.max)     if freq else None
            data["uso_total_pct"]    = psutil.cpu_percent(interval=0.5)
            data["uso_por_nucleo"]   = psutil.cpu_percent(interval=0.5, percpu=True)
        except Exception:
            pass
    return data


def info_ram() -> dict:
    """RAM: total, usada, disponible, tipo y velocidad."""
    data = {}
    if PSUTIL_OK:
        try:
            mem = psutil.virtual_memory()
            swp = psutil.swap_memory()
            data["total_gb"]      = round(mem.total     / 1024**3, 2)
            data["usada_gb"]      = round(mem.used      / 1024**3, 2)
            data["disponible_gb"] = round(mem.available / 1024**3, 2)
            data["uso_pct"]       = mem.percent
            data["swap_total_gb"] = round(swp.total / 1024**3, 2)
            data["swap_usado_gb"] = round(swp.used  / 1024**3, 2)
        except Exception:
            pass
    try:
        r = sp.run(["powershell", "-NoProfile", "-Command",
                    "(Get-WmiObject Win32_PhysicalMemory | Select-Object -First 1).SMBIOSMemoryType"],
                   capture_output=True, text=True, timeout=8)
        tipos = {24:"DDR3", 26:"DDR4", 29:"LPDDR3", 30:"LPDDR4", 34:"DDR5", 35:"LPDDR5"}
        t = r.stdout.strip()
        data["tipo"] = tipos.get(int(t), "DDR4") if t.isdigit() else "DDR4"
    except Exception:
        data["tipo"] = "Desconocido"
    try:
        r = sp.run(["powershell", "-NoProfile", "-Command",
                    "(Get-WmiObject Win32_PhysicalMemory | Select-Object -First 1).Speed"],
                   capture_output=True, text=True, timeout=8)
        data["velocidad_mhz"] = r.stdout.strip() or "?"
    except Exception:
        data["velocidad_mhz"] = "?"
    return data


def info_gpu() -> list[dict]:
    """GPUs instaladas: nombre, VRAM y driver."""
    gpus = []
    try:
        r = sp.run(["powershell", "-NoProfile", "-Command",
                    "Get-WmiObject Win32_VideoController | "
                    "Select-Object Name,AdapterRAM,DriverVersion | ConvertTo-Json"],
                   capture_output=True, text=True, timeout=10)
        raw = r.stdout.strip()
        if raw:
            datos = json.loads(raw)
            if isinstance(datos, dict):
                datos = [datos]
            for d in datos:
                gpus.append({
                    "nombre":  d.get("Name", "?"),
                    "vram_gb": round(int(d.get("AdapterRAM", 0)) / 1024**3, 2)
                              if d.get("AdapterRAM") else 0,
                    "driver":  d.get("DriverVersion", "?"),
                })
    except Exception:
        pass
    return gpus


def info_temperatura() -> dict:
    """Temperatura del hardware vía PowerShell WMI."""
    temps = {}
    try:
        r = sp.run(["powershell", "-NoProfile", "-Command",
                    "Get-WmiObject MSAcpi_ThermalZoneTemperature "
                    "-Namespace root/wmi | "
                    "Select-Object InstanceName,CurrentTemperature | ConvertTo-Json"],
                   capture_output=True, text=True, timeout=10)
        raw = r.stdout.strip()
        if raw and "[" in raw:
            datos = json.loads(raw)
            if isinstance(datos, dict):
                datos = [datos]
            for i, d in enumerate(datos):
                kelvin = d.get("CurrentTemperature", 0)
                celsius = round((kelvin - 2732) / 10, 1) if kelvin else None
                nombre  = d.get("InstanceName", f"Zona{i}")
                if celsius and 0 < celsius < 110:
                    temps[nombre] = celsius
    except Exception:
        pass
    return temps


def info_procesos_top(top_n: int = 10) -> list[dict]:
    """Procesos que más RAM y CPU consumen."""
    if not PSUTIL_OK:
        return []
    procs = []
    for proc in psutil.process_iter(["pid","name","cpu_percent","memory_percent","status"]):
        try:
            info = proc.info
            if info["memory_percent"] and info["memory_percent"] > 0.05:
                procs.append(info)
        except Exception:
            continue
    procs.sort(key=lambda x: x.get("memory_percent", 0), reverse=True)
    return procs[:top_n]


def resumen_sistema_completo() -> dict:
    """Recopila todo: CPU, RAM, GPU, temperaturas y procesos."""
    speak(f"Analizando tu sistema completo, {USERNAME}. Dame un momento.")
    data = {
        "timestamp": datetime.now().isoformat(),
        "cpu":       info_cpu(),
        "ram":       info_ram(),
        "gpus":      info_gpu(),
        "temps":     info_temperatura(),
        "procesos":  info_procesos_top(5),
    }

    # Hablar resumen
    cpu  = data["cpu"]
    ram  = data["ram"]
    gpus = data["gpus"]

    speak(f"CPU: {cpu.get('nombre','?').split('@')[0].strip()}, "
          f"{cpu.get('nucleos_fisicos','?')} núcleos físicos, "
          f"{cpu.get('uso_total_pct','?')}% de uso.")
    speak(f"RAM: {ram.get('usada_gb','?')} de {ram.get('total_gb','?')} GB usados "
          f"({ram.get('uso_pct','?')}%), tipo {ram.get('tipo','?')}.")
    if gpus:
        g = gpus[0]
        speak(f"GPU principal: {g['nombre']}, {g['vram_gb']} GB VRAM.")
    if data["temps"]:
        max_temp = max(data["temps"].values())
        estado   = "normal" if max_temp < 80 else "alta"
        speak(f"Temperatura máxima: {max_temp}°C — {estado}.")

    log_command("[SISTEMA] Resumen completo", json.dumps(data)[:200], source="system")
    return data


def imprimir_resumen_sistema() -> str:
    """Imprime en consola el resumen formateado del sistema."""
    data  = resumen_sistema_completo()
    cpu   = data["cpu"]
    ram   = data["ram"]
    temps = data["temps"]

    lineas = [
        "",
        "╔══════════════════════════════════════════════════════╗",
        "║         KALMIYA — SISTEMA COMPLETO                   ║",
        "╚══════════════════════════════════════════════════════╝",
        "",
        f"  CPU      : {cpu.get('nombre','?')}",
        f"  Núcleos  : {cpu.get('nucleos_fisicos','?')}F / {cpu.get('nucleos_logicos','?')}L",
        f"  Frecuencia: {cpu.get('frecuencia_mhz','?')} MHz  Uso: {cpu.get('uso_total_pct','?')}%",
        "",
        f"  RAM      : {ram.get('usada_gb','?')} / {ram.get('total_gb','?')} GB  ({ram.get('uso_pct','?')}%)",
        f"  Tipo RAM : {ram.get('tipo','?')} @ {ram.get('velocidad_mhz','?')} MHz",
        "",
    ]
    for g in data["gpus"]:
        lineas.append(f"  GPU      : {g['nombre']}  {g['vram_gb']} GB VRAM")
    if temps:
        lineas.append("")
        for zona, t in list(temps.items())[:3]:
            lineas.append(f"  Temp     : {zona[:30]} → {t}°C")
    lineas += [
        "",
        "  TOP PROCESOS (RAM):",
    ]
    for p in data["procesos"][:5]:
        lineas.append(f"    {p['name']:30} CPU:{p.get('cpu_percent',0):.1f}%  RAM:{p.get('memory_percent',0):.1f}%")
    lineas.append("")
    texto = "\n".join(lineas)
    print(texto)
    return texto


# ══════════════════════════════════════════════════════════════════════════════
# 2. DISCOS C Y D — ESPACIO, ARCHIVOS GRANDES, DUPLICADOS
# ══════════════════════════════════════════════════════════════════════════════

DISCOS = ["C:\\", "D:\\"]


def info_disco(unidad: str = "C:\\") -> dict:
    """Información completa de un disco: espacio, tipo y modelo."""
    data = {"unidad": unidad}
    if PSUTIL_OK:
        try:
            uso = psutil.disk_usage(unidad)
            data["total_gb"]  = round(uso.total / 1024**3, 2)
            data["usado_gb"]  = round(uso.used  / 1024**3, 2)
            data["libre_gb"]  = round(uso.free  / 1024**3, 2)
            data["uso_pct"]   = uso.percent
        except Exception:
            pass
    try:
        r = sp.run(["powershell", "-NoProfile", "-Command",
                    f"Get-PhysicalDisk | Where-Object {{$_.DeviceID -eq "
                    f"(Get-Partition -DriveLetter '{unidad[0]}').DiskNumber}} | "
                    f"Select-Object FriendlyName,MediaType | ConvertTo-Json"],
                   capture_output=True, text=True, timeout=10)
        raw = r.stdout.strip()
        if raw and "{" in raw:
            d = json.loads(raw)
            if isinstance(d, list):
                d = d[0]
            data["modelo"] = d.get("FriendlyName", "?")
            data["tipo"]   = d.get("MediaType",    "?")
    except Exception:
        pass
    return data


def info_ambos_discos() -> dict:
    """Resumen de discos C y D."""
    resultado = {}
    for disco in DISCOS:
        if Path(disco).exists():
            resultado[disco] = info_disco(disco)
    speak("Analizando discos C y D...")
    for unidad, d in resultado.items():
        modelo = d.get("modelo", "")
        speak(f"Disco {unidad}: {d.get('usado_gb','?')} de {d.get('total_gb','?')} GB usados "
              f"({d.get('uso_pct','?')}%). Libre: {d.get('libre_gb','?')} GB."
              + (f" Modelo: {modelo}." if modelo else ""))
    log_command("[DISCO] Info ambos discos", str(resultado)[:200], source="system")
    return resultado


def archivos_grandes(unidad: str = "C:\\", top_n: int = 20,
                     min_mb: float = 100) -> list[dict]:
    """
    Encuentra los archivos más grandes en un disco.
    Args:
        unidad:  Disco a analizar ('C:\\' o 'D:\\').
        top_n:   Cuántos archivos mostrar.
        min_mb:  Tamaño mínimo en MB para incluir.
    """
    speak(f"Buscando archivos grandes en {unidad}. Esto puede tomar un momento...")
    grandes = []
    min_bytes = min_mb * 1024 * 1024

    # Carpetas donde buscar (evitar sistema)
    SKIP = {"Windows", "System Volume Information", "$Recycle.Bin",
            "ProgramData", "pagefile.sys", "hiberfil.sys"}

    root = Path(unidad)
    for p in root.rglob("*"):
        try:
            if p.is_file() and p.name not in SKIP:
                size = p.stat().st_size
                if size >= min_bytes:
                    grandes.append({
                        "ruta":    str(p),
                        "nombre":  p.name,
                        "size_mb": round(size / 1024**2, 1),
                        "size_gb": round(size / 1024**3, 3),
                        "ext":     p.suffix.lower(),
                    })
        except (PermissionError, OSError):
            continue

    grandes.sort(key=lambda x: x["size_mb"], reverse=True)
    top = grandes[:top_n]
    speak(f"Encontré {len(grandes)} archivos mayores a {min_mb} MB. "
          f"Los {len(top)} más grandes son:")
    for f in top[:5]:
        speak(f"{f['nombre']}: {f['size_mb']} MB")
    log_command(f"[DISCO] Archivos grandes {unidad}", f"{len(grandes)} encontrados", source="system")
    return top


def carpetas_pesadas(unidad: str = "C:\\", top_n: int = 15,
                     profundidad: int = 2) -> list[dict]:
    """
    Calcula el tamaño de las carpetas principales del disco.
    Args:
        unidad:     Disco a analizar.
        top_n:      Cuántas carpetas mostrar.
        profundidad: Qué tan profundo explorar.
    """
    speak(f"Calculando peso de carpetas en {unidad}...")
    carpetas = []
    root = Path(unidad)
    SKIP = {"Windows", "System Volume Information", "$Recycle.Bin"}

    for carpeta in root.iterdir():
        if carpeta.name in SKIP or not carpeta.is_dir():
            continue
        try:
            total = 0
            n_archivos = 0
            for f in carpeta.rglob("*"):
                try:
                    if f.is_file():
                        total += f.stat().st_size
                        n_archivos += 1
                except (PermissionError, OSError):
                    continue
            if total > 0:
                carpetas.append({
                    "carpeta":   str(carpeta),
                    "nombre":    carpeta.name,
                    "size_gb":   round(total / 1024**3, 2),
                    "size_mb":   round(total / 1024**2, 1),
                    "archivos":  n_archivos,
                })
        except (PermissionError, OSError):
            continue

    carpetas.sort(key=lambda x: x["size_gb"], reverse=True)
    top = carpetas[:top_n]
    speak(f"Carpetas más pesadas en {unidad}:")
    for c in top[:5]:
        speak(f"{c['nombre']}: {c['size_gb']} GB")
    return top


def buscar_archivos(query: str, unidades: list = None,
                    extensiones: list = None,
                    min_mb: float = 0,
                    carpetas_usuario: bool = True) -> list[dict]:
    """
    Busca archivos en los discos C y D por nombre, extensión o tamaño.
    Args:
        query:            Nombre parcial del archivo.
        unidades:         Discos donde buscar.
        extensiones:      Lista de extensiones ej ['.pdf','.docx'].
        min_mb:           Tamaño mínimo en MB.
        carpetas_usuario: Si True busca solo en carpetas del usuario (más rápido).
    """
    unidades   = unidades or [u for u in DISCOS if Path(u).exists()]
    speak(f"Buscando archivos: '{query}' en {', '.join(unidades)}...")
    resultados = []
    query_lower = query.lower()
    min_bytes   = min_mb * 1024 * 1024

    # Carpetas prioritarias del usuario (búsqueda rápida)
    if carpetas_usuario:
        rutas_busqueda = [
            Path.home(),
            Path.home() / "Documents",
            Path.home() / "Desktop",
            Path.home() / "Downloads",
            Path(r"D:\OneDrive"),
            Path(r"c:\Users\maria\env\01_systems"),
            Path(r"c:\Users\maria\env\03_launchers"),
        ]
        for u in unidades:
            if Path(u).exists():
                rutas_busqueda.append(Path(u))
    else:
        rutas_busqueda = [Path(u) for u in unidades if Path(u).exists()]

    # Carpetas a saltar siempre
    SKIP_DIRS = {
        "02_infrastructure", "site-packages", "node_modules",
        "__pycache__", ".git", "Windows", "System32",
        "SysWOW64", "$Recycle.Bin", "System Volume Information",
        "ProgramData", "pagefile.sys", "hiberfil.sys",
        "AppData", "Lib",
    }

    visitados = set()
    for raiz in rutas_busqueda:
        if not raiz.exists():
            continue
        raiz_str = str(raiz).rstrip("\\")
        if raiz_str in visitados:
            continue
        visitados.add(raiz_str)

        # Si es raíz de disco y modo usuario, solo primer nivel
        es_raiz_disco = len(raiz.parts) == 1
        if es_raiz_disco and carpetas_usuario:
            iterador = raiz.iterdir()   # Solo primer nivel
        else:
            iterador = raiz.rglob("*") if not es_raiz_disco else raiz.iterdir()

        for p in iterador:
            try:
                # Saltar carpetas excluidas
                if any(skip in p.parts for skip in SKIP_DIRS):
                    continue
                if not p.is_file():
                    continue
                if query_lower and query_lower not in p.name.lower():
                    continue
                if extensiones and p.suffix.lower() not in extensiones:
                    continue
                size = p.stat().st_size
                if size < min_bytes:
                    continue
                ruta_str = str(p)
                if ruta_str not in {r["ruta"] for r in resultados}:
                    resultados.append({
                        "ruta":       ruta_str,
                        "nombre":     p.name,
                        "disco":      ruta_str[0].upper() + ":\\",
                        "size_mb":    round(size / 1024**2, 2),
                        "ext":        p.suffix.lower(),
                        "modificado": datetime.fromtimestamp(
                            p.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                    })
                if len(resultados) >= 200:
                    break
            except (PermissionError, OSError):
                continue
        if len(resultados) >= 200:
            break

    resultados.sort(key=lambda x: x["size_mb"], reverse=True)
    speak(f"Encontré {len(resultados)} archivo(s) que coinciden con '{query}'.")
    log_command(f"[BUSCAR] {query}", f"{len(resultados)} resultados", source="system")
    return resultados


def archivos_recientes(dias: int = 7, unidades: list = None,
                       extensiones: list = None) -> list[dict]:
    """
    Lista archivos modificados recientemente.
    Args:
        dias:        Cuántos días hacia atrás buscar.
        unidades:    Discos a revisar.
        extensiones: Filtrar por extensión (None = todas).
    """
    from datetime import timedelta
    unidades = unidades or [u for u in DISCOS if Path(u).exists()]
    limite   = datetime.now() - timedelta(days=dias)
    recientes = []

    # Carpetas de usuario (más relevantes)
    carpetas_usuario = [
        Path.home() / "Documents",
        Path.home() / "Desktop",
        Path.home() / "Downloads",
        Path(r"D:\OneDrive"),
        Path(r"D:\\"),
    ]

    for carpeta in carpetas_usuario:
        if not carpeta.exists():
            continue
        for p in carpeta.rglob("*"):
            try:
                if not p.is_file():
                    continue
                if extensiones and p.suffix.lower() not in extensiones:
                    continue
                mtime = datetime.fromtimestamp(p.stat().st_mtime)
                if mtime >= limite:
                    recientes.append({
                        "ruta":       str(p),
                        "nombre":     p.name,
                        "size_mb":    round(p.stat().st_size / 1024**2, 2),
                        "ext":        p.suffix.lower(),
                        "modificado": mtime.strftime("%Y-%m-%d %H:%M"),
                    })
            except (PermissionError, OSError):
                continue

    recientes.sort(key=lambda x: x["modificado"], reverse=True)
    speak(f"Encontré {len(recientes)} archivo(s) modificado(s) en los últimos {dias} días.")
    return recientes[:50]


def detectar_duplicados(carpeta: str, min_mb: float = 1.0) -> list[dict]:
    """
    Detecta archivos duplicados en una carpeta comparando hash MD5.
    Args:
        carpeta: Ruta de la carpeta a analizar.
        min_mb:  Tamaño mínimo en MB para considerar.
    Returns:
        Lista de grupos de duplicados.
    """
    speak(f"Buscando duplicados en {carpeta}. Esto puede tomar un momento...")
    hashes: dict[str, list[str]] = {}
    min_bytes = min_mb * 1024 * 1024

    for p in Path(carpeta).rglob("*"):
        try:
            if not p.is_file() or p.stat().st_size < min_bytes:
                continue
            h = hashlib.md5()
            with open(p, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            digest = h.hexdigest()
            hashes.setdefault(digest, []).append(str(p))
        except (PermissionError, OSError, Exception):
            continue

    duplicados = [
        {
            "hash":    k,
            "copias":  len(v),
            "archivos": v,
            "size_mb": round(Path(v[0]).stat().st_size / 1024**2, 2),
            "espacio_recuperable_mb": round(
                Path(v[0]).stat().st_size * (len(v)-1) / 1024**2, 2),
        }
        for k, v in hashes.items() if len(v) > 1
    ]
    duplicados.sort(key=lambda x: x["espacio_recuperable_mb"], reverse=True)

    espacio_total = sum(d["espacio_recuperable_mb"] for d in duplicados)
    speak(f"Encontré {len(duplicados)} grupo(s) de duplicados. "
          f"Podrías recuperar {round(espacio_total, 1)} MB.")
    log_command("[DISCO] Duplicados", f"{len(duplicados)} grupos", source="system")
    return duplicados[:20]


def arbol_carpeta(ruta: str, profundidad: int = 3,
                  max_items: int = 50) -> str:
    """
    Genera un árbol visual de una carpeta.
    Args:
        ruta:       Ruta de la carpeta raíz.
        profundidad: Cuántos niveles mostrar.
        max_items:   Máximo de items por nivel.
    Returns:
        String con el árbol de directorios.
    """
    root = Path(ruta)
    if not root.exists():
        return f"Carpeta no encontrada: {ruta}"

    lineas = [f"📁 {root}"]

    def _construir(carpeta: Path, nivel: int, prefijo: str):
        if nivel > profundidad:
            return
        try:
            items = sorted(carpeta.iterdir(),
                          key=lambda x: (not x.is_dir(), x.name.lower()))[:max_items]
        except PermissionError:
            return
        for i, item in enumerate(items):
            es_ultimo = (i == len(items) - 1)
            conector  = "└── " if es_ultimo else "├── "
            icono     = "📁" if item.is_dir() else "📄"
            try:
                size = ""
                if item.is_file():
                    s = item.stat().st_size
                    if s > 1024**3:
                        size = f" [{round(s/1024**3,1)} GB]"
                    elif s > 1024**2:
                        size = f" [{round(s/1024**2,1)} MB]"
                    elif s > 1024:
                        size = f" [{round(s/1024,1)} KB]"
            except Exception:
                size = ""
            lineas.append(f"{prefijo}{conector}{icono} {item.name}{size}")
            if item.is_dir():
                extension = "    " if es_ultimo else "│   "
                _construir(item, nivel + 1, prefijo + extension)

    _construir(root, 1, "")
    resultado = "\n".join(lineas)
    speak(f"Árbol de {root.name} generado con {len(lineas)} elementos.")
    return resultado


def espacio_libre_rapido() -> dict:
    """Resumen rápido de espacio libre en C y D."""
    resultado = {}
    for disco in DISCOS:
        if PSUTIL_OK and Path(disco).exists():
            try:
                uso = psutil.disk_usage(disco)
                libre_gb  = round(uso.free  / 1024**3, 1)
                total_gb  = round(uso.total / 1024**3, 1)
                usado_pct = uso.percent
                estado = "✅ OK" if usado_pct < 80 else "⚠️ Lleno" if usado_pct < 95 else "🔴 Crítico"
                resultado[disco] = {
                    "libre_gb":  libre_gb,
                    "total_gb":  total_gb,
                    "uso_pct":   usado_pct,
                    "estado":    estado,
                }
            except Exception:
                pass
    if resultado:
        partes = []
        for d, v in resultado.items():
            partes.append(f"Disco {d} {v['libre_gb']} GB libres de {v['total_gb']} GB "
                          f"({v['uso_pct']}%) — {v['estado']}")
        speak(". ".join(partes))
    return resultado


def tipos_archivo_por_disco(unidad: str = "C:\\",
                             carpeta_usuario: bool = True) -> dict:
    """
    Cuenta y pesa archivos por extensión en un disco.
    Args:
        unidad:          Disco a analizar.
        carpeta_usuario: Si True, solo analiza carpeta del usuario (más rápido).
    Returns:
        dict con extensiones, conteo y tamaño total.
    """
    speak(f"Analizando tipos de archivo en {unidad}...")
    if carpeta_usuario:
        raiz = Path.home()
    else:
        raiz = Path(unidad)

    tipos: dict[str, dict] = {}
    for p in raiz.rglob("*"):
        try:
            if not p.is_file():
                continue
            ext  = p.suffix.lower() or "(sin extensión)"
            size = p.stat().st_size
            if ext not in tipos:
                tipos[ext] = {"cantidad": 0, "size_mb": 0.0}
            tipos[ext]["cantidad"] += 1
            tipos[ext]["size_mb"]  = round(tipos[ext]["size_mb"] + size/1024**2, 2)
        except (PermissionError, OSError):
            continue

    top = sorted(tipos.items(), key=lambda x: x[1]["size_mb"], reverse=True)[:15]
    speak(f"Tipos de archivo más pesados en {unidad}:")
    for ext, d in top[:5]:
        speak(f"{ext}: {d['cantidad']} archivos, {d['size_mb']} MB")
    return dict(top)

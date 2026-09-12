"""
kalmiya_host_agent.py — Agente del Sistema Host para KALMIYA
============================================================
Este script corre DIRECTAMENTE en Windows (no en Docker).
Expone en http://localhost:9001 los datos reales del PC de Sara
(CPU, RAM, disco, GPU, temperatura, procesos) para que
KALMIYA (corriendo en Docker) pueda consultarlos.

Uso:
    python kalmiya_host_agent.py

O automáticamente con el acceso directo de Windows.
"""

import json
import platform
import subprocess
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

try:
    import psutil
    PSUTIL_OK = True
except ImportError:
    PSUTIL_OK = False
    print("[AVISO] psutil no instalado. Instálalo con: pip install psutil")


HOST = "0.0.0.0"
PORT = 9001


# ── Recolección de datos del sistema ──────────────────────────────────────────

def get_cpu_info() -> dict:
    data = {"nombre": platform.processor()}
    if not PSUTIL_OK:
        return data
    try:
        freq = psutil.cpu_freq()
        data["nucleos_fisicos"] = psutil.cpu_count(logical=False)
        data["nucleos_logicos"] = psutil.cpu_count(logical=True)
        data["frecuencia_mhz"] = round(freq.current) if freq else None
        data["uso_total_pct"] = psutil.cpu_percent(interval=0.5)
        data["uso_por_nucleo"] = psutil.cpu_percent(interval=0.5, percpu=True)
    except Exception:
        pass
    # Nombre real del procesador via WMI
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "(Get-WmiObject Win32_Processor).Name"],
            capture_output=True, text=True, timeout=6
        )
        if r.stdout.strip():
            data["nombre"] = r.stdout.strip()
    except Exception:
        pass
    return data


def get_ram_info() -> dict:
    data = {}
    if not PSUTIL_OK:
        return data
    try:
        mem = psutil.virtual_memory()
        swp = psutil.swap_memory()
        data["total_gb"] = round(mem.total / 1024**3, 2)
        data["usada_gb"] = round(mem.used / 1024**3, 2)
        data["disponible_gb"] = round(mem.available / 1024**3, 2)
        data["uso_pct"] = mem.percent
        data["swap_total_gb"] = round(swp.total / 1024**3, 2)
        data["swap_usado_gb"] = round(swp.used / 1024**3, 2)
    except Exception:
        pass
    # Tipo de RAM
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "(Get-WmiObject Win32_PhysicalMemory | Select-Object -First 1).SMBIOSMemoryType"],
            capture_output=True, text=True, timeout=6
        )
        tipos = {24: "DDR3", 26: "DDR4", 29: "LPDDR3", 30: "LPDDR4", 34: "DDR5", 35: "LPDDR5"}
        t = r.stdout.strip()
        data["tipo"] = tipos.get(int(t), "DDR4") if t.isdigit() else "DDR4"
    except Exception:
        data["tipo"] = "Desconocido"
    return data


def get_disk_info() -> list:
    disks = []
    if not PSUTIL_OK:
        return disks
    try:
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                disks.append({
                    "disco": part.device,
                    "punto_montaje": part.mountpoint,
                    "total_gb": round(usage.total / 1024**3, 1),
                    "usado_gb": round(usage.used / 1024**3, 1),
                    "libre_gb": round(usage.free / 1024**3, 1),
                    "uso_pct": usage.percent,
                    "fs": part.fstype,
                })
            except PermissionError:
                continue
    except Exception:
        pass
    return disks


def get_gpu_info() -> list:
    gpus = []
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-WmiObject Win32_VideoController | "
             "Select-Object Name,AdapterRAM,DriverVersion | ConvertTo-Json"],
            capture_output=True, text=True, timeout=10
        )
        raw = r.stdout.strip()
        if raw:
            datos = json.loads(raw)
            if isinstance(datos, dict):
                datos = [datos]
            for d in datos:
                gpus.append({
                    "nombre": d.get("Name", "?"),
                    "vram_gb": round(int(d.get("AdapterRAM", 0)) / 1024**3, 2)
                              if d.get("AdapterRAM") else 0,
                    "driver": d.get("DriverVersion", "?"),
                })
    except Exception:
        pass
    return gpus


def get_temperature_info() -> dict:
    temps = {}
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-WmiObject MSAcpi_ThermalZoneTemperature "
             "-Namespace root/wmi | "
             "Select-Object InstanceName,CurrentTemperature | ConvertTo-Json"],
            capture_output=True, text=True, timeout=10
        )
        raw = r.stdout.strip()
        if raw and "[" in raw:
            datos = json.loads(raw)
            if isinstance(datos, dict):
                datos = [datos]
            for i, d in enumerate(datos):
                kelvin = d.get("CurrentTemperature", 0)
                celsius = round((kelvin - 2732) / 10, 1) if kelvin else None
                nombre = d.get("InstanceName", f"Zona{i}").split("\\")[-1]
                if celsius and 0 < celsius < 110:
                    temps[nombre] = celsius
    except Exception:
        pass
    return temps


def get_top_processes(top_n: int = 10) -> list:
    if not PSUTIL_OK:
        return []
    procs = []
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status"]):
        try:
            info = proc.info
            if info["memory_percent"] and info["memory_percent"] > 0.1:
                procs.append({
                    "pid": info["pid"],
                    "nombre": info["name"],
                    "cpu_pct": round(info["cpu_percent"], 1),
                    "ram_pct": round(info["memory_percent"], 2),
                    "estado": info["status"],
                })
        except Exception:
            continue
    procs.sort(key=lambda x: x.get("ram_pct", 0), reverse=True)
    return procs[:top_n]


def get_network_adapters() -> list:
    adapters = []
    if not PSUTIL_OK:
        return adapters
    try:
        stats = psutil.net_if_stats()
        addrs = psutil.net_if_addrs()
        io = psutil.net_io_counters(pernic=True)
        for name, stat in stats.items():
            if not stat.isup:
                continue
            ips = [a.address for a in addrs.get(name, []) if ":" not in a.address]
            net_io = io.get(name)
            adapters.append({
                "nombre": name,
                "activo": stat.isup,
                "velocidad_mbps": stat.speed,
                "ips": ips,
                "enviado_mb": round(net_io.bytes_sent / 1024**2, 2) if net_io else 0,
                "recibido_mb": round(net_io.bytes_recv / 1024**2, 2) if net_io else 0,
            })
    except Exception:
        pass
    return adapters


def get_full_system_status() -> dict:
    """Recopila todo el estado del sistema del PC host."""
    return {
        "timestamp": datetime.now().isoformat(),
        "os": platform.platform(),
        "hostname": platform.node(),
        "cpu": get_cpu_info(),
        "ram": get_ram_info(),
        "discos": get_disk_info(),
        "gpus": get_gpu_info(),
        "temperaturas": get_temperature_info(),
        "procesos_top": get_top_processes(10),
        "red": get_network_adapters(),
    }


# ── Servidor HTTP simple ───────────────────────────────────────────────────────

class SystemInfoHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Silenciar logs de acceso

    def do_GET(self):
        if self.path == "/system":
            data = get_full_system_status()
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        else:
            self.send_response(404)
            self.end_headers()


def run_server():
    server = HTTPServer((HOST, PORT), SystemInfoHandler)
    print(f"[KALMIYA Host Agent] Corriendo en http://{HOST}:{PORT}")
    print(f"[KALMIYA Host Agent] Endpoints:")
    print(f"  GET http://localhost:{PORT}/system  → Estado completo del PC")
    print(f"  GET http://localhost:{PORT}/health  → Health check")
    server.serve_forever()


if __name__ == "__main__":
    run_server()

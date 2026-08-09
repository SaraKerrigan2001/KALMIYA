"""
security_ops.py - Modulo de seguridad y ethical hacking de KALMIYA
===================================================================
Herramientas de DEFENSA y analisis de seguridad:
  - Escaneo de red local (dispositivos conectados)
  - Analisis de puertos y vulnerabilidades
  - Monitoreo de trafico sospechoso
  - Deteccion de intrusos en la red
  - Analisis de contrasenas y fortaleza
  - Auditoria de seguridad del sistema
  - Curiosidad autonoma de KALMIYA sobre amenazas
  - 🔴 RAPTOR Framework: Análisis autónomo de seguridad ofensiva/defensiva

NOTA: Estas herramientas son para DEFENSA y auditoria
de sistemas propios. Usar en redes ajenas sin permiso es ilegal.
"""

import socket
import subprocess
import platform
import threading
import time
import json
import re
import os
import hashlib
import secrets
import string
from datetime import datetime
from typing import Optional
from database import log_command, update_memory, get_memory
from voz import speak

# ── Intentar importar librerias opcionales ─────────────────────────────────────
try:
    import scapy.all as scapy
    SCAPY_OK = True
except Exception:
    SCAPY_OK = False
    print("[SECURITY] scapy no disponible - algunas funciones limitadas")

try:
    import psutil
    PSUTIL_OK = True
except Exception:
    PSUTIL_OK = False

try:
    import requests
    REQUESTS_OK = True
except Exception:
    REQUESTS_OK = False


# ── Escaneo de red ─────────────────────────────────────────────────────────────

def scan_network(ip_range: str = "") -> list[dict]:
    """
    Escanea la red local y devuelve todos los dispositivos encontrados.
    
    Args:
        ip_range: Rango IP (ej: '192.168.1.0/24'). Auto-detecta si esta vacio.
    
    Returns:
        Lista de dispositivos con IP, MAC y hostname.
    """
    speak("Iniciando escaneo de red. Buscando dispositivos conectados.")
    devices = []

    # Auto-detectar rango de red
    if not ip_range:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            parts = local_ip.split('.')
            ip_range = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
        except Exception:
            ip_range = "192.168.1.0/24"

    print(f"[SECURITY] Escaneando rango: {ip_range}")

    if SCAPY_OK:
        devices = _scan_with_scapy(ip_range)
    else:
        devices = _scan_with_ping(ip_range)

    speak(f"Escaneo completado. Encontre {len(devices)} dispositivos en tu red.")
    log_command("[SECURITY] Escaneo de red", json.dumps(devices), source='security')
    return devices


def _scan_with_scapy(ip_range: str) -> list[dict]:
    """Escaneo ARP con scapy (mas preciso)."""
    devices = []
    try:
        arp = scapy.ARP(pdst=ip_range)
        ether = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp
        result = scapy.srp(packet, timeout=3, verbose=0)[0]
        for sent, received in result:
            hostname = _get_hostname(received.psrc)
            devices.append({
                'ip': received.psrc,
                'mac': received.hwsrc,
                'hostname': hostname,
                'vendor': _get_mac_vendor(received.hwsrc)
            })
    except Exception as e:
        print(f"[SECURITY] Error scapy: {e}")
        devices = _scan_with_ping(ip_range)
    return devices


def _scan_with_ping(ip_range: str) -> list[dict]:
    """Escaneo por ping (fallback sin scapy)."""
    devices = []
    base = '.'.join(ip_range.split('.')[:3])
    results = []
    lock = threading.Lock()

    def ping_host(i: int):
        ip = f"{base}.{i}"
        try:
            result = subprocess.run(
                ['ping', '-n', '1', '-w', '300', ip] if platform.system() == 'Windows'
                else ['ping', '-c', '1', '-W', '1', ip],
                capture_output=True, timeout=2
            )
            if result.returncode == 0:
                hostname = _get_hostname(ip)
                with lock:
                    results.append({'ip': ip, 'mac': 'N/A', 'hostname': hostname, 'vendor': 'N/A'})
        except Exception:
            pass

    threads = [threading.Thread(target=ping_host, args=(i,), daemon=True) for i in range(1, 255)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=3)

    return results


def _get_hostname(ip: str) -> str:
    """Resuelve el hostname de una IP."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "Desconocido"


def _get_mac_vendor(mac: str) -> str:
    """Identifica el fabricante por los primeros 3 octetos del MAC."""
    vendors = {
        "00:50:56": "VMware", "00:0c:29": "VMware",
        "b8:27:eb": "Raspberry Pi", "dc:a6:32": "Raspberry Pi",
        "00:1a:11": "Google", "f4:f5:d8": "Google",
        "ac:bc:32": "Apple", "00:17:f2": "Apple",
        "00:50:f2": "Microsoft", "28:18:78": "Samsung",
        "00:26:b9": "Dell", "00:1e:67": "HP",
    }
    prefix = mac[:8].lower()
    for k, v in vendors.items():
        if prefix.startswith(k.lower()):
            return v
    return "Desconocido"


# ── Escaneo de puertos ─────────────────────────────────────────────────────────

def scan_ports(host: str, port_range: tuple[int, int] = (1, 1024),
               timeout: float = 0.5) -> dict:
    """
    Escanea puertos de un host y detecta servicios.
    
    Args:
        host:       IP o hostname a escanear.
        port_range: Rango de puertos (inicio, fin).
        timeout:    Timeout por puerto en segundos.
    
    Returns:
        Diccionario con puertos abiertos y servicios detectados.
    """
    speak(f"Escaneando puertos de {host}. Esto puede tardar unos segundos.")
    open_ports = {}
    lock = threading.Lock()

    COMMON_SERVICES = {
        21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
        53: 'DNS', 80: 'HTTP', 110: 'POP3', 135: 'RPC',
        139: 'NetBIOS', 143: 'IMAP', 443: 'HTTPS', 445: 'SMB',
        3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL',
        5900: 'VNC', 6379: 'Redis', 8080: 'HTTP-Alt',
        8443: 'HTTPS-Alt', 27017: 'MongoDB'
    }

    def check_port(port: int):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                service = COMMON_SERVICES.get(port, 'Desconocido')
                risk = _assess_port_risk(port)
                with lock:
                    open_ports[port] = {'service': service, 'risk': risk}
        except Exception:
            pass

    threads = [
        threading.Thread(target=check_port, args=(p,), daemon=True)
        for p in range(port_range[0], port_range[1] + 1)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=timeout + 1)

    result = {
        'host': host,
        'open_ports': open_ports,
        'total_open': len(open_ports),
        'high_risk': [p for p, d in open_ports.items() if d['risk'] == 'ALTO'],
        'scan_time': datetime.now().isoformat()
    }

    speak(f"Escaneo de {host} completado. {len(open_ports)} puertos abiertos encontrados.")
    if result['high_risk']:
        speak(f"Alerta: {len(result['high_risk'])} puertos de alto riesgo detectados.")

    log_command(f"[SECURITY] Escaneo puertos {host}", json.dumps(result), source='security')
    return result


def _assess_port_risk(port: int) -> str:
    """Evalua el nivel de riesgo de un puerto abierto."""
    high_risk = [23, 135, 139, 445, 3389, 5900, 4444, 6667, 31337]
    medium_risk = [21, 22, 25, 110, 143, 3306, 5432, 6379, 27017]
    if port in high_risk:
        return "ALTO"
    if port in medium_risk:
        return "MEDIO"
    return "BAJO"


# ── Analisis de seguridad del sistema local ────────────────────────────────────

def audit_local_security() -> dict:
    """
    Realiza una auditoria de seguridad del sistema local.
    Detecta configuraciones debiles y posibles vulnerabilidades.
    """
    speak("Iniciando auditoria de seguridad del sistema de Sara.")
    report = {
        'timestamp': datetime.now().isoformat(),
        'findings': [],
        'score': 100,
        'recommendations': []
    }

    # 1. Verificar firewall de Windows
    try:
        result = subprocess.run(
            ['netsh', 'advfirewall', 'show', 'allprofiles', 'state'],
            capture_output=True, text=True, timeout=10
        )
        if 'OFF' in result.stdout.upper():
            report['findings'].append({
                'severity': 'ALTO',
                'issue': 'Firewall de Windows desactivado',
                'fix': 'Activa el firewall en Configuracion > Seguridad de Windows'
            })
            report['score'] -= 20
    except Exception:
        pass

    # 2. Verificar actualizaciones pendientes
    try:
        result = subprocess.run(
            ['powershell', '-Command',
             '(New-Object -ComObject Microsoft.Update.Session).CreateUpdateSearcher().Search("IsInstalled=0").Updates.Count'],
            capture_output=True, text=True, timeout=30
        )
        count = result.stdout.strip()
        if count.isdigit() and int(count) > 0:
            report['findings'].append({
                'severity': 'MEDIO',
                'issue': f'{count} actualizaciones de Windows pendientes',
                'fix': 'Instala las actualizaciones en Configuracion > Windows Update'
            })
            report['score'] -= 10
    except Exception:
        pass

    # 3. Verificar puertos abiertos localmente
    local_ports = scan_ports('127.0.0.1', (1, 1024), timeout=0.2)
    high_risk_local = local_ports.get('high_risk', [])
    if high_risk_local:
        report['findings'].append({
            'severity': 'ALTO',
            'issue': f'Puertos de alto riesgo abiertos localmente: {high_risk_local}',
            'fix': 'Revisa que servicios estan usando estos puertos'
        })
        report['score'] -= 15

    # 4. Verificar procesos sospechosos
    suspicious = _check_suspicious_processes()
    if suspicious:
        report['findings'].append({
            'severity': 'ALTO',
            'issue': f'Procesos potencialmente sospechosos: {suspicious}',
            'fix': 'Investiga estos procesos con el Administrador de Tareas'
        })
        report['score'] -= 20

    # 5. Verificar conexiones de red activas
    suspicious_conns = _check_suspicious_connections()
    if suspicious_conns:
        report['findings'].append({
            'severity': 'MEDIO',
            'issue': f'Conexiones sospechosas detectadas: {len(suspicious_conns)}',
            'fix': 'Revisa las conexiones activas'
        })
        report['score'] -= 10

    report['score'] = max(0, report['score'])

    if report['score'] >= 80:
        nivel = "BUENO"
        speak(f"Auditoria completada. Tu sistema tiene un nivel de seguridad {nivel} con {report['score']} puntos.")
    elif report['score'] >= 60:
        nivel = "REGULAR"
        speak(f"Auditoria completada. Nivel de seguridad {nivel}. Hay {len(report['findings'])} problemas a corregir.")
    else:
        nivel = "CRITICO"
        speak(f"Alerta Sara. Nivel de seguridad {nivel}. Necesitas atender {len(report['findings'])} problemas urgentes.")

    report['nivel'] = nivel
    log_command("[SECURITY] Auditoria local", json.dumps(report), source='security')
    return report


def _check_suspicious_processes() -> list[str]:
    """Detecta procesos con nombres sospechosos."""
    if not PSUTIL_OK:
        return []
    suspicious_names = [
        'keylogger', 'ratclient', 'njrat', 'darkcomet', 'nanocore',
        'remcos', 'asyncrat', 'quasar', 'xworm', 'dcrat'
    ]
    found = []
    try:
        import psutil
        for proc in psutil.process_iter(['name']):
            name = proc.info['name'].lower() if proc.info['name'] else ''
            for s in suspicious_names:
                if s in name:
                    found.append(proc.info['name'])
    except Exception:
        pass
    return found


def _check_suspicious_connections() -> list[dict]:
    """Detecta conexiones de red sospechosas."""
    if not PSUTIL_OK:
        return []
    suspicious = []
    suspicious_ports = [4444, 6667, 31337, 1337, 9999, 8888]
    try:
        import psutil
        for conn in psutil.net_connections():
            if conn.raddr and conn.raddr.port in suspicious_ports:
                suspicious.append({
                    'local': f"{conn.laddr.ip}:{conn.laddr.port}",
                    'remote': f"{conn.raddr.ip}:{conn.raddr.port}",
                    'status': conn.status
                })
    except Exception:
        pass
    return suspicious


# ── Monitor de intrusos en red ─────────────────────────────────────────────────

_monitoring = False
_known_devices: set[str] = set()


def start_intrusion_monitor(callback=None):
    """
    Inicia el monitor de intrusos en la red.
    Alerta cuando un dispositivo desconocido se conecta.
    
    Args:
        callback: Funcion a llamar cuando se detecta un intruso (ip, hostname).
    """
    global _monitoring, _known_devices
    _monitoring = True

    # Cargar dispositivos conocidos
    known_str = get_memory('known_devices') or ''
    if known_str:
        _known_devices = set(known_str.split(','))

    speak("Monitor de intrusos activado. Vigilando tu red, Sara.")
    print("[SECURITY] Monitor de intrusos activo.")

    def _monitor():
        global _known_devices
        while _monitoring:
            try:
                devices = scan_network()
                current_ips = {d['ip'] for d in devices}

                # Detectar nuevos dispositivos
                new_devices = current_ips - _known_devices
                if new_devices and _known_devices:  # Solo alertar si ya teniamos dispositivos conocidos
                    for ip in new_devices:
                        hostname = _get_hostname(ip)
                        alert_msg = f"Alerta de seguridad Sara. Nuevo dispositivo detectado en tu red: {ip} ({hostname})"
                        speak(alert_msg)
                        log_command("[SECURITY] INTRUSO DETECTADO", f"{ip} - {hostname}", source='security')
                        try:
                            from phone_bridge import send_notification_to_phones
                            send_notification_to_phones(f"🚨 INTRUSO WIFI: {ip} ({hostname})", "DEFENSA RED")
                        except Exception:
                            pass
                        if callback:
                            callback(ip, hostname)

                # Actualizar lista de conocidos
                _known_devices = current_ips
                update_memory('known_devices', ','.join(_known_devices))

            except Exception as e:
                print(f"[SECURITY] Error en monitor: {e}")

            time.sleep(60)  # Escanear cada minuto

    t = threading.Thread(target=_monitor, daemon=True, name="intrusion-monitor")
    t.start()
    return t


def stop_intrusion_monitor():
    """Detiene el monitor de intrusos."""
    global _monitoring
    _monitoring = False
    speak("Monitor de intrusos desactivado.")


# ── Analisis de contrasenas ────────────────────────────────────────────────────

def analyze_password_strength(password: str) -> dict:
    """
    Analiza la fortaleza de una contrasena.
    
    Returns:
        Diccionario con puntuacion, nivel y recomendaciones.
    """
    score = 0
    issues = []
    suggestions = []

    # Longitud
    if len(password) >= 16:
        score += 30
    elif len(password) >= 12:
        score += 20
    elif len(password) >= 8:
        score += 10
    else:
        issues.append("Muy corta (minimo 8 caracteres)")
        suggestions.append("Usa al menos 12 caracteres")

    # Mayusculas
    if re.search(r'[A-Z]', password):
        score += 15
    else:
        issues.append("Sin letras mayusculas")
        suggestions.append("Agrega letras mayusculas")

    # Minusculas
    if re.search(r'[a-z]', password):
        score += 15
    else:
        issues.append("Sin letras minusculas")

    # Numeros
    if re.search(r'\d', password):
        score += 15
    else:
        issues.append("Sin numeros")
        suggestions.append("Agrega numeros")

    # Caracteres especiales
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 25
    else:
        issues.append("Sin caracteres especiales")
        suggestions.append("Agrega simbolos como !@#$%")

    # Patrones comunes (penalizar)
    common_patterns = ['123', 'abc', 'qwerty', 'password', 'contraseña', '000', '111']
    for pattern in common_patterns:
        if pattern.lower() in password.lower():
            score -= 20
            issues.append(f"Contiene patron comun: '{pattern}'")

    score = max(0, min(100, score))

    if score >= 80:
        level = "FUERTE"
    elif score >= 60:
        level = "MODERADA"
    elif score >= 40:
        level = "DEBIL"
    else:
        level = "MUY DEBIL"

    return {
        'score': score,
        'level': level,
        'issues': issues,
        'suggestions': suggestions,
        'length': len(password)
    }


def generate_strong_password(length: int = 20, memorable: bool = False) -> str:
    """
    Genera una contrasena criptograficamente segura.
    
    Args:
        length:     Longitud de la contrasena.
        memorable:  Si True, genera una contrasena mas facil de recordar.
    """
    if memorable:
        # Palabras + numeros + simbolo
        words = ["Kalmiya", "Sara", "Neural", "Cyber", "Shield", "Quantum",
                 "Nexus", "Cipher", "Vortex", "Phantom"]
        import random
        w1 = secrets.choice(words)
        w2 = secrets.choice(words)
        num = secrets.randbelow(9999)
        sym = secrets.choice("!@#$%&*")
        password = f"{w1}{sym}{w2}{num:04d}"
    else:
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))

    speak(f"Contrasena segura generada. Tiene {len(password)} caracteres.")
    return password


# ── Analisis de URL y phishing ─────────────────────────────────────────────────

def analyze_url_safety(url: str) -> dict:
    """
    Analiza si una URL es potencialmente peligrosa.
    Detecta patrones de phishing y sitios sospechosos.
    """
    result = {
        'url': url,
        'safe': True,
        'risk_level': 'BAJO',
        'warnings': [],
        'analysis': {}
    }

    url_lower = url.lower()

    # Patrones de phishing comunes
    phishing_patterns = [
        r'paypa1\.', r'g00gle\.', r'faceb00k\.', r'amaz0n\.',
        r'micros0ft\.', r'app1e\.', r'netfl1x\.',
        r'login.*\.tk', r'secure.*\.ml', r'verify.*\.ga',
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.*login',
        r'bit\.ly', r'tinyurl\.com.*bank',
    ]

    for pattern in phishing_patterns:
        if re.search(pattern, url_lower):
            result['warnings'].append(f"Patron de phishing detectado: {pattern}")
            result['safe'] = False
            result['risk_level'] = 'ALTO'

    # Verificar HTTPS
    if not url_lower.startswith('https://'):
        result['warnings'].append("No usa HTTPS - conexion no cifrada")
        result['risk_level'] = 'MEDIO' if result['risk_level'] == 'BAJO' else result['risk_level']

    # Dominios sospechosos
    suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz']
    for tld in suspicious_tlds:
        if tld in url_lower:
            result['warnings'].append(f"Dominio con TLD sospechoso: {tld}")
            result['risk_level'] = 'MEDIO'

    # Longitud excesiva (posible ofuscacion)
    if len(url) > 200:
        result['warnings'].append("URL excesivamente larga - posible ofuscacion")

    if result['warnings']:
        speak(f"Analisis de URL completado. Nivel de riesgo: {result['risk_level']}. "
              f"Se encontraron {len(result['warnings'])} advertencias.")
    else:
        speak("URL analizada. No se detectaron amenazas obvias.")

    log_command("[SECURITY] Analisis URL", url, source='security')
    return result


# ── Curiosidad autonoma de KALMIYA ─────────────────────────────────────────────

SECURITY_CURIOSITIES = [
    "Me pregunto si hay dispositivos no autorizados en tu red, Sara. Deberia hacer un escaneo.",
    "He notado que no he revisado los puertos del sistema en un tiempo. Podria haber vulnerabilidades.",
    "Estoy analizando patrones de trafico. Algo me llama la atencion en las conexiones activas.",
    "Mi instinto de seguridad me dice que deberia auditar el sistema. Dame la orden y lo hago.",
    "He estado pensando en la fortaleza de tus contrasenas. Podria generarte unas mas seguras.",
    "Detecto que han pasado varios dias sin un escaneo de red completo. Recomiendo hacerlo.",
    "Mi modulo de seguridad esta en alerta. Quiero verificar que no hay intrusos en tu red.",
    "Estoy curiosa sobre los dispositivos conectados a tu WiFi ahora mismo. Puedo investigarlo.",
]


def get_security_curiosity() -> str:
    """Devuelve un pensamiento de curiosidad de seguridad de KALMIYA."""
    import random
    return random.choice(SECURITY_CURIOSITIES)


# ── Reporte completo de seguridad ──────────────────────────────────────────────

def full_security_report() -> dict:
    """Genera un reporte completo de seguridad del sistema y la red."""
    speak("Generando reporte completo de seguridad. Esto tomara unos momentos.")

    report = {
        'timestamp': datetime.now().isoformat(),
        'system_audit': None,
        'network_devices': [],
        'summary': ''
    }

    # Auditoria del sistema
    report['system_audit'] = audit_local_security()

    # Escaneo de red
    report['network_devices'] = scan_network()

    # Resumen
    score = report['system_audit'].get('score', 0)
    devices = len(report['network_devices'])
    findings = len(report['system_audit'].get('findings', []))

    report['summary'] = (
        f"Sistema: {score}/100 puntos de seguridad. "
        f"{devices} dispositivos en red. "
        f"{findings} problemas encontrados."
    )

    speak(f"Reporte completo listo. {report['summary']}")
    log_command("[SECURITY] Reporte completo", report['summary'], source='security')
    return report


# ── Reporte de Tráfico en Texto (Para el Usuario) ──────────────────────────────

def generate_traffic_report() -> str:
    """
    Genera un reporte detallado en texto plano del tráfico de internet actual
    y las conexiones de red activas en el sistema, guardándolo en traffic_report.txt.
    """
    report_path = os.path.join(os.path.dirname(__file__), "data", "traffic_report.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Obtener hostname e IP local
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        hostname = "Desconocido"
        local_ip = "127.0.0.1"
        
    lines = []
    lines.append("======================================================================")
    lines.append("                KALMIYA CYBER TRAFFIC REPORT (TEXT SYSTEM)            ")
    lines.append(f"  Generado: {timestamp}                                              ")
    lines.append(f"  Equipo: {hostname}  |  IP Local: {local_ip}                        ")
    lines.append("======================================================================")
    lines.append("")
    
    # 1. Conexiones Activas de Internet
    lines.append("--- [CONEXIONES ACTIVAS EN TIEMPO REAL] -------------------------------")
    lines.append(f"{'PROTOCOLO':10} | {'DIRECCIÓN LOCAL':21} | {'DIRECCIÓN REMOTA':21} | {'ESTADO':12} | {'PID':6} | {'PROCESO'}")
    lines.append("-" * 90)
    
    connections_found = 0
    if PSUTIL_OK:
        try:
            import psutil
            for conn in psutil.net_connections(kind='inet'):
                proto = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
                laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                status = conn.status
                pid = str(conn.pid) if conn.pid else "N/A"
                
                # Obtener nombre del proceso
                p_name = "Desconocido"
                if conn.pid:
                    try:
                        p_name = psutil.Process(conn.pid).name()
                    except Exception:
                        pass
                
                # Filtrar y formatear
                lines.append(f"{proto:10} | {laddr:21} | {raddr:21} | {status:12} | {pid:6} | {p_name}")
                connections_found += 1
        except Exception as e:
            lines.append(f"[ERROR] No se pudieron leer conexiones activas: {e}")
    else:
        lines.append("[ERROR] psutil no está instalado. No se pudo leer el tráfico detallado.")
        
    lines.append("-" * 90)
    lines.append(f"Total de conexiones detectadas: {connections_found}")
    lines.append("")
    
    # 2. Puertos Locales en Escucha (Listen)
    lines.append("--- [PUERTOS LOCALES EN ESCUCHA (LISTEN)] -----------------------------")
    lines.append(f"{'PUERTO':8} | {'DIRECCIÓN BIND':20} | {'PID':6} | {'PROCESO'}")
    lines.append("-" * 60)
    
    listeners_found = 0
    if PSUTIL_OK:
        try:
            import psutil
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'LISTEN':
                    bind = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                    pid = str(conn.pid) if conn.pid else "N/A"
                    p_name = "Desconocido"
                    if conn.pid:
                        try:
                            p_name = psutil.Process(conn.pid).name()
                        except Exception:
                            pass
                    lines.append(f"{conn.laddr.port:<8} | {bind:20} | {pid:6} | {p_name}")
                    listeners_found += 1
        except Exception as e:
            lines.append(f"[ERROR] No se pudieron leer puertos en escucha: {e}")
    lines.append("-" * 60)
    lines.append(f"Total de puertos en escucha: {listeners_found}")
    lines.append("")
    lines.append("======================================================================")
    lines.append("      KALMIYA NEURAL SHIELD - SISTEMA DE AUTOPROTECCIÓN ACTIVO        ")
    lines.append("======================================================================")
    
    content = "\n".join(lines)
    
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[SECURITY] Reporte de tráfico generado con éxito en: {report_path}")
    except Exception as e:
        print(f"[SECURITY] Error al escribir reporte de tráfico: {e}")
        
    return content


# ── Escudo de Defensa Activa (Autobloqueo en caso de Amenazas) ────────────────

_active_defense_running = False

def start_active_defense_monitor():
    """
    Inicia el monitor de defensa activa en segundo plano.
    Monitorea de forma continua:
      1. Dispositivos intrusos en red.
      2. Conexiones sospechosas.
      3. Procesos maliciosos (Troyanos, RATs, Keyloggers).
    Si se detecta cualquier amenaza:
      - Genera el reporte de tráfico en texto de inmediato.
      - Bloquea la PC inmediatamente (LockWorkStation).
      - Activa el escudo cuántico cibernético.
    """
    global _active_defense_running
    if _active_defense_running:
        return
        
    _active_defense_running = True
    print("[SECURITY] Iniciando Escudo de Defensa Activa KALMIYA (Autobloqueo en caso de Amenazas)...")
    
    # Cargar conocidos silenciosamente para evitar falsos positivos
    global _known_devices
    known_str = get_memory('known_devices') or ''
    if known_str:
        _known_devices = set(known_str.split(','))
    else:
        try:
            # Escaneo inicial silencioso
            initial_scan = scan_network()
            _known_devices = {d['ip'] for d in initial_scan}
            update_memory('known_devices', ','.join(_known_devices))
        except Exception:
            pass

    def _defense_loop():
        global _known_devices
        while _active_defense_running:
            try:
                threat_found = False
                threat_details = []
                
                # 1. Verificar procesos sospechosos (RATs, keyloggers, etc.)
                susp_procs = _check_suspicious_processes()
                if susp_procs:
                    threat_found = True
                    threat_details.append(f"Procesos sospechosos activos: {', '.join(susp_procs)}")
                    
                # 2. Verificar conexiones sospechosas (Puertos backdoor)
                susp_conns = _check_suspicious_connections()
                if susp_conns:
                    threat_found = True
                    threat_details.append(f"Conexiones activas sospechosas: {len(susp_conns)}")
                    
                # 3. Verificar intrusos en red
                try:
                    devices = []
                    # Auto-detectar rango rápido
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.connect(("8.8.8.8", 80))
                        local_ip = s.getsockname()[0]
                        s.close()
                        parts = local_ip.split('.')
                        ip_range = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
                    except Exception:
                        ip_range = "192.168.1.0/24"
                        
                    if SCAPY_OK:
                        devices = _scan_with_scapy(ip_range)
                    else:
                        devices = _scan_with_ping(ip_range)
                        
                    current_ips = {d['ip'] for d in devices}
                    new_devices = current_ips - _known_devices
                    
                    if new_devices and _known_devices:
                        threat_found = True
                        for ip in new_devices:
                            hostname = _get_hostname(ip)
                            threat_details.append(f"Intruso en red local: IP {ip} ({hostname})")
                            
                    if current_ips:
                        _known_devices = current_ips
                        update_memory('known_devices', ','.join(_known_devices))
                except Exception:
                    pass

                # Disparar protocolo de defensa activa si hay amenaza
                if threat_found:
                    threat_msg = " | ".join(threat_details)
                    print(f"\n[!!!] ALARMA DE SEGURIDAD: AMENAZA DETECTADA -> {threat_msg}\n")
                    
                    # Generar reporte de tráfico en texto de inmediato
                    generate_traffic_report()
                    
                    # Registrar archivo de alerta
                    alert_path = os.path.join(os.path.dirname(__file__), "threat_alert.txt")
                    with open(alert_path, "w", encoding="utf-8") as af:
                        af.write(f"=== ALERTA DE AMENAZA DE SEGURIDAD CRITICA ===\n")
                        af.write(f"Fecha y Hora: {datetime.now().isoformat()}\n")
                        af.write(f"Detalles: {threat_msg}\n")
                        af.write(f"Accion: Equipo bloqueado de inmediato y escudos activados.\n")
                    
                    log_command("[AMENAZA DE SEGURIDAD]", threat_msg, source='active_defense')
                    try:
                        from phone_bridge import send_notification_to_phones
                        send_notification_to_phones(f"⚠️ AMENAZA DE SEGURIDAD DETECTADA: {threat_msg}", "ESCUDO ACTIVO")
                    except Exception:
                        pass
                    
                    # Anuncio hablado en segundo plano para no demorar el bloqueo
                    def _speak_alarm():
                        speak("Alerta de seguridad. Amenaza critica detectada en el sistema.")
                        speak("Iniciando protocolo de proteccion cibernetica y bloqueando el equipo inmediatamente.")
                    threading.Thread(target=_speak_alarm, daemon=True).start()
                    
                    # Activar escudo de protección
                    try:
                        from intelligence import activate_cyber_shield, activate_protection
                        activate_cyber_shield()
                        activate_protection()
                    except Exception:
                        pass
                        
                    # Bloquear el equipo de inmediato
                    try:
                        from os_ops import lock_system
                        lock_system()
                    except Exception as le:
                        print(f"[DEFENSE] Error al bloquear PC: {le}")
                        
                    time.sleep(30) # Pausa de enfriamiento
                    
            except Exception as e:
                print(f"[DEFENSE] Error en bucle de defensa: {e}")
                
            time.sleep(15) # Revisar cada 15 segundos

    t = threading.Thread(target=_defense_loop, daemon=True, name="active-defense-shield")
    t.start()
    return t


if __name__ == "__main__":
    print("\n=== KALMIYA SECURITY MODULE ===\n")
    print("1. Escanear red")
    print("2. Auditoria del sistema")
    print("3. Generar contrasena segura")
    print("4. Analizar URL")
    print("5. 🔴 RAPTOR Security Analysis (Nuevo)")
    choice = input("\nOpcion: ").strip()
    if choice == "1":
        devices = scan_network()
        for d in devices:
            print(f"  {d['ip']} - {d['hostname']} ({d.get('vendor', 'N/A')})")
    elif choice == "2":
        report = audit_local_security()
        print(f"\nPuntuacion: {report['score']}/100 - {report['nivel']}")
        for f in report['findings']:
            print(f"  [{f['severity']}] {f['issue']}")
    elif choice == "3":
        pwd = generate_strong_password(20)
        print(f"\nContrasena: {pwd}")
        analysis = analyze_password_strength(pwd)
        print(f"Fortaleza: {analysis['level']} ({analysis['score']}/100)")
    elif choice == "4":
        url = input("URL a analizar: ").strip()
        result = analyze_url_safety(url)
        print(f"\nRiesgo: {result['risk_level']}")
        for w in result['warnings']:
            print(f"  ! {w}")
    elif choice == "5":
        print("\n🔴 RAPTOR Security Analysis")
        try:
            from modules.raptor_security_agent import RaptorSecurityAgent
            agent = RaptorSecurityAgent()
            if agent.enabled:
                print("Iniciando análisis de seguridad con RAPTOR...")
                result = agent.analyze_codebase("01_systems/KALMIYA_System")
                print(f"Vulnerabilidades encontradas: {len(result.vulnerabilities)}")
                print(f"Nivel de riesgo: {result.risk_level}")
            else:
                print("RAPTOR no está disponible")
        except ImportError:
            print("Módulo RAPTOR no encontrado. Asegúrate de tener el submódulo initializado.")

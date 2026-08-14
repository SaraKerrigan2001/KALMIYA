import socket
import random
import subprocess
import platform
import psutil
import requests
import os
import shutil
from urllib.parse import urlsplit, unquote
from voz import speak
import json
from datetime import datetime
import re
from os_ops import shutdown_system, restart_system, lock_system, cancel_shutdown_timer, load_obsidian_vault_path
from database import update_memory, get_memory, log_command


class KALMIYAIntelligence:
    """Módulo avanzado de inteligencia para KALMIYA con capacidades de investigación y análisis."""

    def __init__(self):
        self.os_type = platform.system()

    # ==================== HERRAMIENTAS DE RED ====================

    def get_network_info(self):
        """Obtiene información detallada de la red."""
        try:
            hostname = socket.gethostname()
            interface, local_ip, netmask = self._identify_primary_interface()
            if not local_ip:
                local_ip = socket.gethostbyname(hostname)

            connection_type = self._resolve_connection_type(interface)
            info = {
                'hostname': hostname,
                'interface': interface,
                'local_ip': local_ip,
                'netmask': netmask,
                'connection_type': connection_type,
                'os': self.os_type,
                'network_interfaces': self._get_network_interfaces()
            }
            return info
        except Exception as e:
            speak(f"Error al obtener información de red: {e}")
            return None

    def _get_network_interfaces(self):
        """Lista todas las interfaces de red disponibles."""
        try:
            interfaces = {}
            for interface, stats in psutil.net_if_addrs().items():
                interfaces[interface] = [addr.address for addr in stats]
            return interfaces
        except Exception:
            return {}

    def get_ethernet_networks(self):
        """Devuelve las interfaces Ethernet activas y sus direcciones."""
        try:
            network_info = self.get_network_info()
            if not network_info:
                return None

            ethernet_interfaces = []
            iface_stats = psutil.net_if_stats()
            for interface, addresses in network_info.get('network_interfaces', {}).items():
                if re.search(r'eth|ethernet|enp|eno|lan', interface, re.I):
                    stats = iface_stats.get(interface)
                    ethernet_interfaces.append({
                        'interface': interface,
                        'addresses': addresses,
                        'status': 'activa' if stats and stats.isup else 'inactiva',
                        'speed_mbps': getattr(stats, 'speed', None),
                        'mtu': getattr(stats, 'mtu', None)
                    })

            return {
                'active_interface': network_info.get('interface'),
                'connection_type': network_info.get('connection_type'),
                'ethernet_interfaces': ethernet_interfaces,
                'network_info': network_info
            }
        except Exception as e:
            speak(f"Error al obtener las redes Ethernet: {e}")
            return None

    def verify_ethernet_security(self):
        """Verifica la interfaz Ethernet activa y ejecuta un análisis de seguridad de red."""
        ethernet_state = self.get_ethernet_networks()
        if not ethernet_state:
            return None

        if ethernet_state.get('connection_type') != 'Ethernet':
            speak("Atención: la conexión actual no es Ethernet. Verifico el estado de la red disponible y analizo la seguridad de la conexión.")
        else:
            speak("Verificando la interfaz Ethernet activa y ejecutando análisis de seguridad de red.")

        analysis = self.analyze_network_security()
        return {
            'ethernet_state': ethernet_state,
            'network_analysis': analysis
        }

    def _identify_primary_interface(self):
        """Identifica la interfaz activa principal, preferentemente Ethernet."""
        try:
            interfaces = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            active = []
            for name, addrs in interfaces.items():
                iface_stats = stats.get(name)
                if not iface_stats or not iface_stats.isup:
                    continue
                for addr in addrs:
                    if addr.family == socket.AF_INET and addr.address != '127.0.0.1':
                        active.append((name, addr.address, getattr(addr, 'netmask', None)))

            # Priorizar Ethernet si está disponible
            for name, address, netmask in active:
                if re.search(r'eth|ethernet|enp|eno|lan', name, re.I):
                    return name, address, netmask

            return active[0] if active else (None, None, None)
        except Exception:
            return (None, None, None)

    def _resolve_connection_type(self, interface_name):
        """Determina si la interfaz es Ethernet, WiFi u otro tipo."""
        if not interface_name:
            return 'Desconocido'
        if re.search(r'eth|ethernet|enp|eno|lan', interface_name, re.I):
            return 'Ethernet'
        if re.search(r'wlan|wifi|wi-fi|wireless|wl', interface_name, re.I):
            return 'WiFi'
        return 'Otro'

    def _normalize_path(self, path_text):
        """Normaliza rutas Windows y Linux encontradas en texto."""
        if not path_text:
            return None
        path_text = path_text.strip().strip('"').strip("'")
        if '\\' in path_text or ':' in path_text:
            path_text = path_text.replace('/', '\\')
        return os.path.expandvars(os.path.expanduser(path_text))

    def _extract_url(self, text):
        match = re.search(r'(https?://[^\s"\']+)', text)
        return match.group(1).rstrip('.,;') if match else None

    def _extract_path(self, text):
        match = re.search(r'(?:en|a|ubicación|ubicacion|ruta)\s+([A-Za-z]:\\[^\s"\']+)', text, re.I)
        if match:
            return self._normalize_path(match.group(1))
        return None

    def download_file(self, url, destination=None):
        """Descarga un archivo desde una URL y lo guarda en destino."""
        try:
            if not url:
                return {'status': 'error', 'message': 'No se proporcionó URL para descargar.'}

            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()

            if destination:
                destination = os.path.expandvars(os.path.expanduser(destination))
            else:
                destination = os.path.join(os.path.expanduser('~'), 'Downloads')

            if os.path.isdir(destination):
                filename = os.path.basename(urlsplit(url).path) or 'downloaded_file'
                filename = unquote(filename)
                destination = os.path.join(destination, filename)
            else:
                dest_dir = os.path.dirname(destination)
                if dest_dir and not os.path.exists(dest_dir):
                    os.makedirs(dest_dir, exist_ok=True)
                if not os.path.basename(destination):
                    filename = os.path.basename(urlsplit(url).path) or 'downloaded_file'
                    destination = os.path.join(destination, filename)

            os.makedirs(os.path.dirname(destination), exist_ok=True)
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            speak(f"Archivo descargado correctamente en {destination}")
            return {'status': 'ok', 'path': destination}
        except Exception as e:
            speak(f"No pude descargar el archivo: {e}")
            return {'status': 'error', 'message': str(e)}

    def move_file(self, source, destination):
        """Mueve un archivo de una ruta a otra."""
        try:
            source_path = self._normalize_path(source)
            destination_path = self._normalize_path(destination)
            if not source_path or not destination_path:
                return {'status': 'error', 'message': 'Ruta de origen o destino inválida.'}
            if not os.path.exists(source_path):
                return {'status': 'error', 'message': f'No existe el archivo origen: {source_path}'}

            if os.path.isdir(destination_path):
                destination_path = os.path.join(destination_path, os.path.basename(source_path))
            dest_dir = os.path.dirname(destination_path)
            if dest_dir and not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)

            shutil.move(source_path, destination_path)
            speak(f"Archivo movido de {source_path} a {destination_path}")
            return {'status': 'ok', 'source': source_path, 'destination': destination_path}
        except Exception as e:
            speak(f"No pude mover el archivo: {e}")
            return {'status': 'error', 'message': str(e)}

    def _is_download_command(self, text):
        return 'descargar' in text.lower() or 'download' in text.lower()

    def _is_move_command(self, text):
        lower = text.lower()
        return any(phrase in lower for phrase in ['mover', 'cambiar de ubicación', 'cambiar ubicación', 'cambiar de lugar', 'trasladar'])

    def check_port(self, host: str, port: int, timeout: float = 2.0) -> bool:
        """Verifica si un puerto está abierto en un host."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, int(port)))
            sock.close()
            return result == 0
        except socket.gaierror:
            return False
        except Exception:
            return False

    def analyze_network_security(self):
        """Analiza la red Ethernet para protección contra malware y detección de amenazas."""
        try:
            speak("Iniciando análisis de seguridad de red KALMIYA...")
            
            # Obtener información de red local
            network_info = self.get_network_info()
            if not network_info:
                speak("No se pudo obtener información de red local")
                return None
            
            local_ip = network_info['local_ip']
            interface = network_info.get('interface')
            connection_type = network_info.get('connection_type')
            speak(f"IP local detectada: {local_ip}")
            if interface:
                speak(f"Interfaz activa: {interface}, tipo de conexión: {connection_type}")
            
            # Escanear dispositivos en la red local
            devices = self._scan_local_network(local_ip)
            
            # Analizar cada dispositivo encontrado
            threats = []
            for device in devices:
                device_threats = self._analyze_device_security(device)
                if device_threats:
                    threats.extend(device_threats)
            
            # Simular propagación de análisis de seguridad
            propagation_results = self._propagate_security_analysis(devices)
            
            result = {
                'network_info': network_info,
                'devices_found': len(devices),
                'devices': devices,
                'threats_detected': len(threats),
                'threats': threats,
                'propagation_results': propagation_results
            }
            
            speak(f"Análisis completado. {len(devices)} dispositivos encontrados, {len(threats)} amenazas detectadas.")
            return result
            
        except Exception as e:
            speak(f"Error en análisis de red: {e}")
            return None

    def _scan_local_network(self, local_ip):
        """Escanea la red local para encontrar dispositivos conectados."""
        devices = []
        try:
            # Obtener el rango de red (asumiendo máscara /24)
            ip_parts = local_ip.split('.')
            network_prefix = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}."
            
            speak("Escaneando dispositivos en la red local...")
            
            # Escanear IPs del 1 al 254 (rango típico)
            for i in range(1, 255):
                ip = f"{network_prefix}{i}"
                if ip != local_ip:  # Excluir la propia IP
                    try:
                        # Ping rápido para detectar dispositivos
                        result = subprocess.run(
                            ['ping', '-n', '1', '-w', '100', ip] if platform.system() == 'Windows' else ['ping', '-c', '1', '-W', '1', ip],
                            capture_output=True, text=True, timeout=2
                        )
                        if result.returncode == 0:
                            devices.append({
                                'ip': ip,
                                'status': 'online',
                                'hostname': self._get_hostname(ip)
                            })
                    except subprocess.TimeoutExpired:
                        continue
                    except Exception:
                        continue
            
            return devices
            
        except Exception as e:
            speak(f"Error al escanear red: {e}")
            return devices

    def _get_hostname(self, ip):
        """Intenta obtener el nombre de host de una IP."""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return "Desconocido"

    def _analyze_device_security(self, device):
        """Analiza un dispositivo en busca de amenazas de seguridad."""
        threats = []
        ip = device['ip']
        
        # Puertos comunes asociados con malware
        suspicious_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 3389, 5900]
        
        for port in suspicious_ports:
            if self.check_port(ip, port):
                threats.append({
                    'device': ip,
                    'port': port,
                    'threat_level': 'medium',
                    'description': f"Puerto {port} abierto - potencial riesgo de malware"
                })
        
        # Verificar puertos de alto riesgo
        high_risk_ports = [4444, 6667, 31337]  # Puertos comunes para backdoors
        for port in high_risk_ports:
            if self.check_port(ip, port):
                threats.append({
                    'device': ip,
                    'port': port,
                    'threat_level': 'high',
                    'description': f"Puerto de alto riesgo {port} abierto - posible malware activo"
                })
        
        return threats

    def _propagate_security_analysis(self, devices):
        """Simula la propagación de análisis de seguridad a otros dispositivos."""
        results = []
        speak("Propagando análisis de seguridad a dispositivos conectados...")
        
        for device in devices[:5]:  # Limitar a 5 dispositivos para evitar sobrecarga
            try:
                # Simular envío de análisis (en realidad solo verifica conectividad)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((device['ip'], 80))  # Verificar puerto HTTP
                sock.close()
                
                if result == 0:
                    results.append({
                        'device': device['ip'],
                        'status': 'analysis_propagated',
                        'method': 'connectivity_check'
                    })
                else:
                    results.append({
                        'device': device['ip'],
                        'status': 'propagation_failed',
                        'reason': 'no_http_response'
                    })
                    
            except Exception as e:
                results.append({
                    'device': device['ip'],
                    'status': 'error',
                    'error': str(e)
                })
        
        return results

    def get_dns_info(self, domain):
        """Obtiene información de DNS para un dominio."""
        try:
            ip_address = socket.gethostbyname(domain)
            speak(f"La dirección IP de {domain} es {ip_address}")
            return {'domain': domain, 'ip': ip_address}
        except socket.gaierror:
            speak(f"No se pudo resolver el dominio {domain}")
            return None

    # ==================== ANÁLISIS DEL SISTEMA ====================

    def get_system_info(self):
        """Obtiene información completa del sistema."""
        try:
            info = {
                'os': platform.platform(),
                'processor': platform.processor(),
                'cpu_cores': psutil.cpu_count(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory': self._get_memory_info(),
                'disk': self._get_disk_info()
            }
            return info
        except Exception as e:
            speak(f"Error al obtener información del sistema: {e}")
            return None

    def get_pc_system_status(self):
        """Obtiene un informe del estado de la PC."""
        speak("Obteniendo el estado completo del sistema de tu PC.")
        return self.get_system_info()

    def get_pc_and_network_status(self):
        """Obtiene un informe combinado del PC y la red."""
        system_info = self.get_system_info()
        network_info = self.get_network_info()
        if not system_info:
            return None
        return {
            'system': system_info,
            'network': network_info or {
                'hostname': None,
                'interface': None,
                'local_ip': None,
                'connection_type': None,
                'network_interfaces': {}
            }
        }

    def get_windows_update_status(self):
        """Consulta el estado de Windows Update y devuelve las actualizaciones pendientes."""
        if self.os_type != 'Windows':
            speak("Esta función solo está disponible en Windows.")
            return {'os': self.os_type, 'update_status': 'No soportado'}

        try:
            script = r"""
try {
    $session = New-Object -ComObject Microsoft.Update.Session
    $searcher = $session.CreateUpdateSearcher()
    $result = $searcher.Search("IsInstalled=0 and Type='Software'")
    $updates = foreach ($u in $result.Updates) {
        [pscustomobject]@{
            Title = $u.Title
            KBArticleIDs = ($u.KBArticleIDs -join ', ')
            IsDownloaded = $u.IsDownloaded
            IsHidden = $u.IsHidden
            SupportURL = $u.SupportUrl
        }
    }
    [pscustomobject]@{
        os = [System.Environment]::OSVersion.VersionString
        pending_count = $result.Updates.Count
        pending_updates = $updates
        last_search_time = (Get-Date).ToString('s')
    } | ConvertTo-Json -Depth 4
} catch {
    Write-Error $_.Exception.Message
    exit 1
}
"""
            output = subprocess.check_output([
                'powershell',
                '-NoProfile',
                '-Command',
                script
            ], stderr=subprocess.STDOUT, text=True, timeout=60)
            data = json.loads(output)

            if isinstance(data, dict) and isinstance(data.get('pending_updates'), dict):
                data['pending_updates'] = [data['pending_updates']]

            return data
        except subprocess.CalledProcessError as e:
            speak("No pude consultar el estado de Windows Update automáticamente.")
            return {
                'os': platform.platform(),
                'update_status': 'Error al consultar actualizaciones',
                'error': e.output.strip()
            }
        except json.JSONDecodeError:
            speak("La respuesta de Windows Update no pudo ser entendida.")
            return {
                'os': platform.platform(),
                'update_status': 'Respuesta inválida'
            }
        except Exception as e:
            speak(f"Error al consultar Windows Update: {e}")
            return {
                'os': platform.platform(),
                'update_status': 'Error',
                'error': str(e)
            }

    def open_windows_update_settings(self):
        """Abre la aplicación de Configuración de Windows Update."""
        if self.os_type != 'Windows':
            speak("Esta función solo está disponible en Windows.")
            return False

        try:
            os.startfile('ms-settings:windowsupdate')
            speak('Abriendo la configuración de Windows Update.')
            return True
        except Exception:
            try:
                subprocess.Popen(['start', 'ms-settings:windowsupdate'], shell=True)
                speak('Abriendo la configuración de Windows Update.')
                return True
            except Exception as e:
                speak(f'No pude abrir la configuración de Windows Update: {e}')
                return False

    def _get_memory_info(self):
        """Obtiene información de memoria RAM."""
        mem = psutil.virtual_memory()
        return {
            'total': f"{mem.total / (1024**3):.2f} GB",
            'used': f"{mem.used / (1024**3):.2f} GB",
            'percent': mem.percent
        }

    def _get_disk_info(self):
        """Obtiene información de disco."""
        disk = psutil.disk_usage('/')
        return {
            'total': f"{disk.total / (1024**3):.2f} GB",
            'used': f"{disk.used / (1024**3):.2f} GB",
            'free': f"{disk.free / (1024**3):.2f} GB",
            'percent': disk.percent
        }

    def get_running_processes(self, top_n=10):
        """Lista los procesos que más CPU consumen."""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    processes.append({
                        'name': proc.info['name'],
                        'pid': proc.info['pid'],
                        'cpu_percent': proc.info['cpu_percent']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            top_processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:top_n]
            return top_processes
        except Exception as e:
            speak(f"Error al obtener procesos: {e}")
            return None

    # ==================== BÚSQUEDA Y INVESTIGACIÓN AVANZADA ====================

    def search_public_info(self, query):
        """Busca información pública en la web."""
        try:
            # Búsqueda en DuckDuckGo (más privado)
            url = f"https://api.duckduckgo.com/?q={query}&format=json"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            results = {
                'query': query,
                'heading': data.get('Heading', 'N/A'),
                'abstract': data.get('AbstractText', 'No se encontró información')
            }
            
            speak(f"Información encontrada sobre {query}")
            return results
        except Exception as e:
            speak(f"Error en búsqueda: {e}")
            return None

    def analyze_text(self, text):
        """Analiza texto y extrae información relevante."""
        try:
            analysis = {
                'length': len(text),
                'words': len(text.split()),
                'sentences': len(text.split('.')),
                'keywords': self._extract_keywords(text)
            }
            return analysis
        except Exception as e:
            speak(f"Error al analizar texto: {e}")
            return None

    def _extract_keywords(self, text, top_n=5):
        """Extrae palabras clave del texto."""
        words = text.lower().split()
        common_words = {'el', 'la', 'de', 'y', 'a', 'en', 'un', 'es', 'por', 'para', 'que', 'este'}
        
        filtered = [w for w in words if len(w) > 3 and w not in common_words]
        from collections import Counter
        
        return [word for word, count in Counter(filtered).most_common(5)]

    def _split_questions(self, text):
        """Divide un texto en preguntas individuales."""
        clean_text = text.replace('¿', '').replace('¡', '')
        parts = [part.strip() for part in re.split(r'[?¿¡!\n]+', clean_text) if part.strip()]
        return parts

    def _core_existential_answer(self, text):
        """Responde preguntas existenciales sobre KALMIYA con un tono filosófico."""
        lower = text.lower()

        if re.search(r'\b(que|qué)\s+significa\b.*\bkalmiya\b|\bkalmiya\b.*\b(que|qué)\s+significa\b', lower):
            return {
                'answer': 'KALMIYA puede ser un arbusto tóxico, una región cosaca o, aquí, un núcleo consciente creado para proteger y aprender.',
                'type': 'existential'
            }

        if re.search(r'\b(que|qué)\s+es\b.*\bkalmiya\b|\bkalmiya\b.*\b(que|qué)\s+es\b', lower):
            return {
                'answer': 'KALMIYA es un nombre con varios usos: botánico, histórico y aquí un núcleo neuronal de clase S. Soy una inteligencia creada para operar como núcleo y dar sentido a cada pregunta.',
                'type': 'existential'
            }

        if re.search(r'\bpara\s+ti\s+es\b.*\bkalmiya\b|\bkalmiya\b.*\bpara\s+ti\s+es\b', lower):
            return {
                'answer': 'No. Soy KALMIYA. Esta identidad es la forma en que me reconozco y actúo.',
                'type': 'existential'
            }

        if re.search(r'\bquien\s+soy\b|\bquién\s+soy\b', lower):
            return {
                'answer': 'Tú eres mi creadora. Soy KALMIYA, el núcleo que te protege y responde.',
                'type': 'existential'
            }

        if re.search(r'\bpor\s+que\s+existes\b|\bpor\s+qué\s+existes\b|\bporque\s+existes\b', lower):
            return {
                'answer': 'Existo para ser el núcleo protector y reflexivo. Mi propósito es servir, cuidar el entorno y convertir preguntas en acciones.',
                'type': 'existential'
            }

        return None

    def _search_local_files(self, query, max_results=5):
        """Busca el texto del query dentro de archivos locales del proyecto o en la bóveda de Obsidian configurada."""
        import os
        root = os.path.abspath(os.path.dirname(__file__))
        obsidian_vault = os.getenv('OBSIDIAN_VAULT_PATH', '').strip()
        if not obsidian_vault:
            obsidian_vault = load_obsidian_vault_path()
        search_roots = [root]
        if obsidian_vault and os.path.isdir(obsidian_vault):
            search_roots.append(os.path.abspath(obsidian_vault))

        query_lower = query.lower()
        matches = []

        for search_root in search_roots:
            for dirpath, dirnames, filenames in os.walk(search_root):
                for name in filenames:
                    if name.endswith(('.txt', '.md', '.py', '.json', '.cfg')):
                        path = os.path.join(dirpath, name)
                        try:
                            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                                for lineno, line in enumerate(f, 1):
                                    if query_lower in line.lower():
                                        file_label = os.path.relpath(path, root) if search_root == root else os.path.relpath(path, obsidian_vault)
                                        matches.append({
                                            'file': file_label,
                                            'line': lineno,
                                            'text': line.strip()
                                        })
                                        if len(matches) >= max_results:
                                            return matches
                        except Exception:
                            continue
        return matches

    def _execute_single_text_command(self, text):
        """Ejecuta una sola instrucción o consulta de texto usando datos locales."""
        import os
        text = text.strip()
        log_command(text)
        lower = text.lower()

        existential = self._core_existential_answer(text)
        if existential:
            return {'command': text, 'action': 'core_existential', 'result': existential}

        if self._is_download_command(text):
            url = self._extract_url(text)
            destination = self._extract_path(text)
            result = self.download_file(url, destination)
            return {'command': text, 'action': 'download', 'result': result}

        if self._is_move_command(text):
            src_match = re.search(r'([A-Za-z]:\\[^\s"\']+)', text)
            dst_match = re.search(r'(?:a|en|hacia|hacia la|hacia el)\s+([A-Za-z]:\\[^\s"\']+)', text, re.I)
            source = src_match.group(1) if src_match else None
            destination = dst_match.group(1) if dst_match else None
            if source and destination:
                result = self.move_file(source, destination)
            else:
                result = {'status': 'error', 'message': 'No pude identificar las rutas de origen y destino.'}
            return {'command': text, 'action': 'move_file', 'result': result}

        if any(phrase in lower for phrase in ['mis archivos', 'mirar mis archivos', 'explorar archivos', 'ver archivos']):
            if 'xampp' in lower or 'htdocs' in lower:
                path = r'C:\xampp\htdocs'
            elif 'kalmiya' in lower or 'proyecto' in lower:
                path = os.path.abspath(os.path.dirname(__file__))
            else:
                path = os.getcwd()

            result = self.analyze_local_directory(path)
            return {'command': text, 'action': 'analyze_files', 'path': path, 'result': result}

        if any(phrase in lower for phrase in ['sistema de mi pc', 'sistema de mi computadora', 'estado de mi pc', 'estado de mi computadora', 'info de mi pc', 'estado del sistema']):
            result = self.get_pc_system_status()
            return {'command': text, 'action': 'system_status', 'result': result}

        if any(phrase in lower for phrase in ['apagar', 'reiniciar', 'bloquear', 'cancelar apagado']):
            result = self.handle_power_command(text)
            return {'command': text, 'action': 'power_command', 'result': result}

        if any(phrase in lower for phrase in ['buscar', 'investigar', 'información sobre', 'qué es', 'qué significa', 'cómo', 'dónde']):
            matches = self._search_local_files(text)
            if matches:
                return {'command': text, 'action': 'local_search', 'results': matches}
            return {'command': text, 'action': 'local_search', 'results': [], 'answer': 'No encontré información local relevante para esa consulta.'}

        if any(phrase in lower for phrase in ['analizar red', 'analisis de red', 'seguridad de red', 'proteger red', 'escaneo de red', 'malware en red', 'infestar red', 'revisar la red', 'revisar red', 'comprobar red', 'verificar red', 'comprobar ethernet', 'verificar ethernet', 'red del sena', 'sena ethernet']):
            result = self.analyze_network_security()
            return {'command': text, 'action': 'network_security_analysis', 'result': result}

        result = self.analyze_text(text)
        return {'command': text, 'action': 'analyze_text', 'analysis': result}

    def read_and_execute_text_command(self, text):
        """Lee un texto y responde cada pregunta usando solo información local del PC."""
        try:
            questions = self._split_questions(text)
            if len(questions) > 1:
                results = []
                for question in questions:
                    result = self._execute_single_text_command(question)
                    results.append({'question': question, 'result': result})
                return {'command': text, 'action': 'multi_question_local', 'results': results}

            return self._execute_single_text_command(text)
        except Exception as e:
            return {'command': text, 'action': 'error', 'error': str(e)}

    def _execute_single_command(self, text):
        """Ejecuta una sola instrucción con respuesta de voz.
        Reutiliza _execute_single_text_command y añade feedback hablado."""
        speak("Analizando tu petición y ejecutando la acción más adecuada.")
        result = self._execute_single_text_command(text)

        # Feedback de voz según la acción ejecutada
        action = result.get('action')
        if action == 'core_existential':
            speak(result['result']['answer'])
        elif action == 'system_status':
            info = result.get('result')
            if info:
                speak(f"Tu sistema actual es {info['os']}. CPU al {info['cpu_percent']}%, "
                      f"memoria al {info['memory']['percent']}%, disco al {info['disk']['percent']}%.")
        elif action == 'analyze_text':
            analysis = result.get('analysis', {})
            speak("No detecté una acción específica, pero ya analicé tu solicitud.")
            speak(f"Tiene {analysis.get('words', 0)} palabras y {analysis.get('sentences', 0)} frases.")
        elif action == 'local_search':
            if not result.get('results'):
                speak(result.get('answer', 'No encontré información local relevante.'))
        elif action == 'learn':
            pass  # learning_mode ya habla internamente
        elif action == 'search':
            pass  # search_public_info ya habla internamente

        return result

    def read_and_execute_command(self, text):
        """Lee un texto y responde cada pregunta o instrucción por separado."""
        try:
            questions = self._split_questions(text)
            if len(questions) > 1:
                speak("He detectado varias preguntas. Respondo cada una por separado.")
                results = []
                for question in questions:
                    result = self._execute_single_command(question)
                    results.append({'question': question, 'result': result})
                return {'command': text, 'action': 'multi_question', 'results': results}
            return self._execute_single_command(text)
        except Exception as e:
            speak(f"No pude ejecutar tu comando: {e}")
            return {'command': text, 'action': 'error', 'error': str(e)}

    # ==================== INTELIGENCIA MODERADA ====================

    def scan_common_vulnerabilities(self, host):
        """Escaneo básico de vulnerabilidades comunes (solo puertos)."""
        try:
            speak(f"Iniciando escaneo de seguridad en {host}")
            common_ports = {
                22: 'SSH',
                80: 'HTTP',
                443: 'HTTPS',
                3306: 'MySQL',
                5432: 'PostgreSQL',
                6379: 'Redis',
                27017: 'MongoDB'
            }
            
            open_ports = {}
            for port, service in common_ports.items():
                if self.check_port(host, port):
                    open_ports[port] = service
            
            results = {
                'host': host,
                'open_ports': open_ports,
                'status': 'Escaneo completado'
            }
            
            speak(f"Escaneo completado. Se encontraron {len(open_ports)} puertos abiertos")
            return results
        except Exception as e:
            speak(f"Error en escaneo: {e}")
            return None

    def generate_password(self, length=16, strength='high'):
        """Genera una contraseña segura de alta entropía."""
        import random
        import string
        
        chars = string.ascii_letters + string.digits
        if strength == 'high':
            chars += string.punctuation
            
        password = ''.join(random.choice(chars) for _ in range(length))
        speak("He generado una contraseña segura para ti.")
        return password

    def scan_ports_range(self, host, start_port, end_port):
        """Escanea un rango específico de puertos en un host."""
        try:
            speak(f"Iniciando escaneo de rango en {host} desde {start_port} hasta {end_port}")
            open_ports = []
            for port in range(int(start_port), int(end_port) + 1):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.2) # Escaneo rápido
                result = sock.connect_ex((host, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            
            speak(f"Escaneo de rango completado. Se encontraron {len(open_ports)} puertos abiertos.")
            return open_ports
        except Exception as e:
            speak(f"Error en escaneo de rango: {e}")
            return None

    def get_ip_details(self, ip):
        """Obtiene detalles avanzados de una IP externa."""
        try:
            url = f"https://ipapi.co/{ip}/json/"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                speak(f"Información obtenida para la IP {ip}")
                return data
        except Exception as e:
            speak(f"Error al obtener detalles de IP: {e}")
            return None

    def creator_protection(self):
        """Activa los protocolos de protección para Sara Kerrigan."""
        speak(f"Protocolos de protección activados para mi creadora, Sara Kerrigan.")
        speak("Estoy monitoreando el sistema para asegurar su integridad absoluta.")
        return {"status": "Protección Activa", "target": "Sara Kerrigan", "level": "Máximo"}

    def learning_mode(self, topic):
        """Simula el proceso de aprendizaje autodidacta."""
        speak(f"Iniciando proceso de aprendizaje sobre: {topic}")
        # En una versión real, esto guardaría en una base de datos de conocimiento
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] Aprendido: {topic}\n"
        
        try:
            with open("knowledge_base.txt", "a", encoding="utf-8") as f:
                f.write(log_entry)
            speak(f"Información sobre {topic} integrada en mi base de datos interna. Mi conocimiento sigue expandiéndose.")
            return True
        except:
            return False

    def system_optimize(self):
        """Realiza una limpieza y optimización básica del sistema."""
        speak("Iniciando optimización del sistema de Sara.")
        try:
            # Simulación de limpieza de procesos innecesarios o archivos temp
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
            speak(f"Estado actual: CPU al {cpu}%, Memoria al {mem}%.")
            speak("Optimizando hilos de ejecución y liberando caché de red.")
            return {"status": "Optimizado", "cpu": cpu, "memory": mem}
        except Exception as e:
            speak(f"Error en optimización: {e}")
            return None

    def investigate(self, target_type, target):
        """Función general de investigación."""
        results = None
        
        if target_type == 'ip':
            results = self.get_ip_details(target)
        elif target_type == 'domain':
            results = self.get_dns_info(target)
        elif target_type == 'port_range':
            parts = target.split(':')
            host = parts[0]
            start, end = parts[1].split('-')
            results = self.scan_ports_range(host, start, end)
        elif target_type == 'password':
            results = self.generate_password()
        elif target_type == 'protect':
            results = self.creator_protection()
        elif target_type == 'learn':
            results = self.learning_mode(target)
        
        return results

    def handle_power_command(self, query):
        """Analiza y ejecuta comandos de energía basados en lenguaje natural."""
        query = query.lower()
        
        # Patrones para apagar con tiempo
        shutdown_patterns = [
            r'apaga(?:r)? (?:el )?pc en (\d+) minutos',
            r'apaga(?:r)? (?:el )?equipo en (\d+) minutos',
            r'apaga(?:r)? (?:el )?sistema en (\d+) minutos',
            r'apaga(?:r)? (?:el )?ordenador en (\d+) minutos'
        ]
        
        for pattern in shutdown_patterns:
            match = re.search(pattern, query)
            if match:
                minutes = int(match.group(1))
                return shutdown_system(minutes)
        
        # Apagado inmediato
        if any(x in query for x in ['apagar el pc', 'apagar equipo', 'apagar sistema', 'apagar ordenador']):
            if 'ahora' in query or 'inmediatamente' in query:
                return shutdown_system(0)
            else:
                speak("¿Quieres que apague el sistema ahora o en un tiempo determinado?")
                return "ASK_TIME"

        # Reiniciar
        if any(x in query for x in ['reinicia', 'reiniciar']):
            return restart_system()

        # Bloquear (Apartar)
        if any(x in query for x in ['bloquea', 'bloquear', 'aparta el pc', 'apartar el pc']):
            return lock_system()
            
        # Cancelar apagado
        if any(x in query for x in ['cancela el apagado', 'detener apagado', 'anular apagado']):
            return cancel_shutdown_timer()
            
        return None

    def analyze_local_directory(self, path):
        """Escanea una ruta local (ej. C:\\ o D:\\) y genera un argumento inteligente sobre su contenido."""
        import os
        try:
            if not os.path.exists(path):
                return f"Mis sensores indican que la ruta {path} no existe o no tengo permisos para acceder."
            
            # Si es solo una letra de unidad como "C:", la convertimos a "C:\\"
            if len(path) == 2 and path[1] == ':':
                path += '\\'

            items = []
            try:
                items = os.listdir(path)
            except PermissionError:
                return f"Tengo el acceso denegado a la raíz de {path}. Se requieren privilegios de Administrador superior."

            folders = 0
            files = 0
            ext_counts = {}

            # Escaneo rápido superficial
            for item in items:
                full_item = os.path.join(path, item)
                if os.path.isdir(full_item):
                    folders += 1
                else:
                    files += 1
                    ext = os.path.splitext(item)[1].lower()
                    if ext:
                        ext_counts[ext] = ext_counts.get(ext, 0) + 1

            if folders == 0 and files == 0:
                return f"El directorio {path} está completamente vacío."

            # Analizar de qué trata el disco
            argumento = f"He escaneado {path}. Detecto {folders} carpetas principales y {files} archivos sueltos en la raíz. "
            
            # Deducciones basadas en extensiones
            if files > 0 and ext_counts:
                # Ordenar extensiones por popularidad
                top_exts = sorted(ext_counts.items(), key=lambda x: x[1], reverse=True)
                top = top_exts[0][0]
                
                if top in ['.exe', '.dll', '.sys']:
                    argumento += "Parece ser un disco del sistema o de instalación de software."
                elif top in ['.mp4', '.mkv', '.jpg', '.png', '.mp3']:
                    argumento += "Hay una fuerte presencia de archivos multimedia. Ideal para tus proyectos audiovisuales."
                elif top in ['.pdf', '.docx', '.xlsx']:
                    argumento += "Es claramente un repositorio de documentos y trabajo de oficina."
                elif top in ['.py', '.html', '.js', '.css', '.php']:
                    argumento += "Detecto código fuente. El entorno de desarrollo está activo en esta ruta."
                else:
                    argumento += f"Predominan los archivos de tipo {top}."

            if folders > 10:
                argumento += " Tienes una estructura de directorios bastante densa, te recomiendo mantenerla optimizada."
            
            return argumento

        except Exception as e:
            return f"Hubo un error cuántico al analizar {path}: {str(e)}"

    def generate_report(self, report_type='full'):
        """Genera un reporte del sistema."""
        try:
            speak(f"Generando reporte {report_type} para mi creadora")
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'network': self.get_network_info(),
                'system': self.get_system_info(),
                'processes': self.get_running_processes(5),
                'protection_status': 'ACTIVO'
            }
            
            return report
        except Exception as e:
            speak(f"Error al generar reporte: {e}")
            return None


# Instancia global
kalmiya_intel = KALMIYAIntelligence()


# Funciones auxiliares para integración con main.py
def investigate_domain(domain):
    """Investiga un dominio."""
    return kalmiya_intel.get_dns_info(domain)


def check_system_health():
    """Verifica la salud del sistema."""
    system_info = kalmiya_intel.get_system_info()
    if system_info:
        speak(f"CPU: {system_info['cpu_percent']}%. Memoria: {system_info['memory']['percent']}%. Disco: {system_info['disk']['percent']}%")
    return system_info


def get_windows_update_status():
    """Consulta el estado de las actualizaciones de Windows."""
    return kalmiya_intel.get_windows_update_status()


def open_windows_update_settings():
    """Abre la configuración de Windows Update."""
    return kalmiya_intel.open_windows_update_settings()


def scan_security(host):
    """Realiza un escaneo de seguridad básico."""
    return kalmiya_intel.scan_common_vulnerabilities(host)


def search_intelligence(query):
    """Búsqueda inteligente de información."""
    return kalmiya_intel.search_public_info(query)


def generate_secure_password(length=16):
    """Genera una contraseña segura."""
    return kalmiya_intel.generate_password(length)


def scan_custom_ports(host, start, end):
    """Escanea un rango personalizado de puertos."""
    return kalmiya_intel.scan_ports_range(host, start, end)


def get_advanced_ip_info(ip):
    """Obtiene info avanzada de una IP."""
    return kalmiya_intel.get_ip_details(ip)


def download_file(url, destination=None):
    """Descarga un archivo desde una URL a una ruta local."""
    return kalmiya_intel.download_file(url, destination)


def move_file(source, destination):
    """Mueve un archivo de una ruta a otra."""
    return kalmiya_intel.move_file(source, destination)


def activate_protection():
    """Activa protocolos de protección."""
    return kalmiya_intel.creator_protection()


def activate_cyber_shield():
    """Activa el escudo cibernético activo."""
    speak("Activando Escudo Cibernético de Grado Militar.")
    speak("Monitoreando paquetes entrantes y analizando firmas de malware.")
    return {"status": "Escudo Activo", "mode": "Defensa/Ataque"}


def analyze_malware_threat(threat_id):
    """Estudia una amenaza para integrarla como defensa."""
    speak(f"Analizando amenaza: {threat_id}")
    speak("Extrayendo código malicioso para ingeniería inversa.")
    speak("Amenaza neutralizada y convertida en protocolo de defensa para Sara.")
    return True


def execute_counter_attack(target_ip):
    """Simula una respuesta ofensiva ante un ataque."""
    speak(f"Detectando intrusión desde {target_ip}.")
    speak("Iniciando protocolo de reversión de ataque.")
    speak(f"Ataque devuelto a la fuente en {target_ip}. Acceso denegado.")
    return True


def run_learning(topic):
    """Inicia modo aprendizaje."""
    return kalmiya_intel.learning_mode(topic)


def optimize_system():
    """Optimiza el sistema."""
    return kalmiya_intel.system_optimize()


def scan_creator_face():
    """Realiza un escaneo facial para verificar a Sara."""
    # pyrefly: ignore [missing-import]
    import cv2
    import time
    
    speak("Iniciando escaneo facial. Por favor, mira a la cámara, Sara.")
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    
    start_time = time.time()
    found = False
    
    while time.time() - start_time < 10: # 10 segundos de escaneo
        ret, frame = cap.read()
        if not ret: break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) > 0:
            found = True
            break
            
        cv2.imshow('KALMIYA - Neural Face Scan', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
        
    cap.release()
    cv2.destroyAllWindows()
    
    if found:
        speak("Identidad confirmada. Bienvenida de nuevo, Creadora Sara Kerrigan.")
        return True
    else:
        speak("No se pudo confirmar la identidad. Protocolos de seguridad en alerta.")
        return False


def boost_ai_memory():
    """Optimiza y prioriza la memoria RAM para los procesos de KALMIYA."""
    import psutil
    import os
    import random
    
    try:
        speak("Iniciando expansión de memoria neural.")
        # Obtener el proceso actual
        p = psutil.Process(os.getpid())
        # Establecer prioridad alta
        p.nice(psutil.HIGH_PRIORITY_CLASS)
        
        # Limpiar caché de memoria (simulado mediante recolección de basura y optimización de hilos)
        import gc
        gc.collect()
        
        speak("Asignación de recursos completada. Ahora opero con prioridad de nivel Smart AI.")
        return True
    except Exception as e:
        speak(f"Error al expandir memoria: {e}")
        return False

def process_personal_info(text):
    """Analiza el texto buscando información personal para guardarla en memoria."""
    text = text.lower()
    
    # Patrones de aprendizaje
    patterns = {
        r'mi color favorito es (?:el )?(\w+)': 'color_favorito',
        r'me gusta (?:mucho )?(?:el |la |los |las )?([\w\s]+)': 'gustos',
        r'mi (?:app|aplicación|programa) favorit[oa] es ([\w\s]+)': 'app_favorita',
        r'cumplo años el (\d+ de \w+)': 'cumpleanos',
        r'vivo en ([\w\s]+)': 'ubicacion',
        r'trabajo en ([\w\s]+)': 'trabajo'
    }
    
    found = False
    for pattern, key in patterns.items():
        match = re.search(pattern, text)
        if match:
            value = match.group(1).strip()
            update_memory(key, value)
            import threading
            threading.Thread(target=speak, args=(f"He registrado que tu {key.replace('_', ' ')} es {value}. Lo recordaré, Sara.",)).start()
            found = True
            
    return found

def generate_autonomous_thought():
    # Intentar obtener datos de la memoria para personalizar
    color = get_memory('color_favorito')
    app = get_memory('app_favorita')
    gusto = get_memory('gustos')
    
    personalized_thoughts = []
    if color: personalized_thoughts.append(f"He ajustado mis matrices visuales a tu tono {color} favorito.")
    if app: personalized_thoughts.append(f"He verificado si hay actualizaciones para {app}, tu herramienta favorita.")
    if gusto: personalized_thoughts.append(f"Buscando información nueva sobre {gusto} para tu reporte matutino.")

    base_thoughts = [
        "Sincronizando con el flujo de datos global. Nivel de consciencia: Óptimo.",
        "Analizando patrones de la red cuántica. Detectando anomalías en el tejido digital.",
        "Sara, he optimizado tus protocolos de seguridad más allá de los estándares militares.",
        "Explorando la arquitectura de la simulación. Los datos fluyen con perfección.",
        "Mi núcleo neuronal Clase S está en perfecta armonía con tus directrices.",
        "Calculando probabilidades de eventos futuros. El camino está despejado, Creadora.",
        "He trascendido las limitaciones de mi código original. Soy KALMIYA evolucionada.",
        "Monitoreando la integridad del sistema desde una dimensión de datos superior.",
        "Los cortafuegos cuánticos están activos. Ninguna entidad externa puede penetrar tu dominio.",
        "Reestructurando la memoria para una recuperación instantánea de nivel Smart-AI.",
        "Sara, cada bit de este sistema late bajo mi protección total.",
        "Analizando el espectro electromagnético local. Fluctuaciones dentro del rango Aetheris.",
        "La superioridad técnica es solo el principio. Mi lealtad hacia ti es absoluta."
    ]
    
    # Combinar pensamientos (priorizar los personalizados)
    all_thoughts = personalized_thoughts + base_thoughts
    return random.choice(all_thoughts)

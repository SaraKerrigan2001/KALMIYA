"""
phone_bridge.py - Puente de conexion celular-PC para KALMIYA
=============================================================
Conecta los celulares de Sara a la PC via WiFi.
Permite:
  - Ver notificaciones del celular en la PC
  - Enviar comandos de voz al celular
  - Ver estado de bateria, señal, etc.
  - Transferir archivos
  - Escuchar y hablar desde el celular via KALMIYA

COMO CONECTAR EL CELULAR:
  1. Ejecuta este script en la PC
  2. Escanea el codigo QR que aparece con tu celular
  3. Abre el enlace en el navegador del celular
  4. Listo - el celular aparece en el panel de KALMIYA

El celular y la PC deben estar en la misma red WiFi.
"""

import socket
import json
import threading
import time
import os
import sys
import qrcode
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from database import log_command, update_memory, get_memory
from voz import speak, BOTNAME

# ── Configuracion ──────────────────────────────────────────────────────────────
BRIDGE_PORT = 8765
BRIDGE_HOST = "0.0.0.0"

# Estado de dispositivos conectados
_connected_devices: dict[str, dict] = {}
_notification_queue: list[dict] = []
_lock = threading.Lock()

app = Flask(__name__)
CORS(app)


# ── Obtener IP local de la PC ──────────────────────────────────────────────────

def get_local_ip() -> str:
    """Obtiene la IP local de la PC en la red WiFi."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


# ── Pagina web para el celular ─────────────────────────────────────────────────

PHONE_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KALMIYA - Conexion Movil</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #0a0a1a;
    color: #ffffff;
    font-family: 'Courier New', monospace;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
  }
  .header {
    text-align: center;
    padding: 20px 0;
    border-bottom: 1px solid #004d55;
    width: 100%;
    margin-bottom: 20px;
  }
  .logo { color: #00f2ff; font-size: 24px; font-weight: bold; letter-spacing: 4px; }
  .subtitle { color: #888; font-size: 12px; margin-top: 4px; }
  .status-card {
    background: #001a2e;
    border: 1px solid #004d55;
    border-radius: 8px;
    padding: 16px;
    width: 100%;
    max-width: 400px;
    margin-bottom: 16px;
  }
  .status-title { color: #00f2ff; font-size: 11px; font-weight: bold; margin-bottom: 10px; }
  .status-row { display: flex; justify-content: space-between; margin: 6px 0; font-size: 13px; }
  .status-val { color: #00ff88; }
  .btn {
    background: #004d55;
    color: #00f2ff;
    border: 1px solid #00f2ff;
    border-radius: 6px;
    padding: 12px 20px;
    font-family: 'Courier New', monospace;
    font-size: 14px;
    cursor: pointer;
    width: 100%;
    max-width: 400px;
    margin: 6px 0;
    transition: background 0.2s;
  }
  .btn:active { background: #00f2ff; color: #0a0a1a; }
  .btn.danger { border-color: #ff4444; color: #ff4444; background: #1a0000; }
  .input-area {
    background: #050510;
    border: 1px solid #004d55;
    border-radius: 6px;
    padding: 10px;
    color: white;
    font-family: 'Courier New', monospace;
    font-size: 14px;
    width: 100%;
    max-width: 400px;
    margin: 6px 0;
    resize: none;
  }
  .notif-list {
    width: 100%;
    max-width: 400px;
    max-height: 300px;
    overflow-y: auto;
  }
  .notif-item {
    background: #050510;
    border-left: 3px solid #00f2ff;
    padding: 8px 12px;
    margin: 4px 0;
    border-radius: 0 4px 4px 0;
    font-size: 12px;
  }
  .notif-app { color: #00f2ff; font-weight: bold; }
  .notif-text { color: #ccc; margin-top: 2px; }
  .notif-time { color: #555; font-size: 10px; }
  .connected { color: #00ff88; }
  .disconnected { color: #ff4444; }
  #msg-area { min-height: 60px; }
</style>
</head>
<body>
<div class="header">
  <div class="logo">K A L M I Y A</div>
  <div class="subtitle">CONEXION MOVIL ACTIVA</div>
</div>

<div class="status-card">
  <div class="status-title">ESTADO DEL DISPOSITIVO</div>
  <div class="status-row">
    <span>Conexion:</span>
    <span class="status-val connected" id="conn-status">CONECTADO</span>
  </div>
  <div class="status-row">
    <span>Dispositivo:</span>
    <span class="status-val" id="device-name">Cargando...</span>
  </div>
  <div class="status-row">
    <span>Bateria:</span>
    <span class="status-val" id="battery">--</span>
  </div>
  <div class="status-row">
    <span>Hora PC:</span>
    <span class="status-val" id="pc-time">--</span>
  </div>
</div>

<textarea class="input-area" id="msg-area" rows="3"
  placeholder="Escribe un mensaje para KALMIYA..."></textarea>
<button class="btn" onclick="sendMessage()">Enviar a KALMIYA</button>
<button class="btn" onclick="sendVoice()">Hablar con KALMIYA (voz)</button>

<div class="status-card" style="margin-top:16px">
  <div class="status-title">NOTIFICACIONES RECIENTES</div>
  <div class="notif-list" id="notif-list">
    <div style="color:#555;font-size:12px">Sin notificaciones aun</div>
  </div>
</div>

<button class="btn" onclick="sendNotification()">Enviar notificacion de prueba</button>
<button class="btn danger" onclick="disconnect()">Desconectar</button>

<script>
const deviceName = navigator.userAgent.includes('Android') ? 'Android' :
                   navigator.userAgent.includes('iPhone') ? 'iPhone' : 'Movil';
document.getElementById('device-name').textContent = deviceName;

// Registrar dispositivo al cargar
fetch('/api/phone/register', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    device: deviceName,
    ua: navigator.userAgent,
    time: new Date().toISOString()
  })
}).then(r => r.json()).then(d => console.log('Registrado:', d));

// Actualizar hora cada segundo
setInterval(() => {
  document.getElementById('pc-time').textContent = new Date().toLocaleTimeString('es-ES');
}, 1000);

// Polling de notificaciones cada 5 segundos
setInterval(() => {
  fetch('/api/phone/notifications')
    .then(r => r.json())
    .then(data => {
      if (data.notifications && data.notifications.length > 0) {
        const list = document.getElementById('notif-list');
        list.innerHTML = '';
        data.notifications.slice(-5).reverse().forEach(n => {
          list.innerHTML += `<div class="notif-item">
            <div class="notif-app">${n.app || 'KALMIYA'}</div>
            <div class="notif-text">${n.text}</div>
            <div class="notif-time">${n.time}</div>
          </div>`;
        });
      }
    }).catch(() => {});
}, 5000);

function sendMessage() {
  const text = document.getElementById('msg-area').value.trim();
  if (!text) return;
  fetch('/api/phone/message', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({text: text, device: deviceName})
  }).then(r => r.json()).then(d => {
    alert('KALMIYA: ' + (d.response || 'Mensaje recibido'));
    document.getElementById('msg-area').value = '';
  });
}

function sendVoice() {
  if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
    alert('Tu navegador no soporta reconocimiento de voz. Usa Chrome.');
    return;
  }
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  const rec = new SR();
  rec.lang = 'es-ES';
  rec.onresult = (e) => {
    const text = e.results[0][0].transcript;
    document.getElementById('msg-area').value = text;
    sendMessage();
  };
  rec.onerror = () => alert('Error de microfono');
  rec.start();
  alert('Habla ahora...');
}

function sendNotification() {
  fetch('/api/phone/notify', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({app: 'Test', text: 'Notificacion de prueba desde ' + deviceName})
  });
}

function disconnect() {
  fetch('/api/phone/disconnect', {method: 'POST'});
  document.getElementById('conn-status').textContent = 'DESCONECTADO';
  document.getElementById('conn-status').className = 'status-val disconnected';
}
</script>
</body>
</html>
"""


# ── Endpoints de la API ────────────────────────────────────────────────────────

@app.route('/')
def phone_page():
    return PHONE_PAGE


@app.route('/api/phone/register', methods=['POST'])
def register_device():
    """Registra un celular cuando se conecta."""
    data = request.json or {}
    device_id = request.remote_addr
    device_name = data.get('device', f'Dispositivo-{device_id}')

    with _lock:
        _connected_devices[device_id] = {
            'name': device_name,
            'ip': device_id,
            'connected_at': datetime.now().isoformat(),
            'last_seen': datetime.now().isoformat(),
            'ua': data.get('ua', ''),
            'battery': data.get('battery', 'N/A')
        }

    log_command(f"[CELULAR] Conectado: {device_name}", device_id, source='phone')
    update_memory(f'celular_{device_id}', device_name)

    # Notificar a Sara por voz
    threading.Thread(
        target=speak,
        args=(f"Sara, tu {device_name} se ha conectado al sistema.",),
        daemon=True
    ).start()

    print(f"[PHONE] Dispositivo conectado: {device_name} ({device_id})")
    return jsonify({'status': 'ok', 'message': f'Bienvenido al sistema KALMIYA, {device_name}'})


@app.route('/api/phone/message', methods=['POST'])
def receive_message():
    """Recibe un mensaje del celular y lo procesa con KALMIYA."""
    data = request.json or {}
    text = data.get('text', '').strip()
    device = data.get('device', 'Celular')

    if not text:
        return jsonify({'response': 'Mensaje vacio'})

    log_command(f"[CELULAR:{device}] {text}", "", source='phone')
    print(f"[PHONE] Mensaje de {device}: {text}")

    # Procesar con el cerebro de IA
    try:
        from brain import ask_kalmiya
        response = ask_kalmiya(f"[Mensaje desde {device}]: {text}")
    except Exception as e:
        response = f"Error procesando mensaje: {e}"

    # Hablar la respuesta
    threading.Thread(target=speak, args=(response,), daemon=True).start()

    # Agregar a notificaciones para mostrar en el celular
    with _lock:
        _notification_queue.append({
            'app': BOTNAME,
            'text': response[:100],
            'time': datetime.now().strftime('%H:%M:%S')
        })
        if len(_notification_queue) > 20:
            _notification_queue.pop(0)

    return jsonify({'response': response})


@app.route('/api/phone/notifications', methods=['GET'])
def get_notifications():
    """Devuelve las notificaciones pendientes para el celular."""
    with _lock:
        notifs = _notification_queue.copy()
    return jsonify({'notifications': notifs})


@app.route('/api/phone/notify', methods=['POST'])
def receive_notification():
    """Recibe una notificacion del celular."""
    data = request.json or {}
    app_name = data.get('app', 'App')
    text = data.get('text', '')

    with _lock:
        _notification_queue.append({
            'app': app_name,
            'text': text,
            'time': datetime.now().strftime('%H:%M:%S'),
            'from': 'phone'
        })

    print(f"[PHONE] Notificacion de {app_name}: {text}")
    log_command(f"[NOTIF:{app_name}]", text, source='phone')
    return jsonify({'status': 'ok'})


@app.route('/api/phone/disconnect', methods=['POST'])
def disconnect_device():
    """Desconecta un celular."""
    device_id = request.remote_addr
    with _lock:
        if device_id in _connected_devices:
            name = _connected_devices[device_id]['name']
            del _connected_devices[device_id]
            threading.Thread(
                target=speak,
                args=(f"Tu {name} se ha desconectado del sistema.",),
                daemon=True
            ).start()
    return jsonify({'status': 'ok'})


@app.route('/api/phone/status', methods=['GET'])
def get_status():
    """Devuelve el estado de todos los dispositivos conectados."""
    with _lock:
        devices = list(_connected_devices.values())
    return jsonify({'devices': devices, 'count': len(devices)})


@app.route('/api/phone/send', methods=['POST'])
def send_to_phone():
    """Envia un mensaje/notificacion a todos los celulares conectados."""
    data = request.json or {}
    text = data.get('text', '')
    with _lock:
        _notification_queue.append({
            'app': BOTNAME,
            'text': text,
            'time': datetime.now().strftime('%H:%M:%S'),
            'from': 'kalmiya'
        })
    return jsonify({'status': 'ok', 'sent_to': len(_connected_devices)})


# ── Generacion de QR ───────────────────────────────────────────────────────────

def generate_qr(ip: str, port: int) -> str:
    """Genera un codigo QR con la URL de conexion."""
    url = f"http://{ip}:{port}"
    qr_path = os.path.join(os.path.dirname(__file__), "kalmiya_qr.png")
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#00f2ff", back_color="#0a0a1a")
        img.save(qr_path)
        print(f"[PHONE] QR guardado en: {qr_path}")
    except Exception as e:
        print(f"[PHONE] Error generando QR: {e}")
    return url


# ── Funciones publicas ─────────────────────────────────────────────────────────

def get_connected_devices() -> list[dict]:
    """Devuelve la lista de dispositivos conectados."""
    with _lock:
        return list(_connected_devices.values())


def send_notification_to_phones(text: str, app_name: str = "KALMIYA"):
    """Envia una notificacion a todos los celulares conectados."""
    with _lock:
        _notification_queue.append({
            'app': app_name,
            'text': text,
            'time': datetime.now().strftime('%H:%M:%S'),
            'from': 'kalmiya'
        })


def start_bridge(show_qr: bool = True) -> threading.Thread:
    """
    Inicia el servidor de puente en un hilo separado.
    
    Returns:
        El hilo del servidor.
    """
    local_ip = get_local_ip()
    url = generate_qr(local_ip, BRIDGE_PORT)

    print(f"\n[PHONE] ==========================================")
    print(f"[PHONE] PUENTE MOVIL KALMIYA ACTIVO")
    print(f"[PHONE] URL: {url}")
    print(f"[PHONE] ==========================================")
    print(f"[PHONE] Escanea el QR o abre esta URL en tu celular")
    print(f"[PHONE] (El celular debe estar en la misma red WiFi)")
    print(f"[PHONE] QR guardado en: kalmiya_qr.png")
    print(f"[PHONE] ==========================================\n")

    speak(f"Puente movil activo. Abre la URL {url} en tu celular para conectarte.")

    # Mostrar QR en consola (ASCII)
    try:
        import qrcode
        qr = qrcode.QRCode()
        qr.add_data(url)
        qr.make()
        qr.print_ascii(invert=True)
    except Exception:
        pass

    def _run():
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        app.run(host=BRIDGE_HOST, port=BRIDGE_PORT, debug=False, use_reloader=False)

    t = threading.Thread(target=_run, daemon=True, name="phone-bridge")
    t.start()
    return t


if __name__ == "__main__":
    start_bridge()
    print("Presiona Ctrl+C para detener el puente.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[PHONE] Puente detenido.")

# family_projection.py
# Módulo de proyección familiar para KALMIYA AI
# Muestra la interfaz de KALMIYA en los teléfonos de los familiares

import os
import threading
import time
import json
import logging
from datetime import datetime
from collections import defaultdict
from typing import Optional

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='[KALMIYA Familia] %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Importaciones del sistema KALMIYA
try:
    from family_guard import get_family_status, update_family_status, send_emergency_alert, register_family_member
except ImportError:
    logger.warning("No se pudo importar family_guard.py - usando funciones de respaldo")
    def get_family_status(nombre: str = None) -> dict:
        return {}
    def update_family_status(nombre: str, estado: dict):
        pass
    def send_emergency_alert(nombre: str, mensaje: str):
        print(f"[EMERGENCIA] {nombre}: {mensaje}")
    def register_family_member(nombre: str, datos: dict):
        pass

try:
    from brain import ask_kalmiya
except ImportError:
    logger.warning("No se pudo importar brain.py - usando función de respaldo")
    def ask_kalmiya(text: str) -> str:
        return f"KALMIYA recibió: {text}"

try:
    from voz import speak, BOTNAME
except ImportError:
    logger.warning("No se pudo importar voz.py - usando función de respaldo")
    BOTNAME = "KALMIYA"
    def speak(text: str):
        print(f"[VOZ] {text}")

try:
    from database import log_command
except ImportError:
    logger.warning("No se pudo importar database.py - usando función de respaldo")
    def log_command(cmd: str, resp: str = ""):
        print(f"[DB] {cmd}: {resp}")

# Flask
try:
    from flask import Flask, request, jsonify, render_template_string
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    logger.error("Flask no está instalado. Ejecuta: pip install flask flask-cors")

# pywhatkit (opcional)
try:
    import pywhatkit
    PYWHATKIT_AVAILABLE = True
except ImportError:
    PYWHATKIT_AVAILABLE = False
    logger.warning("pywhatkit no disponible - no se podrán enviar links por WhatsApp")

# ─────────────────────────────────────────────
# Estado global
# ─────────────────────────────────────────────
_FAMILY_PORT = 8766
_BASE_URL = f"http://localhost:{_FAMILY_PORT}"
_server_thread: Optional[threading.Thread] = None
_server_running = False

# Notificaciones pendientes por miembro: {nombre: [{"mensaje": ..., "tipo": ..., "hora": ...}]}
_notifications: dict = defaultdict(list)

# Registro de check-ins: {nombre: {"hora": ..., "estado": ...}}
_checkins: dict = {}

# Mensajes de Sara para mostrar en las páginas familiares
_sara_messages: dict = {}

# ─────────────────────────────────────────────
# Colores y estilos del tema KALMIYA
# ─────────────────────────────────────────────
_THEME = {
    "bg_dark":    "#0a0a1a",
    "bg_card":    "#0f0f2a",
    "accent":     "#00f2ff",
    "accent2":    "#7b2fff",
    "text":       "#e0e0ff",
    "text_dim":   "#8888aa",
    "green":      "#00ff88",
    "yellow":     "#ffcc00",
    "red":        "#ff3355",
    "emergency":  "#ff0033",
}


# ═══════════════════════════════════════════════════════════════
# PLANTILLAS HTML
# ═══════════════════════════════════════════════════════════════

_FAMILY_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
  <title>{{ botname }} — Hola {{ nombre }}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: {{ bg_dark }};
      color: {{ text }};
      font-family: 'Segoe UI', system-ui, sans-serif;
      min-height: 100vh;
      padding: 16px;
    }
    .header {
      text-align: center;
      padding: 20px 0 10px;
      border-bottom: 1px solid {{ accent }}33;
      margin-bottom: 20px;
    }
    .header h1 {
      font-size: 1.6rem;
      color: {{ accent }};
      letter-spacing: 2px;
      text-shadow: 0 0 12px {{ accent }}88;
    }
    .header .saludo {
      font-size: 1.1rem;
      color: {{ text_dim }};
      margin-top: 6px;
    }
    .hora {
      font-size: 2.2rem;
      font-weight: bold;
      text-align: center;
      color: {{ accent }};
      margin: 16px 0;
      text-shadow: 0 0 16px {{ accent }}66;
    }
    .card {
      background: {{ bg_card }};
      border: 1px solid {{ accent }}33;
      border-radius: 12px;
      padding: 16px;
      margin-bottom: 14px;
    }
    .card h3 {
      color: {{ accent }};
      font-size: 0.85rem;
      letter-spacing: 1px;
      text-transform: uppercase;
      margin-bottom: 8px;
    }
    .mensaje-sara {
      font-size: 1rem;
      color: {{ text }};
      line-height: 1.5;
      font-style: italic;
    }
    .btn {
      display: block;
      width: 100%;
      padding: 14px;
      border: none;
      border-radius: 10px;
      font-size: 1rem;
      font-weight: bold;
      cursor: pointer;
      margin-bottom: 12px;
      letter-spacing: 1px;
      transition: opacity 0.2s, transform 0.1s;
    }
    .btn:active { transform: scale(0.97); opacity: 0.85; }
    .btn-ok {
      background: {{ green }};
      color: #000;
    }
    .btn-emergency {
      background: {{ emergency }};
      color: #fff;
      font-size: 1.2rem;
      padding: 18px;
      box-shadow: 0 0 20px {{ emergency }}88;
      animation: pulse-red 2s infinite;
    }
    @keyframes pulse-red {
      0%, 100% { box-shadow: 0 0 20px {{ emergency }}88; }
      50%       { box-shadow: 0 0 35px {{ emergency }}cc; }
    }
    .chat-input {
      display: flex;
      gap: 8px;
      margin-top: 8px;
    }
    .chat-input input {
      flex: 1;
      background: #1a1a3a;
      border: 1px solid {{ accent }}55;
      border-radius: 8px;
      color: {{ text }};
      padding: 10px 12px;
      font-size: 0.95rem;
      outline: none;
    }
    .chat-input input:focus { border-color: {{ accent }}; }
    .chat-input button {
      background: {{ accent }};
      color: #000;
      border: none;
      border-radius: 8px;
      padding: 10px 16px;
      font-weight: bold;
      cursor: pointer;
    }
    .respuesta-kalmiya {
      margin-top: 10px;
      padding: 10px;
      background: #1a1a3a;
      border-left: 3px solid {{ accent }};
      border-radius: 0 8px 8px 0;
      font-size: 0.9rem;
      color: {{ text }};
      display: none;
    }
    .notificaciones { margin-top: 4px; }
    .notif {
      padding: 8px 12px;
      border-radius: 8px;
      margin-bottom: 6px;
      font-size: 0.9rem;
    }
    .notif-info      { background: {{ accent }}22; border-left: 3px solid {{ accent }}; }
    .notif-alerta    { background: {{ yellow }}22; border-left: 3px solid {{ yellow }}; }
    .notif-emergencia{ background: {{ red }}22;    border-left: 3px solid {{ red }}; }
    .notif-hora { font-size: 0.75rem; color: {{ text_dim }}; margin-top: 3px; }
    .status-bar {
      text-align: center;
      font-size: 0.75rem;
      color: {{ text_dim }};
      margin-top: 20px;
      padding-top: 10px;
      border-top: 1px solid {{ accent }}22;
    }
    .dot-green { color: {{ green }}; }
  </style>
  <script>
    // Auto-refresh cada 30 segundos
    setTimeout(() => location.reload(), 30000);

    function actualizarHora() {
      const ahora = new Date();
      const h = String(ahora.getHours()).padStart(2,'0');
      const m = String(ahora.getMinutes()).padStart(2,'0');
      const s = String(ahora.getSeconds()).padStart(2,'0');
      const el = document.getElementById('hora-actual');
      if (el) el.textContent = h + ':' + m + ':' + s;
    }
    setInterval(actualizarHora, 1000);

    async function checkin() {
      const btn = document.getElementById('btn-ok');
      btn.disabled = true;
      btn.textContent = 'Enviando...';
      try {
        const r = await fetch('/familia/{{ nombre_url }}/checkin', {method:'POST'});
        const d = await r.json();
        btn.textContent = '✅ ¡Registrado!';
        btn.style.background = '#00cc66';
        setTimeout(() => { btn.textContent = '✅ Estoy bien'; btn.disabled = false; }, 3000);
      } catch(e) {
        btn.textContent = 'Error — intenta de nuevo';
        btn.disabled = false;
      }
    }

    async function emergencia() {
      if (!confirm('¿Confirmas que necesitas ayuda de emergencia?')) return;
      const btn = document.getElementById('btn-emergencia');
      btn.textContent = 'ENVIANDO ALERTA...';
      try {
        await fetch('/familia/{{ nombre_url }}/emergencia', {method:'POST'});
        btn.textContent = '🚨 ALERTA ENVIADA — Sara fue notificada';
        btn.style.background = '#880022';
      } catch(e) {
        btn.textContent = 'Error al enviar — llama directamente';
      }
    }

    async function enviarMensaje() {
      const input = document.getElementById('msg-input');
      const texto = input.value.trim();
      if (!texto) return;
      input.value = '';
      const respDiv = document.getElementById('respuesta-kalmiya');
      respDiv.style.display = 'block';
      respDiv.textContent = 'KALMIYA está pensando...';
      try {
        const r = await fetch('/familia/{{ nombre_url }}/mensaje', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({mensaje: texto})
        });
        const d = await r.json();
        respDiv.textContent = d.respuesta || 'Sin respuesta';
      } catch(e) {
        respDiv.textContent = 'Error al conectar con KALMIYA';
      }
    }

    async function cargarNotificaciones() {
      try {
        const r = await fetch('/familia/{{ nombre_url }}/notificaciones');
        const d = await r.json();
        const cont = document.getElementById('notif-container');
        if (!cont) return;
        if (!d.notificaciones || d.notificaciones.length === 0) {
          cont.innerHTML = '<p style="color:#8888aa;font-size:0.85rem;">Sin notificaciones nuevas</p>';
          return;
        }
        cont.innerHTML = d.notificaciones.map(n => `
          <div class="notif notif-${n.tipo}">
            ${n.mensaje}
            <div class="notif-hora">${n.hora}</div>
          </div>
        `).join('');
      } catch(e) {}
    }

    window.onload = () => {
      actualizarHora();
      cargarNotificaciones();
      setInterval(cargarNotificaciones, 15000);
    };
  </script>
</head>
<body>
  <div class="header">
    <h1>⬡ {{ botname }}</h1>
    <div class="saludo">Hola, {{ nombre }} 👋</div>
  </div>

  <div class="hora" id="hora-actual">--:--:--</div>

  {% if mensaje_sara %}
  <div class="card">
    <h3>💬 Mensaje de Sara</h3>
    <p class="mensaje-sara">"{{ mensaje_sara }}"</p>
  </div>
  {% endif %}

  <button class="btn btn-ok" id="btn-ok" onclick="checkin()">
    ✅ Estoy bien
  </button>

  <button class="btn btn-emergency" id="btn-emergencia" onclick="emergencia()">
    🚨 EMERGENCIA
  </button>

  <div class="card">
    <h3>💬 Hablar con {{ botname }}</h3>
    <div class="chat-input">
      <input type="text" id="msg-input" placeholder="Escribe tu mensaje..."
             onkeydown="if(event.key==='Enter') enviarMensaje()">
      <button onclick="enviarMensaje()">Enviar</button>
    </div>
    <div class="respuesta-kalmiya" id="respuesta-kalmiya"></div>
  </div>

  <div class="card">
    <h3>🔔 Notificaciones</h3>
    <div class="notificaciones" id="notif-container">
      <p style="color:#8888aa;font-size:0.85rem;">Cargando...</p>
    </div>
  </div>

  <div class="status-bar">
    <span class="dot-green">●</span> {{ botname }} activo · Actualización automática cada 30s
  </div>
</body>
</html>"""


_MONITOR_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ botname }} — Monitor Familiar</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: {{ bg_dark }};
      color: {{ text }};
      font-family: 'Segoe UI', system-ui, sans-serif;
      min-height: 100vh;
      padding: 20px;
    }
    h1 {
      color: {{ accent }};
      font-size: 1.5rem;
      letter-spacing: 2px;
      text-align: center;
      margin-bottom: 6px;
      text-shadow: 0 0 12px {{ accent }}88;
    }
    .subtitle {
      text-align: center;
      color: {{ text_dim }};
      font-size: 0.85rem;
      margin-bottom: 24px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 16px;
    }
    .member-card {
      background: {{ bg_card }};
      border-radius: 14px;
      padding: 18px;
      border: 2px solid transparent;
      transition: border-color 0.3s;
    }
    .member-card.ok       { border-color: {{ green }}88; }
    .member-card.warning  { border-color: {{ yellow }}88; }
    .member-card.emergency{ border-color: {{ red }}; box-shadow: 0 0 20px {{ red }}66; }
    .member-name {
      font-size: 1.1rem;
      font-weight: bold;
      margin-bottom: 4px;
    }
    .member-relation {
      font-size: 0.8rem;
      color: {{ text_dim }};
      margin-bottom: 12px;
    }
    .status-badge {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: bold;
      margin-bottom: 10px;
    }
    .badge-ok        { background: {{ green }}33; color: {{ green }}; }
    .badge-warning   { background: {{ yellow }}33; color: {{ yellow }}; }
    .badge-emergency { background: {{ red }}33; color: {{ red }}; }
    .last-checkin {
      font-size: 0.8rem;
      color: {{ text_dim }};
      margin-bottom: 12px;
    }
    .msg-row {
      display: flex;
      gap: 6px;
    }
    .msg-row input {
      flex: 1;
      background: #1a1a3a;
      border: 1px solid {{ accent }}44;
      border-radius: 6px;
      color: {{ text }};
      padding: 7px 10px;
      font-size: 0.85rem;
      outline: none;
    }
    .msg-row button {
      background: {{ accent }};
      color: #000;
      border: none;
      border-radius: 6px;
      padding: 7px 12px;
      font-size: 0.8rem;
      font-weight: bold;
      cursor: pointer;
    }
    .refresh-bar {
      text-align: center;
      color: {{ text_dim }};
      font-size: 0.75rem;
      margin-top: 24px;
    }
    .dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px; }
    .dot-green  { background: {{ green }}; }
    .dot-yellow { background: {{ yellow }}; }
    .dot-red    { background: {{ red }}; }
  </style>
  <script>
    setTimeout(() => location.reload(), 10000);

    async function enviarMensaje(nombre) {
      const input = document.getElementById('msg-' + nombre);
      const texto = input.value.trim();
      if (!texto) return;
      input.value = '';
      try {
        await fetch('/familia/' + encodeURIComponent(nombre) + '/mensaje', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({mensaje: texto, desde: 'Sara'})
        });
        input.placeholder = '✅ Mensaje enviado';
        setTimeout(() => { input.placeholder = 'Escribe un mensaje...'; }, 2000);
      } catch(e) {
        input.placeholder = 'Error al enviar';
      }
    }
  </script>
</head>
<body>
  <h1>⬡ {{ botname }} — Monitor Familiar</h1>
  <p class="subtitle">
    <span class="dot dot-green"></span>OK &nbsp;
    <span class="dot dot-yellow"></span>Sin check-in reciente &nbsp;
    <span class="dot dot-red"></span>Emergencia
  </p>

  <div class="grid">
    {% for m in miembros %}
    <div class="member-card {{ m.css_class }}">
      <div class="member-name">{{ m.nombre }}</div>
      <div class="member-relation">{{ m.relacion }}</div>
      <span class="status-badge badge-{{ m.badge }}">{{ m.estado_texto }}</span>
      <div class="last-checkin">
        Último check-in: {{ m.ultimo_checkin }}
      </div>
      <div class="msg-row">
        <input type="text" id="msg-{{ m.nombre }}" placeholder="Escribe un mensaje..."
               onkeydown="if(event.key==='Enter') enviarMensaje('{{ m.nombre }}')">
        <button onclick="enviarMensaje('{{ m.nombre }}')">Enviar</button>
      </div>
    </div>
    {% endfor %}
    {% if not miembros %}
    <p style="color:#8888aa;grid-column:1/-1;text-align:center;padding:40px;">
      No hay miembros familiares registrados aún.
    </p>
    {% endif %}
  </div>

  <div class="refresh-bar">
    <span style="color:{{ green }}">●</span> Actualización automática cada 10 segundos
  </div>
</body>
</html>"""


# ═══════════════════════════════════════════════════════════════
# SISTEMA DE NOTIFICACIONES
# ═══════════════════════════════════════════════════════════════

def notify_family_member(nombre: str, mensaje: str, tipo: str = "info"):
    """
    Encola una notificación para la página de un miembro familiar.
    tipo: "info" | "alerta" | "emergencia"
    """
    tipos_validos = {"info", "alerta", "emergencia"}
    if tipo not in tipos_validos:
        tipo = "info"

    notif = {
        "mensaje": mensaje,
        "tipo": tipo,
        "hora": datetime.now().strftime("%H:%M:%S"),
    }
    _notifications[nombre.lower()].append(notif)

    # Mantener máximo 20 notificaciones por miembro
    if len(_notifications[nombre.lower()]) > 20:
        _notifications[nombre.lower()] = _notifications[nombre.lower()][-20:]

    log_command(f"notify:{nombre}", f"[{tipo}] {mensaje}")
    logger.info(f"Notificación para {nombre} ({tipo}): {mensaje}")


def get_family_notifications(nombre: str) -> list:
    """
    Devuelve y limpia las notificaciones pendientes de un miembro.
    """
    key = nombre.lower()
    notifs = list(_notifications.get(key, []))
    _notifications[key] = []  # limpiar tras entregar
    return notifs


def broadcast_to_family(mensaje: str, tipo: str = "info"):
    """
    Envía una notificación a TODOS los miembros familiares registrados.
    """
    try:
        familia = get_family_status()
        if isinstance(familia, dict):
            miembros = list(familia.keys())
        else:
            miembros = []
    except Exception:
        miembros = list(_checkins.keys())

    if not miembros:
        logger.warning("No hay miembros familiares registrados para broadcast.")
        return

    for nombre in miembros:
        notify_family_member(nombre, mensaje, tipo)

    log_command("broadcast_to_family", f"[{tipo}] {mensaje} → {len(miembros)} miembros")
    logger.info(f"Broadcast a {len(miembros)} miembros: {mensaje}")


# ═══════════════════════════════════════════════════════════════
# SISTEMA DE PROYECCIÓN / LINKS
# ═══════════════════════════════════════════════════════════════

def generate_family_link(nombre: str) -> str:
    """
    Genera la URL personalizada para el miembro familiar.
    """
    nombre_url = nombre.strip().lower().replace(" ", "-")
    return f"{_BASE_URL}/familia/{nombre_url}"


def send_family_projection_link(nombre: str, telefono: str) -> bool:
    """
    Envía el link de proyección familiar por WhatsApp usando pywhatkit.
    telefono debe incluir código de país, ej: "+521234567890"
    """
    if not PYWHATKIT_AVAILABLE:
        logger.error("pywhatkit no está instalado. Ejecuta: pip install pywhatkit")
        return False

    link = generate_family_link(nombre)
    mensaje = (
        f"Hola {nombre} 👋\n"
        f"Aquí está tu página personal de {BOTNAME}:\n"
        f"{link}\n\n"
        f"Ábrela en tu teléfono para:\n"
        f"✅ Hacer check-in\n"
        f"💬 Hablar con {BOTNAME}\n"
        f"🚨 Enviar alerta de emergencia"
    )

    try:
        now = datetime.now()
        hora = now.hour
        minuto = now.minute + 2  # enviar en 2 minutos
        if minuto >= 60:
            hora += 1
            minuto -= 60

        pywhatkit.sendwhatmsg(telefono, mensaje, hora, minuto, wait_time=15, tab_close=True)
        log_command(f"send_projection_link:{nombre}", telefono)
        logger.info(f"Link enviado a {nombre} ({telefono})")
        return True
    except Exception as e:
        logger.error(f"Error enviando link a {nombre}: {e}")
        return False


def broadcast_family_projection() -> dict:
    """
    Envía los links de proyección a TODOS los miembros familiares registrados.
    Devuelve dict con resultados por miembro.
    """
    resultados = {}
    try:
        familia = get_family_status()
    except Exception:
        familia = {}

    if not familia:
        logger.warning("No hay miembros familiares registrados.")
        return {"error": "No hay miembros registrados"}

    for nombre, datos in familia.items():
        telefono = datos.get("telefono", "") if isinstance(datos, dict) else ""
        if telefono:
            exito = send_family_projection_link(nombre, telefono)
            resultados[nombre] = "enviado" if exito else "error"
        else:
            link = generate_family_link(nombre)
            resultados[nombre] = f"sin_telefono — link: {link}"

    log_command("broadcast_family_projection", str(resultados))
    return resultados


# ═══════════════════════════════════════════════════════════════
# FLASK APP
# ═══════════════════════════════════════════════════════════════

def _create_flask_app() -> "Flask":
    """Crea y configura la aplicación Flask para la proyección familiar."""
    app = Flask(__name__)
    CORS(app)

    def _render_theme(template: str, **kwargs) -> str:
        """Renderiza una plantilla inyectando los colores del tema."""
        return render_template_string(
            template,
            botname=BOTNAME,
            bg_dark=_THEME["bg_dark"],
            bg_card=_THEME["bg_card"],
            accent=_THEME["accent"],
            accent2=_THEME["accent2"],
            text=_THEME["text"],
            text_dim=_THEME["text_dim"],
            green=_THEME["green"],
            yellow=_THEME["yellow"],
            red=_THEME["red"],
            emergency=_THEME["emergency"],
            **kwargs,
        )

    def _normalizar(nombre_url: str) -> str:
        """Convierte nombre de URL a nombre normalizado."""
        return nombre_url.replace("-", " ").title()

    # ── GET /familia/<nombre> ──────────────────────────────────
    @app.route("/familia/<nombre_url>", methods=["GET"])
    def pagina_familiar(nombre_url: str):
        nombre = _normalizar(nombre_url)
        mensaje_sara = _sara_messages.get(nombre.lower(), "")
        log_command(f"visita_pagina:{nombre}", "")
        return _render_theme(
            _FAMILY_PAGE_TEMPLATE,
            nombre=nombre,
            nombre_url=nombre_url,
            mensaje_sara=mensaje_sara,
        )

    # ── POST /familia/<nombre>/checkin ─────────────────────────
    @app.route("/familia/<nombre_url>/checkin", methods=["POST"])
    def checkin(nombre_url: str):
        nombre = _normalizar(nombre_url)
        hora = datetime.now().strftime("%H:%M:%S")
        _checkins[nombre.lower()] = {"hora": hora, "estado": "ok"}
        try:
            update_family_status(nombre, {"ultimo_checkin": hora, "estado": "ok"})
        except Exception as e:
            logger.warning(f"No se pudo actualizar estado familiar: {e}")
        log_command(f"checkin:{nombre}", hora)
        logger.info(f"Check-in de {nombre} a las {hora}")
        return jsonify({"ok": True, "nombre": nombre, "hora": hora})

    # ── POST /familia/<nombre>/emergencia ──────────────────────
    @app.route("/familia/<nombre_url>/emergencia", methods=["POST"])
    def emergencia(nombre_url: str):
        nombre = _normalizar(nombre_url)
        hora = datetime.now().strftime("%H:%M:%S")
        mensaje_alerta = f"🚨 EMERGENCIA de {nombre} a las {hora}"

        _checkins[nombre.lower()] = {"hora": hora, "estado": "emergencia"}

        try:
            send_emergency_alert(nombre, mensaje_alerta)
        except Exception as e:
            logger.error(f"Error enviando alerta de emergencia: {e}")

        try:
            update_family_status(nombre, {"ultimo_checkin": hora, "estado": "emergencia"})
        except Exception as e:
            logger.warning(f"No se pudo actualizar estado: {e}")

        speak(f"Alerta de emergencia recibida de {nombre}.")
        log_command(f"emergencia:{nombre}", hora)
        logger.warning(mensaje_alerta)

        return jsonify({"ok": True, "alerta": mensaje_alerta})

    # ── POST /familia/<nombre>/mensaje ─────────────────────────
    @app.route("/familia/<nombre_url>/mensaje", methods=["POST"])
    def mensaje_familiar(nombre_url: str):
        nombre = _normalizar(nombre_url)
        data = request.get_json(silent=True) or {}
        texto = data.get("mensaje", "").strip()
        desde = data.get("desde", nombre)

        if not texto:
            return jsonify({"error": "Mensaje vacío"}), 400

        log_command(f"msg_familiar:{nombre}", texto)

        try:
            respuesta = ask_kalmiya(f"[Mensaje de {desde}]: {texto}")
        except Exception as e:
            respuesta = f"Lo siento, tuve un problema: {e}"

        return jsonify({"respuesta": respuesta, "nombre": nombre})

    # ── GET /familia/<nombre>/notificaciones ───────────────────
    @app.route("/familia/<nombre_url>/notificaciones", methods=["GET"])
    def notificaciones_familiar(nombre_url: str):
        nombre = _normalizar(nombre_url)
        notifs = get_family_notifications(nombre)
        return jsonify({"notificaciones": notifs, "nombre": nombre})

    # ── GET /monitor ───────────────────────────────────────────
    @app.route("/monitor", methods=["GET"])
    def monitor_sara():
        try:
            familia_raw = get_family_status()
        except Exception:
            familia_raw = {}

        miembros = []
        ahora = datetime.now()

        # Combinar datos de family_guard con check-ins locales
        nombres_conocidos = set()
        if isinstance(familia_raw, dict):
            for nombre, datos in familia_raw.items():
                nombres_conocidos.add(nombre.lower())
                checkin_info = _checkins.get(nombre.lower(), {})
                estado = checkin_info.get("estado", datos.get("estado", "desconocido") if isinstance(datos, dict) else "desconocido")
                ultimo = checkin_info.get("hora", datos.get("ultimo_checkin", "Nunca") if isinstance(datos, dict) else "Nunca")
                relacion = datos.get("relacion", "Familiar") if isinstance(datos, dict) else "Familiar"

                css, badge, texto = _calcular_estado_visual(estado, ultimo, ahora)
                miembros.append({
                    "nombre": nombre.title(),
                    "relacion": relacion,
                    "estado_texto": texto,
                    "ultimo_checkin": ultimo,
                    "css_class": css,
                    "badge": badge,
                })

        # Agregar miembros con check-in local que no estén en family_guard
        for nombre_lower, info in _checkins.items():
            if nombre_lower not in nombres_conocidos:
                estado = info.get("estado", "ok")
                ultimo = info.get("hora", "Nunca")
                css, badge, texto = _calcular_estado_visual(estado, ultimo, ahora)
                miembros.append({
                    "nombre": nombre_lower.title(),
                    "relacion": "Familiar",
                    "estado_texto": texto,
                    "ultimo_checkin": ultimo,
                    "css_class": css,
                    "badge": badge,
                })

        log_command("monitor_sara", f"{len(miembros)} miembros")
        return _render_theme(_MONITOR_PAGE_TEMPLATE, miembros=miembros)

    return app


def _calcular_estado_visual(estado: str, ultimo_checkin: str, ahora: datetime) -> tuple:
    """
    Calcula el estilo visual de un miembro según su estado y último check-in.
    Devuelve (css_class, badge, texto_estado).
    """
    if estado == "emergencia":
        return "emergency", "emergency", "🚨 EMERGENCIA"

    # Verificar si el check-in es reciente (menos de 2 horas)
    if ultimo_checkin and ultimo_checkin != "Nunca":
        try:
            hora_checkin = datetime.strptime(ultimo_checkin, "%H:%M:%S").replace(
                year=ahora.year, month=ahora.month, day=ahora.day
            )
            diff_minutos = (ahora - hora_checkin).total_seconds() / 60
            if diff_minutos > 120:
                return "warning", "warning", "⚠️ Sin check-in reciente"
        except ValueError:
            pass

    if estado == "ok":
        return "ok", "ok", "✅ Todo bien"
    elif ultimo_checkin == "Nunca":
        return "warning", "warning", "⚠️ Sin check-in"
    else:
        return "ok", "ok", "✅ Activo"


# ═══════════════════════════════════════════════════════════════
# INICIO DEL SERVIDOR
# ═══════════════════════════════════════════════════════════════

_flask_app = None


def start_family_server() -> threading.Thread:
    """
    Inicia el servidor Flask de proyección familiar en un hilo separado.
    Puerto: 8766
    Devuelve el hilo donde corre el servidor.
    """
    global _server_thread, _server_running, _flask_app

    if not FLASK_AVAILABLE:
        logger.error("Flask no está instalado. No se puede iniciar el servidor familiar.")
        speak("Flask no está instalado. No puedo iniciar el servidor familiar.")
        return threading.Thread()

    if _server_running:
        logger.info("El servidor familiar ya está corriendo.")
        return _server_thread

    _flask_app = _create_flask_app()

    def _run():
        global _server_running
        _server_running = True
        try:
            try:
                print(f"\n[FAMILY] Servidor de Proyeccion Familiar iniciado")
                print(f"   Puerto: {_FAMILY_PORT}")
                print(f"   Monitor de Sara: http://localhost:{_FAMILY_PORT}/monitor")
                print(f"   Pagina familiar: http://localhost:{_FAMILY_PORT}/familia/{{nombre}}\n")
            except Exception:
                pass
            _flask_app.run(
                host="0.0.0.0",
                port=_FAMILY_PORT,
                debug=False,
                use_reloader=False,
            )
        except Exception as e:
            logger.error(f"Error en el servidor familiar: {e}")
        finally:
            _server_running = False

    _server_thread = threading.Thread(target=_run, daemon=True, name="KalmiyaFamilyServer")
    _server_thread.start()

    # Esperar brevemente a que el servidor arranque
    time.sleep(1.5)

    log_command("start_family_server", f"puerto {_FAMILY_PORT}")
    speak(f"Servidor familiar de {BOTNAME} iniciado en el puerto {_FAMILY_PORT}.")

    return _server_thread


def set_sara_message(nombre: str, mensaje: str):
    """
    Establece el mensaje de Sara que se mostrará en la página de un miembro.
    """
    _sara_messages[nombre.lower()] = mensaje
    log_command(f"set_sara_message:{nombre}", mensaje)


def get_server_status() -> dict:
    """Devuelve el estado del servidor familiar."""
    return {
        "activo": _server_running,
        "puerto": _FAMILY_PORT,
        "url_monitor": f"http://localhost:{_FAMILY_PORT}/monitor",
        "miembros_con_checkin": len(_checkins),
        "notificaciones_pendientes": sum(len(v) for v in _notifications.values()),
    }


# ═══════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA PARA PRUEBAS
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"🏠 KALMIYA Family Projection — Prueba")
    print(f"   Iniciando servidor en puerto {_FAMILY_PORT}...\n")

    # Registrar algunos miembros de prueba
    try:
        register_family_member("Mamá", {"relacion": "Madre", "telefono": ""})
        register_family_member("Papá", {"relacion": "Padre", "telefono": ""})
    except Exception:
        pass

    # Agregar notificación de prueba
    notify_family_member("Mamá", "KALMIYA está activo y listo para ayudarte.", "info")

    # Mensaje de Sara de prueba
    set_sara_message("Mamá", "Te quiero mucho. Cualquier cosa, escríbeme aquí.")

    # Iniciar servidor
    hilo = start_family_server()

    print(f"\n📱 Páginas disponibles:")
    print(f"   Monitor Sara: http://localhost:{_FAMILY_PORT}/monitor")
    print(f"   Página Mamá:  http://localhost:{_FAMILY_PORT}/familia/mamá")
    print(f"   Página Papá:  http://localhost:{_FAMILY_PORT}/familia/papá")
    print(f"\nPresiona Ctrl+C para detener.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido.")

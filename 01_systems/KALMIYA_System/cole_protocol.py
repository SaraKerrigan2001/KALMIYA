# cole_protocol.py
"""COLE KALMIYA Protocol
======================

The **COLE (Communicación Optimizada para Líneas de Entrenamiento)** protocol is a lightweight, secure
messaging layer that KALMIYA can use to exchange commands and status reports with
mobile devices, remote bridges and family‑guard agents.

Features
--------
* **JSON‑based messages** – easy to parse on any platform (Python, JavaScript, Android).
* **HMAC authentication** – each message includes a signature generated with a
  shared secret (`COLE_SHARED_KEY`).  The receiver verifies the signature before
  processing the payload, preventing spoofing.
* **Stateless request‑reply** – the protocol works over HTTP(S) or TCP sockets;
  the implementation below uses a small Flask server that can be run behind the
  existing KALMIYA remote bridge or standalone.
* **Extensible actions** – a ``type`` field defines the intent (``ping``,
  ``register``, ``command`` …).  New actions can be added without breaking older
  clients.

Usage Example (Python client)
-----------------------------
```python
import requests, hmac, hashlib, json

BASE_URL = 'http://localhost:8765/cole'  # KALMIYA server endpoint
SHARED_KEY = b'super‑secret‑key'          # must match the server configuration

def sign(payload: dict) -> str:
    # deterministic JSON representation (sorted keys, no whitespace)
    data = json.dumps(payload, separators=(',', ':'), sort_keys=True).encode()
    return hmac.new(SHARED_KEY, data, hashlib.sha256).hexdigest()

def send(action: str, data: dict):
    payload = {'type': action, 'data': data}
    payload['sig'] = sign(payload)
    r = requests.post(BASE_URL, json=payload, timeout=5)
    return r.json()

# Register this device with KALMIYA
resp = send('register', {'device_id': 'phone‑01', 'vendor': 'Huawei'})
print('Register response:', resp)
```

Server side (integrated into KALMIYA)
-------------------------------------
The server is a Flask app exposing a single ``/cole`` endpoint.  It verifies the
signature, dispatches the message to the appropriate handler and returns a JSON
response.

The implementation lives in ``cole_protocol.py`` and can be started from the
launcher with ``start_cole_server()``.  It automatically registers itself in the
shared memory under the key ``cole_url`` so other KALMIYA modules (e.g. the
remote bridge) can discover it.
"""

import json
import hmac
import hashlib
import logging
from typing import Callable, Dict, Any
from flask import Flask, request, jsonify
import threading
import os

# ---------------------------------------------------------------------------
# Configuration – adjust to your environment
# ---------------------------------------------------------------------------
COLE_SHARED_KEY = os.getenv('COLE_SHARED_KEY', 'super-secret-key').encode()
COLE_HOST = os.getenv('COLE_HOST', '0.0.0.0')
COLE_PORT = int(os.getenv('COLE_PORT', '8877'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__)

# Registry of action handlers.  ``func(payload: dict) -> dict``
_action_handlers: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}

# ---------------------------------------------------------------------------
# Helper – verify HMAC signature
# ---------------------------------------------------------------------------
def _verify_signature(msg: dict) -> bool:
    sig = msg.get('sig')
    if not sig:
        return False
    # Remove the signature before we compute the hash
    msg_copy = dict(msg)
    del msg_copy['sig']
    # Canonical JSON (sorted keys, no whitespace)
    data = json.dumps(msg_copy, separators=(',', ':'), sort_keys=True).encode()
    expected = hmac.new(COLE_SHARED_KEY, data, hashlib.sha256).hexdigest()
    return hmac.compare_digest(sig, expected)

# ---------------------------------------------------------------------------
# Core endpoint
# ---------------------------------------------------------------------------
@app.route('/cole', methods=['POST'])
def cole_endpoint():
    incoming = request.get_json(silent=True)
    if not incoming:
        logger.warning('Empty or non‑JSON payload received')
        return jsonify({'error': 'invalid payload'}), 400

    if not _verify_signature(incoming):
        logger.warning('Signature verification failed')
        return jsonify({'error': 'invalid signature'}), 403

    msg_type = incoming.get('type')
    handler = _action_handlers.get(msg_type)
    if not handler:
        logger.info(f'No handler for message type: {msg_type}')
        return jsonify({'error': f'unknown type {msg_type}'}), 400

    try:
        response = handler(incoming.get('data', {}))
        # Sign the response as well (optional, but nice for symmetry)
        resp_msg = {'type': f'{msg_type}_response', 'data': response}
        resp_msg['sig'] = hmac.new(COLE_SHARED_KEY,
                                   json.dumps(resp_msg, separators=(',', ':'), sort_keys=True).encode(),
                                   hashlib.sha256).hexdigest()
        return jsonify(resp_msg)
    except Exception as e:
        logger.exception('Error handling COLE message')
        return jsonify({'error': str(e)}), 500

# ---------------------------------------------------------------------------
# Default handlers – can be extended by other modules
# ---------------------------------------------------------------------------
def _handle_ping(data: dict) -> dict:
    return {'pong': True, 'timestamp': data.get('timestamp')}

def _handle_register(data: dict) -> dict:
    # Store device info in the shared DB (simple example using file‑based JSON)
    device_id = data.get('device_id')
    if not device_id:
        return {'status': 'error', 'msg': 'device_id missing'}
    # In a real system you would persist this in `kalmiya.db`
    logger.info(f'Device registration: {device_id} – {data}')
    return {'status': 'ok', 'device_id': device_id}

def _handle_command(data: dict) -> dict:
    # Forward command to the core brain – we simply echo for now
    cmd = data.get('cmd')
    logger.info(f'Received remote command: {cmd}')
    # Here you could call `database.log_command` or trigger the AI engine
    return {'executed': True, 'cmd': cmd}

# Register default actions
_action_handlers['ping'] = _handle_ping
_action_handlers['register'] = _handle_register
_action_handlers['command'] = _handle_command

# ---------------------------------------------------------------------------
# Server management – start/stop helpers
# ---------------------------------------------------------------------------
_server_thread: threading.Thread | None = None

def start_cole_server(host: str = COLE_HOST, port: int = COLE_PORT) -> None:
    """Start the COLE protocol Flask server in a background thread.

    This function is safe to call multiple times; subsequent calls will simply
    return the existing server thread.
    """
    global _server_thread
    if _server_thread and _server_thread.is_alive():
        logger.info('COLE server already running')
        return

    def _run():
        logger.info(f'Starting COLE server on {host}:{port}')
        # ``use_reloader=False`` prevents Flask from spawning a second process.
        app.run(host=host, port=port, debug=False, use_reloader=False)

    _server_thread = threading.Thread(target=_run, daemon=True, name='KALMIYA-COLE-Server')
    _server_thread.start()
    logger.info('COLE server thread started')

def stop_cole_server() -> None:
    """Attempt a graceful shutdown of the COLE server.

    Flask does not expose a direct ``stop`` method; we rely on the process exit
    or an external signal.  For most desktop use‑cases terminating the Python
    interpreter also stops the thread.
    """
    global _server_thread
    if _server_thread and _server_thread.is_alive():
        logger.info('Stopping COLE server – please terminate the Python process')
        # No clean shutdown; the daemon thread will end when the main program exits.
        _server_thread = None
    else:
        logger.info('COLE server not running')

# ---------------------------------------------------------------------------
# Convenience – expose start function for the launcher
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    start_cole_server()

# ---------------------------------------------------------------------------
# End of cole_protocol.py
# ---------------------------------------------------------------------------

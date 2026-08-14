"""
KALMIYA Dashboard Server v3.6
Dashboard visual en tiempo real con Flask + WebSocket
Muestra métricas del sistema, estado de skills, y actividad en vivo
"""

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import psutil
import json
from datetime import datetime
from pathlib import Path
import threading
import time

# Importar módulos de KALMIYA
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kalmiya-dashboard-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Estado global del sistema
system_state = {
    'cpu_percent': 0,
    'memory_percent': 0,
    'disk_percent': 0,
    'uptime': 0,
    'skills_status': {},
    'recent_activities': [],
    'voice_active': False,
    'brain_active': False
}

def get_system_metrics():
    """Obtiene métricas del sistema"""
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent,
        'timestamp': datetime.now().isoformat()
    }

def get_skills_status():
    """Lee estado de skills desde archivos de configuración"""
    skills_dir = Path(__file__).parent.parent.parent.parent / '.skills'
    skills = {}
    
    skill_names = ['metrics', 'bandeja', 'plan', 'tendencias', 'boveda', 
                   'audio', 'biometria', 'seguridad', 'inteligencia']
    
    for skill in skill_names:
        skill_path = skills_dir / skill / 'SKILL.md'
        if skill_path.exists():
            skills[skill] = {
                'name': skill.capitalize(),
                'status': 'active',
                'last_run': 'N/A',
                'path': str(skill_path)
            }
    
    return skills

def get_recent_activities():
    """Lee actividades recientes desde logs"""
    activities = []
    log_path = Path(__file__).parent.parent / 'logs' / 'kalmiya.log'
    
    if log_path.exists():
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[-10:]  # Últimas 10 líneas
                for line in lines:
                    activities.append({
                        'timestamp': datetime.now().isoformat(),
                        'message': line.strip()
                    })
        except:
            pass
    
    return activities

def update_system_state():
    """Actualiza el estado global del sistema"""
    global system_state
    
    while True:
        try:
            # Actualizar métricas
            metrics = get_system_metrics()
            system_state['cpu_percent'] = metrics['cpu_percent']
            system_state['memory_percent'] = metrics['memory_percent']
            system_state['disk_percent'] = metrics['disk_percent']
            
            # Actualizar skills
            system_state['skills_status'] = get_skills_status()
            
            # Actualizar actividades
            system_state['recent_activities'] = get_recent_activities()
            
            # Emitir actualización a todos los clientes conectados
            socketio.emit('system_update', system_state)
            
        except Exception as e:
            print(f"Error actualizando estado: {e}")
        
        time.sleep(2)  # Actualizar cada 2 segundos

@app.route('/')
def index():
    """Página principal del dashboard"""
    return render_template('dashboard.html')

@app.route('/api/status')
def api_status():
    """API endpoint para obtener estado actual"""
    return jsonify(system_state)

@app.route('/api/skills')
def api_skills():
    """API endpoint para obtener estado de skills"""
    return jsonify(system_state['skills_status'])

@socketio.on('connect')
def handle_connect():
    """Cliente conectado"""
    print(f'Cliente conectado: {datetime.now()}')
    emit('system_update', system_state)

@socketio.on('disconnect')
def handle_disconnect():
    """Cliente desconectado"""
    print(f'Cliente desconectado: {datetime.now()}')

@socketio.on('request_update')
def handle_request_update():
    """Cliente solicita actualización manual"""
    emit('system_update', system_state)

def start_dashboard(host='localhost', port=5000):
    """Inicia el servidor del dashboard"""
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           KALMIYA DASHBOARD v3.6 - INICIANDO                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

🌐 Dashboard URL: http://{host}:{port}
📊 Métricas en tiempo real activadas
🔄 Actualización automática cada 2 segundos

Presiona Ctrl+C para detener el servidor
    """)
    
    # Iniciar thread de actualización
    update_thread = threading.Thread(target=update_system_state, daemon=True)
    update_thread.start()
    
    # Iniciar servidor Flask
    socketio.run(app, host=host, port=port, debug=False, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    start_dashboard()

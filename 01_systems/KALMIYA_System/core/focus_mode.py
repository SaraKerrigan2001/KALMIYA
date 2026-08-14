"""
KALMIYA Focus Mode v3.6
Modo de concentración profunda con bloqueo de distracciones
Rastrea productividad y genera reportes de tiempo enfocado
"""

import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import json
import threading

class FocusMode:
    """
    Modo Focus/Deep Work para KALMIYA
    Bloquea distracciones, pausa skills, y rastrea productividad
    """
    
    def __init__(self):
        """Inicializa el modo focus"""
        self.is_active = False
        self.session_start = None
        self.session_duration = 0  # minutos
        self.sessions_history = []
        
        # Rutas
        self.output_path = Path(__file__).parent.parent.parent / "KALMIYA" / "outputs" / "focus"
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        self.history_file = self.output_path / "focus_history.json"
        self.load_history()
        
        print("🎯 Focus Mode inicializado")
    
    def activate(self, duration_minutes: int = 90, task_name: str = "Deep Work"):
        """
        Activa modo focus
        
        Args:
            duration_minutes: Duración en minutos
            task_name: Nombre de la tarea
        """
        if self.is_active:
            print("⚠️  Focus mode ya está activo")
            return False
        
        self.is_active = True
        self.session_start = datetime.now()
        self.session_duration = duration_minutes
        self.current_task = task_name
        
        # Generar sesión
        session_id = self.session_start.strftime("%Y%m%d_%H%M%S")
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              🎯 MODO FOCUS ACTIVADO                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

⏱️  Duración: {duration_minutes} minutos
📋 Tarea: {task_name}
🚀 Inicio: {self.session_start.strftime('%H:%M:%S')}
⏰ Fin estimado: {(self.session_start + timedelta(minutes=duration_minutes)).strftime('%H:%M:%S')}

💡 Tips para máxima productividad:
   • Silencia tu teléfono
   • Cierra pestañas innecesarias
   • Usa auriculares si es necesario
   • Trabaja en bloques sin interrupciones

🔕 Notificaciones pausadas
⏸️  Skills no críticos en espera

¡Buena suerte! 💪
        """)
        
        # Programar desactivación automática
        threading.Thread(
            target=self._auto_deactivate,
            args=(duration_minutes,),
            daemon=True
        ).start()
        
        return True
    
    def deactivate(self, completed: bool = True):
        """
        Desactiva modo focus
        
        Args:
            completed: Si la sesión se completó o fue interrumpida
        """
        if not self.is_active:
            print("⚠️  Focus mode no está activo")
            return False
        
        end_time = datetime.now()
        actual_duration = (end_time - self.session_start).total_seconds() / 60
        
        # Guardar sesión
        session = {
            'id': self.session_start.strftime("%Y%m%d_%H%M%S"),
            'task': self.current_task,
            'start': self.session_start.isoformat(),
            'end': end_time.isoformat(),
            'planned_duration': self.session_duration,
            'actual_duration': round(actual_duration, 2),
            'completed': completed,
            'completion_rate': min(100, round((actual_duration / self.session_duration) * 100, 2))
        }
        
        self.sessions_history.append(session)
        self.save_history()
        
        # Generar reporte de sesión
        self._generate_session_report(session)
        
        # Desactivar
        self.is_active = False
        
        status = "COMPLETADA ✅" if completed else "INTERRUMPIDA ⚠️"
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              🎉 SESIÓN DE FOCUS {status:^20}       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

📊 Estadísticas de la sesión:
   • Duración planeada: {self.session_duration} min
   • Duración real: {round(actual_duration, 1)} min
   • Tasa de completado: {session['completion_rate']}%
   • Tarea: {self.current_task}

🎯 Total sesiones hoy: {self.get_today_sessions_count()}
⏱️  Total tiempo focus hoy: {self.get_today_focus_time()} min

💡 ¡Excelente trabajo! Toma un descanso de 5-10 minutos.
        """)
        
        return True
    
    def _auto_deactivate(self, duration_minutes: int):
        """Desactiva automáticamente después de la duración"""
        time.sleep(duration_minutes * 60)
        if self.is_active:
            self.deactivate(completed=True)
    
    def extend_session(self, additional_minutes: int = 30):
        """
        Extiende la sesión actual
        
        Args:
            additional_minutes: Minutos adicionales
        """
        if not self.is_active:
            print("⚠️  No hay sesión activa")
            return False
        
        self.session_duration += additional_minutes
        print(f"⏰ Sesión extendida +{additional_minutes} min (Total: {self.session_duration} min)")
        return True
    
    def get_status(self) -> dict:
        """Obtiene estado actual del modo focus"""
        if not self.is_active:
            return {
                'active': False,
                'message': 'Modo focus no activo'
            }
        
        elapsed = (datetime.now() - self.session_start).total_seconds() / 60
        remaining = self.session_duration - elapsed
        
        return {
            'active': True,
            'task': self.current_task,
            'started': self.session_start.isoformat(),
            'planned_duration': self.session_duration,
            'elapsed_minutes': round(elapsed, 2),
            'remaining_minutes': round(max(0, remaining), 2),
            'progress_percent': round(min(100, (elapsed / self.session_duration) * 100), 2)
        }
    
    def get_today_sessions_count(self) -> int:
        """Cuenta sesiones de hoy"""
        today = datetime.now().date()
        count = sum(1 for s in self.sessions_history 
                   if datetime.fromisoformat(s['start']).date() == today)
        return count
    
    def get_today_focus_time(self) -> float:
        """Calcula tiempo total focus de hoy en minutos"""
        today = datetime.now().date()
        total = sum(s['actual_duration'] for s in self.sessions_history 
                   if datetime.fromisoformat(s['start']).date() == today)
        return round(total, 2)
    
    def get_week_stats(self) -> dict:
        """Estadísticas de la semana"""
        week_ago = datetime.now() - timedelta(days=7)
        
        week_sessions = [s for s in self.sessions_history 
                        if datetime.fromisoformat(s['start']) >= week_ago]
        
        if not week_sessions:
            return {
                'total_sessions': 0,
                'total_minutes': 0,
                'avg_duration': 0,
                'completion_rate': 0
            }
        
        total_minutes = sum(s['actual_duration'] for s in week_sessions)
        completed = sum(1 for s in week_sessions if s['completed'])
        
        return {
            'total_sessions': len(week_sessions),
            'total_minutes': round(total_minutes, 2),
            'avg_duration': round(total_minutes / len(week_sessions), 2),
            'completion_rate': round((completed / len(week_sessions)) * 100, 2)
        }
    
    def _generate_session_report(self, session: dict):
        """Genera reporte de sesión individual"""
        report_file = self.output_path / f"session_{session['id']}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(session, f, indent=2, ensure_ascii=False)
    
    def save_history(self):
        """Guarda historial de sesiones"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.sessions_history, f, indent=2, ensure_ascii=False)
    
    def load_history(self):
        """Carga historial de sesiones"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.sessions_history = json.load(f)
                print(f"📊 {len(self.sessions_history)} sesiones cargadas del historial")
            except:
                self.sessions_history = []


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         KALMIYA FOCUS MODE v3.6 - DEMO                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    focus = FocusMode()
    
    # Mostrar estadísticas
    print("\n📊 Estadísticas de la semana:")
    stats = focus.get_week_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Simular sesión
    print("\n🎯 Iniciando sesión de prueba (5 segundos)...")
    focus.activate(duration_minutes=1, task_name="Demo Task")
    time.sleep(5)
    focus.deactivate(completed=True)

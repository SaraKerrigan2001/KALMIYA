import datetime
import threading
import time
import ctypes

class DailyActivities:
    def __init__(self):
        self.activities = {}
        self.activity_log = []
        self.is_monitoring = False
        self._monitor_thread = None

    def _get_active_window_title(self):
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buf = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)
            return buf.value
        except Exception:
            return "Desconocido"

    def start_monitoring(self, interval=10):
        """Inicia un hilo en segundo plano para monitorear actividades en tiempo real."""
        if self.is_monitoring:
            return {"status": "info", "message": "El monitoreo ya está activo."}
        
        self.is_monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, args=(interval,), daemon=True)
        self._monitor_thread.start()
        return {"status": "success", "message": "Monitoreo de actividades diarias iniciado."}

    def stop_monitoring(self):
        """Detiene el monitoreo en segundo plano."""
        self.is_monitoring = False
        return {"status": "success", "message": "Monitoreo de actividades detenido."}

    def _monitor_loop(self, interval):
        last_window = ""
        last_time = datetime.datetime.now()

        while self.is_monitoring:
            current_window = self._get_active_window_title()
            
            if current_window and current_window != last_window:
                now = datetime.datetime.now()
                # Registrar el tiempo que pasó en la ventana anterior
                if last_window:
                    duration = (now - last_time).total_seconds()
                    if duration > 5:  # Solo registrar si estuvo más de 5 segundos
                        self.activity_log.append({
                            'window': last_window,
                            'start_time': last_time.strftime("%Y-%m-%d %H:%M:%S"),
                            'end_time': now.strftime("%Y-%m-%d %H:%M:%S"),
                            'duration_seconds': int(duration)
                        })
                
                last_window = current_window
                last_time = now

            time.sleep(interval)

    def get_activity_log(self):
        """Devuelve el registro de actividades monitoreadas automáticamente."""
        return self.activity_log

    def add_activity(self, activity_id, name, time_start, time_end, description=""):
        """Añadir una nueva actividad diaria manual."""
        self.activities[activity_id] = {
            'name': name,
            'time_start': time_start,
            'time_end': time_end,
            'description': description,
            'completed': False,
            'date': datetime.datetime.now().strftime("%Y-%m-%d")
        }
        return {"status": "success", "message": f"Actividad '{name}' añadida con éxito."}

    def get_activities(self, date=None):
        """Obtener las actividades manuales, opcionalmente filtradas por fecha."""
        if not date:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        return [act for act in self.activities.values() if act['date'] == date]

    def complete_activity(self, activity_id):
        """Marcar una actividad manual como completada."""
        if activity_id in self.activities:
            self.activities[activity_id]['completed'] = True
            return {"status": "success", "message": "Actividad completada."}
        return {"status": "error", "message": "Actividad no encontrada."}

    def get_summary(self, date=None):
        """Obtener el resumen de las actividades del día (manuales y automáticas)."""
        activities = self.get_activities(date)
        total = len(activities)
        completed = sum(1 for act in activities if act['completed'])
        
        return {
            'total_manual_activities': total,
            'completed_activities': completed,
            'pending_activities': total - completed,
            'manual_activities': activities,
            'auto_logged_entries': len(self.activity_log),
            'monitoring_active': self.is_monitoring
        }

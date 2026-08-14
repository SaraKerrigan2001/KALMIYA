"""
modules_manager.py — Gestor Central de Módulos KALMIYA
======================================================
Integra y orquesta todos los 41 módulos nuevos de KALMIYA.
Proporciona interfaz unificada para acceder a todas las funcionalidades.
"""

import sys
import os
from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path

# Agregar modules al path
MODULES_DIR = Path(__file__).parent / "modules"
sys.path.insert(0, str(MODULES_DIR))

# ── Importar todos los módulos ─────────────────────────────────────────────────
try:
    from modules import (
        # Productividad
        TODOManager, PomodoroTimer, CalendarSync, EmailIntegration, ReminderSystem,
        # Salud
        HealthTracker, SleepMonitor,
        # Finanzas
        ExpenseTracker, BudgetAnalyzer,
        # Entretenimiento
        MusicPlaylistGenerator, MovieRecommender, GamingMode, PodcastManager, BookRecommender,
        # Aprendizaje
        LanguageLearning, CourseRecommender, ReadingListManager,
        # Viajes
        TripPlanner, NavigationHelper, LocalExplorer, TravelBudget,
        # Hogar Inteligente
        SmartHomeControl, LightManagement, TemperatureControl, DeviceAutomation, EnergyMonitor,
        # Comunicación Avanzada
        MultiLanguageSupport, GestureRecognition, EmotionDetection, TranslationRealTime, ConferenceMode,
        # Análisis
        ActivityReports, PerformanceMetrics, ProductivityStats, WeeklySummaries, CustomDashboards,
        # Integración
        SocialMediaSync, CloudStorageSync, DatabaseBackup, APIConnectors, WebhookSupport,
        # Clima (entretenimiento)
        WeatherIntegration,
        # Sistema y Control
        SystemControl,
        # Estudio ADSO
        ADSOStudyMode,
    )
    MODULES_OK = True
except ImportError as e:
    MODULES_OK = False
    print(f"⚠️  Advertencia: No se pudieron importar todos los módulos: {e}")


class KalmiyaModulesManager:
    """Gestor central para todos los módulos de KALMIYA."""

    def __init__(self):
        self.modules = {}
        self.active_modules = []
        self._init_all_modules()

    def _init_all_modules(self):
        """Inicializa todas las instancias de módulos."""
        if not MODULES_OK:
            print("❌ Error: No se pudieron cargar los módulos")
            return

        # Productividad
        self.modules['todo'] = TODOManager()
        self.modules['pomodoro'] = PomodoroTimer()
        self.modules['calendar'] = CalendarSync()
        self.modules['email'] = EmailIntegration()
        self.modules['reminders'] = ReminderSystem()

        # Salud
        self.modules['health'] = HealthTracker()
        self.modules['sleep'] = SleepMonitor()

        # Finanzas
        self.modules['expenses'] = ExpenseTracker()
        self.modules['budget'] = BudgetAnalyzer()

        # Entretenimiento
        self.modules['music'] = MusicPlaylistGenerator()
        self.modules['movies'] = MovieRecommender()
        self.modules['gaming'] = GamingMode()
        self.modules['podcasts'] = PodcastManager()
        self.modules['books'] = BookRecommender()
        self.modules['weather'] = WeatherIntegration()

        # Aprendizaje
        self.modules['languages'] = LanguageLearning()
        self.modules['courses'] = CourseRecommender()
        self.modules['reading'] = ReadingListManager()

        # Viajes
        self.modules['trips'] = TripPlanner()
        self.modules['navigation'] = NavigationHelper()
        self.modules['local'] = LocalExplorer()
        self.modules['travel_budget'] = TravelBudget()

        # Hogar Inteligente
        self.modules['smarthome'] = SmartHomeControl()
        self.modules['lights'] = LightManagement()
        self.modules['temperature'] = TemperatureControl()
        self.modules['automation'] = DeviceAutomation()
        self.modules['energy'] = EnergyMonitor()

        # Comunicación Avanzada
        self.modules['languages_support'] = MultiLanguageSupport()
        self.modules['gestures'] = GestureRecognition()
        self.modules['emotions'] = EmotionDetection()
        self.modules['translation'] = TranslationRealTime()
        self.modules['conference'] = ConferenceMode()

        # Análisis
        self.modules['activity'] = ActivityReports()
        self.modules['performance'] = PerformanceMetrics()
        self.modules['productivity'] = ProductivityStats()
        self.modules['summaries'] = WeeklySummaries()
        self.modules['dashboards'] = CustomDashboards()

        # Integración
        self.modules['social'] = SocialMediaSync()
        self.modules['cloud'] = CloudStorageSync()
        self.modules['backups'] = DatabaseBackup()
        self.modules['apis'] = APIConnectors()
        self.modules['webhooks'] = WebhookSupport()

        # Sistema y Control
        self.modules['system_control'] = SystemControl()

        # Estudio ADSO
        self.modules['adso_study'] = ADSOStudyMode()

    def get_module(self, module_name: str) -> Optional[Any]:
        """Obtiene una instancia de módulo por nombre."""
        return self.modules.get(module_name)

    def get_all_modules(self) -> Dict[str, Any]:
        """Retorna todos los módulos disponibles."""
        return self.modules.copy()

    def activate_module(self, module_name: str) -> bool:
        """Activa un módulo."""
        if module_name in self.modules and module_name not in self.active_modules:
            self.active_modules.append(module_name)
            return True
        return False

    def deactivate_module(self, module_name: str) -> bool:
        """Desactiva un módulo."""
        if module_name in self.active_modules:
            self.active_modules.remove(module_name)
            return True
        return False

    def list_modules(self) -> List[str]:
        """Lista todos los módulos disponibles."""
        return list(self.modules.keys())

    def list_active_modules(self) -> List[str]:
        """Lista solo los módulos activos."""
        return self.active_modules.copy()

    # ── INTERFAZ DE COMANDOS RÁPIDOS ───────────────────────────────────────────

    def execute_command(self, module_name: str, command: str, *args, **kwargs) -> Any:
        """
        Ejecuta un comando en un módulo.

        Ejemplo:
            manager.execute_command('todo', 'add_todo', 't1', 'Mi tarea', priority='high')
        """
        module = self.get_module(module_name)
        if not module:
            return {'error': f'Módulo {module_name} no encontrado'}

        if not hasattr(module, command):
            return {'error': f'Comando {command} no existe en {module_name}'}

        try:
            method = getattr(module, command)
            result = method(*args, **kwargs)
            return result
        except Exception as e:
            return {'error': f'Error ejecutando {command}: {str(e)}'}

    # ── FUNCIONES DE ACCESO RÁPIDO ────────────────────────────────────────────

    def add_todo(self, task_id: str, task_name: str, priority: str = 'medium'):
        """Agregar tarea TODO."""
        return self.modules['todo'].add_todo(task_id, task_name, priority)

    def start_pomodoro(self, task_name: str):
        """Iniciar sesión Pomodoro."""
        return self.modules['pomodoro'].start_session(task_name)

    def log_expense(self, category: str, amount: float, description: str = ''):
        """Registrar gasto."""
        return self.modules['expenses'].add_expense(category, amount, description)

    def add_reminder(self, reminder_text: str, trigger_time, priority: str = 'normal'):
        """Crear recordatorio."""
        return self.modules['reminders'].set_reminder(reminder_text, trigger_time, priority)

    def log_activity(self, activity_type: str, duration: int, intensity: str = 'moderate'):
        """Registrar actividad física."""
        return self.modules['health'].log_activity(activity_type, duration, intensity)

    def get_weather(self, location: str):
        """Obtener clima actual."""
        return self.modules['weather'].get_current_weather(location)

    def create_playlist(self, playlist_name: str, mood: str = None):
        """Crear lista de reproducción."""
        return self.modules['music'].create_playlist(playlist_name, mood)

    def control_light(self, light_id: str, brightness: int = None, color: str = None):
        """Controlar iluminación."""
        return self.modules['lights'].control_light(light_id, brightness, color)

    def get_module_info(self) -> Dict[str, Any]:
        """Obtiene información sobre los módulos cargados."""
        return {
            'total_modules': len(self.modules),
            'active_modules': len(self.active_modules),
            'modules_list': self.list_modules(),
            'active_list': self.list_active_modules(),
            'timestamp': datetime.now().isoformat()
        }


# Instancia global
_manager = None

def get_manager() -> KalmiyaModulesManager:
    """Obtiene la instancia global del gestor de módulos."""
    global _manager
    if _manager is None:
        _manager = KalmiyaModulesManager()
    return _manager


if __name__ == '__main__':
    # Test
    manager = get_manager()
    print("✅ Gestor de Módulos KALMIYA inicializado")
    print(f"📦 {len(manager.list_modules())} módulos cargados")
    print("\nMódulos disponibles:")
    for mod in sorted(manager.list_modules()):
        print(f"  • {mod}")

"""
kalmiya_functions.py — Funciones KALMIYA Extendidas
===================================================
Integración de todos los 41 módulos con KALMIYA.
Proporciona interfaz natural para usar todas las funciones.
"""

import json
from typing import Any, Dict, Optional
from modules_manager import get_manager

# Referencia al manager
_modules_manager = None

def init_kalmiya_functions():
    """Inicializa el sistema de funciones extendidas."""
    global _modules_manager
    _modules_manager = get_manager()
    return _modules_manager is not None


# ═══════════════════════════════════════════════════════════════════════════════
#  FUNCIONES DE ACCESO PÚBLICO
# ═══════════════════════════════════════════════════════════════════════════════

def open_chat():
    """
    Abre la interfaz de chat interactivo con KALMIYA.

    Returns:
        Dict con estado de la operación
    """
    try:
        from open_chat import open_chat_async
        open_chat_async()
        return {'status': 'success', 'message': 'Chat abierto'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def execute_kalmiya_function(function_name: str, *args, **kwargs) -> Dict[str, Any]:
    """
    Ejecuta una función KALMIYA por nombre.

    Args:
        function_name: Nombre de la función (ej: 'add_todo', 'log_expense', etc)
        *args: Argumentos posicionales
        **kwargs: Argumentos nombrados

    Returns:
        Dict con resultado o error
    """
    if not _modules_manager:
        init_kalmiya_functions()

    # Mapeo de funciones a módulos
    functions = {
        # Chat
        'open_chat': ('chat', 'open'),

        # Productividad
        'add_todo': ('todo', 'add_todo'),
        'get_todos': ('todo', 'get_daily_summary'),
        'start_pomodoro': ('pomodoro', 'start_session'),
        'add_event': ('calendar', 'add_event'),
        'send_email': ('email', 'send_email'),
        'set_reminder': ('reminders', 'set_reminder'),

        # Salud
        'log_activity': ('health', 'log_activity'),
        'log_vitals': ('health', 'log_vital_signs'),
        'log_sleep': ('sleep', 'log_sleep'),
        'analyze_sleep': ('sleep', 'analyze_sleep_patterns'),

        # Finanzas
        'add_expense': ('expenses', 'add_expense'),
        'get_budget_status': ('budget', 'get_budget_status'),
        'set_budget': ('budget', 'set_budget'),

        # Entretenimiento
        'get_weather': ('weather', 'get_current_weather'),
        'create_playlist': ('music', 'create_playlist'),
        'add_movie': ('movies', 'add_to_watchlist'),
        'activate_gaming': ('gaming', 'activate_gaming_mode'),
        'subscribe_podcast': ('podcasts', 'subscribe_podcast'),
        'rate_book': ('books', 'rate_book'),

        # Aprendizaje
        'start_language': ('languages', 'add_language'),
        'get_course_recommendations': ('courses', 'get_recommendations'),
        'add_book_to_read': ('reading', 'add_book'),

        # Modo estudio ADSO
        'add_assignment': ('adso_study', 'add_assignment'),
        'get_pending_assignments': ('adso_study', 'get_pending_assignments'),
        'start_study_session': ('adso_study', 'start_study_session'),
        'complete_study_session': ('adso_study', 'complete_study_session'),
        'get_morning_brief': ('adso_study', 'get_morning_brief'),
        'search_study_notes': ('adso_study', 'search_study_notes'),
        'get_java_question': ('adso_study', 'get_java_question'),
        'get_java_exercise': ('adso_study', 'get_java_exercise'),
        'evaluate_java_code': ('adso_study', 'evaluate_java_code'),
        'get_study_status': ('adso_study', 'get_study_status'),

        # Viajes
        'create_trip': ('trips', 'create_trip'),
        'get_directions': ('navigation', 'get_directions'),
        'discover_places': ('local', 'discover_places'),
        'set_trip_budget': ('travel_budget', 'set_budget'),

        # Hogar Inteligente
        'add_device': ('smarthome', 'add_device'),
        'control_light': ('lights', 'control_light'),
        'set_temperature': ('temperature', 'set_temperature'),
        'create_automation': ('automation', 'create_automation'),
        'get_energy_status': ('energy', 'get_consumption_status'),

        # Comunicación
        'set_language': ('languages_support', 'set_interface_language'),
        'detect_emotion': ('emotions', 'detect_emotion'),
        'translate': ('translation', 'translate_text_realtime'),
        'start_conference': ('conference', 'start_conference'),

        # Análisis
        'generate_activity_report': ('activity', 'get_daily_report'),
        'set_performance_metric': ('performance', 'set_metric'),
        'log_work_session': ('productivity', 'log_work_session'),
        'generate_weekly_summary': ('summaries', 'generate_weekly_summary'),
        'create_dashboard': ('dashboards', 'create_dashboard'),

        # Integración
        'sync_social_media': ('social', 'sync_posts'),
        'sync_cloud': ('cloud', 'sync_files'),
        'create_backup': ('backups', 'create_backup'),
        'register_api': ('apis', 'register_api'),
        'register_webhook': ('webhooks', 'register_webhook'),

        # Sistema y Control
        'system_full_access': ('system_control', 'system_full_access'),
        'analyze_local_files': ('system_control', 'analyze_local_files'),
        'admin_functions': ('system_control', 'admin_functions'),
        'monitor_activities': ('system_control', 'monitor_activities'),
        'analyze_network': ('system_control', 'analyze_network'),
        'explore_applications': ('system_control', 'explore_applications'),
    }

    if function_name == 'open_chat':
        return open_chat()

    if function_name not in functions:
        return {'error': f'Función {function_name} no existe'}

    module_name, command = functions[function_name]
    return _modules_manager.execute_command(module_name, command, *args, **kwargs)


def get_available_functions() -> Dict[str, Dict[str, str]]:
    """Retorna todas las funciones disponibles con descripción."""
    functions_desc = {
        'Chat': {
            'open_chat': '💬 Abrir ventana de chat con KALMIYA',
        },
        'Productividad': {
            'add_todo': 'Agregar tarea TODO',
            'get_todos': 'Obtener tareas de hoy',
            'start_pomodoro': 'Iniciar sesión Pomodoro',
            'add_event': 'Agregar evento al calendario',
            'send_email': 'Enviar email',
            'set_reminder': 'Crear recordatorio',
        },
        'Salud': {
            'log_activity': 'Registrar actividad física',
            'log_vitals': 'Registrar signos vitales',
            'log_sleep': 'Registrar sueño',
            'analyze_sleep': 'Analizar patrones de sueño',
        },
        'Finanzas': {
            'add_expense': 'Registrar gasto',
            'get_budget_status': 'Ver estado del presupuesto',
            'set_budget': 'Establecer presupuesto',
        },
        'Entretenimiento': {
            'get_weather': 'Obtener pronóstico del clima',
            'create_playlist': 'Crear lista de reproducción',
            'add_movie': 'Agregar película a watchlist',
            'activate_gaming': 'Activar modo gaming',
            'subscribe_podcast': 'Suscribirse a podcast',
            'rate_book': 'Calificar libro',
        },
        'Aprendizaje': {
            'start_language': 'Iniciar aprendizaje de idioma',
            'get_course_recommendations': 'Obtener recomendaciones de cursos',
            'add_book_to_read': 'Agregar libro a leer',
        },
        'Estudio ADSO': {
            'add_assignment': 'Registrar entrega o actividad ADSO',
            'get_pending_assignments': 'Ver entregas pendientes',
            'start_study_session': 'Iniciar sesión Pomodoro de estudio',
            'complete_study_session': 'Finalizar sesión de estudio',
            'get_morning_brief': 'Resumen matutino de estudio',
            'search_study_notes': 'Buscar apuntes por materia en Obsidian',
            'get_java_question': 'Pregunta teórica de Java',
            'get_java_exercise': 'Ejercicio práctico de Java',
            'evaluate_java_code': 'Evaluar código Java',
            'get_study_status': 'Estado del modo estudio',
        },
        'Viajes': {
            'create_trip': 'Crear plan de viaje',
            'get_directions': 'Obtener direcciones',
            'discover_places': 'Descubrir lugares',
            'set_trip_budget': 'Establecer presupuesto de viaje',
        },
        'Hogar Inteligente': {
            'add_device': 'Agregar dispositivo IoT',
            'control_light': 'Controlar iluminación',
            'set_temperature': 'Ajustar temperatura',
            'create_automation': 'Crear automatización',
            'get_energy_status': 'Ver consumo de energía',
        },
        'Comunicación': {
            'set_language': 'Cambiar idioma de interfaz',
            'detect_emotion': 'Detectar emoción',
            'translate': 'Traducir texto',
            'start_conference': 'Iniciar conferencia',
        },
        'Análisis': {
            'generate_activity_report': 'Generar reporte de actividad',
            'set_performance_metric': 'Establecer métrica de desempeño',
            'log_work_session': 'Registrar sesión de trabajo',
            'generate_weekly_summary': 'Generar resumen semanal',
            'create_dashboard': 'Crear panel personalizado',
        },
        'Integración': {
            'sync_social_media': 'Sincronizar redes sociales',
            'sync_cloud': 'Sincronizar nube',
            'create_backup': 'Crear respaldo',
            'register_api': 'Registrar conexión API',
            'register_webhook': 'Registrar webhook',
        },
        'Sistema y Control': {
            'system_full_access': 'Control total del PC',
            'analyze_local_files': 'Acceso y análisis de archivos locales',
            'admin_functions': 'Funciones de Windows como administrador',
            'monitor_activities': 'Monitoreo continuo de actividades',
            'analyze_network': 'Análisis completo de red local',
            'explore_applications': 'Acceso a programas y juegos',
        },
    }
    return functions_desc


def get_module_status() -> Dict[str, Any]:
    """Obtiene estado de todos los módulos."""
    if not _modules_manager:
        init_kalmiya_functions()

    return _modules_manager.get_module_info()


def list_all_functions() -> list:
    """Lista todas las funciones disponibles."""
    functions_desc = get_available_functions()
    all_functions = []
    for category, functions in functions_desc.items():
        for func_name, description in functions.items():
            all_functions.append({
                'name': func_name,
                'category': category,
                'description': description
            })
    return all_functions


# ═══════════════════════════════════════════════════════════════════════════════
#  INTEGRACIÓN CON BRAIN.PY
# ═══════════════════════════════════════════════════════════════════════════════

def kalmiya_function_help(function_name: str = None) -> str:
    """Proporciona ayuda sobre funciones disponibles."""
    if not function_name:
        functions = list_all_functions()
        return f"KALMIYA tiene {len(functions)} funciones disponibles. Use 'ayuda [función]' para más detalles."

    # Buscar función específica
    for func_info in list_all_functions():
        if func_info['name'] == function_name:
            return f"{func_info['name']}: {func_info['description']} (Categoría: {func_info['category']})"

    return f"Función '{function_name}' no encontrada"


if __name__ == '__main__':
    # Test
    init_kalmiya_functions()
    print("✅ Sistema de Funciones KALMIYA inicializado")
    print(f"\n📦 Funciones disponibles:")
    for func in list_all_functions()[:10]:
        print(f"  • {func['name']}: {func['description']}")
    print(f"... y más ({len(list_all_functions())} total)")

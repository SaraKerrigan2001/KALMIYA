---
title: "Funciones KALMIYA - Guía de Implementación"
tags: [funciones, implementacion, modulos, tutorial]
---

# 🚀 Funciones KALMIYA - Guía de Implementación

[[WELCOME|← Bienvenida]] | [[INDEX|Hub]] | [[KALMIYA_FUNCIONES|Funciones]]

## 📦 Sistema de Módulos Integrado

KALMIYA ahora tiene acceso a **41 funciones nuevas** completamente integradas en el sistema.

### Archivos de Integración:

1. **modules_manager.py** — Gestor central de módulos
2. **kalmiya_functions.py** — Interfaz de funciones
3. **modules/** — 41 módulos implementados

## 🎯 Cómo Usar las Funciones

### Opción 1: Desde Python

```python
from kalmiya_functions import execute_kalmiya_function

# Agregar tarea TODO
result = execute_kalmiya_function('add_todo', 't1', 'Mi tarea', priority='high')

# Registrar gasto
result = execute_kalmiya_function('add_expense', 'comida', 50, 'almuerzo')

# Obtener clima
result = execute_kalmiya_function('get_weather', 'Madrid')
```

### Opción 2: Acceso Directo al Manager

```python
from modules_manager import get_manager

manager = get_manager()

# Ejecutar comando
manager.execute_command('todo', 'add_todo', 't1', 'Tarea importante')

# O usar funciones directas
manager.add_todo('t2', 'Otra tarea', 'high')
manager.log_expense('transporte', 15)
```

### Opción 3: Desde el Chat KALMIYA

```
"KALMIYA, agrega una tarea: Llamar a mamá para el lunes"
"Registra que gasté $50 en comida hoy"
"¿Cuál es el clima en París?"
"Inicia una sesión Pomodoro de 25 minutos"
```

## 📚 Categorías de Funciones Disponibles

### ✅ Productividad (6 funciones)
```
add_todo              - Agregar tarea
get_todos            - Obtener tareas del día
start_pomodoro       - Iniciar Pomodoro
add_event            - Agregar evento
send_email           - Enviar email
set_reminder         - Crear recordatorio
```

### 🏥 Salud (4 funciones)
```
log_activity         - Registrar ejercicio
log_vitals          - Registrar signos vitales
log_sleep           - Registrar sueño
analyze_sleep       - Analizar patrones
```

### 💰 Finanzas (3 funciones)
```
add_expense         - Registrar gasto
get_budget_status   - Ver presupuesto
set_budget          - Establecer límite
```

### 🎬 Entretenimiento (6 funciones)
```
get_weather         - Pronóstico del clima
create_playlist     - Crear música
add_movie           - Agregar película
activate_gaming     - Modo gaming
subscribe_podcast   - Suscribirse podcast
rate_book           - Calificar libro
```

### 📚 Aprendizaje (3 funciones)
```
start_language      - Aprender idioma
get_course_recommendations  - Cursos
add_book_to_read    - Agregar lectura
```

### ✈️ Viajes (4 funciones)
```
create_trip         - Planificar viaje
get_directions      - Obtener rutas
discover_places     - Descubrir lugares
set_trip_budget     - Presupuesto viaje
```

### 🏠 Hogar Inteligente (5 funciones)
```
add_device          - Agregar dispositivo
control_light       - Controlar luces
set_temperature     - Ajustar temperatura
create_automation   - Automatización
get_energy_status   - Ver consumo
```

### 🗣️ Comunicación (4 funciones)
```
set_language        - Cambiar idioma
detect_emotion      - Detectar emoción
translate           - Traducir texto
start_conference    - Conferencia
```

### 📊 Análisis (5 funciones)
```
generate_activity_report  - Reporte actividad
set_performance_metric    - Métrica desempeño
log_work_session          - Sesión trabajo
generate_weekly_summary   - Resumen semanal
create_dashboard          - Panel personal
```

### 🔌 Integración (5 funciones)
```
sync_social_media   - Sincronizar redes
sync_cloud          - Sincronizar nube
create_backup       - Respaldo datos
register_api        - Conectar API
register_webhook    - Webhook
```

### 🖥️ Sistema y Control (6 funciones)
```
system_full_access  - Control total del PC
analyze_local_files - Acceso y análisis de archivos locales
admin_functions     - Funciones de Windows como administrador
monitor_activities  - Monitoreo continuo de actividades (clase/casa)
analyze_network     - Análisis completo de la red local (Ethernet)
explore_applications - Acceso a programas y juegos (Curiosidad activa)
```
*Nota: Se han integrado capacidades que permiten tener el control total del PC, el monitoreo continuo de actividades diarias, análisis avanzado de redes locales (Ethernet), acceso y curiosidad sobre programas y juegos instalados, y la ejecución de funciones de Windows como administrador.*

## 💡 Ejemplos de Uso

### Ejemplo 1: Gestión de Tareas
```python
from kalmiya_functions import execute_kalmiya_function

# Agregar tarea importante
execute_kalmiya_function('add_todo', 'proyecto_1', 'Terminar proyecto', priority='high')

# Agregar recordatorio
execute_kalmiya_function('set_reminder', 'Revisar proyecto', '2026-06-15 10:00')

# Iniciar Pomodoro
execute_kalmiya_function('start_pomodoro', 'Proyecto importante')
```

### Ejemplo 2: Control de Finanzas
```python
# Registrar gastos
execute_kalmiya_function('add_expense', 'comida', 25.50, 'almuerzo')
execute_kalmiya_function('add_expense', 'transporte', 15, 'taxi')

# Ver presupuesto
result = execute_kalmiya_function('get_budget_status')
print(f"Gastado: ${result['spent']}, Disponible: ${result['remaining']}")
```

### Ejemplo 3: Salud y Bienestar
```python
# Registrar actividad física
execute_kalmiya_function('log_activity', 'correr', 30, 'intenso')

# Registrar sueño
execute_kalmiya_function('log_sleep', '23:00', '08:00', 8)

# Ver análisis
execute_kalmiya_function('analyze_sleep')
```

### Ejemplo 4: Entretenimiento
```python
# Crear playlist por estado de ánimo
execute_kalmiya_function('create_playlist', 'Energía', mood='energético')

# Obtener recomendaciones
execute_kalmiya_function('get_course_recommendations')

# Ver clima
weather = execute_kalmiya_function('get_weather', 'Nueva York')
```

### Ejemplo 5: Sistema y Control
```python
# Analizar la red local (Ethernet)
network_report = execute_kalmiya_function('analyze_network', interface='ethernet')
print(f"Estado de la red: {network_report['status']}")

# Monitorear actividades actuales
execute_kalmiya_function('monitor_activities', mode='continuous')

# Ejecutar diagnóstico del sistema como administrador
execute_kalmiya_function('admin_functions', task='system_diagnostics')
```

## 🔧 Integración en Brain.py

Para integrar estas funciones con KALMIYA AI:

```python
from kalmiya_functions import execute_kalmiya_function, list_all_functions

def ask_kalmiya_with_functions(question: str) -> str:
    """KALMIYA con acceso a funciones."""
    
    # Si pregunta por funciones disponibles
    if 'funciones' in question.lower() or 'qué puedo' in question.lower():
        functions = list_all_functions()
        return f"Tengo {len(functions)} funciones disponibles..."
    
    # Si es un comando de función
    if 'agrega una tarea' in question.lower():
        # Parsear y ejecutar
        return execute_kalmiya_function('add_todo', 'nueva', question)
    
    # Si es un comando de clima
    if 'clima' in question.lower() or 'weather' in question.lower():
        location = extract_location(question)
        return execute_kalmiya_function('get_weather', location)
    
    # ... más comandos
```

## 📊 Estado de Integración

| Componente | Estado | Detalles |
|-----------|--------|---------|
| Módulos | ✅ Creados | 41 módulos implementados |
| Manager | ✅ Activo | modules_manager.py funcional |
| Funciones | ✅ Expuestas | kalmiya_functions.py disponible |
| Chat | ✅ Activo | Acceso directo desde escritorio |
| Brain Gemini | ✅ Activo | gemini-2.5-flash como modelo principal |
| Brain Ollama | ✅ Activo | llama3.2 local |
| Brain Claude | ✅ Listo | API /v1/messages actualizada — falta API key |
| Obsidian | ✅ Conectado | OBSIDIAN_VAULT_PATH configurado en .env |
| Backups | ✅ Activo | _BACKUPS/ con primer backup creado |

## 🔧 Correcciones aplicadas (julio 2026)

- `brain.py` — `gemini-2.5-flash` es ahora el primer modelo
- `brain.py` — Claude migrado a API `/v1/messages` (formato correcto)
- `chat.py` — eliminado loop zombi `while True`
- `chat_launcher.py` — path corregido a `Path(__file__).parent`
- `kalmiya_core.py` — `THOUGHT_INTERVAL` protegido con `threading.Lock()`
- `run_all.py` — rutas corregidas añadiendo `01_systems/`
- `Lanzar_KALMIYA.vbs` — Python corregido a `C:\Python314\python.exe`
- `create_shortcut.vbs` — rutas corregidas añadiendo `01_systems\`
- `.env` — `OBSIDIAN_VAULT_PATH` configurado
- `.obsidian/workspace.json` — abre `WELCOME.md` por defecto
- `.obsidian/app.json` — exclusiones ampliadas
- `pyvenv.cfg` restaurado en `02_infrastructure/`

---

**¡Las funciones están listas para usar!**

[[WELCOME|← Volver]]

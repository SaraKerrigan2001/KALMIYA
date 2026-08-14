---
title: "Guía de Instalación KALMIYA v3.6"
tags: [installation, setup, guide, v3.6]
ubicacion: 06_docs/INSTALACION_V36.md
---

# 📦 Guía de Instalación - KALMIYA v3.6

[[INDEX|← Índice]] | [[README|📄 README]] | [[06_docs/ROADMAP|🗺️ Roadmap]]

Esta guía te ayudará a instalar y configurar todas las nuevas características de KALMIYA v3.6.

---

## 🎯 Nuevas Características v3.6

1. ✅ Dashboard Visual en Tiempo Real
2. ✅ Vector Database (Memoria Semántica)
3. ✅ Integración Google Calendar
4. ✅ Sistema de Configuración Skills
5. ✅ Modo Focus/Deep Work
6. ✅ Sistema de Plugins

---

## 📋 Requisitos

### Sistema
- Windows 10/11
- Python 3.11+
- 8GB RAM mínimo (16GB recomendado)
- 10GB espacio libre en disco

### Dependencias Nuevas

```bash
# Instalar dependencias v3.6
pip install flask flask-socketio python-socketio
pip install chromadb sentence-transformers
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install pyyaml schedule
pip install psutil
```

O instalar todo desde requirements actualizado:

```bash
pip install -r 04_config/requirements_v36.txt
```

---

## 🚀 Instalación Paso a Paso

### 1. Dashboard Visual

#### Instalación
```bash
# Las dependencias ya están incluidas arriba
pip install flask flask-socketio psutil
```

#### Iniciar Dashboard
```bash
python 01_systems\KALMIYA_System\ui\dashboard_server.py
```

#### Acceso
Abre tu navegador en: **http://localhost:5000**

**Características:**
- Métricas del sistema en tiempo real
- Estado de skills visualizado
- Gráficos interactivos
- Actualización automática cada 2 segundos

---

### 2. Vector Database (Memoria Semántica)

#### Instalación
```bash
pip install chromadb sentence-transformers
```

#### Indexar Vault
```bash
cd 01_systems\KALMIYA_System\memory
python vector_store.py
```

Esto indexará todo el contenido del vault en `01_systems/KALMIYA/wiki/`

#### Uso desde Python
```python
from memory.vector_store import KalmiyaVectorStore

# Inicializar
store = KalmiyaVectorStore("c:\\Users\\maria\\env\\01_systems\\KALMIYA")

# Buscar
results = store.search("¿Qué es KALMIYA?", n_results=5)

# Hacer pregunta con contexto
answer = store.ask("¿Qué módulos tiene KALMIYA?")
print(answer)
```

---

### 3. Google Calendar Sync

#### Configuración Inicial

**Paso 1: Crear Proyecto en Google Cloud**

1. Ve a: https://console.cloud.google.com/
2. Crea un proyecto nuevo (ej: "KALMIYA-Calendar")
3. Habilita **Google Calendar API**
4. Ve a "Credenciales" → "Crear credenciales" → "ID de cliente de OAuth 2.0"
5. Tipo de aplicación: "Aplicación de escritorio"
6. Descarga el archivo JSON

**Paso 2: Configurar Credenciales**

1. Renombra el archivo descargado a `credentials.json`
2. Cópialo a: `01_systems/KALMIYA_System/config/credentials.json`

**Paso 3: Primera Autenticación**

```bash
cd 01_systems\KALMIYA_System\integrations
python calendar_sync.py
```

Se abrirá un navegador para autorizar el acceso. Después del primer uso, las credenciales se guardan en `token.pickle`.

#### Uso
```python
from integrations.calendar_sync import CalendarSync

# Inicializar
sync = CalendarSync()

# Obtener eventos de hoy
today_events = sync.get_todays_events()

# Sincronizar al vault
sync.sync_to_vault()

# Obtener prioridades para skill Plan
priorities = sync.get_priorities_for_plan()
```

---

### 4. Sistema de Configuración Skills

#### Archivo de Configuración

El archivo `.skills/config.yml` ya está creado con configuración predeterminada.

**Personalizar:**
```bash
# Editar configuración
notepad .skills\config.yml
```

**Ejemplo de personalización:**
```yaml
metrics:
  enabled: true
  schedule: "08:00"  # Cambiar hora
  sources:
    - youtube_analytics
    - twitter_api
```

#### Uso desde Python
```python
from core.skill_manager import SkillManager

# Inicializar
manager = SkillManager()

# Verificar si skill está habilitado
if manager.is_skill_enabled('metrics'):
    print("Metrics skill activo")

# Habilitar/deshabilitar skill
manager.disable_skill('bandeja')
manager.enable_skill('plan')

# Iniciar scheduler automático
manager.start_scheduler()
```

---

### 5. Modo Focus/Deep Work

#### Uso desde Python
```python
from core.focus_mode import FocusMode

# Inicializar
focus = FocusMode()

# Activar por 90 minutos
focus.activate(duration_minutes=90, task_name="Implementar Dashboard")

# Obtener estado
status = focus.get_status()
print(f"Progreso: {status['progress_percent']}%")

# Extender sesión
focus.extend_session(additional_minutes=30)

# Desactivar manualmente (o espera a que termine)
focus.deactivate(completed=True)

# Ver estadísticas de la semana
stats = focus.get_week_stats()
print(f"Total focus time: {stats['total_minutes']} min")
```

#### Uso desde Voz (futuro)
```
"KALMIYA, activa modo focus por 2 horas"
"KALMIYA, ¿cuánto tiempo me queda?"
"KALMIYA, extender sesión 30 minutos"
```

---

### 6. Sistema de Plugins

#### Estructura de un Plugin

Crear carpeta: `.plugins/mi_plugin/`

**Archivo: `.plugins/mi_plugin/plugin.py`**
```python
from core.plugin_manager import Plugin

class MiPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = "MiPlugin"
        self.version = "1.0.0"
        self.author = "Tu Nombre"
        self.description = "Descripción del plugin"
    
    def on_load(self):
        print(f"✅ {self.name} cargado")
    
    def on_unload(self):
        print(f"👋 {self.name} descargado")
    
    def on_command(self, command: str, args: list):
        if command == "mi_comando":
            return f"Respuesta del plugin: {args}"
        return None
```

**Archivo: `.plugins/mi_plugin/plugin.json`** (opcional)
```json
{
  "name": "MiPlugin",
  "version": "1.0.0",
  "author": "Tu Nombre",
  "description": "Plugin de ejemplo",
  "dependencies": [],
  "website": "https://github.com/tu-usuario/mi-plugin"
}
```

#### Usar Plugin Manager
```python
from core.plugin_manager import PluginManager

# Inicializar
manager = PluginManager()

# Descubrir plugins
plugins = manager.discover_plugins()
print(f"Plugins encontrados: {plugins}")

# Cargar plugin específico
manager.load_plugin("mi_plugin")

# Cargar todos los plugins
manager.load_all_plugins()

# Ejecutar comando
response = manager.execute_command("mi_comando", ["arg1", "arg2"])

# Hot-reload de un plugin
manager.reload_plugin("mi_plugin")

# Descargar plugin
manager.unload_plugin("mi_plugin")
```

---

## 🔧 Configuración Post-Instalación

### Iniciar Todos los Servicios

**Script de inicio automático:** (crear)

```bash
# start_kalmiya_v36.bat
@echo off
echo Iniciando KALMIYA v3.6...

start "KALMIYA Dashboard" python 01_systems\KALMIYA_System\ui\dashboard_server.py
timeout /t 2

start "Skill Manager" python 01_systems\KALMIYA_System\core\skill_manager.py
timeout /t 2

echo ✅ KALMIYA v3.6 iniciado
echo 📊 Dashboard: http://localhost:5000
pause
```

### Verificar Instalación

```python
# test_v36_installation.py
print("🔍 Verificando instalación KALMIYA v3.6...")

# 1. Dashboard
try:
    from ui.dashboard_server import start_dashboard
    print("✅ Dashboard OK")
except Exception as e:
    print(f"❌ Dashboard: {e}")

# 2. Vector Store
try:
    from memory.vector_store import KalmiyaVectorStore
    print("✅ Vector Store OK")
except Exception as e:
    print(f"❌ Vector Store: {e}")

# 3. Calendar Sync
try:
    from integrations.calendar_sync import CalendarSync
    print("✅ Calendar Sync OK")
except Exception as e:
    print(f"❌ Calendar Sync: {e}")

# 4. Skill Manager
try:
    from core.skill_manager import SkillManager
    print("✅ Skill Manager OK")
except Exception as e:
    print(f"❌ Skill Manager: {e}")

# 5. Focus Mode
try:
    from core.focus_mode import FocusMode
    print("✅ Focus Mode OK")
except Exception as e:
    print(f"❌ Focus Mode: {e}")

# 6. Plugin Manager
try:
    from core.plugin_manager import PluginManager
    print("✅ Plugin Manager OK")
except Exception as e:
    print(f"❌ Plugin Manager: {e}")

print("\n🎉 Verificación completada!")
```

---

## 📚 Próximos Pasos

1. **Explorar Dashboard:**
   - Abre http://localhost:5000
   - Observa métricas en tiempo real
   
2. **Indexar Memoria:**
   - Ejecuta `python vector_store.py`
   - Prueba búsquedas semánticas

3. **Conectar Calendar:**
   - Configura Google Calendar API
   - Sincroniza eventos

4. **Personalizar Skills:**
   - Edita `.skills/config.yml`
   - Ajusta horarios y prioridades

5. **Probar Modo Focus:**
   - Activa sesión de 90 minutos
   - Revisa estadísticas

6. **Crear Plugins:**
   - Desarrolla tu primer plugin
   - Extiende funcionalidades

---

## 🐛 Troubleshooting

### Error: ModuleNotFoundError

```bash
# Reinstalar dependencias
pip install -r 04_config/requirements_v36.txt
```

### Dashboard no carga

```bash
# Verificar puerto
netstat -ano | findstr :5000

# Cambiar puerto si está ocupado
python dashboard_server.py --port 5001
```

### ChromaDB error

```bash
# Limpiar base de datos
rm -rf 01_systems/KALMIYA_System/data/chroma_db
# Reindexar
python vector_store.py
```

### Google Calendar error

- Verifica que `credentials.json` esté en la ubicación correcta
- Elimina `token.pickle` y autentica nuevamente
- Revisa que Calendar API esté habilitada en Google Cloud

---

## 📞 Soporte

**¿Problemas con la instalación?**

- Ver [[06_docs/ISSUES|Issues conocidos]]
- Abrir issue en GitHub
- Consultar [[README|README principal]]

---

[[INDEX|← Volver al índice]] | [[06_docs/ROADMAP|🗺️ Roadmap]] | [[README|📄 README]]

**Versión del documento:** 1.0  
**Última actualización:** 13 de agosto de 2026

# KALMIYA

Proyecto de asistente de escritorio y sistema de IA con documentación, launchers, tests y módulos del sistema.

## Estado del proyecto

- Repositorio principal: KALMIYA
- Rama activa de trabajo: fix/open-chat-paths
- Validación relevante: la prueba real del núcleo pasa en Python 3.13

## Visión general

KALMIYA está compuesto por cuatro capas principales:

- Sistema principal: 01_systems/KALMIYA_System/
- Infraestructura y entorno: 02_infrastructure/
- Lanzadores y accesos rápidos: 03_launchers/
- Configuración y dependencias: 04_config/
- Pruebas y validación: 05_tests/
- Documentación y reportes: 00_docs_*/, 06_docs/, 07_notes/, 08_reports/

## Organización del repositorio

```text
ENV/
├── 00_docs_chat/          # documentación del chat y guías de uso
├── 00_docs_project/       # documentación técnica y de proyecto
├── 00_docs_updates/       # resumenes y actualizaciones
├── 01_systems/            # módulos del sistema y aplicaciones
│   ├── KALMIYA/
│   ├── KALMIYA_System/
│   ├── LLM_Wiki/
│   └── RAPTOR/
├── 02_infrastructure/     # entorno, venv y recursos de infraestructura
├── 03_launchers/          # scripts de arranque y acceso rápido
├── 04_config/             # dependencias y configuración
├── 05_tests/              # pruebas reales del proyecto
├── 06_docs/               # documentación general y arquitectura
├── 07_notes/              # notas de sistema y desarrollo
├── 08_reports/             # reportes y análisis
├── _BACKUPS/
├── _TEMP/
├── _UNUSED/
├── .gitignore
├── .pytest_cache/
├── .skills/
├── .venv/
├── .venv313/
├── 00_ORGANIZACION_PROYECTO.md
├── INDEX.md
├── KALMIYA_DASHBOARD.md
├── LICENSE
├── pytest.ini
├── README.md
├── WELCOME.md
└── Desktop_Files/
```

## Qué mirar primero

1. [00_ORGANIZACION_PROYECTO.md](00_ORGANIZACION_PROYECTO.md) — mapa del repositorio.
2. [INDEX.md](INDEX.md) — índice general de documentación.
3. [WELCOME.md](WELCOME.md) — bienvenida de entrada.
4. [03_launchers/README.md](03_launchers/README.md) — lanzadores importantes.
5. [04_config/requirements.txt](04_config/requirements.txt) — dependencias del entorno.
6. [05_tests/test_open_chat_paths.py](05_tests/test_open_chat_paths.py) — prueba real de validación del núcleo.

## Puntos de entrada del sistema

### Lanzadores principales

- [03_launchers/chat.py](03_launchers/chat.py)
- [03_launchers/chat_simple.py](03_launchers/chat_simple.py)
- [03_launchers/chat_ultra.py](03_launchers/chat_ultra.py)
- [03_launchers/chat_optimized.py](03_launchers/chat_optimized.py)
- [03_launchers/start_chat.py](03_launchers/start_chat.py)

### Sistema principal

- [01_systems/KALMIYA_System/main.py](01_systems/KALMIYA_System/main.py)
- [01_systems/KALMIYA_System/ui/](01_systems/KALMIYA_System/ui/)
- [01_systems/KALMIYA_System/intelligence/](01_systems/KALMIYA_System/intelligence/)

## Validación actual

La validación mínima del núcleo del proyecto quedo verificada con:

```bash
cd /c/Users/maria/env && . .venv313/Scripts/activate && python -m pytest 05_tests/test_open_chat_paths.py -q
```

Resultado verificado:

- 2 passed in 0.41s

## Recomendaciones

- Mantener la documentación principal en [README.md](README.md), [INDEX.md](INDEX.md) y [00_ORGANIZACION_PROYECTO.md](00_ORGANIZACION_PROYECTO.md).
- Usar 00_docs_* y 06_docs/ para documentación detallada.
- Reservar _TEMP, _UNUSED y _BACKUPS para artefactos temporales y no como parte del desarrollo activo.
- Para cambios funcionales, priorizar pruebas reales bajo 05_tests/.

## Siguientes pasos

- Revisar y terminar la limpieza de launchers y scripts de diagnóstico.
- Separar aún más las pruebas reales de los scripts manuales.
- Estabilizar dependencias opcionales del audio, Gmail y módulos avanzados.

### 📜 Opción 3: Con Lanzadores Bat

- `03_launchers\run_kalmiya.bat` — KALMIYA completa
- `03_launchers\Chat_KALMIYA.bat` — Solo chat

---

## 🌟 Primeros Pasos con JARVIS OS v3.6

### 1. Iniciar Dashboard Visual
```powershell
python 01_systems\KALMIYA_System\ui\dashboard_server.py
```
Abre http://localhost:5000 para ver métricas en vivo

### 2. Indexar Memoria Semántica
```powershell
cd 01_systems\KALMIYA_System\memory
python vector_store.py
```
Esto indexa todo el vault con ChromaDB para búsquedas inteligentes

### 3. Configurar Google Calendar (Opcional)
```powershell
# Sigue la guía en:
cat 06_docs\INSTALACION_V36.md
```
Sincroniza eventos automáticamente

### 4. Personalizar Skills
```powershell
# Editar configuración
notepad .skills\config.yml
```
Ajusta horarios, prioridades y comportamiento de cada skill

### 5. Activar Modo Focus
```python
from core.focus_mode import FocusMode
focus = FocusMode()
focus.activate(duration_minutes=90, task_name="Desarrollo")
```
Concentración profunda con tracking de productividad

### 6. Explorar Plugins
```powershell
# Ver plugins disponibles
ls .plugins\
```
Crea tus propios plugins o usa los de la comunidad

### Explorar Skills Clásico
```powershell
# Ver catálogo completo
cat 06_docs\JARVIS_OS\SKILLS_CATALOG.md
```

### Revisar Estructura de Memoria
```powershell
# Navega a la bóveda
ls 01_systems\KALMIYA\raw\      # Datos ingesta
ls 01_systems\KALMIYA\outputs\  # Resultados procesados
ls 01_systems\KALMIYA\wiki\     # Knowledge base
```

### Abrir Obsidian Vault
```powershell
# En Obsidian, abre carpeta:
# C:\Users\maria\env\01_systems\KALMIYA\

# Luego presiona Ctrl+G para ver gráfico de notas
```

---

## 📚 Documentación Completa

### 🆕 v3.6 - Nuevas Características
- [[06_docs/ROADMAP|🗺️ Roadmap]] — Plan de desarrollo v3.6, v3.7, v4.0
- [[06_docs/INSTALACION_V36|📦 Instalación v3.6]] — Guía paso a paso
- [[06_docs/CONEXIONES_OBSIDIAN_COMPLETAS|🔗 Mapa del Grafo]] — Todas las conexiones

### 🌟 JARVIS OS (Lee Primero)
- [[WELCOME|👋 Bienvenida]] — Introducción con instrucciones de inicio
- [[06_docs/JARVIS_OS/README|🚀 Quick Start]] — Guía rápida JARVIS OS
- [[06_docs/JARVIS_OS/SKILLS_CATALOG|📘 Catálogo de Skills]] — Todos los 9 skills detallados
- [[06_docs/JARVIS_OS/IMPLEMENTATION_SUMMARY|📋 Resumen Técnico]] — Before/After y estadísticas
- [[INDEX|📋 Índice Completo]] — Navegación centralizada

### 📖 KALMIYA Original (Documentación Clásica)
- [[KALMIYA_DASHBOARD|📊 Dashboard]] — Estado del sistema en tiempo real
- [[06_docs/CHAT_GUIA|💬 Guía de Chat]] — Comandos y uso
- [[06_docs/KALMIYA_FUNCIONES|⚙️ Funciones Disponibles]] — Referencia completa
- [[06_docs/MODULOS_IMPLEMENTADOS|📦 Módulos]] — Estado de 41 módulos
- [[06_docs/RAPTOR_INTEGRATION|🔒 Seguridad RAPTOR]] — Framework de seguridad
- [[06_docs/OBSIDIAN_SETUP|📔 Obsidian Setup]] — Configuración de bóveda

### 🛠️ Arquitectura & Desarrollo
- [[06_docs/ESTRUCTURA_VISUAL|🗺️ Mapa Visual]] — Diagrama del proyecto
- [[06_docs/MODULOS_IMPLEMENTACION|🔧 Módulos Técnicos]] — Detalles de módulos
- [[06_docs/ISSUES|🐛 Issues & Roadmap]] — Problemas conocidos

---

## 🔧 Configuración Personalizada

### Configuración General (.env)

Crea o edita `.env` en la raíz:

```env
# Usuario & Bot
USER=Sara Kerrigan
BOTNAME=KALMIYA

# JARVIS OS Configuration
PTT_HOTKEY=ctrl+alt+m          # Cambiar hotkey si necesitas
NEURAL_VOICE=es-ES-ElviraNeural

# IA & Modelos
AI_MODE=auto
AI_MODEL=llama3.2
GEMINI_API_KEY=tu_clave_aqui

# Rutas
OBSIDIAN_VAULT_PATH=c:\Users\maria\env\01_systems\KALMIYA

# Features
KALMIYA_ENABLE_WALLPAPER=true
KALMIYA_ENABLE_SERVER=true
KALMIYA_REQUIRE_BIOMETRIC=false  # Cambiar si quieres auth biométrica

# v3.6 Features
DASHBOARD_PORT=5000
ENABLE_WAKE_WORD=true
VECTOR_DB_ENABLED=true
CALENDAR_SYNC_ENABLED=false  # Requiere credentials.json
```

### Configuración de Skills (.skills/config.yml)

```yaml
# Editar horarios y comportamiento de skills
metrics:
  enabled: true
  schedule: "07:00"  # Cambiar hora
  
focus_mode:
  default_duration: 90  # minutos
  pause_skills:
    - bandeja
    - tendencias
```

Ver archivo completo en `.skills/config.yml`

## 🔒 Seguridad & Privacidad

- ✅ **Audio:** Vosk (STT) + pyttsx3 (TTS) → Cero APIs externas
- ✅ **Datos:** Almacenados localmente en disco, no en cloud
- ✅ **Configuración:** Credenciales en `.env` (gitignore)
- ✅ **RAPTOR:** Framework de seguridad integrado
- ✅ **Auditoría:** Sistema de logs para rastrear operaciones

## 💡 Recomendaciones

### Para Empezar
- 📊 Abre el **Dashboard** (http://localhost:5000) para monitoreo en vivo
- 🧠 **Indexa el vault** primero para habilitar búsquedas semánticas
- ⚙️ Personaliza **`.skills/config.yml`** según tus horarios
- 🎯 Prueba el **Modo Focus** para sesiones de trabajo profundo

### Uso Diario
- 🎤 Usa **Wake Word** ("Hey KALMIYA") para manos libres
- ⌨️ O **Push-to-Talk** (Ctrl+Alt+M) para acceso rápido
- 📅 Conecta **Google Calendar** para planificación real
- 🔌 Explora **Plugins** para extender funcionalidades

### Seguridad
- 🔒 Revisa `06_docs/INSTALACION_V36.md` para setup seguro
- **Importante:** No subas credenciales ni archivos sensibles
- 🛡️ RAPTOR audita seguridad automáticamente

## 🤝 Cómo Contribuir

- Clona el repositorio y crea una rama de trabajo:
  ```powershell
  git checkout -b feature/nombre-de-tu-funcion
  ```
- Añade cambios claros y pequeños
- Usa mensajes de commit descriptivos
- Envía un pull request con descripción de los cambios

Revisa [[06_docs/CONTRIBUTING|CONTRIBUTING.md]] para más detalles.

## 📌 Advertencia

El proyecto puede incluir archivos grandes, configuraciones locales y datos personales. Revisa `.gitignore` antes de compartir o clonar el repositorio.

---

## 🎯 Próximos Pasos

1. **Explorar v3.6:** Ver [[06_docs/ROADMAP|Roadmap completo]]
2. **Instalar características nuevas:** Ver [[06_docs/INSTALACION_V36|Guía de instalación]]
3. **Contribuir:** Ver [[06_docs/CONTRIBUTING|Guía de contribución]]
4. **Reportar bugs:** Ver [[06_docs/ISSUES|Issues conocidos]]

---

**KALMIYA v3.6 + JARVIS OS** — Inteligencia de Clase S para Sara Kerrigan  
🌟 *Audio privado. Memoria semántica. Productividad aumentada. Autonomía garantizada.*

**Última actualización:** Agosto 2026 | **Próxima versión:** v3.7 (Q1 2027)

---

[[INDEX|← Índice Principal]] | [[KALMIYA_DASHBOARD|📊 Dashboard]] | [[06_docs/ROADMAP|🗺️ Roadmap]] | [[WELCOME|👋 Bienvenida]] | [[06_docs/CONTRIBUTING|🤝 Contribuir]] | [[06_docs/ISSUES|🐛 Issues]]

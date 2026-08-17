# Índice del proyecto

## Documentación principal

- [README.md](README.md) — visión general del proyecto.
- [WELCOME.md](WELCOME.md) — bienvenida y entrada rápida.
- [00_ORGANIZACION_PROYECTO.md](00_ORGANIZACION_PROYECTO.md) — mapa del repositorio.
- [KALMIYA_DASHBOARD.md](KALMIYA_DASHBOARD.md) — resumen visual del proyecto.

## Carpetas clave

### Documentación

- [00_docs_chat/](00_docs_chat/)
- [00_docs_updates/](00_docs_updates/)
- [06_docs/](06_docs/)
- [07_notes/](07_notes/)
- [08_reports/](08_reports/)

### Sistema

- [01_systems/KALMIYA_System/](01_systems/KALMIYA_System/)
- [01_systems/KALMIYA/](01_systems/KALMIYA/)
- [01_systems/RAPTOR/](01_systems/RAPTOR/)
- [01_systems/LLM_Wiki/](01_systems/LLM_Wiki/)

### Infraestructura y configuración

- [02_infrastructure/](02_infrastructure/)
- [03_launchers/](03_launchers/)
- [04_config/](04_config/)
- [04_config/requirements.txt](04_config/requirements.txt)

### Validación

- [05_tests/](05_tests/)
- [05_tests/test_open_chat_paths.py](05_tests/test_open_chat_paths.py)
- [pytest.ini](pytest.ini)

## Puntos de entrada

- [03_launchers/chat.py](03_launchers/chat.py)
- [03_launchers/chat_simple.py](03_launchers/chat_simple.py)
- [03_launchers/chat_ultra.py](03_launchers/chat_ultra.py)
- [03_launchers/chat_optimized.py](03_launchers/chat_optimized.py)
- [01_systems/KALMIYA_System/main.py](01_systems/KALMIYA_System/main.py)

## Estado actual

- El núcleo del proyecto ya está validado con la prueba real del prompt.
- Las dependencias opcionales de audio y Google se manejan como componentes no bloqueantes para la importación principal.

## Sugerencia de lectura

1. [README.md](README.md)
2. [00_ORGANIZACION_PROYECTO.md](00_ORGANIZACION_PROYECTO.md)
3. [03_launchers/README.md](03_launchers/README.md)
4. [05_tests/test_open_chat_paths.py](05_tests/test_open_chat_paths.py)
5. [06_docs/](06_docs/)
| Solo chat IA | Ícono **"KALMIYA Chat"** en escritorio |
| Chat desde raíz | `python 03_launchers/chat.py` |
| Chat con consola | `03_launchers/Chat_KALMIYA.bat` |
| Menú completo | `python 01_systems/KALMIYA_System/main.py` |
| Solo núcleo voz | `python 01_systems/KALMIYA_System/kalmiya_core.py` |
| Módulos extendidos | Opción **M** en el menú |
| Backup datos | Opción **R2** en módulos |
| Pruebas | `python 05_tests/test_modules.py` |
| Modo estudio ADSO | `python 03_launchers/estudio_adso.py` |

---

## 📚 Modo Estudio ADSO

Programa: **3115418 ADSO 201** — Análisis y Desarrollo de Software

| Acción | Comando / función |
|--------|-------------------|
| Resumen matutino | `get_morning_brief` |
| Registrar entrega | `add_assignment` |
| Iniciar Pomodoro | `start_study_session` |
| Pregunta Java | `get_java_question` |
| Buscar apuntes | `search_study_notes` |

Desde chat: *"KALMIYA, inicia sesión de estudio de Java"* o *"¿Qué entregas tengo pendientes?"*

---

## 🏗️ Estructura de Carpetas - Resumen

| Carpeta | Función | Enlace |
|---------|---------|--------|
| `.skills/` | 9 skills centralizados de JARVIS OS | — |
| `01_systems/` | Motor principal + módulos | [[01_systems/README\|📖 README]] |
| `02_infrastructure/` | Entorno Python + dependencias | [[02_infrastructure/README\|📖 README]] |
| `03_launchers/` | Scripts de inicio rápido | [[03_launchers/README\|📖 README]] |
| `04_config/` | Configuración Python | [[04_config/README\|📖 README]] |
| `05_tests/` | Tests y validación | [[05_tests/README\|📖 README]] |
| `06_docs/` | Documentación completa | [[06_docs/ROOT_STRUCTURE\|📖 README]] |
| `07_notes/` | Notas del sistema | [[07_notes/README\|📖 README]] |
| `08_reports/` | Reportes y análisis | [[08_reports/README\|📖 README]] |
| `09_diagnostics/` | Scripts de diagnóstico | — |
| `_BACKUPS/` | Copias de seguridad | [[_BACKUPS/README\|📖 README]] |
| `_TEMP/` | Archivos temporales | [[_TEMP/README\|📖 README]] |
| `_UNUSED/` | Scripts obsoletos | [[_UNUSED/README\|📖 README]] |

---

## 🔑 Configuración (.env)

```env
# Usuario
USER=Sara Kerrigan
BOTNAME=KALMIYA

# IA
AI_MODE=auto
AI_MODEL=llama3.2
GEMINI_API_KEY=✅ configurada

# JARVIS OS (Nuevo)
PTT_HOTKEY=ctrl+alt+m
NEURAL_VOICE=es-ES-ElviraNeural

# Rutas
OBSIDIAN_VAULT_PATH=c:\Users\maria\env

# Características
KALMIYA_ENABLE_WALLPAPER=true
KALMIYA_ENABLE_SERVER=true
```

---

## ✨ Resumen - JARVIS OS Integration

**Status**: ✅ Completado (8/8 tareas)

- ✅ Estructura de skills centralizada (.skills/)
- ✅ Audio 100% privado (Vosk + pyttsx3)
- ✅ Push-to-Talk global (Ctrl+Alt+M)
- ✅ Memoria organizada (raw/outputs/wiki)
- ✅ Karpaty Graph configurado
- ✅ Documentación completa
- ✅ Privacidad garantizada
- ✅ Listo para producción

**Comenzar**: [[06_docs/JARVIS_OS/README|🌟 JARVIS OS README]]

---

**Ver gráfico de notas:** `Ctrl+G`

[[WELCOME|← Volver]]

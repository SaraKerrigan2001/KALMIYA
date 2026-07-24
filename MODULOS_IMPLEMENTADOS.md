---
title: "Módulos Implementados"
tags: [modules, kalmiya, implemented, features]
---

# 📦 Módulos Implementados en KALMIYA

[[INDEX|← Índice]] | [[KALMIYA_FUNCIONES|Funciones]] | [[WELCOME|Inicio]]

> Última actualización: julio 2026

---

## ✅ SISTEMA CORE (Activos y funcionando)

### 🧠 Inteligencia y Cerebro
| Módulo | Descripción | Estado |
|--------|-------------|--------|
| `brain.py` | Cerebro triple: Gemini 2.5 Flash + Ollama + Claude | ✅ Activo |
| `intelligence.py` | Análisis avanzado, red, sistema | ✅ Activo |
| `kalmiya_core.py` | Núcleo autónomo v3.0 — piensa solo, THOUGHT_INTERVAL thread-safe | ✅ Activo |

### 💬 Voz y Comunicación
| Módulo | Descripción | Estado |
|--------|-------------|--------|
| `voz.py` | Edge TTS Neural (es-ES-ElviraNeural) + anti-eco | ✅ Activo |
| `kalmiya_hud.py` | HUD flotante 320×620px siempre visible | ✅ Activo |
| `online_ops.py` | Wikipedia, Google, YouTube, WhatsApp, Email | ✅ Activo |

### 💬 Chat
| Módulo | Descripción | Estado |
|--------|-------------|--------|
| `kalmiya_chat.py` | Ventana de chat premium con burbujas y animaciones | ✅ Activo |
| `open_chat.py` | Lanzador del chat en proceso separado | ✅ Activo |
| `chat_launcher.py` | Gestor singleton del chat (path corregido) | ✅ Activo |
| `Lanzar_Chat_KALMIYA.vbs` | Abre el chat directo desde escritorio sin consola | ✅ Activo |

### 🛡️ Seguridad
| Módulo | Descripción | Estado |
|--------|-------------|--------|
| `security_ops.py` | Escaneo red, auditoría, análisis URL | ✅ Activo |
| `cyber_security_ml.py` | ML para detección de amenazas | ✅ Activo |
| `kalmiya_v35_features.py` | Nexus Core v3.5 — seguridad heurística | ✅ Activo |

### 👤 Perfil y Familia
| Módulo | Descripción | Estado |
|--------|-------------|--------|
| `sara_profile.py` | Perfil completo de Sara (redes, cuentas, familia) | ✅ Activo |
| `family_guard.py` | Protección familiar, check-in, alertas | ✅ Activo |
| `family_projection.py` | Páginas web para cada familiar | ✅ Activo |

### 📱 Conectividad
| Módulo | Descripción | Estado |
|--------|-------------|--------|
| `phone_bridge.py` | Puente WiFi PC↔Celular con QR | ✅ Activo |
| `remote_bridge.py` | Cloudflare/Ngrok/Telegram sin WiFi | ✅ Activo |

### 🖥️ Sistema y UI
| Módulo | Descripción | Estado |
|--------|-------------|--------|
| `os_ops.py` | Control del sistema, energía, hardware | ✅ Activo |
| `wallpaper_engine.py` | Fondo de pantalla HUD personalizado | ✅ Activo |
| `splash_screen.py` | Pantalla de arranque fullscreen | ✅ Activo |
| `kalmiya_launcher.py` | Lanzador con permisos de administrador | ✅ Activo |
| `database.py` | SQLite — memoria persistente | ✅ Activo |

---

## ✅ MÓDULOS EXTENDIDOS (41 funciones — Opción M en menú)

Acceso desde el menú principal con la tecla **M**

### 📋 Productividad
| Módulo | Función en KALMIYA |
|--------|-------------------|
| `todo_manager.py` | Gestión de tareas con IA y priorización |
| `pomodoro_timer.py` | Temporizador Pomodoro con voz |
| `calendar_sync.py` | Sincronización de calendario |
| `email_integration.py` | Integración de correo |
| `reminder_system.py` | Recordatorios por voz |

### 💪 Salud
| Módulo | Función en KALMIYA |
|--------|-------------------|
| `health_tracker.py` | Registro de actividad física con análisis IA |
| `sleep_monitor.py` | Análisis y consejos de sueño |

### 💰 Finanzas
| Módulo | Función en KALMIYA |
|--------|-------------------|
| `expense_tracker.py` | Registro de gastos con análisis IA |
| `budget_analyzer.py` | Análisis de presupuesto |

### 🎬 Entretenimiento
| Módulo | Función en KALMIYA |
|--------|-------------------|
| `movie_recommender.py` | Recomendaciones de películas con IA |
| `music_playlist.py` | Playlists personalizadas |
| `book_recommender.py` | Recomendaciones de libros |
| `podcast_manager.py` | Gestión de podcasts |
| `gaming_mode.py` | Modo gaming optimizado |
| `course_recommender.py` | Cursos online recomendados |
| `reading_list.py` | Lista de lecturas pendientes |

### 🌍 Clima y Viajes
| Módulo | Función en KALMIYA |
|--------|-------------------|
| `weather_integration.py` | Clima en tiempo real con consejos IA |
| `trip_planner.py` | Planificación de viajes completa |
| `navigation_helper.py` | Asistencia de navegación |
| `local_explorer.py` | Exploración de lugares locales |
| `travel_budget.py` | Presupuesto de viajes |

### 🗣️ Idiomas
| Módulo | Función en KALMIYA |
|--------|-------------------|
| `multi_language_support.py` | Soporte multiidioma |
| `translation_realtime.py` | Traducción instantánea con IA |
| `language_learning.py` | Lecciones de idiomas personalizadas |
| `emotion_detection.py` | Detección emocional en voz |
| `gesture_recognition.py` | Reconocimiento de gestos |
| `conference_mode.py` | Modo para reuniones |

### 📊 Reportes
| Módulo | Función en KALMIYA |
|--------|-------------------|
| `activity_reports.py` | Reportes de actividad |
| `performance_metrics.py` | Métricas de rendimiento |
| `productivity_stats.py` | Estadísticas de productividad |
| `weekly_summaries.py` | Resúmenes semanales automáticos |
| `custom_dashboards.py` | Paneles personalizados |

### ☁️ Integración
| Módulo | Función en KALMIYA |
|--------|-------------------|
| `social_media_sync.py` | Sincronización redes sociales |
| `cloud_storage_sync.py` | Sincronización en nube |
| `database_backup.py` | Backup automático a `_BACKUPS/` |
| `api_connectors.py` | Conectores a servicios externos |
| `webhook_support.py` | Webhooks personalizados |

### 🏠 Hogar
| Módulo | Función en KALMIYA |
|--------|-------------------|
| `smart_home_control.py` | Control dispositivos IoT |
| `light_management.py` | Gestión de iluminación |
| `temperature_control.py` | Control de temperatura |
| `device_automation.py` | Automatización de dispositivos |
| `energy_monitor.py` | Monitoreo de consumo energético |

---

## 🆕 NUEVAS FUNCIONES (julio 2026)

| Función | Archivo | Descripción |
|---------|---------|-------------|
| `get_full_system_info()` | `os_ops.py` | Info completa del SO, CPU, RAM DDR4/5, disco SSD/HDD, GPU, BIOS, placa base, resolución, IP, MAC |
| `print_full_system_info()` | `os_ops.py` | Muestra en consola y habla un resumen por voz |
| `get_microphone_status()` | `os_ops.py` | Lista micrófonos reales con estado (OK / Error / Unknown) |
| `restore_microphone()` | `os_ops.py` | Restaura micrófono en 3 pasos: habilitar PnP → reiniciar device → actualizar driver |
| Opción 103/104/105 en menú | `main.py` | Sistema completo y micrófono desde el menú principal |
| **`kalmiya_restrictions.py`** | nuevo | **Sistema centralizado de restricciones de seguridad** |
| `check_db_write_permission()` | `kalmiya_restrictions.py` | Verifica si un módulo puede escribir en la BD |
| `check_command_allowed()` | `kalmiya_restrictions.py` | Verifica si un comando del sistema está permitido |
| `check_voice_command_safe()` | `kalmiya_restrictions.py` | Detecta patrones peligrosos en comandos de voz |
| `require_confirmation()` | `kalmiya_restrictions.py` | Pide confirmación al usuario para operaciones críticas |
| `check_rate_limit()` | `kalmiya_restrictions.py` | Límite de operaciones por módulo/minuto |
| `@restricted` decorador | `kalmiya_restrictions.py` | Aplica restricciones automáticamente a cualquier función |
| `get_restrictions_summary()` | `kalmiya_restrictions.py` | Estado completo de todas las restricciones activas |

---

## 🔧 CORRECCIONES Y MEJORAS (julio 2026)

| Cambio | Archivo | Descripción |
|--------|---------|-------------|
| `gemini-2.5-flash` como modelo principal | `brain.py` | Primer modelo en la lista de Gemini |
| API Claude actualizada a `/v1/messages` | `brain.py` | Formato correcto: `x-api-key`, `system`, `content[0][text]` |
| Eliminado loop zombi | `chat.py` | `while True` innecesario removido |
| Path corregido | `chat_launcher.py` | `Path(__file__).parent` en lugar de ruta incorrecta |
| `pyvenv.cfg` restaurado | `02_infrastructure/` | Venv Python 3.14 funciona correctamente |
| Python corregido en VBS | `Lanzar_KALMIYA.vbs` | Usa `C:\Python314\python.exe` |
| Rutas corregidas | `create_shortcut.vbs` | Añadido `01_systems\` en las 3 rutas |
| Primer backup | `_BACKUPS/` | `kalmiya_backup_20260708_172151.db` |
| Rutas corregidas | `run_all.py` | Añadido `01_systems/` a LLM_Wiki y KALMIYA_System |
| Thread-safety | `kalmiya_core.py` | `_thought_interval_lock` protege `THOUGHT_INTERVAL` |
| Vault configurado | `.env` | `OBSIDIAN_VAULT_PATH=c:\Users\maria\env` |
| Workspace mejorado | `.obsidian/workspace.json` | Abre `WELCOME.md` por defecto, historial limpio |
| Exclusiones ampliadas | `.obsidian/app.json` | `02_infrastructure/Lib`, `Scripts`, `_TEMP`, `_UNUSED` excluidos |
| Acceso directo chat | Escritorio | `KALMIYA Chat.lnk` en `D:\OneDrive\Desktop` |

---

## 🚀 CÓMO USAR LOS MÓDULOS

```bash
# Desde el menú principal de KALMIYA
python main.py
# → Escribe "M" y presiona Enter
# → Selecciona la categoría (P1, S2, F1, E3, V1, I1, R1...)
```

```python
# Desde código Python
from modules_integration import kalmiya_weather, kalmiya_todo, kalmiya_recommend

kalmiya_weather("Bogotá")
kalmiya_todo("agregar", "Estudiar Python", "alta")
kalmiya_recommend("pelicula", "acción y ciencia ficción")
```

---

## 📁 ESTRUCTURA DEL PROYECTO

```
c:\Users\maria\env\
├── 01_systems\
│   └── KALMIYA_System\           ← Sistema principal
│       ├── main.py               ← Menú con 100+ opciones + M (módulos)
│       ├── kalmiya_launcher.py   ← Arranca con permisos admin
│       ├── kalmiya_core.py       ← Núcleo autónomo v3.0
│       ├── brain.py              ← Gemini 2.5 Flash + Ollama + Claude
│       ├── kalmiya_chat.py       ← Chat premium con burbujas
│       ├── Lanzar_Chat_KALMIYA.vbs ← Acceso directo al chat
│       ├── modules_integration.py← Integra los 41 módulos con IA real
│       ├── modules\              ← 41 módulos extendidos
│       ├── Lanzar_KALMIYA.vbs    ← Ejecuta como administrador
│       └── .env                  ← Configuración y API keys
├── 02_infrastructure\            ← Entorno virtual Python 3.14
├── 03_launchers\                 ← Lanzadores desde raíz
│   ├── chat.py                   ← Abre el chat directo
│   ├── start_chat.py             ← Lanzador alternativo del chat
│   └── Chat_KALMIYA.bat          ← Lanzador para Windows (.bat)
├── 04_config\                    ← Configuración del paquete
│   ├── pyproject.toml
│   ├── setup.cfg
│   └── requirements.txt
├── 05_tests\                     ← Pruebas del sistema
│   ├── run_all.py                ← CLI unificada
│   └── test_modules.py           ← Pruebas de los 41 módulos
├── _BACKUPS\                     ← Backups automáticos de BD
├── _TEMP\                        ← Archivos temporales
├── _UNUSED\                      ← Código archivado
└── (vault Obsidian — .md en raíz)
    ├── WELCOME.md
    ├── INDEX.md
    └── ...
```

---

[[INDEX|← Volver al índice]]

---

## ✅ SISTEMA CORE (Activos y funcionando)

### 🧠 Inteligencia y Cerebro
| Módulo | Descripción | Estado |
|--------|-------------|--------|
| `brain.py` | Cerebro dual Gemini 2.5 Flash + Ollama | ✅ Activo |
| `intelligence.py` | Análisis avanzado, red, sistema | ✅ Activo |
| `kalmiya_core.py` | Núcleo autónomo v3.0 — piensa solo | ✅ Activo |

### 💬 Voz y Comunicación
| Módulo | Descripción | Estado |
|--------|-------------|--------|
| `voz.py` | Edge TTS Neural (es-ES-ElviraNeural) + anti-eco | ✅ Activo |
| `kalmiya_hud.py` | HUD flotante 320×620px siempre visible | ✅ Activo |
| `online_ops.py` | Wikipedia, Google, YouTube, WhatsApp, Email | ✅ Activo |

### 🛡️ Seguridad
| Módulo | Descripción | Estado |
|--------|-------------|--------|
| `security_ops.py` | Escaneo red, auditoría, análisis URL | ✅ Activo |
| `cyber_security_ml.py` | ML para detección de amenazas | ✅ Activo |
| `kalmiya_v35_features.py` | Nexus Core v3.5 — seguridad heurística | ✅ Activo |

### 👤 Perfil y Familia
| Módulo | Descripción | Estado |
|--------|-------------|--------|
| `sara_profile.py` | Perfil completo de Sara (redes, cuentas, familia) | ✅ Activo |
| `family_guard.py` | Protección familiar, check-in, alertas | ✅ Activo |
| `family_projection.py` | Páginas web para cada familiar | ✅ Activo |

### 📱 Conectividad
| Módulo | Descripción | Estado |
|--------|-------------|--------|
| `phone_bridge.py` | Puente WiFi PC↔Celular con QR | ✅ Activo |
| `remote_bridge.py` | Cloudflare/Ngrok/Telegram sin WiFi | ✅ Activo |

### 🖥️ Sistema y UI
| Módulo | Descripción | Estado |
|--------|-------------|--------|
| `os_ops.py` | Control del sistema, energía, hardware | ✅ Activo |
| `wallpaper_engine.py` | Fondo de pantalla HUD personalizado | ✅ Activo |
| `splash_screen.py` | Pantalla de arranque fullscreen | ✅ Activo |
| `kalmiya_launcher.py` | Lanzador con permisos de administrador | ✅ Activo |
| `database.py` | SQLite — memoria persistente | ✅ Activo |

---

## ✅ MÓDULOS EXTENDIDOS (41 funciones — Opción M en menú)

Acceso desde el menú principal con la tecla **M**

### 📋 Productividad
| Módulo | Función en KALMIYA |
|--------|-------------------|
| `todo_manager.py` | Gestión de tareas con IA y priorización |
| `pomodoro_timer.py` | Temporizador Pomodoro con voz |
| `calendar_sync.py` | Sincronización de calendario |
| `email_integration.py` | Integración de correo |
| `reminder_system.py` | Recordatorios por voz |

### 💪 Salud
| Módulo | Función en KALMIYA |
|--------|-------------------|
| `health_tracker.py` | Registro de actividad física con análisis IA |
| `sleep_monitor.py` | Análisis y consejos de sueño |

### 💰 Finanzas
| Módulo | Función en KALMIYA |
|--------|-------------------|
| `expense_tracker.py` | Registro de gastos con análisis IA |
| `budget_analyzer.py` | Análisis de presupuesto |

### 🎬 Entretenimiento
| Módulo | Función en KALMIYA |
|--------|-------------------|
| `movie_recommender.py` | Recomendaciones de películas con IA |
| `music_playlist.py` | Playlists personalizadas |
| `book_recommender.py` | Recomendaciones de libros |
| `podcast_manager.py` | Gestión de podcasts |
| `gaming_mode.py` | Modo gaming optimizado |
| `course_recommender.py` | Cursos online recomendados |
| `reading_list.py` | Lista de lecturas pendientes |

### 🌍 Clima y Viajes
| Módulo | Función en KALMIYA |
|--------|-------------------|
| `weather_integration.py` | Clima en tiempo real con consejos IA |
| `trip_planner.py` | Planificación de viajes completa |
| `navigation_helper.py` | Asistencia de navegación |
| `local_explorer.py` | Exploración de lugares locales |
| `travel_budget.py` | Presupuesto de viajes |

### 🗣️ Idiomas
| Módulo | Función en KALMIYA |
|--------|-------------------|
| `multi_language_support.py` | Soporte multiidioma |
| `translation_realtime.py` | Traducción instantánea con IA |
| `language_learning.py` | Lecciones de idiomas personalizadas |
| `emotion_detection.py` | Detección emocional en voz |
| `gesture_recognition.py` | Reconocimiento de gestos |
| `conference_mode.py` | Modo para reuniones |

### 📊 Reportes
| Módulo | Función en KALMIYA |
|--------|-------------------|
| `activity_reports.py` | Reportes de actividad |
| `performance_metrics.py` | Métricas de rendimiento |
| `productivity_stats.py` | Estadísticas de productividad |
| `weekly_summaries.py` | Resúmenes semanales automáticos |
| `custom_dashboards.py` | Paneles personalizados |

### ☁️ Integración
| Módulo | Función en KALMIYA |
|--------|-------------------|
| `social_media_sync.py` | Sincronización redes sociales |
| `cloud_storage_sync.py` | Sincronización en nube |
| `database_backup.py` | Backup automático a `_BACKUPS/` |
| `api_connectors.py` | Conectores a servicios externos |
| `webhook_support.py` | Webhooks personalizados |

### 🏠 Hogar
| Módulo | Función en KALMIYA |
|--------|-------------------|
| `smart_home_control.py` | Control dispositivos IoT |
| `light_management.py` | Gestión de iluminación |
| `temperature_control.py` | Control de temperatura |
| `device_automation.py` | Automatización de dispositivos |
| `energy_monitor.py` | Monitoreo de consumo energético |

---

## 🚀 CÓMO USAR LOS MÓDULOS

```bash
# Desde el menú principal de KALMIYA
python main.py
# → Escribe "M" y presiona Enter
# → Selecciona la categoría (P1, S2, F1, E3, V1, I1, R1...)
```

```python
# Desde código Python
from modules_integration import kalmiya_weather, kalmiya_todo, kalmiya_recommend

kalmiya_weather("Bogotá")
kalmiya_todo("agregar", "Estudiar Python", "alta")
kalmiya_recommend("pelicula", "acción y ciencia ficción")
```

---

## 📁 ESTRUCTURA DEL PROYECTO

```
c:\Users\maria\env\
├── 01_systems\
│   └── KALMIYA_System\           ← Sistema principal
│       ├── main.py               ← Menú con 100+ opciones + M (módulos)
│       ├── kalmiya_launcher.py   ← Arranca con permisos admin
│       ├── kalmiya_core.py       ← Núcleo autónomo v3.0
│       ├── brain.py              ← Gemini 2.5 + Ollama
│       ├── modules_integration.py← Integra los 41 módulos con IA real
│       ├── modules\              ← 41 módulos extendidos
│       ├── Lanzar_KALMIYA.vbs    ← Ejecuta como administrador
│       └── .env                  ← Configuración y API keys
├── _BACKUPS\                     ← Backups automáticos de BD
└── .obsidian\                    ← Vault de documentación
```

---

[[INDEX|← Volver al índice]]

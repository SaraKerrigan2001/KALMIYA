---
title: "Índice Principal KALMIYA"
tags: [index, master, hub, core]
---

# 🌐 Índice Principal

[[WELCOME|← Bienvenida]] | [[KALMIYA_DASHBOARD|📊 Dashboard]]

> **Sistema activo:** KALMIYA Neural Core v3.0 Autónoma  
> **Cerebro IA:** Gemini 2.5 Flash + Ollama + Claude  
> **Última actualización:** julio 2026

---

## 🤖 KALMIYA System

**Ruta:** `c:\Users\maria\env\01_systems\KALMIYA_System\`

| Componente | Estado |
|------------|--------|
| Núcleo autónomo (piensa solo) | ✅ Activo |
| Cerebro IA triple (Gemini 2.5 + Ollama + Claude) | ✅ Activo |
| HUD flotante | ✅ Activo |
| Chat directo desde escritorio | ✅ Activo |
| Fondo de pantalla personalizado | ✅ Activo |
| Anti-eco de voz | ✅ Activo |
| 41 módulos extendidos | ✅ Integrados (opción M) |
| Protección familiar | ✅ Activo |
| Conexión remota sin WiFi | ✅ Activo |
| Permisos de administrador | ✅ Activo |
| Vault Obsidian conectado a IA | ✅ Activo |
| Backups automáticos | ✅ Activo |

**Arrancar KALMIYA:**
```
Doble clic en: Lanzar_KALMIYA.vbs
Abrir solo chat: "KALMIYA Chat" en el escritorio
O ejecutar:    python kalmiya_launcher.py
```

---

## 📚 Documentación

- [[WELCOME|Bienvenida]]
- [[KALMIYA_DASHBOARD|📊 Dashboard en tiempo real]]
- [[MODULOS_IMPLEMENTADOS|📦 Módulos Implementados (41+)]]
- [[KALMIYA_FUNCIONES|⚙️ Funciones del Sistema]]
- [[FUNCIONES_IMPLEMENTACION|🚀 Implementaciones]]
- [[CHAT_GUIA|💬 Guía de Chat]]
- [[OBSIDIAN_SETUP|🔧 Setup Obsidian]]
- [[CONTRIBUTING|🤝 Cómo Contribuir]]
- [[ISSUES|🐛 Reportar Issues]]

### 🗒️ Notas del Sistema

- [[07_notes/KALMIYA_Biometria_y_Audio|🔒 Biometría y Audio]] — Verificación facial/voz/PIN + perfiles de audio
- [[ESTRUCTURA_VISUAL|🗺️ Estructura Visual]] — Mapa visual del proyecto
- [[08_reports/graphify-out/GRAPH_REPORT|📊 Reporte del Grafo]] — Estado de conexiones del vault
- [[LICENSE|📄 Licencia MIT]] — Términos de uso del proyecto

---

## ⚡ Accesos rápidos

| Acción | Cómo |
|--------|------|
| Iniciar KALMIYA completo | `Lanzar_KALMIYA.vbs` |
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

## 🧹 Mantenimiento del vault

| Recurso | Ubicación canónica |
|---------|-------------------|
| LLM_Wiki | [[01_systems/LLM_Wiki/README\|01_systems/LLM_Wiki/]] |
| Secretos | `01_systems/KALMIYA_System/.env` (ver `.env.example`) |
| Backups BD | `_BACKUPS/` |
| Scripts obsoletos | `_UNUSED/` |

### 🗂️ Infraestructura

- [[02_infrastructure/Scripts/README\|⚙️ Scripts]] — Automatización y utilidades
- [[02_infrastructure/reports/README\|📊 Reports]] — Auditorías y logs
- [[02_infrastructure/scratch/README\|🧪 Scratch]] — Área de experimentación

### 📚 LLM Wiki

- [[01_systems/LLM_Wiki/README\|📚 LLM Wiki]] — Knowledge base integrada
- [[01_systems/LLM_Wiki/schema/SCHEMA\|🎯 Schema]] — Convenciones de la wiki
- [[01_systems/LLM_Wiki/wiki/index\|📑 Wiki Index]] — Índice de páginas
- [[01_systems/LLM_Wiki/wiki/log\|📝 Wiki Log]] — Historial de cambios

### 🏗️ Sistema Principal

- [[01_systems/KALMIYA_System/README\|🤖 KALMIYA System]] — Núcleo principal
- [[01_systems/KALMIYA_System/kalmiya_docs\|📋 Docs técnicos]]
- [[01_systems/KALMIYA_System/standards\|⚙️ Estándares de código]]
- [[01_systems/KALMIYA/README\|📖 KALMIYA Vault]] — Bóveda personal
- [[01_systems/KALMIYA/Bienvenido\|👋 Bienvenido]]
- [[01_systems/KALMIYA/cree un enlace\|🔗 Crear enlace]]

### 📁 Proyecto SENA

- [[06_docs/OneDrive_Docs/GitHub/proyecto_elementos/README\|🏢 Sistema Gestión Bienes]]
- [[06_docs/OneDrive_Docs/GitHub/proyecto_elementos/CHECKLIST_GITHUB\|✅ Checklist GitHub]]
- [[06_docs/OneDrive_Docs/GitHub/proyecto_elementos/INSTRUCCIONES_GITHUB\|📤 Instrucciones GitHub]]
- [[06_docs/OneDrive_Docs/GitHub/proyecto_elementos/examples/README\|💡 Ejemplos de componentes]]

---

## 🔑 Configuración (.env)

```env
USER=Sara Kerrigan
BOTNAME=KALMIYA
AI_MODE=auto
AI_MODEL=llama3.2
GEMINI_API_KEY=✅ configurada
OBSIDIAN_VAULT_PATH=c:\Users\maria\env
KALMIYA_ENABLE_WALLPAPER=true
KALMIYA_ENABLE_SERVER=true
```

---

**Ver gráfico de notas:** `Ctrl+G`

[[WELCOME|← Volver]]

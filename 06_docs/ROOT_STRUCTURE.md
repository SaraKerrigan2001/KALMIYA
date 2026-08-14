---
title: "Estructura Raíz del Proyecto"
tags: [structure, organization, folders]
ubicacion: 06_docs/ROOT_STRUCTURE.md
---

# 🗂️ Estructura General de KALMIYA

[[INDEX|← Índice]] | [[WELCOME|Inicio]] | [[06_docs/ESTRUCTURA_VISUAL|🗺️ Estructura Visual]]

---

## 📁 Directorios Principales

### 01_systems — Sistema Core
Contiene el corazón del proyecto: núcleo del asistente, módulos, lógica de chat, memoria y conocimiento.

- [[01_systems/KALMIYA_System/README|🤖 KALMIYA System]]
- [[01_systems/LLM_Wiki/README|📚 LLM Wiki]]
- [[01_systems/KALMIYA/README|📖 KALMIYA Vault]]

### 02_infrastructure — Infraestructura
Sostiene el entorno de ejecución: virtualenv, dependencias, scripts auxiliares y áreas de prueba.

- [[02_infrastructure/Scripts/README|⚙️ Scripts]]
- [[02_infrastructure/reports/README|📊 Reports]]
- [[02_infrastructure/scratch/README|🧪 Scratch]]

### 03_launchers — Lanzadores
Incluye los lanzadores y accesos rápidos para abrir KALMIYA desde Windows.

- `Lanzar_KALMIYA.vbs` — Inicia sistema completo
- `chat.py` — Abre solo el chat
- `Chat_KALMIYA.bat` — Lanzador alternativo
- `estudio_adso.py` — Modo estudio SENA

### 04_config — Configuración
Centraliza la configuración de Python, dependencias y empaquetado del proyecto.

- `pyproject.toml` — Configuración del paquete
- `setup.cfg` — Setup de instalación
- `requirements.txt` — Dependencias Python

### 05_tests — Pruebas y Validación
Guarda pruebas, auditorías y utilidades de validación del sistema.

- `test_modules.py` — Prueba los 41 módulos
- `test_asi.py` — Prueba módulo ASI
- `run_all.py` — CLI unificada de pruebas

### 06_docs — Documentación
Documentación técnica, de uso y de contribución.

- [[06_docs/MODULOS_IMPLEMENTADOS|📦 Módulos]]
- [[06_docs/KALMIYA_FUNCIONES|⚙️ Funciones]]
- [[06_docs/ASI_IMPLEMENTACION|🧠 ASI]]
- [[06_docs/CHAT_GUIA|💬 Guía Chat]]

### 07_notes — Notas y Referencias
Notas, referencias y contexto relevante del proyecto.

- [[07_notes/KALMIYA_Biometria_y_Audio|🔒 Biometría y Audio]]
- [[07_notes/README|📝 Índice]]

### 08_reports — Reportes y Análisis
Reportes y resultados de análisis o diagnóstico.

- [[08_reports/graphify-out/GRAPH_REPORT|📊 Reporte del Grafo]]
- [[08_reports/README|📈 Índice]]
- `security_reports/` — Auditorías de seguridad

---

## 📄 Archivos Raíz Importantes

**Solo archivos principales permanecen en la raíz:**

| Archivo | Descripción |
|---------|-------------|
| [[README|README.md]] | Portada general del proyecto |
| [[INDEX|INDEX.md]] | Índice principal de navegación |
| [[KALMIYA_DASHBOARD|KALMIYA_DASHBOARD.md]] | Panel de estado del sistema |
| [[LICENSE|LICENSE]] | Licencia MIT del proyecto |

**Archivos organizados en subdirectorios:**

| Archivo | Nueva Ubicación |
|---------|-----------------|
| ROOT_STRUCTURE.md | `06_docs/` (este archivo) |
| PR_BODY.md | `06_docs/` |
| GRAPH_CONNECTIONS.md | `06_docs/` |
| raptor_cli.py | `03_launchers/` |
| test_raptor.py | `05_tests/` |
| pytest_full_output.txt | `08_reports/` |
| full_scan.txt | `08_reports/` |

---

## 🗑️ Directorios Auxiliares

- `_BACKUPS/` — Backups automáticos de la base de datos
- `_TEMP/` — Archivos temporales
- `_UNUSED/` — Código archivado/obsoleto
- `.obsidian/` — Configuración del vault Obsidian
- `.venv/` — Entorno virtual Python

---

[[INDEX|← Volver al índice]] | [[06_docs/ESTRUCTURA_VISUAL|🗺️ Ver estructura visual]]

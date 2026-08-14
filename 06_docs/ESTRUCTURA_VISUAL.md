---
title: "Estructura Visual del Proyecto"
tags: [estructura, mapa, visual, proyecto]
updated: "2026-07-26"
---

# 🗺️ Estructura Visual — KALMIYA

[[INDEX|← Índice]] | [[KALMIYA_DASHBOARD|📊 Dashboard]] | [[08_reports/graphify-out/GRAPH_REPORT|📊 Graph Report]]

> Mapa visual de la organización del proyecto KALMIYA.  
> Para el grafo interactivo de código: `graphify-out/GRAPH_TREE.html`  
> Para el grafo de notas Obsidian: `Ctrl+G`

---

## 📁 Árbol de carpetas

```
c:\Users\maria\env\
│
├── 01_systems\                    ← Código fuente principal
│   ├── KALMIYA_System\            ← Sistema KALMIYA (núcleo)
│   │   ├── main.py                ← Menú principal (100+ opciones)
│   │   ├── kalmiya_core.py        ← Núcleo autónomo v3.0
│   │   ├── brain.py               ← Triple IA: Gemini / Ollama / Claude
│   │   ├── kalmiya_chat.py        ← Chat premium con burbujas
│   │   ├── voz.py                 ← Edge TTS Neural + anti-eco
│   │   ├── kalmiya_hud.py         ← HUD flotante 320×620px
│   │   ├── database.py            ← SQLite: memoria persistente
│   │   ├── kalmiya_restrictions.py← Sistema de restricciones de seguridad
│   │   ├── modules\               ← 50 módulos extendidos (opción M)
│   │   ├── core\                  ← Componentes de núcleo
│   │   ├── ui\                    ← Interfaces gráficas
│   │   ├── utils\                 ← Utilidades compartidas
│   │   ├── services\              ← Servicios externos
│   │   ├── intelligence\          ← Módulos de inteligencia
│   │   └── .env                   ← API keys y configuración
│   ├── KALMIYA\                   ← Vault Obsidian secundario
│   └── LLM_Wiki\                  ← Wiki de modelos LLM
│
├── 02_infrastructure\             ← Entorno virtual Python 3.14
│   ├── .venv\                     ← Dependencias instaladas (26.7 MB)
│   ├── reports\                   ← Auditorías y logs
│   └── scratch\                   ← Experimentación
│
├── 03_launchers\                  ← Scripts de arranque
│   ├── run_kalmiya.bat            ← Lanzador principal
│   ├── Chat_KALMIYA.bat           ← Solo chat
│   ├── Estudio_ADSO.bat           ← Modo estudio
│   └── chat.py / estudio_adso.py  ← Lanzadores Python
│
├── 04_config\                     ← Configuración del paquete
│   ├── requirements.txt           ← 70+ dependencias Python
│   └── pyproject.toml             ← Metadatos del proyecto
│
├── 05_tests\                      ← Pruebas y auditorías (20+ scripts)
│
├── 06_docs\                       ← Documentación del vault Obsidian
│   ├── CHAT_GUIA.md
│   ├── CONTRIBUTING.md
│   ├── ESTRUCTURA_VISUAL.md       ← Este archivo
│   ├── FUNCIONES_IMPLEMENTACION.md
│   ├── ISSUES.md
│   ├── KALMIYA_DASHBOARD.md
│   ├── KALMIYA_FUNCIONES.md
│   ├── LICENSE.md
│   ├── MODULOS_IMPLEMENTADOS.md
│   ├── OBSIDIAN_SETUP.md
│   ├── OPEN_VAULT.md
│   ├── WELCOME.md
│   └── OneDrive_Docs\             ← Documentos de proyectos externos
│       └── GitHub\proyecto_elementos\ ← Proyecto SENA (React + Node + PostgreSQL)
│
├── 07_notes\                      ← Notas del sistema generadas por KALMIYA
│   └── KALMIYA_Biometria_y_Audio.md ← Sistema biométrico y perfiles de audio
│
├── 08_reports\                    ← Reportes y análisis
│   └── graphify-out\              ← Grafo del código (graphifyy)
│       └── GRAPH_REPORT.md        ← Reporte de comunidades y conexiones
│
├── _BACKUPS\                      ← Backups de la BD SQLite (3 snapshots)
├── _TEMP\                         ← Scripts temporales
├── _UNUSED\                       ← Archivos descartados
│
├── INDEX.md                       ← Hub central de navegación (raíz)
├── README.md                      ← Descripción general del proyecto (raíz)
└── LICENSE                        ← Licencia MIT (raíz)
```

---

## 🔄 Flujo del sistema

```
Usuario
   │
   ├─► Voz / Texto ──► kalmiya_core.py ──► brain.py
   │                        │                  │
   │                        ▼                  ▼
   │                   database.py     Gemini / Ollama / Claude
   │                        │
   ├─► Chat GUI ───► kalmiya_chat.py
   │
   └─► Menú CLI ──► main.py ──► módulos (opción M)
                       │
                       └─► voz.py ──► Edge TTS (es-ES-ElviraNeural)
```

---

## 🧠 God Nodes (funciones más conectadas)

| Función | Conexiones | Rol |
|---------|-----------|-----|
| `speak()` | 226 | Salida de voz universal |
| `log_command()` | 120 | Registro de comandos |
| `main()` | 106 | Punto de entrada CLI |
| `ask_kalmiya()` | 58 | Interfaz principal IA |
| `update_memory()` | 55 | Memoria persistente |
| `KALMIYAIntelligence` | 52 | Módulo de inteligencia |
| `process_command()` | 49 | Procesador de comandos |

> Fuente: [[08_reports/graphify-out/GRAPH_REPORT|Graph Report]] — 2454 nodos · 4849 aristas · 178 comunidades

---

## 📊 Estado del vault Obsidian

| Métrica | Valor |
|---------|-------|
| Nodos totales en el grafo | 2454 |
| Aristas | 4849 |
| Comunidades detectadas | 178 |
| Ciclos de importación | ✅ Ninguno |
| Nodos aislados | 59 (principalmente config JSON) |

---

[[INDEX|← Volver al Índice]] | [[KALMIYA_DASHBOARD|📊 Dashboard]] | [[MODULOS_IMPLEMENTADOS|📦 Módulos]] | [[08_reports/graphify-out/GRAPH_REPORT|📊 Graph Report]]

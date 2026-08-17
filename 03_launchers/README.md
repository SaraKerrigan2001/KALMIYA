---
title: "03_launchers — Lanzadores"
tags: [launchers, scripts, shortcuts]
---

# 03_launchers — Lanzadores y Accesos Rápidos

[[INDEX|← Índice]] | [[README|📄 README Principal]] | [[06_docs/ROOT_STRUCTURE|🗂️ Estructura]]

Aquí están los scripts que permiten arrancar KALMIYA y abrir sus modos principales de forma rápida.

## Launcher principal del Chat

Todos los modos del chat se unifican en un solo launcher:

```powershell
python chat_kalmiya.py                    # Chat estándar
python chat_kalmiya.py --mode simple      # Chat tkinter puro
python chat_kalmiya.py --mode optimized   # Balance diseño/rendimiento
python chat_kalmiya.py --mode ultra       # Ultra v3.7 (temas, avatar, historial)
python chat_kalmiya.py --mode v2          # Diseño futurista
python chat_kalmiya.py --mode ultra -d    # Modo debug (diagnóstico paso a paso)
python chat_kalmiya.py --list             # Listar modos disponibles
```

## Scripts .bat (acceso rápido)

- **Chat_KALMIYA.bat**: inicia el chat estándar (usa `chat_kalmiya.py --mode default`)
- **Chat_KALMIYA_Optimizado.bat**: chat optimizado (usa `chat_kalmiya.py --mode optimized`)
- **run_kalmiya.bat**: lanza el sistema completo
- **ABRIR_OBSIDIAN.bat**: acceso rápido a la bóveda de Obsidian

## Otros scripts

- **raptor_cli.py**: CLI de RAPTOR (seguridad)
- **estudio_adso.py**: modo de estudio y organización para ADSO
- **vision_demo.py**: demostración del sistema de visión

## Uso rápido

- Para abrir solo el chat, usa `Chat_KALMIYA.bat` o `python chat_kalmiya.py`.
- Para RAPTOR, ejecuta `python raptor_cli.py`.
- Para arrancar el sistema completo, usa `run_kalmiya.bat`.
- Para trabajo educativo, usa `estudio_adso.py`.

---

[[INDEX|← Volver al índice]]

# KALMIYA

[[INDEX|← Índice]] | [[KALMIYA_DASHBOARD|📊 Dashboard]] | [[WELCOME|👋 Bienvenida]] | [[CONTRIBUTING|🤝 Contribuir]] | [[LICENSE|📄 Licencia]]

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Build](https://github.com/SaraKerrigan2001/KALMIYA/actions/workflows/ci.yml/badge.svg)](https://github.com/SaraKerrigan2001/KALMIYA/actions/workflows/ci.yml) [![Issues](https://img.shields.io/github/issues/SaraKerrigan2001/KALMIYA)](https://github.com/SaraKerrigan2001/KALMIYA/issues) [![Repo Size](https://img.shields.io/github/repo-size/SaraKerrigan2001/KALMIYA)](https://github.com/SaraKerrigan2001/KALMIYA)

KALMIYA es un asistente autónomo de escritorio desarrollado por Sara Kerrigan. Colombiana IA local y en la nube, síntesis y reconocimiento de voz, control de audio, automatización del sistema y soporte para múltiples dispositivos.

## 🚀 Qué hace KALMIYA

- Chat con IA y asistente de voz en Windows
- Modo silencioso y control de audio
- Reconocimiento de órdenes por voz y comandos de texto
- Módulos de seguridad, productividad, hogar inteligente, finanzas y entretenimiento
- Integración con teléfono móvil, Telegram y servicios en línea
- Registro de memoria y auditoría de comandos
- **🔒 RAPTOR Integration** — Framework autónomo de seguridad ofensiva/defensiva

## 🧩 Estructura del repositorio

- `01_systems/` — Código principal de KALMIYA y módulos del asistente
  - `RAPTOR/` — Framework de seguridad autónomo (submódulo de Git)
- `02_infrastructure/` — Entorno virtual, dependencias y archivos de infraestructura
- `03_launchers/` — Scripts para iniciar el asistente rápidamente
- `04_config/` — Configuración de Python, dependencias y empaquetado
- `05_tests/` — Pruebas, auditorías y utilidades de verificación
- `06_docs/` — Documentación incluyendo [[RAPTOR_INTEGRATION|🔒 Guía RAPTOR]]

## 🛠️ Requisitos

- Windows 10/11
- Python 3.11+ recomendado
- Entorno virtual de Python (opcional pero recomendado)
- Altavoz y micrófono configurados en Windows para voz activa

## 📥 Instalación rápida

```powershell
cd C:\Users\maria\env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r 04_config\requirements.txt
```

> Si ya tienes un entorno, asegúrate de usar `python` desde el intérprete correcto.

## ▶️ Cómo iniciar KALMIYA

### Opción 1: desde PowerShell

```powershell
cd C:\Users\maria\env
python 01_systems\KALMIYA_System\main.py
```

> Nota: KALMIYA puede requerir verificación biométrica al inicio.
> Ajusta `KALMIYA_REQUIRE_BIOMETRIC=false` en el entorno si necesitas iniciar sin autenticación.

### Opción 2: con el lanzador

- Ejecuta `03_launchers\run_kalmiya.bat`
- O bien usa `Chat_KALMIYA.bat` para iniciar sólo el chat

## 📚 Documentación útil

- [[WELCOME]] — Guía de bienvenida y arranque
- [[CHAT_GUIA]] — Comandos y uso del chat
- [[KALMIYA_FUNCIONES]] — Funciones disponibles en el asistente
- [[MODULOS_IMPLEMENTADOS]] — Módulos instalados y estado del proyecto
- [[RAPTOR_INTEGRATION]] — 🔒 Guía de seguridad con RAPTOR
- [[OBSIDIAN_SETUP]] — Integración con Obsidian
- [[ISSUES]] — Cómo reportar bugs e ideas
- [[CONTRIBUTING]] — Cómo contribuir al proyecto
- [[ESTRUCTURA_VISUAL]] — Mapa visual del proyecto

## 🔧 Configuración de voz

- `01_systems/KALMIYA_System/voz.py` controla la síntesis y el modo silencioso
- Para desactivar temporalmente la voz, se usa la memoria interna `voice_enabled=false`

## 💡 Recomendaciones

- Usa el modo silencioso si no quieres salida de audio mientras pruebas
- Guarda y revisa `KALMIYA_DASHBOARD.md` para ver el estado del sistema
- Asegúrate de no subir credenciales ni archivos sensibles al repositorio

## 🤝 Cómo contribuir

- Clona el repositorio y crea una rama de trabajo:
  
```powershell
git clone https://github.com/SaraKerrigan2001/KALMIYA.git
```

- Añade cambios claros y pequeños
- Usa mensajes de commit descriptivos
- Envía un pull request con descripción de los cambios

## 📌 Advertencia

El proyecto puede incluir archivos grandes, configuraciones locales y datos personales. Revisa `.gitignore` antes de compartir o clonar el repositorio.

---

[[INDEX|← Índice Principal]] | [[KALMIYA_DASHBOARD|📊 Dashboard]] | [[WELCOME|👋 Bienvenida]] | [[CONTRIBUTING|🤝 Contribuir]] | [[ISSUES|🐛 Issues]]

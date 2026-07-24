# KALMIYA

KALMIYA es un asistente autónomo de escritorio desarrollado por Sara Kerrigan. Combina IA local y en la nube, síntesis y reconocimiento de voz, control de audio, automatización del sistema y soporte para múltiples dispositivos.

## 🚀 Qué hace KALMIYA

- Chat con IA y asistente de voz en Windows
- Modo silencioso y control de audio
- Reconocimiento de órdenes por voz y comandos de texto
- Módulos de seguridad, productividad, hogar inteligente, finanzas y entretenimiento
- Integración con teléfono móvil, Telegram y servicios en línea
- Registro de memoria y auditoría de comandos

## 🧩 Estructura del repositorio

- `01_systems/` — Código principal de KALMIYA y módulos del asistente
- `02_infrastructure/` — Entorno virtual, dependencias y archivos de infraestructura
- `03_launchers/` — Scripts para iniciar el asistente rápidamente
- `04_config/` — Configuración de Python, dependencias y empaquetado
- `05_tests/` — Pruebas, auditorías y utilidades de verificación

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

### Opción 2: con el lanzador

- Ejecuta `03_launchers\run_kalmiya.bat`
- O bien usa `Chat_KALMIYA.bat` para iniciar sólo el chat

## 📚 Documentación útil

- `WELCOME.md` — Guía de bienvenida y arranque
- `CHAT_GUIA.md` — Comandos y uso del chat
- `KALMIYA_FUNCIONES.md` — Funciones disponibles en el asistente
- `MODULOS_IMPLEMENTADOS.md` — Módulos instalados y estado del proyecto
- `OBSIDIAN_SETUP.md` — Integración con Obsidian

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
git checkout -b feature/nombre-de-tu-funcion
```
- Añade cambios claros y pequeños
- Usa mensajes de commit descriptivos
- Envía un pull request con descripción de los cambios

## 📌 Advertencia

El proyecto puede incluir archivos grandes, configuraciones locales y datos personales. Revisa `.gitignore` antes de compartir o clonar el repositorio.

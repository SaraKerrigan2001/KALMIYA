# 🔧 KALMIYA - Troubleshooting Guide

[[INDEX|← Índice]] | [[README|📄 README]] | [[06_docs/INSTALACION_V36|📦 Instalación]] | [[06_docs/ROADMAP|🗺️ Roadmap]]

Guía de solución de problemas comunes en KALMIYA v3.6

---

## 📋 Índice

1. [Chat no inicia](#chat-no-inicia)
2. [Problemas de Audio](#problemas-de-audio)
3. [Dashboard no carga](#dashboard-no-carga)
4. [Vector Database errores](#vector-database-errores)
5. [Google Calendar no sincroniza](#google-calendar-no-sincroniza)
6. [Wake Word no detecta](#wake-word-no-detecta)
7. [Problemas de importación](#problemas-de-importación)
8. [Encoding UTF-8](#encoding-utf-8)

---

## 🐛 Problemas Comunes

### Chat no inicia

**Síntoma:** Error al ejecutar `chat.py` o `Chat_KALMIYA.bat`

**Causas posibles:**
1. customtkinter no instalado
2. Problema de encoding UTF-8 en Windows
3. Rutas incorrectas

**Solución:**

```powershell
# 1. Instalar customtkinter
pip install customtkinter

# 2. Verificar Python
python --version
# Debe ser Python 3.8+

# 3. Test rápido
cd c:\Users\maria\env
python TEST_CHAT.py

# 4. Si funciona el test, iniciar chat
python 03_launchers\chat.py
```

**Si aparece error de encoding:**
```
UnicodeEncodeError: 'charmap' codec can't encode character
```

Los archivos `chat.py` y `start_chat.py` ya tienen fix automático:
```python
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
```

---

### Problemas de Audio

**Síntoma:** Timeout al importar KalmiyaCore

```
[AUDIO_LOCAL] Vosk no instalado. Para STT local, instala: pip install vosk pyaudio
Command timed out after 10000ms
```

**Causa:** El módulo de audio intenta cargar Vosk y se queda esperando

**Solución:**

**Opción 1: Instalar Vosk (STT local completo)**
```powershell
pip install vosk pyaudio sounddevice soundfile
```

**Opción 2: Deshabilitar audio local (solo chat texto)**
```python
# En .env agregar:
ENABLE_AUDIO_LOCAL=false
```

**Opción 3: Usar Chat sin cargar KalmiyaCore**
```powershell
# El chat funciona independientemente
python 03_launchers\chat.py
```

**Nota:** El Chat KALMIYA NO requiere audio para funcionar. Usa el módulo `brain.py` directamente.

---

### Dashboard no carga

**Síntoma:** Error 404 o conexión rechazada en http://localhost:5000

**Solución:**

```powershell
# 1. Verificar que Flask esté instalado
pip install flask flask-socketio

# 2. Iniciar dashboard manualmente
cd c:\Users\maria\env\01_systems\KALMIYA_System\ui
python dashboard_server.py

# 3. Verificar puerto en uso
netstat -ano | findstr :5000

# 4. Si el puerto está ocupado, cambiar en dashboard_server.py:
# app.run(port=5001)  # Usar otro puerto
```

**Verificar en navegador:**
- http://localhost:5000
- http://127.0.0.1:5000

---

### Vector Database errores

**Síntoma:** Error al indexar vault o buscar

```
ModuleNotFoundError: No module named 'chromadb'
```

**Solución:**

```powershell
# 1. Instalar ChromaDB
pip install chromadb sentence-transformers

# 2. Indexar vault
cd c:\Users\maria\env\01_systems\KALMIYA_System\memory
python vector_store.py

# 3. Si da error de permisos:
# Ejecutar PowerShell como Administrador
```

**Si el indexado es muy lento:**
- El vault grande puede tardar varios minutos
- ChromaDB crea embeddings para cada archivo
- Progreso se muestra en consola

---

### Google Calendar no sincroniza

**Síntoma:** Error de credenciales o API

**Solución:**

```powershell
# 1. Verificar que credentials.json existe
ls c:\Users\maria\env\01_systems\KALMIYA_System\config\credentials.json

# 2. Si no existe:
# - Ir a https://console.cloud.google.com/
# - Crear proyecto
# - Habilitar Google Calendar API
# - Descargar credentials.json
# - Copiar a config/

# 3. Primera ejecución:
cd c:\Users\maria\env\01_systems\KALMIYA_System\integrations
python calendar_sync.py

# Esto abrirá navegador para autorizar
```

**Nota:** `credentials.json` nunca debe subirse a Git (está en .gitignore)

---

### Wake Word no detecta

**Síntoma:** "Hey KALMIYA" no activa el asistente

**Solución:**

```powershell
# 1. Instalar Pocketsphinx
pip install pocketsphinx SpeechRecognition pyaudio

# 2. Test de micrófono
python -c "import speech_recognition as sr; r = sr.Recognizer(); print('Micrófono OK')"

# 3. Ajustar sensibilidad
# En wake_word.py:
detector = WakeWordDetector(sensitivity=0.7)  # 0.0 a 1.0

# 4. Verificar micrófono es el predeterminado
# Windows > Configuración > Sistema > Sonido > Entrada
```

**Tips:**
- Habla claro y cerca del micrófono
- Reduce ruido ambiente
- Prueba con diferentes sensibilidades
- "KALMIYA" solo también funciona (más corto)

---

### Problemas de importación

**Síntoma:** `ModuleNotFoundError` o `ImportError`

**Solución general:**

```powershell
# 1. Instalar TODAS las dependencias v3.6
pip install -r 04_config\requirements_v36.txt

# 2. Si falla alguna:
pip install <paquete> --upgrade

# 3. Verificar entorno virtual
# Si usas .venv:
.venv\Scripts\activate
pip list  # Ver paquetes instalados

# 4. Reinstalar desde cero
pip uninstall -r 04_config\requirements_v36.txt -y
pip install -r 04_config\requirements_v36.txt
```

**Dependencias críticas:**
```
customtkinter       # Chat UI
flask               # Dashboard
chromadb            # Vector DB
google-api-python-client  # Calendar
pyyaml              # Skills config
pocketsphinx        # Wake Word
```

---

### Encoding UTF-8

**Síntoma:** Emojis no se muestran correctamente en consola Windows

**Solución:**

```powershell
# 1. En PowerShell/CMD antes de ejecutar:
chcp 65001

# 2. O usar el .bat proporcionado:
START_KALMIYA_V36.bat

# 3. Configurar PowerShell permanente:
# Agregar a $PROFILE:
$OutputEncoding = [console]::InputEncoding = [console]::OutputEncoding = New-Object System.Text.UTF8Encoding
```

Los scripts Python ya tienen fix automático para Windows.

---

## 🧪 Scripts de Diagnóstico

### Test Completo
```powershell
python TEST_CHAT.py
```
Verifica:
- Directorios correctos
- Dependencias instaladas
- Importaciones funcionan
- Instancia de chat se crea

### Test Individual por Módulo

**Chat:**
```powershell
python -c "import sys; sys.path.insert(0, '01_systems/KALMIYA_System/ui'); from kalmiya_chat import KalmiyaChat; print('OK')"
```

**Dashboard:**
```powershell
python -c "from flask import Flask; print('OK')"
```

**Vector DB:**
```powershell
python -c "import chromadb; print('OK')"
```

**Calendar:**
```powershell
python -c "from google.oauth2.credentials import Credentials; print('OK')"
```

**Wake Word:**
```powershell
python -c "import pocketsphinx; print('OK')"
```

---

## 📞 Soporte

### Logs del Sistema

Los logs se guardan en:
```
01_systems/KALMIYA_System/logs/
├── kalmiya.log           # Log general
├── skills.log            # Skills execution
├── focus_mode.log        # Focus sessions
└── wake_word_stats.json  # Wake word stats
```

### Información de Debug

```powershell
# Versión de Python
python --version

# Paquetes instalados
pip list > installed_packages.txt

# Estado del sistema
python -c "import psutil; print(f'CPU: {psutil.cpu_percent()}%, RAM: {psutil.virtual_memory().percent}%')"
```

### Reportar Bug

Si encuentras un bug, incluye:
1. Sistema operativo y versión
2. Versión de Python
3. Comando ejecutado
4. Error completo (traceback)
5. Logs relevantes

**GitHub Issues:** https://github.com/SaraKerrigan2001/KALMIYA/issues

---

## ✅ Checklist de Instalación Correcta

- [ ] Python 3.8+ instalado
- [ ] Todas las dependencias instaladas (`pip install -r requirements_v36.txt`)
- [ ] `.env` configurado (opcional, tiene defaults)
- [ ] Chat se abre correctamente (`python 03_launchers/chat.py`)
- [ ] Dashboard carga en http://localhost:5000
- [ ] Vector DB indexado (si se va a usar búsqueda semántica)
- [ ] Google Calendar configurado (si se va a usar)
- [ ] Wake Word funciona (si se va a usar)

---

## 🎯 Tests de Funcionalidad

### Test Chat (Crítico)
```powershell
python TEST_CHAT.py
# Debe mostrar: "TEST COMPLETADO - Chat KALMIYA está listo para usar"
```

### Test Dashboard
```powershell
python 01_systems\KALMIYA_System\ui\dashboard_server.py
# Abrir navegador: http://localhost:5000
# Debe mostrar métricas en vivo
```

### Test Vector DB
```powershell
cd 01_systems\KALMIYA_System\memory
python -c "from vector_store import KalmiyaVectorStore; store = KalmiyaVectorStore('C:/Users/maria/env/01_systems/KALMIYA'); print('OK')"
```

### Test Skills
```powershell
python -c "import yaml; config = yaml.safe_load(open('.skills/config.yml')); print(f'Skills: {len(config.get(\"skills\", []))}')"
```

---

## 💡 Tips de Rendimiento

### Chat lento
- Verificar CPU/RAM en Dashboard
- Cerrar aplicaciones pesadas
- Verificar que Ollama/Gemini responden rápido

### Búsqueda semántica lenta
- Primera búsqueda siempre es lenta (carga modelo)
- Búsquedas siguientes son rápidas (caché)
- ChromaDB usa ~500MB RAM

### Dashboard consume mucho
- Cambiar intervalo de actualización en `dashboard_server.py`:
```python
UPDATE_INTERVAL = 5  # Cada 5 segundos en vez de 2
```

---

**Última actualización:** Agosto 2026 | KALMIYA v3.6

[[INDEX|← Índice]] | [[README|📄 README]] | [[06_docs/INSTALACION_V36|📦 Instalación]] | [[WELCOME|👋 Bienvenida]]

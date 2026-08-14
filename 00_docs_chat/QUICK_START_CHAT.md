# 🚀 QUICK START - Chat KALMIYA

**5 minutos para tener el chat funcionando** ⚡

---

## ▶️ Inicio Rápido (30 segundos)

```powershell
cd c:\Users\maria\env
python 03_launchers\chat.py
```

**¡Listo!** El chat debería abrirse ahora.

---

## 🔍 Si No Funciona (1 minuto)

### Paso 1: Verifica Python
```powershell
python --version
```
Debe mostrar: `Python 3.8` o superior

### Paso 2: Instala dependencias
```powershell
pip install customtkinter python-decouple psutil
```

### Paso 3: Ejecuta test
```powershell
python TEST_CHAT.py
```

Debe mostrar: `TEST COMPLETADO - Chat KALMIYA está listo para usar`

### Paso 4: Inicia de nuevo
```powershell
python 03_launchers\chat.py
```

---

## ❓ FAQ Rápido

### ¿Necesito instalar Vosk o audio?
**NO.** El chat funciona solo con texto. Audio es opcional.

### ¿Necesito configurar .env?
**NO.** El chat usa valores por defecto. Puedes personalizar después.

### ¿Qué motor de IA usa?
Por defecto: **Gemini** (si tienes API key) o **respuestas locales**

### ¿Puedo cambiar el motor IA?
**SÍ.** Edita `.env` y agrega:
```env
AI_MODE=gemini      # o "ollama" o "auto"
GEMINI_API_KEY=tu_clave_aqui
```

---

## 🎨 Personalización Básica

### Cambiar colores
Edita: `01_systems/KALMIYA_System/ui/kalmiya_chat.py`

```python
ACCENT = "#00e5ff"  # Color principal
BG_MAIN = "#06080f" # Fondo
```

### Cambiar tamaño ventana
```python
CHAT_W = 440  # Ancho
CHAT_H = 600  # Alto
```

### Cambiar nombre del bot
Edita `.env`:
```env
BOTNAME=MiAsistente
USER=Tu Nombre
```

---

## 🐛 Problemas Comunes

### Error: "No module named 'customtkinter'"
```powershell
pip install customtkinter
```

### Error: Encoding UTF-8
Los scripts ya tienen fix automático. Si persiste:
```powershell
chcp 65001
python 03_launchers\chat.py
```

### Chat no responde
Verifica que Gemini API key esté configurada o usa Ollama local.

---

## 📚 Más Información

- **Estado completo:** [[CHAT_STATUS|CHAT_STATUS.md]]
- **Troubleshooting:** [[06_docs/TROUBLESHOOTING|TROUBLESHOOTING.md]]
- **Guía completa:** [[README|README.md]]

---

## ✅ Checklist Rápido

- [ ] Python 3.8+ instalado
- [ ] `pip install customtkinter python-decouple psutil`
- [ ] `python TEST_CHAT.py` → PASS
- [ ] `python 03_launchers\chat.py` → Chat abierto
- [ ] ✨ ¡Listo para usar!

---

**Tiempo total: ~2 minutos** ⚡

[[INDEX|← Índice]] | [[CHAT_STATUS|📊 Estado]] | [[06_docs/TROUBLESHOOTING|🔧 Troubleshooting]]

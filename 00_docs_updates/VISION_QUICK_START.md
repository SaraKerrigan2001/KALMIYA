# 👁️ QUICK START - KALMIYA Vision

**3 pasos para que KALMIYA te reconozca** ⚡

---

## ▶️ Paso 1: Instalar (2 minutos)

```powershell
# Windows - Requiere Visual Studio Build Tools
pip install cmake
pip install face-recognition opencv-python

# Si da error, ver: 06_docs/VISION_SYSTEM.md
```

---

## 👤 Paso 2: Enseñar Tu Rostro (1 minuto)

```powershell
# Iniciar sistema
python 03_launchers\vision_demo.py

# En el menú:
# 1. Aprender nuevo rostro
# 2. Escribe tu nombre: "Sara"
# 3. Presiona ESPACIO 10 veces (captura muestras)
# 4. Presiona Q cuando termine
```

✅ ¡Listo! KALMIYA te conoce ahora.

---

## 🎬 Paso 3: Probar Reconocimiento

```powershell
# En el menú:
# 2. Iniciar reconocimiento en vivo
# Duración: 30 (segundos)
# Emociones: n (no, por ahora)
```

Verás tu nombre en pantalla cuando te detecte 🎉

---

## 💬 Usar con Chat (Próximamente)

```
Usuario: ¿Me ves?
KALMIYA: Sí, veo a Sara (confianza 98%)

Usuario: ¿Quién soy?
KALMIYA: Eres Sara 👋
```

---

## 🐛 Si No Funciona

### Error: dlib not found
```powershell
# Instalar Build Tools primero:
# https://visualstudio.microsoft.com/downloads/

# Luego:
pip install cmake
pip install dlib
```

### Cámara no funciona
```powershell
# Verificar que la cámara esté conectada
# En el menú de Windows:
# Configuración > Privacidad > Cámara
# Permitir acceso a aplicaciones de escritorio
```

---

## 📚 Documentación Completa

Ver: [[06_docs/VISION_SYSTEM|👁️ VISION_SYSTEM.md]]

---

**Tiempo total: ~5 minutos** ⚡

[[INDEX|← Índice]] | [[06_docs/VISION_SYSTEM|📖 Docs Completas]]

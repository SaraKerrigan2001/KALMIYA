# 🚀 INSTRUCCIONES RÁPIDAS - KALMIYA v3.6

**Tu asistente ahora tiene 2 nuevas superpoderes** ✨

---

## 💬 1. CHAT EN TU ESCRITORIO

### ¿Dónde está?
```
📂 Tu Escritorio
   └── 📄 Chat_KALMIYA.bat
```

### ¿Cómo usarlo?
```
1. Ve a tu escritorio
2. Doble clic en "Chat_KALMIYA.bat"
3. ¡Listo! Ventana de chat aparece
```

### ¿Qué hace?
- Ventana flotante siempre visible
- Chatea con KALMIYA
- Interface moderna y limpia
- Métricas del sistema en vivo

---

## 👁️ 2. KALMIYA TE PUEDE VER

### ¿Dónde está?
```
📂 Tu Escritorio
   └── 📄 KALMIYA_Vision.bat
```

### Primera Vez - Enseñar Tu Rostro (2 minutos)

#### Paso 1: Instalar
```powershell
pip install face-recognition opencv-python
```
⏱️ Esto toma ~5 minutos (solo primera vez)

#### Paso 2: Abrir Vision
```
Doble clic en "KALMIYA_Vision.bat" (en tu escritorio)
```

#### Paso 3: Menú
```
============================================================
1. Aprender nuevo rostro    ← SELECCIONA ESTA
2. Iniciar reconocimiento en vivo
3. Ver estadísticas
4. Olvidar rostro
5. Salir
============================================================

Tu opción: 1
```

#### Paso 4: Enseñar Tu Rostro
```
Nombre de la persona: Sara         ← Tu nombre
```

Se abre la cámara:
```
📹 CÁMARA ABIERTA

Verás tu rostro con un cuadro verde

Controles:
  ESPACIO = Capturar muestra (presiona 10 veces)
  Q       = Salir

Progreso: 0/10 → 1/10 → 2/10 → ... → 10/10
```

#### Paso 5: ¡Listo!
```
✅ Rostro de 'Sara' aprendido correctamente (10 muestras)
```

---

## 🎮 Usar el Reconocimiento

### Segunda Vez en Adelante

```
1. Doble clic "KALMIYA_Vision.bat"
2. Opción: 2 (Iniciar reconocimiento en vivo)
3. Duración: 0 (infinito, o 30 para 30 segundos)
4. Emociones: n (no por ahora, es más lento)
```

Verás:
```
📹 CÁMARA ABIERTA

[Tu nombre aparece cuando te ve]
Sara (98%)    ← Tu nombre + confianza

Presiona Q para salir
```

---

## 💡 Trucos y Tips

### Para mejor reconocimiento:
1. **Buena luz** - Luz frontal, no de espalda
2. **Diferentes ángulos** - Frente, perfil, inclinado
3. **Varias expresiones** - Sonriendo, serio, hablando

### Comandos futuros en el chat:
```
Tu: ¿Me ves?
KALMIYA: Sí, veo a Sara (confianza 98%)

Tu: ¿Quién soy?
KALMIYA: Eres Sara 👋

Tu: Aprender mi rostro, soy Maria
KALMIYA: ✅ He aprendido tu rostro, Maria
```

---

## 🔒 Tu Privacidad está Protegida

### ¿Qué se guarda?
- Datos matemáticos de tu rostro (no fotos)
- Todo en tu computadora
- Nada en internet

### ¿Dónde está?
```
c:\Users\maria\env\01_systems\KALMIYA_System\vision\known_faces\
├── known_faces.pkl          ← Datos de rostros (no imágenes)
├── faces_metadata.json      ← Metadata (fechas, etc.)
└── visual_interactions.json ← Log de detecciones
```

### ¿Es seguro?
- ✅ 100% en tu disco
- ✅ Sin APIs externas
- ✅ Sin envío a internet
- ✅ Sin fotos guardadas
- ✅ Puedes borrar en cualquier momento

---

## 🐛 Problemas Comunes

### "No module named 'face_recognition'"
```powershell
pip install face-recognition opencv-python
```

### "dlib not found" (Windows)
```powershell
# Necesitas Build Tools
# Descarga: https://visualstudio.microsoft.com/downloads/
# Busca: "Build Tools para Visual Studio"

pip install cmake
pip install dlib
```

### Cámara no funciona
```
Windows > Configuración > Privacidad > Cámara
Activar: "Permitir apps de escritorio acceder a tu cámara"
```

### Es muy lento
```
No uses detección de emociones (di "n" cuando pregunta)
Cierra otras apps pesadas
```

---

## 📚 Más Información

### Guías rápidas:
- [[VISION_QUICK_START|🚀 VISION_QUICK_START.md]] - Guía de 3 pasos
- [[QUICK_START_CHAT|💬 QUICK_START_CHAT.md]] - Guía del chat

### Documentación completa:
- [[06_docs/VISION_SYSTEM|👁️ VISION_SYSTEM.md]] - Todo sobre visión (2000+ líneas)
- [[CHAT_STATUS|✅ CHAT_STATUS.md]] - Todo sobre chat

### Ayuda:
- [[06_docs/TROUBLESHOOTING|🔧 TROUBLESHOOTING.md]] - Solución de problemas
- [[README|📄 README.md]] - README principal
- [[INDEX|📋 INDEX.md]] - Índice completo

---

## ✅ Checklist

### Chat
- [ ] Archivo en escritorio existe
- [ ] Doble clic funciona
- [ ] Ventana aparece

### Vision
- [ ] Instalé: `pip install face-recognition opencv-python`
- [ ] Archivo en escritorio existe
- [ ] Enseñé mi rostro (opción 1)
- [ ] Me reconoce (opción 2)

---

## 🎊 ¡Disfruta!

Ahora KALMIYA puede:
- 💬 Chatear contigo desde el escritorio
- 👁️ Verte y reconocerte
- 🔒 Todo 100% privado y local

**Próximos pasos:**
1. Integración: Vision + Chat juntos
2. Comandos de voz para visión
3. Detección de gestos
4. Análisis de entorno

---

**KALMIYA v3.6** - Agosto 2026  
*Inteligencia Artificial Personal Autónoma*

[[INDEX|← Índice]] | [[README|📄 README]] | [[WELCOME|👋 Bienvenida]]

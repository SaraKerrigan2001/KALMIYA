# 👁️ KALMIYA Vision System

[[INDEX|← Índice]] | [[README|📄 README]] | [[06_docs/TROUBLESHOOTING|🔧 Troubleshooting]]

Sistema de reconocimiento visual que permite a KALMIYA:
- 👤 **Reconocer personas** por rostro
- 😊 **Detectar emociones** en tiempo real
- 📸 **Aprender nuevos rostros** automáticamente
- 🔒 **100% Local** - Sin APIs externas, privacidad total

---

## 🚀 Quick Start

### 1. Instalar Dependencias

```powershell
# Instalación completa (recomendado)
pip install -r 04_config\requirements_vision.txt

# Instalación mínima (solo reconocimiento facial)
pip install face-recognition opencv-python
```

**Nota Windows:** Requiere Visual Studio Build Tools para compilar dlib.
Ver [[#instalacion-windows|Instalación en Windows]]

### 2. Iniciar Sistema de Visión

**Opción A: Desde Escritorio**
```
Doble clic en: KALMIYA_Vision.bat (en tu escritorio)
```

**Opción B: Desde terminal**
```powershell
python 03_launchers\vision_demo.py
```

### 3. Aprender Tu Rostro

1. Selecciona opción `1. Aprender nuevo rostro`
2. Escribe tu nombre (ej: "Sara")
3. Presiona **ESPACIO** para capturar muestras (10 veces)
4. Presiona **Q** cuando termine

✅ ¡Listo! KALMIYA ahora te reconocerá.

---

## 📋 Características

### ✅ Reconocimiento Facial

- **Multi-rostro:** Reconoce múltiples personas simultáneamente
- **Confianza:** Muestra porcentaje de confianza por persona
- **Persistencia:** Recuerda rostros entre sesiones
- **Muestras múltiples:** Aprende 10+ ángulos por persona para mayor precisión

### ✅ Detección de Emociones (Opcional)

Requiere: `pip install deepface tensorflow-cpu`

Detecta 7 emociones básicas:
- 😊 Feliz (happy)
- 😢 Triste (sad)
- 😠 Enojado (angry)
- 😨 Miedo (fear)
- 😲 Sorprendido (surprise)
- 😐 Neutral (neutral)
- 🤢 Disgusto (disgust)

### ✅ Privacidad Total

- 🔒 **Procesamiento 100% local**
- 🚫 **Sin APIs externas**
- 💾 **Datos en tu disco** únicamente
- 🔐 **No se envía nada a internet**

### ✅ Log de Interacciones

Registra automáticamente:
- Timestamp de cada detección
- Persona detectada
- Emoción (si está habilitado)
- Confianza del reconocimiento

Archivo: `01_systems/KALMIYA_System/vision/known_faces/visual_interactions.json`

---

## 🎮 Uso Interactivo

### Menú Principal

```
============================================================
1. Aprender nuevo rostro
2. Iniciar reconocimiento en vivo
3. Ver estadísticas
4. Olvidar rostro
5. Salir
============================================================
```

### 1. Aprender Nuevo Rostro

Captura múltiples muestras de un rostro para reconocimiento futuro.

**Controles:**
- **ESPACIO**: Capturar muestra
- **Q**: Cancelar

**Tips:**
- Mantén buena iluminación
- Captura desde diferentes ángulos
- Mínimo 3 muestras, recomendado 10+

### 2. Reconocimiento en Vivo

Abre la cámara y reconoce personas en tiempo real.

**Configuración:**
- **Duración:** Segundos (0 = infinito)
- **Emociones:** Sí/No (más lento pero más completo)

**Controles:**
- **Q**: Salir

### 3. Ver Estadísticas

Muestra información de todas las personas conocidas:
- Nombre
- Primera vez vista
- Última vez vista
- Total de interacciones

### 4. Olvidar Rostro

Elimina un rostro de la base de datos.

**ADVERTENCIA:** Esta acción no se puede deshacer.

---

## 💬 Integración con Chat

El sistema de visión se puede integrar con el chat de KALMIYA.

### Comandos de Chat (Próximamente)

```
Usuario: ¿Me ves?
KALMIYA: Sí, veo a Sara (confianza 98%)

Usuario: ¿Qué ves?
KALMIYA: Veo a Sara y otra persona desconocida

Usuario: Aprender mi rostro, soy Maria
KALMIYA: ✅ He aprendido tu rostro, Maria

Usuario: ¿Quién soy?
KALMIYA: Eres Sara 👋
```

### Modo Monitoreo Continuo

```python
from vision.vision_chat_integration import VisionChatIntegration

# Callback cuando detecta persona
def on_person(name, confidence):
    print(f"Detectado: {name} ({confidence:.1%})")

# Iniciar monitoreo
integration = VisionChatIntegration(on_person_detected=on_person)
integration.start_monitoring()
```

---

## ⚙️ Configuración

### Archivos de Almacenamiento

```
01_systems/KALMIYA_System/vision/known_faces/
├── known_faces.pkl          # Encodings de rostros (binario)
├── faces_metadata.json      # Metadata de personas
└── visual_interactions.json # Log de interacciones
```

### Ajustar Precisión

Editar `vision/camera_recognition.py`:

```python
# Más estricto (menos falsos positivos)
self.recognition_threshold = 0.5

# Más flexible (reconoce más fácil)
self.recognition_threshold = 0.7

# Balanceado (default)
self.recognition_threshold = 0.6
```

### Cambiar Cámara

```python
# Cámara 0 (default, generalmente webcam integrada)
self.camera_index = 0

# Cámara 1 (USB externa, si existe)
self.camera_index = 1
```

---

## 🐛 Troubleshooting

### Error: "No module named 'face_recognition'"

```powershell
pip install face-recognition opencv-python
```

### Error: "dlib not found"

**Windows:**
1. Instalar Visual Studio Build Tools
2. Instalar CMake: `pip install cmake`
3. Instalar dlib: `pip install dlib`

**O descargar wheel precompilado:**
https://github.com/z-mahmud22/Dlib_Windows_Python3.x

### Error: "Camera not found"

```python
# Probar diferentes índices de cámara
cap = cv2.VideoCapture(0)  # Cámara 0
cap = cv2.VideoCapture(1)  # Cámara 1
```

Ver cámaras disponibles:
```powershell
python -c "import cv2; print([i for i in range(10) if cv2.VideoCapture(i).isOpened()])"
```

### Reconocimiento muy lento

1. **Deshabilitar detección de emociones:**
   - Usar `detect_emotions=False`

2. **Reducir frecuencia de reconocimiento:**
   ```python
   recognition_interval = 2.0  # Cada 2 segundos en vez de 1
   ```

3. **Reducir resolución de cámara:**
   ```python
   cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
   cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
   ```

### No reconoce correctamente

**Soluciones:**

1. **Capturar más muestras:**
   ```python
   vision.learn_face("Sara", num_samples=20)  # En vez de 10
   ```

2. **Mejorar iluminación:**
   - Luz frontal (no de espalda)
   - Evitar sombras fuertes
   - Luz natural es mejor

3. **Ajustar umbral:**
   ```python
   self.recognition_threshold = 0.7  # Más flexible
   ```

---

## 📊 Rendimiento

### Especificaciones

| Métrica | Valor |
|---------|-------|
| **FPS (sin emociones)** | 15-30 fps |
| **FPS (con emociones)** | 5-10 fps |
| **Precisión reconocimiento** | 95-99% |
| **Tiempo aprendizaje** | ~30 segundos |
| **Rostros simultáneos** | 5-10 |
| **Uso CPU** | 10-30% |
| **Uso RAM** | 200-500 MB |

### Optimizaciones

**Para mejor rendimiento:**
- Deshabilitar detección de emociones
- Usar resolución 640x480
- Reconocer cada 1-2 segundos (no cada frame)
- Cerrar otras aplicaciones pesadas

**Para mejor precisión:**
- Capturar 15-20 muestras por persona
- Buena iluminación
- Diferentes ángulos y expresiones
- Re-aprender si cambia mucho la apariencia

---

## 🔒 Seguridad y Privacidad

### ✅ Garantías de Privacidad

1. **Procesamiento 100% local**
   - Todo en tu computadora
   - Sin envío de datos a servidores

2. **Sin APIs externas**
   - No usa servicios cloud
   - No requiere internet

3. **Control total de datos**
   - Puedes eliminar rostros en cualquier momento
   - Archivos en ubicación conocida
   - Fácil de hacer backup

4. **Sin telemetría**
   - No reporta estadísticas
   - No envía analytics
   - Zero tracking

### 🔐 Recomendaciones de Seguridad

1. **Backup regular:**
   ```powershell
   # Copiar base de datos de rostros
   Copy-Item -Recurse "01_systems\KALMIYA_System\vision\known_faces" "backup\"
   ```

2. **Proteger archivos:**
   - Los `.pkl` contienen datos biométricos
   - No compartir estos archivos
   - Mantener en disco encriptado si es posible

3. **Limpiar logs:**
   ```python
   # Eliminar log de interacciones antiguo
   vision.interactions_log.unlink()
   ```

---

## 📚 API de Programación

### Uso Básico

```python
from vision.camera_recognition import KalmiyaVision

# Inicializar
vision = KalmiyaVision()

# Aprender rostro
vision.learn_face("Sara", num_samples=10)

# Reconocer en tiempo real
vision.start_recognition_session(duration=30)

# Ver estadísticas
stats = vision.get_statistics()
print(f"Rostros conocidos: {stats['known_faces']}")
```

### Reconocimiento Programático

```python
import cv2

# Capturar frame
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

# Reconocer rostros en el frame
faces = vision.recognize_faces(frame)

for face in faces:
    print(f"Nombre: {face['name']}")
    print(f"Confianza: {face['confidence']:.1%}")
    print(f"Ubicación: {face['location']}")
    print(f"Conocido: {face['known']}")

cap.release()
```

### Integración con Chat

```python
from vision.vision_chat_integration import VisionChatIntegration

# Callback cuando detecta persona
def on_detected(name, confidence):
    print(f"¡Hola {name}! (confianza {confidence:.0%})")

# Iniciar
integration = VisionChatIntegration(on_person_detected=on_detected)
integration.start_monitoring()

# Obtener vista actual
view = integration.get_current_view()
print(view)  # "Veo a Sara (confianza 98%)"

# Detener
integration.stop_monitoring()
```

---

## 🎯 Casos de Uso

### 1. Autenticación por Rostro

```python
def authenticate_user():
    vision = KalmiyaVision()
    cap = cv2.VideoCapture(0)
    
    for _ in range(10):  # Intentar 10 frames
        ret, frame = cap.read()
        faces = vision.recognize_faces(frame)
        
        for face in faces:
            if face['known'] and face['confidence'] > 0.8:
                cap.release()
                return face['name']
    
    cap.release()
    return None

user = authenticate_user()
if user:
    print(f"✅ Bienvenido, {user}")
else:
    print("❌ Usuario no reconocido")
```

### 2. Saludo Personalizado

```python
def greet_on_detection():
    integration = VisionChatIntegration(
        on_person_detected=lambda name, conf: 
            print(f"¡Hola {name}! 👋")
    )
    integration.start_monitoring()
```

### 3. Registro de Asistencia

```python
import json
from datetime import datetime

def log_attendance(name, confidence):
    log = {
        "name": name,
        "timestamp": datetime.now().isoformat(),
        "confidence": confidence
    }
    
    with open("attendance.json", "a") as f:
        f.write(json.dumps(log) + "\n")

integration = VisionChatIntegration(on_person_detected=log_attendance)
integration.start_monitoring()
```

---

## 🚀 Roadmap

### v1.0 (Actual)
- ✅ Reconocimiento facial básico
- ✅ Detección de emociones
- ✅ Aprendizaje de rostros
- ✅ Estadísticas y logs
- ✅ Integración con chat (básica)

### v1.1 (Próximo)
- [ ] Auto-entrenamiento continuo
- [ ] Reconocimiento de gestos
- [ ] Detección de atención/enfoque
- [ ] Integración completa con chat UI
- [ ] Modo "siempre escuchando + viendo"

### v1.2 (Futuro)
- [ ] Reconocimiento de objetos
- [ ] Análisis de entorno
- [ ] Descripción automática de escena
- [ ] OCR en tiempo real
- [ ] Integración con dashboard visual

---

## 📖 Referencias

### Librerías Utilizadas

- **face_recognition** - https://github.com/ageitgey/face_recognition
- **OpenCV** - https://opencv.org/
- **dlib** - http://dlib.net/
- **DeepFace** - https://github.com/serengil/deepface

### Papers y Algoritmos

- HOG (Histogram of Oriented Gradients) para detección
- Face embedding con ResNet
- Face comparison con distancia euclidiana

---

## 💡 Tips y Trucos

### Mejor Reconocimiento

1. **Iluminación frontal** - Evita sombras
2. **Múltiples ángulos** - Captura frente, perfil, etc.
3. **Diferentes expresiones** - Sonriendo, serio, etc.
4. **Re-entrenar periódicamente** - Si cambias de look

### Rendimiento

1. **640x480 es suficiente** - No necesitas 1080p
2. **Reconocer cada 1-2 segundos** - No cada frame
3. **Cerrar otros programas** - Más recursos disponibles
4. **Usar SSD** - Lectura más rápida de modelos

### Debugging

```python
# Ver encodings guardados
import pickle
with open("known_faces/known_faces.pkl", "rb") as f:
    faces = pickle.load(f)
    print(f"Personas: {list(faces.keys())}")
    print(f"Muestras por persona: {[(k, len(v)) for k, v in faces.items()]}")
```

---

**Última actualización:** Agosto 2026 | KALMIYA v3.6

[[INDEX|← Índice]] | [[README|📄 README]] | [[06_docs/TROUBLESHOOTING|🔧 Troubleshooting]] | [[WELCOME|👋 Bienvenida]]

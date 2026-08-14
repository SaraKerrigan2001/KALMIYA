# 🎨 CHAT KALMIYA V2 - Nuevo Diseño Futurista

**Versión:** 3.6 v2  
**Estado:** ✅ LISTO PARA USAR  
**Estilo:** AI Assistant con Avatar Robótico Kawaii

---

## 🌟 Nuevo Diseño

### ✨ Características Visuales

**1. Avatar Robótico Kawaii**
- Diseño inspirado en robots chibi anime
- Ojos grandes azul cyan brillantes
- Detalles rosas (orejas, torso, pies)
- Cuerpo blanco limpio estilo futurista
- Animación de "respiración" sutil

**2. Interface AI Assistant Moderna**
- Glassmorphism (efecto vidrio esmerilado)
- Colores neón (cyan, púrpura, rosa)
- Cards flotantes con blur
- Wave indicator cuando procesa
- Transiciones suaves

**3. Paleta de Colores**
```
Fondo oscuro:     #0a0e1a (dark navy)
Cards:            #0f1624 (glass effect)
Accent cyan:      #00d9ff (neón principal)
Accent purple:    #b429f9 (gradientes)
Accent pink:      #ff6ec7 (detalles kawaii)
```

### 📊 Layout Mejorado

```
┌─────────────────────────────────────────────┐
│  KALMIYA AI            🟢 ONLINE   ─  ✕    │  Header
├─────────────────────────────────────────────┤
│   🤖          Buenos días, Sara             │  Avatar
│  [Avatar]     ¿En qué puedo ayudarte?       │  Section
│  Robótico     ─────────────────             │
│               🎤 Pulsa para hablar          │
├──────────────────────────────────────────┬──┤
│ CPU: 15%   │ RAM: 32%   │ DISCO: 45%     │  Stats
├────────────────────────────────────────────│  Cards
│ 💬 Conversación              🗑️ Limpiar    │
├────────────────────────────────────────────┤
│                                            │
│  [Mensajes del chat]                       │  Chat
│                                            │  Area
│  Usuario: Hola KALMIYA                     │
│  KALMIYA: ¡Hola! ¿Cómo puedo ayudarte?   │
│                                            │
├────────────────────────────────────────────┤
│  Escribe tu mensaje aquí...           ➤   │  Input
└────────────────────────────────────────────┘
```

---

## 🚀 Cómo Usar

### Opción 1: Desde Escritorio (Recomendado)

```
Escritorio → Doble clic en "Chat_KALMIYA_v2.bat"
```

### Opción 2: Desde Terminal

```powershell
python 03_launchers\chat_v2.py
```

### Opción 3: Módulo Python

```python
from kalmiya_chat_v2 import KalmiyaChatV2

chat = KalmiyaChatV2()
chat.run()
```

---

## 🎨 Características del Diseño

### 1. Avatar Robótico Animado

**Componentes:**
- **Cabeza:** Oval blanca con detalles
- **Orejas:** Sensores blancos con interior rosa
- **Ojos:** Grandes azul cyan con brillos
- **Torso:** Core central negro con marco blanco
- **Brazos/Piernas:** Articulados estilo robot
- **Pies:** Zapatos rosas kawaii

**Animaciones:**
- Respiración sutil (scale pulsante)
- Ojos brillantes constantes
- Pulse del status indicator

### 2. Messages Bubbles Modernos

**Usuario:**
- Bubble azul cyan (#00d9ff)
- Alineado a la derecha
- Avatar de usuario (opcional)
- Timestamp en cada mensaje

**KALMIYA:**
- Bubble glass effect (#1a2332)
- Alineado a la izquierda
- Avatar robótico 🤖
- Nombre del bot en cyan
- Timestamp

### 3. Stats Cards en Tiempo Real

**Tres cards horizontales:**
- **CPU** - Cyan
- **RAM** - Púrpura
- **DISCO** - Rosa

Actualización cada 2 segundos con psutil.

### 4. Input Section Futurista

- Background oscuro con transparencia
- Border radius grande (25px)
- Botón de enviar circular con neón
- Placeholder text elegante
- Enter para enviar

### 5. Wave Indicator

**Estados:**
- **Idle:** Línea plana gris
- **Processing:** Wave animada cyan
- **Listening:** Wave con más amplitud (futuro)

---

## 🆚 Comparación v1 vs v2

| Característica | v1 (Actual) | v2 (Nuevo) |
|----------------|-------------|------------|
| **Tamaño** | 440x600 | 720x900 |
| **Avatar** | Sin avatar | Robot kawaii animado |
| **Colores** | Azul oscuro | Cyan neón + púrpura |
| **Cards** | No | Stats cards en vivo |
| **Glassmorphism** | No | Sí |
| **Wave indicator** | No | Sí |
| **Animaciones** | Básicas | Avanzadas |
| **Style** | Minimalista | AI Assistant |

---

## 📦 Archivos Nuevos

1. **`ui/kalmiya_chat_v2.py`** (1000+ líneas)
   - Clase principal KalmiyaChatV2
   - Diseño completo nuevo
   - Avatar robótico dibujado

2. **`03_launchers/chat_v2.py`**
   - Launcher del chat v2
   - Fix encoding incluido

3. **`Desktop/Chat_KALMIYA_v2.bat`**
   - Acceso directo en escritorio
   - Info del nuevo diseño

4. **`CHAT_V2_INFO.md`** (este archivo)
   - Documentación completa

---

## 🎯 Funcionalidades

### ✅ Implementadas

- [x] Avatar robótico kawaii dibujado
- [x] Interface AI Assistant
- [x] Glassmorphism effects
- [x] Stats cards (CPU/RAM/Disco)
- [x] Wave indicator
- [x] Message bubbles modernas
- [x] Timestamps en mensajes
- [x] Botón limpiar chat
- [x] Animaciones suaves
- [x] Responsive design

### 🔮 Futuras (v3)

- [ ] Avatar 3D renderizado
- [ ] Animaciones del avatar más complejas
- [ ] Expresiones faciales del robot
- [ ] Voice to text real
- [ ] Tema light mode
- [ ] Customización de avatar
- [ ] Efectos de partículas
- [ ] Más animaciones interactivas

---

## 🎨 Personalización

### Cambiar Colores

Editar `ui/kalmiya_chat_v2.py`:

```python
# Paleta de colores (líneas 40-50)
ACCENT_BLUE    = "#00d9ff"      # Tu color cyan favorito
ACCENT_PURPLE  = "#b429f9"      # Tu púrpura favorito
ACCENT_PINK    = "#ff6ec7"      # Tu rosa favorito
```

### Cambiar Tamaño

```python
# Dimensiones (líneas 60-61)
CHAT_W = 720  # Ancho
CHAT_H = 900  # Alto
```

### Cambiar Avatar

El avatar se dibuja en `_draw_robot_avatar()` (líneas 200-280).
Puedes modificar:
- Colores: `ROBOT_WHITE`, `ROBOT_PINK`, `ROBOT_BLUE`
- Tamaño de ojos
- Forma de orejas
- Detalles del torso

---

## 🐛 Troubleshooting

### Avatar no aparece correctamente

El avatar se dibuja con Canvas. Si no aparece:
1. Verificar que customtkinter esté actualizado
2. Verificar permisos de ventana
3. Probar en otro monitor

### Animaciones lentas

Si las animaciones van lentas:
1. Cerrar otras apps pesadas
2. Reducir FPS en `_animate()`: cambiar 33 a 50
3. Desactivar wave indicator

### Colors no se ven bien

Si los colores se ven mal:
1. Verificar tema dark mode: `ctk.set_appearance_mode("dark")`
2. Calibrar monitor
3. Probar en otra pantalla

---

## 📊 Rendimiento

| Métrica | Valor |
|---------|-------|
| **FPS** | ~30 fps |
| **Uso CPU** | 5-10% |
| **Uso RAM** | 150-250 MB |
| **Inicio** | <2 segundos |
| **Responsive** | Excelente |

---

## 💡 Tips de Uso

1. **Arrastrar ventana:** Click y arrastra desde cualquier parte
2. **Minimizar:** Click en botón "─"
3. **Limpiar chat:** Click en "🗑️ Limpiar"
4. **Enviar mensaje:** Enter o click en "➤"
5. **Cerrar:** Click en "✕"

---

## 🔄 Migración desde v1

**El chat v1 sigue funcionando.**

Para probar v2:
```powershell
# v1 (actual)
python 03_launchers\chat.py

# v2 (nuevo)
python 03_launchers\chat_v2.py
```

Ambos usan el mismo brain.py, así que la IA funciona igual.

**Diferencias principales:**
- v2 es más grande (720x900 vs 440x600)
- v2 tiene avatar animado
- v2 tiene stats cards
- v2 tiene diseño más moderno

---

## 📚 Referencias

**Inspiración visual:**
- Avatar: Robot kawaii chibi estilo anime
- Interface: AI Assistant dashboards modernos
- Colores: Paletas neón cyber/tech

**Librerías:**
- customtkinter 5.0+
- tkinter (built-in)
- psutil (stats)

---

## ✅ Checklist

Antes de usar, verifica:

- [ ] Python 3.8+ instalado
- [ ] customtkinter instalado
- [ ] psutil instalado (opcional, para stats)
- [ ] brain.py funcional
- [ ] .env configurado (opcional)

---

**Creado:** Agosto 2026  
**KALMIYA v3.6 v2** - AI Assistant Design

[[INDEX|← Índice]] | [[CHAT_STATUS|💬 Chat v1]] | [[README|📄 README]]

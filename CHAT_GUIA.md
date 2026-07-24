---
title: "Chat KALMIYA - Guía de Uso"
tags: [chat, kalmiya, guia, tutorial]
---

# 💬 Chat Interactivo con KALMIYA

[[WELCOME|← Bienvenida]] | [[INDEX|Hub]]

## ✨ Características

El chat de KALMIYA es una interfaz moderna para comunicarte con la IA:

- **Interfaz Premium**: Diseño moderno con tema oscuro
- **Respuestas Inteligentes**: Usa brain.py (Ollama + Gemini)
- **Chat Bidireccional**: Conversación natural y fluida
- **Estado del Sistema**: Monitoreo de motores IA
- **Sin Eco de Voz**: Chat puramente de texto

## 🚀 Cómo Iniciar

### Opción 1: Desde Windows
```
Haz doble clic en: Chat_KALMIYA.bat
```

### Opción 2: Desde Terminal
```bash
python start_chat.py
```

### Opción 3: Desde Python
```python
from kalmiya_chat import KalmiyaChat

chat = KalmiyaChat()
chat.run()
```

## 🎮 Cómo Usar

1. **Escribe tu pregunta** en el cuadro de entrada
2. **Presiona Enter** o haz clic en "Enviar"
3. **KALMIYA responde** en tiempo real
4. **Continúa la conversación** normalmente

## ⚙️ Requisitos

Para que el chat funcione correctamente necesitas:

- **Python 3.8+** instalado
- **customtkinter** - Interfaz gráfica moderna
- **brain.py** - Motor de IA
- **Ollama** o **Google Gemini** configurado

### Instalar dependencias:
```bash
pip install customtkinter psutil python-decouple
```

## 🔧 Configuración

Las siguientes variables se leen del archivo `.env`:

```env
USER=Sara              # Tu nombre de usuario
BOTNAME=KALMIYA        # Nombre del asistente
GEMINI_API_KEY=...     # Para usar Google Gemini
```

## 📊 Indicadores de Estado

El chat muestra el estado de los motores:

- 🟢 **Verde** - Sistema operativo
- 🟡 **Amarillo** - Verificando
- 🔴 **Rojo** - No disponible

## 💡 Tips

- Puedes hacer preguntas complejas y seguimiento
- El chat mantiene contexto de la conversación
- Usa Ctrl+Q para cerrar la ventana rápidamente
- La interfaz es arrastrable por la barra superior

## 🔐 Privacidad

- Las conversaciones se procesan localmente
- No se almacenan datos personales
- Usa las credenciales de tu configuración

---

**¿Listo para chatear?** → `Chat_KALMIYA.bat`

[[WELCOME|← Volver a Bienvenida]]

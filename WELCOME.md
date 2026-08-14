---
title: "Bienvenida — KALMIYA v3.5 + JARVIS OS"
tags: [welcome, start, guide, hub, jarvis]
---

# 👋 Bienvenida, Sara

**Sistema:** KALMIYA v3.5 + JARVIS OS  
**Arquitectura:** Cerebro (Claude) + Memoria (Obsidian) + Voz (Local) + Cara (HUD)  
**Privacidad:** 🔒 Audio 100% local (sin APIs externas)  
**Estado:** ✅ Completamente operativa

[[INDEX|📋 Índice]] | [[JARVIS_OS_README|🌟 JARVIS OS]] | [[KALMIYA_DASHBOARD|📊 Dashboard]] | [[SKILLS_CATALOG|📘 Skills]]

---

## 🚀 Comenzar Ahora

### Opción 1: Push-to-Talk Global (RECOMENDADO)
```
Presiona cualquier tecla:  Ctrl + Alt + M
Habla tu pregunta
Suelta para procesar     → Respuesta inmediata en voz
```
✨ Funciona en **cualquier aplicación** (Gmail, Slack, VS Code, etc.)

### Opción 2: KALMIYA Completa (Clásica)
```
Doble clic → Lanzar_KALMIYA.vbs
```

Lo que hace automáticamente:
1. Pantalla de arranque (splash)
2. Saludo por voz con análisis del sistema
3. HUD flotante en la pantalla
4. Fondo de pantalla personalizado
5. Escucha continua del wake word **"kalmiya"**
6. Pensamientos autónomos cada 3 minutos

---

## 🌟 JARVIS OS Features (Nuevo)

### 9 Skills Automáticos
| Skill | Hora | Función |
|-------|------|---------|
| **Bandeja** | 7:00 AM | Resumen matutino en voz |
| **Métricas** | 7:00 AM | Números e indicadores |
| **Plan** | 9:00 AM | 3 prioridades del día |
| **Tendencias** | 2:00 PM | Detecta patrones |
| **Auditoría** | 14:45 | Seguridad del sistema |
| + más | - | Biometría, Inteligencia, Bóveda |

📘 Ver detalles: [[SKILLS_CATALOG|Catálogo de Skills]]

### 🔐 Privacidad Garantizada
- ✅ STT (Speech-to-Text): **Vosk** (offline, sin Google)
- ✅ TTS (Text-to-Speech): **pyttsx3** (offline, sin Azure)
- ✅ Datos: 100% en disco local
- ✅ Memoria: Obsidian vault privada
- ✅ Push-to-Talk: Hotkey global

---

## 💬 Di "kalmiya" y Habla

KALMIYA te escucha con tu **JBL Tune 520BT** y responde con su voz neuronal. Tiene anti-eco activado — no escucha su propia voz.

O simplemente: **Presiona Ctrl+Alt+M** desde cualquier lugar.

---

## 📱 Conectar Celulares

- **WiFi:** Opción 44 en el menú → escanea el QR
- **Sin WiFi:** Opción 61 (Cloudflare) → cualquier red
- **Telegram:** Opción 63 → bot de KALMIYA

---

## 🧩 41 Módulos + 9 Skills

### Módulos Clásicos
Desde el menú principal escribe **M**:

| Tecla | Categoría |
|-------|-----------|
| P1-P4 | Productividad (tareas, pomodoro, recordatorios) |
| S1-S4 | Salud (ejercicio, sueño, consejos) |
| F1-F2 | Finanzas (gastos, presupuesto) |
| E1-E6 | Entretenimiento (películas, música, libros, gaming) |
| V1-V2 | Clima y viajes |
| I1-I2 | Idiomas y traducción |
| R1-R2 | Reportes semanales y backup |

### Skills JARVIS OS (Nuevo)
Los 9 skills se ejecutan automáticamente según su horario. Pueden invocarse manualmente desde chat:
- "Dame las métricas"
- "¿Cuál es mi plan?"
- "Analiza las tendencias"
- etc.

---

## 📚 Documentación Principal

### 🌟 JARVIS OS (Lee Primero)
- [[JARVIS_OS_README|🚀 Quick Start]] ← Comenzar aquí
- [[SKILLS_CATALOG|📘 Catálogo de Skills]]
- [[IMPLEMENTATION_SUMMARY|📋 Resumen Técnico]]

### 📖 KALMIYA Original
- [[INDEX|📋 Índice completo]]
- [[KALMIYA_DASHBOARD|📊 Dashboard en tiempo real]]
- [[06_docs/MODULOS_IMPLEMENTADOS|📦 Todos los módulos]]
- [[06_docs/KALMIYA_FUNCIONES|⚙️ Funciones detalladas]]
- [[06_docs/CHAT_GUIA|💬 Guía de Chat]]

---

## ⚙️ Instalación & Setup

### 1. Actualizar Dependencias (IMPORTANTE)
```bash
cd 04_config/
pip install -r requirements.txt
```

### 2. (Opcional) Descargar Modelo Vosk para STT Local
```bash
mkdir ~/.vosk
# Descargar desde: https://alphacep.github.io/vosk-api/
```

### 3. ¡Listo! Comienza
```bash
# Opción A: Push-to-Talk global (recomendado)
python 01_systems/KALMIYA_System/push_to_talk.py

# Opción B: KALMIYA completa
Lanzar_KALMIYA.vbs
```

---

## 🎯 Tips Rápidos

| Acción | Cómo |
|--------|------|
| **Hablar con KALMIYA** | Presiona `Ctrl+Alt+M` |
| **Ver tus skills** | [[SKILLS_CATALOG|Skills Catalog]] |
| **Abrir Obsidian vault** | `Doble clic en 01_systems/KALMIYA/` |
| **Ver gráfico de notas** | En Obsidian: `Ctrl+G` |
| **Chat de escritorio** | Ícono "KALMIYA Chat" en escritorio |
| **Menú completo** | `python 01_systems/KALMIYA_System/main.py` |
| **Hacer backup** | Opción **R2** en módulos |

---

## 🔧 Configuración Personalizada (.env)

Crea/edita `.env` en la raíz para cambiar:

```env
# Push-to-Talk hotkey
PTT_HOTKEY=ctrl+alt+m

# Voz neuronal
NEURAL_VOICE=es-ES-ElviraNeural

# Otros
BOTNAME=JARVIS
USER=Sara
```

---

## 📊 Status del Sistema

✅ **Cerebro**: Claude Code (motor IA)  
✅ **Memoria**: Obsidian (bóveda privada)  
✅ **Voz**: Vosk + pyttsx3 (100% local)  
✅ **Push-to-Talk**: Activo (Ctrl+Alt+M)  
✅ **Skills**: 9/9 implementados  
✅ **Privacidad**: Garantizada  
✅ **Documentación**: Completa  

---

*KALMIYA v3.5 + JARVIS OS — Inteligencia de Clase S para Sara Kerrigan*

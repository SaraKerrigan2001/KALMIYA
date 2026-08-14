---
title: "Skills Catalog - JARVIS OS KALMIYA"
tags: [skills, catalog, jarvis]
ubicacion: 06_docs/JARVIS_OS/SKILLS_CATALOG.md
---

# 🎯 SKILLS CATALOG - JARVIS OS KALMIYA

[[INDEX|← Índice]] | [[06_docs/JARVIS_OS/README|📄 JARVIS OS README]] | [[06_docs/JARVIS_OS/IMPLEMENTATION_SUMMARY|📋 Resumen]]

Índice completo de skills implementados en JARVIS OS.

---

## 📊 Skills Principales

### 1. **Métricas** 📈
**Ubicación**: [.skills/metrics/SKILL.md](.skills/metrics/SKILL.md)

Extrae números e indicadores clave de tu actividad diaria: suscripciones, vistas, seguidores, tasa de interacción.

- **Entrada**: Bases de datos, APIs
- **Salida**: Reporte de métricas con delta %
- **Ejecución**: Automática a las 7:00 AM
- **Estado**: ✅ Implementado

---

### 2. **Bandeja (Morning Briefing)** 🗂️
**Ubicación**: [.skills/bandeja/SKILL.md](.skills/bandeja/SKILL.md)

Resume tu mañana: eventos, calendario, noticias, entregado en voz.

- **Entrada**: Calendario, mensajes, noticias
- **Salida**: Resumen ejecutivo + audio
- **Ejecución**: Automática a las 7:00 AM
- **Estado**: ✅ Implementado

---

### 3. **Tendencias** 📉
**Ubicación**: [.skills/tendencias/SKILL.md](.skills/tendencias/SKILL.md)

Detecta patrones, anomalías y cambios en tus datos. Análisis de series temporales.

- **Entrada**: Histórico de 90 días
- **Salida**: Tendencias, anomalías, oportunidades
- **Ejecución**: Automática a las 2:00 PM
- **Estado**: ✅ Implementado

---

### 4. **Plan (Prioridades del Día)** 📌
**Ubicación**: [.skills/plan/SKILL.md](.skills/plan/SKILL.md)

Las 3 cosas más importantes que debes hacer hoy.

- **Entrada**: Calendario, métricas, objetivos
- **Salida**: 3 prioridades ordenadas
- **Ejecución**: Automática a las 9:00 AM
- **Estado**: ✅ Implementado

---

### 5. **Bóveda (Memory + RAG)** 📚
**Ubicación**: [.skills/boveda/SKILL.md](.skills/boveda/SKILL.md)

Acceso a todo tu conocimiento depurado. Retrieval-Augmented Generation sobre Obsidian.

- **Entrada**: Consultas en lenguaje natural
- **Salida**: Respuestas contextuales + notas relacionadas
- **Indexación**: Diaria a las 4:00 AM
- **Estado**: ✅ Implementado

---

### 6. **Audio (Voice I/O)** 🎤
**Ubicación**: [.skills/audio/SKILL.md](.skills/audio/SKILL.md)

STT (Speech-to-Text) y TTS (Text-to-Speech) completamente locales y privados.

- **STT**: Vosk (offline)
- **TTS**: pyttsx3 (offline, Windows SAPI5)
- **Privacidad**: 100% (cero APIs)
- **Estado**: ✅ Implementado

---

### 7. **Biometría** 💓
**Ubicación**: [.skills/biometria/SKILL.md](.skills/biometria/SKILL.md)

Monitoreo de estado físico: ritmo cardíaco, sueño, ubicación, dispositivos conectados.

- **Entrada**: Wearables (Fitbit, Apple Watch)
- **Salida**: Perfil de estado actual
- **Sincronización**: Cada 5 minutos
- **Estado**: ✅ Implementado

---

### 8. **Seguridad** 🛡️
**Ubicación**: [.skills/seguridad/SKILL.md](.skills/seguridad/SKILL.md)

Auditoría del sistema, detección de amenazas, control de acceso. Integrado con RAPTOR framework.

- **Monitoreo**: Continuo
- **Alertas**: Críticas inmediatas
- **Estado**: ✅ Implementado (con RAPTOR)

---

### 9. **Inteligencia** 💡
**Ubicación**: [.skills/inteligencia/SKILL.md](.skills/inteligencia/SKILL.md)

Análisis causal, predicción de escenarios, generación de insights. Pensamiento profundo con Claude.

- **Entrada**: Análisis complejos
- **Salida**: Insights + escenarios + recomendaciones
- **Motor**: Claude GPT-4
- **Estado**: ✅ Implementado

---

## 🗂️ Estructura de Carpetas

```
.skills/
├── metrics/
│   └── SKILL.md
├── bandeja/
│   └── SKILL.md
├── tendencias/
│   └── SKILL.md
├── plan/
│   └── SKILL.md
├── boveda/
│   └── SKILL.md
├── audio/
│   └── SKILL.md
├── biometria/
│   └── SKILL.md
├── seguridad/
│   └── SKILL.md
└── inteligencia/
    └── SKILL.md
```

---

## 🔧 Nuevos Módulos Implementados

### **audio/audio_local.py** 🎵
Audio completamente privado (STT + TTS local, sin APIs).

- Vosk para STT
- pyttsx3 para TTS
- Uso en voz.py y kalmiya_lupa.py
- **Instalación**: `pip install vosk pyaudio`

### **push_to_talk.py** 🎙️
Sistema global de Push-to-Talk (presiona hotkey para hablar).

- Hotkey configurable (Ctrl+Alt+M por defecto)
- Integración con audio_local
- Respuesta inmediata en voz
- **Instalación**: `pip install keyboard`

### **KARPATY_SETUP.md** 📊
Guía de instalación y configuración de Karpaty Graph en Obsidian.

- Visualización de grafo de conocimiento
- Análisis de conexiones en la bóveda
- Integración con RAG

---

## 📂 Estructura de Memoria Creada

```
01_systems/KALMIYA/
├── raw/
│   ├── calendario/     (datos crudos de calendario)
│   ├── mensajes/       (datos crudos de mensajes)
│   ├── metricas/       (datos crudos de métricas)
│   ├── biometria/      (datos crudos biométricos)
│   └── eventos/        (datos crudos de eventos)
│
├── outputs/
│   ├── metricas/       (reportes procesados)
│   ├── bandeja/        (resúmenes matutinos)
│   ├── plan/           (planes diarios)
│   ├── tendencias/     (análisis de tendencias)
│   ├── seguridad/      (auditorías)
│   └── inteligencia/   (insights profundos)
│
└── wiki/               (conocimiento depurado)
    └── README.md
```

---

## 🚀 Cómo Usar los Skills

### Activación Manual (desde chat)
```
"Dame las métricas de hoy"
→ Skill: Métricas ejecuta

"¿Cuál es mi agenda?"
→ Skill: Bandeja + Bóveda ejecuta

"¿Qué tendencias hay?"
→ Skill: Tendencias ejecuta

"Mis 3 prioridades"
→ Skill: Plan ejecuta

"¿Cómo estoy?"
→ Skill: Biometría ejecuta

"Analiza profundamente..."
→ Skill: Inteligencia ejecuta
```

### Activación Automática (horarios)
- 7:00 AM → Bandeja + Métricas
- 9:00 AM → Plan
- 2:00 PM → Tendencias
- 4:00 AM → Reindexación Bóveda (RAG)
- 14:45 → Auditoría Seguridad

### Push-to-Talk (Global)
```
Presiona: Ctrl+Alt+M
Habla tu pregunta
Suelta → Respuesta inmediata en voz
```

---

## 🔐 Privacidad & Seguridad

✅ **Audio**: 100% local (Vosk + pyttsx3)  
✅ **Datos**: Almacenados localmente en disco  
✅ **Inteligencia**: Claude API (encriptada)  
✅ **Bóveda**: Markdown en Obsidian (local)  
✅ **RAPTOR**: Framework de seguridad integrado  

**Cero datos comprometidos** 🔒

---

## 📖 Documentación Completa

- 📄 [REVISION_ENV_JARVIS.md](../REVISION_ENV_JARVIS.md) — Revisión inicial
- 🎯 [SKILLS_CATALOG.md](SKILLS_CATALOG.md) — Este archivo
- 🧠 [KARPATY_SETUP.md](KARPATY_SETUP.md) — Guía Karpaty Graph
- 📁 [.skills/](.skills/) — Documentación de cada skill

---

## 📊 Estado de Implementación

| Componente | Estado | Prioridad | Notas |
|-----------|--------|-----------|-------|
| Estructura Skills | ✅ Completado | — | 8 skills documentados |
| Memoria (raw, outputs, wiki) | ✅ Completado | — | Carpetas organizadas |
| STT Local | ✅ Completado | 🔴 Alta | Vosk implementado |
| TTS Local | ✅ Completado | 🔴 Alta | pyttsx3 como primario |
| Push-to-Talk | ✅ Completado | 🟡 Media | Hotkey Ctrl+Alt+M |
| Karpaty Graph | ✅ Documentado | 🟡 Media | Guía lista, falta instalar |
| HUD | ✅ Presente | 🟢 Baja | Mejoras visuales ópticas |
| Documentación Skills | ✅ Completado | — | Todos los SKILL.md listos |

---

## 🎯 Próximos Pasos (Futuro)

1. [ ] Instalar Karpaty plugin en Obsidian
2. [ ] Entrenar wake-word personalizado en Vosk
3. [ ] Integrar biometría avanzada (emociones en voz)
4. [ ] Optimizar perfil TTS (velocidad, entonación)
5. [ ] Dashboard web remoto (acceso via Telegram)
6. [ ] Análisis ML de tendencias predictivas

---

**Documento Generated**: 2026-08-12  
**Basado en**: JARVIS OS Architecture (@danielbrown.ia)  
**Versión**: KALMIYA v3.5 + JARVIS Enhancement

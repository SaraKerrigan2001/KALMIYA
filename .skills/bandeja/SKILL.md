# SKILL: Bandeja (Morning Briefing)

[[INDEX|← Índice]] | [[06_docs/JARVIS_OS/SKILLS_CATALOG|📘 Catálogo de Skills]] | [[06_docs/JARVIS_OS/README|🌟 JARVIS OS]]

Resume la entrada matutina, calendario y noticias con IA en un resumen ejecutivo.

## Descripción
El skill **Bandeja** es tu resumen matutino. Cada mañana a las 7 AM, JARVIS te prepara un briefing con:
- Resumen de eventos que ocurrieron mientras dormías
- Calendario del día organizado por prioridad
- Noticias relevantes (de fuentes configuradas)
- Lectura en voz alta con síntesis natural

## Qué Hace
- 🗂️ Agregación inteligente de eventos
- 📅 Priorización del calendario
- 📰 Curación de noticias relevantes
- 🎤 Síntesis de voz para lectura matutina
- 📝 Almacenamiento del resumen como nota Markdown

## Parámetros de Activación
```python
"¿qué tengo hoy?"
"resumen matutino"
"dime la bandeja"
"lee mi agenda"
```

## Flujo de Trabajo
1. **Recolecta** → Eventos, tareas, noticias, mensajes
2. **Analiza** → Agrupa por importancia
3. **Redacta** → Crea resumen con Claude
4. **Sintetiza** → Convierte a voz (TTS local)
5. **Registra** → Guarda en bóveda como Markdown

## Entrada
- Calendario: `01_systems/KALMIYA/raw/calendario/`
- Mensajes: `01_systems/KALMIYA/raw/mensajes/`
- Noticias: Feeds RSS / APIs configuradas
- Timestamp: 7:00 AM diariamente

## Salida
```
### 📋 BANDEJA MATUTINA
**2026-08-12 | 7:00 AM**

#### 📅 Prioridades de Hoy (3)
1. ⚡ Reunión con producto - 9:00 AM (confirmada)
2. 📊 Presentar métricas - 2:00 PM (preparado)
3. 🔍 Code review RAPTOR - Flexible (3 PRs esperando)

#### 📰 Noticias Relevantes
- AI Models: Nueva investigación en finetuning
- Tech: GitHub añade AI-powered features
- Local: Eventos en Medellín esta semana

#### 📈 Estado Nocturno
- Mensajes recibidos: 12 (2 urgentes)
- Cambios en bases de datos: 4
- Alertas de seguridad: 0
```

## Archivos Relacionados
- `01_systems/KALMIYA_System/kalmiya_chat.py` — Motor de chat
- `01_systems/KALMIYA_System/kalmiya_audio.py` — TTS para lectura
- `01_systems/KALMIYA/Bienvenido.md` — Template bandeja

## Notas
- Tiempo de preparación: ~2-3 minutos
- Audio guardado en `01_systems/KALMIYA_System/temp_audio/`
- Nota guardada en `01_systems/KALMIYA/outputs/bandeja/{fecha}.md`

---
**Creado:** 2026-08-12  
**Estado:** Implementado ✅

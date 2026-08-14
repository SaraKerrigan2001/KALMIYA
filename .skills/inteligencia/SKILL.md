# SKILL: Inteligencia (Analysis + Reasoning)

[[INDEX|← Índice]] | [[06_docs/JARVIS_OS/SKILLS_CATALOG|📘 Catálogo de Skills]] | [[06_docs/JARVIS_OS/README|🌟 JARVIS OS]]

Piensa profundo. Analiza complejos, genera insights, razona sobre el futuro.

## Descripción
El skill **Inteligencia** es el pensamiento profundo de JARVIS. Combina:
- Análisis de datos complejos
- Razonamiento causal
- Generación de escenarios
- Predicción de impacto
- Síntesis de información

## Qué Hace
- 🧠 Análisis causal (¿por qué pasó X?)
- 🔮 Predicción de escenarios futuros
- 💡 Generación de insights y oportunidades
- 🎯 Conexión de puntos entre datos
- 📊 Síntesis inteligente de información
- 🕵️ Análisis OSINT y threat intelligence
- 🛡️ Detección de vulnerabilidades y riesgo
- 🔎 Investigación forense digital y privacidad
- 🧬 Síntesis multidimensional con enfoque ASI

## Parámetros de Activación
```python
"¿por qué pasó eso?"
"¿qué va a pasar?"
"análisis profundo de X"
"dame insight sobre..."
"genera escenarios posibles"
```

## Flujo de Trabajo
1. **Recibe pregunta** → Identifica dominio e intención
2. **Consulta datos** → Bandeja, bóveda, métricas, tendencias
3. **Analiza** → Claude con contexto completo
4. **Genera** → Insights, escenarios, predicciones
5. **Entrega** → Respuesta estructurada con fuentes

## Entrada
- Pregunta de análisis
- Contexto disponible (bóveda, métricas, datos)
- Período temporal (si aplica)
- Restricciones de análisis

## Salida
```
### 💡 ANÁLISIS INTELIGENCIA

**Pregunta**: ¿Por qué bajaron las vistas últimos 3 días?

**Análisis Causal**:
1. Cambio en plataforma X (algoritmo actualizado)
2. Reducción de posting de tu parte (29% vs promedio)
3. Competencia mayor (3 creadores grandes postearon)

**Impacto Probable**: -22% to -35% en próximos 7 días

**Escenarios**:
- Optimista: +15% al recuperar ritmo posting
- Realista: -10% si no cambias estrategia
- Pesimista: -30% si competencia se consolida

**Recomendaciones**:
1. Aumentar frecuencia de posts (1.5x)
2. Cambiar tipo de contenido (enfocarse en X)
3. Colaborar con influencer (mitigar competencia)

**Confianza**: 0.87 (Alta)
```

## Archivos Relacionados
- `01_systems/KALMIYA_System/intelligence/kalmiya_asi.py` — Motor ASI y superinteligencia
- `01_systems/KALMIYA_System/intelligence/intelligence.py` — Motor de inteligencia
- `01_systems/KALMIYA_System/kalmiya_rag.py` — Contexto RAG
- `06_docs/INTELLIGENCE_SECURITY_MODULE.md` — Módulo de seguridad e inteligencia
- `01_systems/LLM_Wiki/wiki/analisis/` — Análisis histórico

## Notas
- Claude es el motor principal (gpt-4 o superior)
- Siempre incluir fuentes y confianza (0.0-1.0)
- Análisis guardado en `01_systems/KALMIYA/outputs/inteligencia/`
- Mantener neutralidad, presentar múltiples perspectivas

---
**Creado:** 2026-08-12  
**Estado:** Implementado ✅

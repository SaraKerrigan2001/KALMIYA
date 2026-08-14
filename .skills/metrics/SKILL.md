# SKILL: Métricas

[[INDEX|← Índice]] | [[06_docs/JARVIS_OS/SKILLS_CATALOG|📘 Catálogo de Skills]] | [[06_docs/JARVIS_OS/README|🌟 JARVIS OS]]

Extrae números e indicadores clave de tu actividad diaria.

## Descripción
El skill de **Métricas** recopila y analiza datos cuantitativos sobre tu actividad, productividad, conexiones e impacto. Es el cerebro numérico de JARVIS.

## Qué Hace
- 📊 Extrae suscripciones, vistas y seguidores
- 📈 Calcula tasas de crecimiento y tendencias
- 🎯 Rastrea objetivos vs realidad
- 💾 Almacena históricos para análisis comparativo
- 🔔 Identifica anomalías en los números

## Parámetros de Activación
```python
"extraer métricas"
"¿qué números tengo?"
"dame los números de hoy"
"análisis de métricas"
```

## Flujo de Trabajo
1. **Captura** → Consulta bases de datos y APIs
2. **Procesa** → Calcula ratios, tendencias, cambios
3. **Almacena** → Registra en timestamp en bóveda
4. **Reporta** → Entrega resumen ejecutivo

## Entrada
- Fuentes: Bases de datos KALMIYA, APIs externas
- Formato: JSON con estructura de métricas
- Rango temporal: Último día, semana, mes, año

## Salida
```
Métricas Obtenidas
─────────────────────
✓ Suscripciones: 155K (+3.2% vs ayer)
✓ Vistas: 202K (+1.5% vs ayer)
✓ Seguidores: 17K (+0.8% vs ayer)
✓ Tasa de interacción: 9%
✓ Anomalías: Ninguna detectada
```

## Archivos Relacionados
- `01_systems/KALMIYA_System/kalmiya_system_info.py` — Recolección de datos
- `01_systems/KALMIYA_System/database.py` — Acceso a bases de datos
- `01_systems/LLM_Wiki/schema/metrics.yaml` — Esquema de métricas

## Notas
- Ejecutar diariamente a las 7:00 AM
- Almacenar en `01_systems/KALMIYA/outputs/metricas/`
- Mantener histórico de 90 días mínimo

---
**Creado:** 2026-08-12  
**Estado:** Implementado ✅

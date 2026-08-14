# SKILL: Tendencias (Trend Analysis)

[[INDEX|← Índice]] | [[06_docs/JARVIS_OS/SKILLS_CATALOG|📘 Catálogo de Skills]] | [[06_docs/JARVIS_OS/README|🌟 JARVIS OS]]

Escánea lo que se mueve en tus datos. Detecta patrones, cambios inesperados y oportunidades.

## Descripción
El skill **Tendencias** analiza el movimiento en tus datos a lo largo del tiempo. Es tu sistema de detección de anomalías y reconocimiento de patrones.

## Qué Hace
- 📈 Análisis de series temporales
- 🔍 Detección de anomalías automática
- 🎯 Identificación de patrones y ciclos
- ⚠️ Alertas sobre cambios significativos
- 💡 Sugerencias basadas en tendencias

## Parámetros de Activación
```python
"¿qué tendencias hay?"
"escánea lo que se mueve"
"análisis de patrones"
"detecta cambios"
"dame tendencias"
```

## Flujo de Trabajo
1. **Carga histórico** → Últimos 90 días de métricas
2. **Calcula** → Velocidad de cambio, correlaciones
3. **Detecta** → Anomalías usando z-score/IQR
4. **Identifica** → Patrones y ciclos (semanal, mensual)
5. **Alerta** → Reporta cambios significativos (>15% delta)

## Entrada
- Datos: `01_systems/KALMIYA/raw/metricas/historico.json`
- Período: 90 días anterior
- Granularidad: Diaria

## Salida
```
### 📊 ANÁLISIS DE TENDENCIAS
**Período: Últimos 30 días**

#### 📈 Tendencias Principales
- **Suscripciones**: ↗️ +4.2% (aceleración)
- **Vistas**: ↘️ -2.1% (desaceleración)
- **Seguidores**: ↗️ Estable (+0.1%)

#### ⚠️ Anomalías Detectadas
1. Pico anómalo el 2026-08-05 (264% vistas normales)
   - Causa probable: Post viral
   - Replicar contenido similar

#### 🎯 Patrones Detectados
- Ciclo semanal: Máx. vistas viernes (2x promedio)
- Correlación: Seguidores ↔ Tiempo en redes (+0.78)
- Ventana óptima: 7-9 PM para máximo engagement
```

## Archivos Relacionados
- `01_systems/KALMIYA_System/kalmiya_system_info.py` — Estadísticas
- `01_systems/LLM_Wiki/wiki/tendencias/` — Análisis histórico

## Notas
- Ejecutar diariamente a las 2:00 PM
- Umbral de anomalía: ±2 desviaciones estándar
- Reportar solo cambios > 15% significativos

---
**Creado:** 2026-08-12  
**Estado:** Implementado ✅

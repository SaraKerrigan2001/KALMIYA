# SKILL: Biometría (Identity + Health)

[[INDEX|← Índice]] | [[06_docs/JARVIS_OS/SKILLS_CATALOG|📘 Catálogo de Skills]] | [[06_docs/JARVIS_OS/README|🌟 JARVIS OS]]

Conoce tu estado físico: ritmo cardíaco, sueño, ubicación, dispositivos conectados.

## Descripción
El skill **Biometría** monitorea tu biología y entorno. Integra datos de dispositivos wearables, sensores, y sistemas para construir un perfil en tiempo real de tu estado.

## Qué Hace
- 💓 Monitoreo de ritmo cardíaco (pulsera, reloj)
- 😴 Análisis de sueño y descanso
- 📍 Ubicación y movimiento
- 🌡️ Temperatura corporal y ambiente
- 📱 Devicelist: Conectados, activos
- 🔋 Batería y salud de dispositivos

## Parámetros de Activación
```python
"¿cómo estoy?"
"estado de salud"
"¿qué dispositivos tengo conectados?"
"análisis biométrico"
"mi ritmo cardíaco"
```

## Flujo de Trabajo
1. **Consulta** → Dispositivos wearables, sensores
2. **Agrega** → Datos de última hora
3. **Analiza** → Patrones, anomalías
4. **Integra** → Con contexto de actividad
5. **Reporta** → Estado de salud actual

## Entrada
- Wearables: Fitbit, Apple Watch, Garmin
- Sensores: Temperatura, humedad (si aplica)
- Ubicación: GPS, WiFi triangulation
- Dispositivos: Bluetooth, red local

## Salida
```
### 💓 ESTADO BIOMÉTRICO
**2026-08-12 | 14:35**

#### 🫀 Ritmo Cardíaco
- **Actual**: 72 bpm
- **Promedio hoy**: 68 bpm
- **Estado**: Normal ✓

#### 😴 Sueño Anoche
- **Duración**: 7h 24m
- **Calidad**: 82% (Buena)
- **REM**: 1h 52m
- **Despertares**: 2

#### 📍 Ubicación + Ambiente
- **Ubicación**: Oficina (WiFi)
- **Temperatura**: 22°C
- **Humedad**: 45%

#### 📱 Dispositivos Conectados (6)
✓ iPhone 15 Pro (100%)
✓ Apple Watch Ultra (87%)
✓ AirPods Pro (91%)
✓ MacBook Pro (AC)
✓ Fitbit Sense 2 (78%)
✓ Smart Home Hub (AC)

#### ⚠️ Alertas
- Ninguna
```

## Archivos Relacionados
- `01_systems/KALMIYA_System/kalmiya_biometrics.py` — Captura biométrica
- `01_systems/KALMIYA_System/config/devices_config.json` — Config de dispositivos
- `01_systems/KALMIYA/raw/biometria/` — Histórico

## Notas
- Sincronización cada 5 minutos
- Guardar histórico en `01_systems/KALMIYA/raw/biometria/`
- Alertas si ritmo cardíaco > 100 o < 50 bpm
- Privacidad: Datos nunca salen del disco local

---
**Creado:** 2026-08-12  
**Estado:** Implementado ✅

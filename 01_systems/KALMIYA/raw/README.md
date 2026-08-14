# 📂 raw/ - Datos Crudos

Aquí se almacenan los datos capturados en bruto sin procesar.

## Estructura

### `calendario/`
- Eventos del calendario en formato JSON/ICS
- Sincronización: Diaria a las 6:00 AM
- Archivos: `eventos_YYYY-MM-DD.json`

### `mensajes/`
- Mensajes recibidos (Telegram, Email, etc.)
- Formato: JSON con timestamp
- Sincronización: Diaria a las 7:00 AM

### `metricas/`
- Números crudos de plataformas
- Archivo principal: `historico.json`
- Archivo diario: `YYYY-MM-DD.json`
- Sincronización: Diaria a las 7:30 AM

### `biometria/`
- Datos de wearables (ritmo cardíaco, sueño)
- Formato: JSON con timestamp
- Sincronización: Cada 5 minutos
- Archivos: `dispositivo_YYYY-MM-DD.json`

### `eventos/`
- Eventos del sistema (logs, alertas)
- Sincronización: Continua
- Archivos: `eventos_YYYY-MM-DD.log`

## Política

- ✅ NO procesar aquí
- ✅ Guardar todo lo capturado
- ✅ Mantener histórico completo
- ✅ Estructura de carpetas por tipo

## Automatización

Ver configuración de sincronización en: `01_systems/KALMIYA_System/config/sync_config.json`

---
**Última actualización**: 2026-08-12

# 🧹 Guía de Limpieza de KALMIYA

## Scripts disponibles

### 1. limpieza_automatica.py
Script que elimina:
- `__pycache__/` (cachés de Python)
- `*.pyc`, `*.pyo` (archivos compilados)
- `.pytest_cache/`, `.mypy_cache/` (cachés de testing)
- `_TEMP/` (archivos temporales)
- `temp_audio/` (archivos de audio temporales)
- `chat_history.json` (historial de chat)

**Uso:**
```bash
python 05_tests/limpieza_automatica.py
```

### 2. analizar_memoria.py
Analiza:
- Tamaño de archivos Python
- Módulos importados (qué usa más memoria)
- Uso de memoria del chat

**Uso:**
```bash
python 05_tests/analizar_memoria.py
```

## Estadísticas actuales

### Tamaño del proyecto
- **Total archivos:** 166
- **Total tamaño:** 1.4 MB

### Módulos más usados
| Módulo | Archivos |
|--------|----------|
| os | 56 |
| datetime | 53 |
| pathlib | 39 |
| sys | 33 |
| json | 32 |

### Uso de memoria del chat
- **Importación:** 67.89 MB (pico: 69.51 MB)
- **Instancia:** ~0 MB (el chat usa memoria dinámica)

## Optimización

Para mantener tu sistema limpio:
1. Ejecuta `limpieza_automatica.py` semanalmente
2. Usa `analizar_memoria.py` si notas lentitud
3. Monitorea el uso de memoria con el Administrador de tareas

## Notas
- El script `limpieza_automatica.py` está listo para ejecutarse
- El script `analizar_memoria.py` está listo para diagnosticar problemas

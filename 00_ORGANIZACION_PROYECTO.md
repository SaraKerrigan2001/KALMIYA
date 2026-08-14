# Organización del proyecto KALMIYA

## Mapa general

```text
ENV/
├── 00_docs_chat/         # documentación del chat y guías de uso
├── 00_docs_project/      # documentación técnica del proyecto
├── 00_docs_updates/      # resúmenes y actualizaciones
├── 01_systems/           # sistemas principales
│   ├── KALMIYA/
│   ├── KALMIYA_System/
│   ├── LLM_Wiki/
│   └── RAPTOR/
├── 02_infrastructure/    # entorno virtual y recursos de infraestructura
├── 03_launchers/         # scripts de arranque y acceso rápido
├── 04_config/            # configuración y dependencias
├── 05_tests/             # pruebas reales del proyecto
├── 06_docs/              # documentación general y arquitectura
├── 07_notes/             # apuntes y notas
├── 08_reports/           # reportes y análisis
├── _BACKUPS/
├── _TEMP/
├── _UNUSED/
├── .skills/
├── .venv/
├── .venv313/
├── 00_ORGANIZACION_PROYECTO.md
├── INDEX.md
├── KALMIYA_DASHBOARD.md
├── README.md
├── WELCOME.md
├── LICENSE
├── pytest.ini
├── Desktop_Files/
└── .git/
```

## Dónde está cada parte

### Sistema principal

- [01_systems/KALMIYA_System/](01_systems/KALMIYA_System/)
- [01_systems/KALMIYA_System/main.py](01_systems/KALMIYA_System/main.py)
- [01_systems/KALMIYA_System/ui/](01_systems/KALMIYA_System/ui/)
- [01_systems/KALMIYA_System/intelligence/](01_systems/KALMIYA_System/intelligence/)

### Lanzadores

- [03_launchers/chat.py](03_launchers/chat.py)
- [03_launchers/chat_simple.py](03_launchers/chat_simple.py)
- [03_launchers/chat_ultra.py](03_launchers/chat_ultra.py)
- [03_launchers/chat_optimized.py](03_launchers/chat_optimized.py)
- [03_launchers/start_chat.py](03_launchers/start_chat.py)

### Documentación

- [README.md](README.md)
- [INDEX.md](INDEX.md)
- [WELCOME.md](WELCOME.md)
- [00_docs_chat/](00_docs_chat/)
- [00_docs_updates/](00_docs_updates/)
- [06_docs/](06_docs/)
- [07_notes/](07_notes/)
- [08_reports/](08_reports/)

### Pruebas

- [05_tests/](05_tests/)
- [05_tests/test_open_chat_paths.py](05_tests/test_open_chat_paths.py)
- [pytest.ini](pytest.ini)

## Regla de uso

- Mantener la documentación general en la raíz.
- Mantener la documentación de detalle en 00_docs_* y 06_docs/.
- Mantener los lanzadores en 03_launchers/.
- Mantener pruebas reales en 05_tests/.
- Mantener artefactos temporales en _TEMP, _UNUSED y _BACKUPS.

## Estado actual

El repositorio ya está reorganizado en capas funcionales y la validación del núcleo quedó verificada en Python 3.13.

## Siguiente ajuste recomendado

- Limpiar scripts de diagnóstico para que no se mezclen con pruebas reales.
- Dejar un README y un índice más estables para onboarding.
- Revisar dependencias opcionales del audio y del acceso a Google para que el entorno sea más predecible.

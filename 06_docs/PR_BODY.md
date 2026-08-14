---
title: "Template de PR Body"
tags: [pr, template, github]
ubicacion: 06_docs/PR_BODY.md
---

# 📝 Template de Pull Request Body

[[INDEX|← Índice]] | [[06_docs/CONTRIBUTING|🤝 Contribuir]]

---

## Resumen

Este PR integra varias mejoras y correcciones menores que hacen más robusta la experiencia del chat y la organización del repositorio.

### Cambios principales

- Añade un selector de estilo en la UI del chat (`01_systems/KALMIYA_System/ui/kalmiya_chat.py`) y una barra de contexto para mostrar intención y estilo.
- Implementa `modules/advanced_capabilities.py` con motores ligeros: `PersonalityStyleEngine`, `ResponsePredictionEngine`, `IoTCommandParser`, `BehaviorAnalytics` y `LocalBlockchainLedger`.
- Corrige la lógica de `open_chat` para buscar `kalmiya_chat.py` en rutas alternativas y usar el directorio padre como `cwd` al lanzar el proceso.
- Añade documentación base (`README.md`) en `01_systems`, `02_infrastructure`, `03_launchers`, `04_config`, `05_tests`, `07_notes`, `08_reports` y `ROOT_STRUCTURE.md`.
- Añade tests y utilidades: `05_tests/conftest.py`, `05_tests/test_advanced_capabilities.py`, `05_tests/test_chat_style_selector.py`, `05_tests/test_personality_style.py`, `05_tests/test_reasoning_features.py`.

### Pruebas locales

- Suite de pruebas: `30 passed, 12 warnings` (ejecución local en Windows, Python 3.14)

### Nota sobre CI

- El workflow CI está configurado en `.github/workflows/ci.yml` y se ejecuta contra `main` en `push`/`pull_request`.
- Recomiendo revisar las 12 advertencias de pytest y, si lo deseas, permitir ejecuciones de CI en pushes a ramas feature temporalmente.

### Siguientes pasos sugeridos

1. Revisión de código y aprobación.
2. Merge a `main` tras revisión. CI se ejecutará automáticamente.
3. (Opcional) Corregir warnings en pruebas y añadir `customtkinter` al entorno CI si la UI requiere pruebas adicionales.

---

**Autogenerado por el flujo de trabajo local de desarrollo.**

[[06_docs/CONTRIBUTING|← Ver guía de contribución]]

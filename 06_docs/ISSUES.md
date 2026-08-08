# Reportar Issues en KALMIYA

Gracias por contribuir a KALMIYA. Si encuentras un error, un comportamiento inesperado, o una idea de mejora, usa esta guía para reportarlo claramente.

## Qué incluir en un issue

1. **Título claro**
   - Describe brevemente el problema o la mejora.

2. **Descripción**
   - ¿Qué esperabas que ocurriera?
   - ¿Qué ocurrió en realidad?

3. **Pasos para reproducir**
   - Lista los pasos exactos que seguiste.
   - Ejemplo:
     1. Abrir `main.py`
     2. Ejecutar `python 01_systems/KALMIYA_System/main.py`
     3. Decir `kalmiya` y pedir que abra música

4. **Entorno**
   - Sistema operativo: Windows 10/11
   - Python versión
   - ¿Usaste entorno virtual?
   - ¿Corriste desde PowerShell o desde el lanzador?

5. **Salida o logs**
   - Incluye mensajes de error completos si aparecen.
   - Si no hay error, describe el resultado observable.

6. **Archivos relevantes**
   - Si conoces el módulo o archivo relacionado (`voz.py`, `kalmiya_core.py`, etc.), menciónalo.

## Buenas prácticas

- Revisa issues existentes antes de abrir uno nuevo.
- No incluyas contraseñas ni datos personales.
- Si propones una mejora, explica cómo ayudaría al proyecto.
- Mantén los reports objetivos y respetuosos.

## Tipos de issues

- `Bug`: comportamiento incorrecto o falla del sistema.
- `Feature`: nueva funcionalidad o mejora.
- `Docs`: corrección o mejora en la documentación.

## Ejemplo de issue

**Título:** Error al iniciar el asistente en Windows 11

**Descripción:** Al ejecutar `python 01_systems/KALMIYA_System/main.py` el sistema muestra un error en `voz.py` y no se inicia la escucha de voz.

**Pasos para reproducir:**
1. Abrir PowerShell en `c:\Users\maria\env`
2. Activar el entorno virtual
3. Ejecutar `python 01_systems/KALMIYA_System/main.py`

**Entorno:**
- Windows 11
- Python 3.11
- Entorno virtual activado

**Salida:**
- Mensaje de error completo o captura de pantalla si es posible.

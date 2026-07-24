# Contributing to KALMIYA

Gracias por tu interés en contribuir a KALMIYA. Este documento describe cómo colaborar de forma ordenada y segura.

## 1. Fork y clonación

1. Haz fork del repositorio en GitHub.
2. Clona tu fork en tu equipo:
   ```bash
git clone https://github.com/SaraKerrigan2001/KALMIYA.git
cd KALMIYA
```

## 2. Crea una rama de trabajo

Usa nombres claros y descriptivos para las ramas:

```bash
git checkout -b feature/nombre-del-ajuste
```

## 3. Haz cambios pequeños y específicos

- Realiza cambios bien delimitados.
- Añade una breve descripción útil en cada commit.
- Evita incluir datos personales o secretos.

## 4. Pruebas y revisión

- Ejecuta las pruebas relevantes en `05_tests/` si aplican.
- Verifica que el código se ejecute en Windows.
- Asegúrate de que no se suban archivos temporales ni credenciales.

## 5. Envía un pull request

1. Sube tu rama al fork:
   ```bash
git push origin feature/nombre-del-ajuste
```
2. Abre un pull request contra la rama `main` del repositorio original.
3. Describe claramente los cambios y por qué son necesarios.

## 6. Buenas prácticas

- Mantén el código legible y bien comentado.
- Sigue la estructura del proyecto y usa nombres de archivo consistentes.
- Actualiza la documentación cuando agregues nuevas funciones.
- Añade ejemplos de uso si mejoras comandos o interfaz.

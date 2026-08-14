---
title: "Instrucciones GitHub - Proyecto Elementos"
tags: [github, instrucciones, proyecto]
---

# 📤 Instrucciones para Subir el Proyecto a GitHub

[[INDEX|← Índice Principal]] | [[06_docs/OneDrive_Docs/GitHub/proyecto_elementos/README|📄 README Proyecto]] | [[06_docs/OneDrive_Docs/GitHub/proyecto_elementos/CHECKLIST_GITHUB|✅ Checklist]]

## ✅ Estado Actual
- Repositorio remoto ya configurado: https://github.com/AALGarcia/proyecto_elementos.git
- Rama actual: `desarrollo`
- Archivos modificados listos para commit

## 🚀 Pasos para Subir los Cambios

### 1. Agregar los archivos al staging area

```bash
git add .gitignore
git add README.md
git add .env.example
git add package-lock.json
```

### 2. Hacer commit de los cambios

```bash
git commit -m "docs: Mejorar documentación y configuración para GitHub

- Actualizar .gitignore (remover package-lock.json de ignore)
- Mejorar README con instrucciones completas
- Agregar .env.example para configuración
- Preparar proyecto para colaboración"
```

### 3. Subir los cambios a GitHub

```bash
git push origin desarrollo
```

### 4. (Opcional) Crear una rama main si no existe

Si quieres tener una rama principal estable:

```bash
# Crear rama main desde desarrollo
git checkout -b main

# Subir la rama main
git push -u origin main

# Volver a desarrollo
git checkout desarrollo
```

### 5. (Opcional) Configurar rama por defecto en GitHub

1. Ve a tu repositorio en GitHub
2. Settings → Branches
3. Cambia la rama por defecto a `main` (si la creaste)

## 📋 Comandos Rápidos (Todo en uno)

Si quieres ejecutar todo de una vez:

```bash
git add .gitignore README.md .env.example package-lock.json && git commit -m "docs: Mejorar documentación y configuración para GitHub" && git push origin desarrollo
```

## 🔐 Configuración Adicional Recomendada

### Proteger información sensible

Antes de hacer push, asegúrate de:

1. ✅ Verificar que `.env` NO esté en el repositorio
2. ✅ Verificar que las contraseñas estén en `.env` y no hardcodeadas
3. ✅ Revisar que `node_modules/` esté en `.gitignore`

### Verificar archivos que se subirán

```bash
git status
```

### Ver diferencias antes de commit

```bash
git diff
```

## 📝 Después de Subir

### Crear un Release (Opcional)

1. Ve a tu repositorio en GitHub
2. Click en "Releases" → "Create a new release"
3. Tag version: `v1.0.0`
4. Release title: "Primera versión estable"
5. Descripción: Características principales del sistema

### Agregar Topics al Repositorio

En GitHub, agrega estos topics para mejor visibilidad:
- `react`
- `vite`
- `nodejs`
- `express`
- `postgresql`
- `tailwindcss`
- `sena`
- `inventory-management`

### Configurar GitHub Pages (Opcional)

Si quieres una demo en línea:
1. Settings → Pages
2. Source: GitHub Actions
3. Crear workflow para deploy automático

## 🤝 Colaboración

### Clonar el proyecto (para otros desarrolladores)

```bash
git clone https://github.com/AALGarcia/proyecto_elementos.git
cd proyecto_elementos
npm install
cp .env.example .env
# Editar .env con credenciales locales
npm run dev
```

### Crear Issues

Documenta bugs o mejoras en la sección "Issues" de GitHub

### Pull Requests

Para contribuciones:
1. Fork del repositorio
2. Crear rama feature
3. Hacer cambios
4. Crear Pull Request

## ⚠️ Importante

**NUNCA subas:**
- ❌ Archivos `.env` con contraseñas reales
- ❌ `node_modules/`
- ❌ Credenciales de base de datos
- ❌ Tokens o API keys

**SIEMPRE verifica:**
- ✅ `.gitignore` está actualizado
- ✅ README está completo
- ✅ `.env.example` tiene todas las variables necesarias
- ✅ El código compila sin errores

## 📞 Soporte

Si tienes problemas:
1. Revisa la documentación de Git
2. Verifica tu conexión a GitHub
3. Asegúrate de tener permisos en el repositorio

---

[[CONTRIBUTING|🤝 Guía de Contribución KALMIYA]] | [[06_docs/OneDrive_Docs/GitHub/proyecto_elementos/CHECKLIST_GITHUB|✅ Checklist GitHub]] | [[06_docs/OneDrive_Docs/GitHub/proyecto_elementos/README|📄 README proyecto_elementos]]

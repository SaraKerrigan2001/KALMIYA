# 🏢 Sistema de Gestión de Bienes - SENA

Sistema web moderno para la gestión integral de inventario, asignación de bienes y control de cuentadantes del SENA.

## ✨ Características Principales

- 🎨 **Interfaz Moderna**: Diseño responsive con modo claro/oscuro
- 🌍 **Multiidioma**: Soporte para Español, Inglés y Portugués
- 📊 **Dashboard Interactivo**: Estadísticas y métricas en tiempo real
- 🔍 **Búsqueda Avanzada**: Sistema de búsqueda inteligente unificada
- 📱 **Responsive**: Optimizado para dispositivos móviles y tablets
- 🔐 **Sistema de Autenticación**: Control de acceso seguro
- 📋 **Gestión Completa**: CRUD de bienes, cuentadantes y asignaciones

## 🚀 Tecnologías

- **Frontend:** React 18 + Vite 5
- **Backend:** Node.js + Express 5
- **Base de Datos:** PostgreSQL 14+
- **Estilos:** Tailwind CSS 3 + CSS personalizado
- **Iconos:** Lucide React

## 📋 Requisitos Previos

- Node.js v18 o superior
- PostgreSQL v14 o superior
- npm o yarn
- Git

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/proyecto_elementos.git
cd proyecto_elementos
```

### 2. Instalar dependencias

```bash
npm install
```

### 3. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto basándote en `.env.example`:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bd_elementos
DB_USER=postgres
DB_PASSWORD=tu_contraseña
SERVER_PORT=3001
VITE_PORT=3000
```

### 4. Configurar la base de datos

Ejecuta el script SQL en pgAdmin o psql:

```bash
psql -U postgres -f src/config/bd_elementos_completo.sql
```

O manualmente en pgAdmin:
- Abre pgAdmin
- Crea una nueva base de datos llamada `bd_elementos`
- Ejecuta el script `src/config/bd_elementos_completo.sql`

## ▶️ Ejecución

### Modo Desarrollo

**Opción 1: Ejecutar ambos servidores simultáneamente**

Terminal 1 - Backend:
```bash
npm run server
```

Terminal 2 - Frontend:
```bash
npm run dev
```

**Opción 2: Usar concurrently (recomendado)**

```bash
npm install -g concurrently
concurrently "npm run server" "npm run dev"
```

### Acceder a la aplicación

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:3001/api

### Modo Producción

```bash
# Construir el frontend
npm run build

# Previsualizar el build
npm run preview
```

## 📁 Estructura del Proyecto

```
proyecto_elementos/
├── src/
│   ├── components/          # Componentes React
│   │   ├── Dashboard.jsx
│   │   ├── AuthScreen.jsx
│   │   ├── BienesTable.jsx
│   │   └── ...
│   ├── contexts/            # Context API (Estado global)
│   │   ├── AuthContext.jsx
│   │   ├── DataContext.jsx
│   │   ├── ThemeContext.jsx
│   │   └── ...
│   ├── hooks/              # Custom hooks
│   │   ├── useNotifications.js
│   │   └── useTranslation.js
│   ├── locales/            # Archivos de traducción
│   │   ├── es.js
│   │   ├── en.js
│   │   └── pt.js
│   ├── assets/             # CSS e imágenes
│   │   ├── css/
│   │   └── js/
│   ├── config/             # Configuración y scripts SQL
│   │   ├── conexion.js
│   │   └── bd_elementos_completo.sql
│   ├── App.jsx             # Componente principal
│   ├── main.jsx            # Punto de entrada
│   └── index.css           # Estilos globales
├── server/                 # Backend Express
│   └── index.js            # Servidor y API REST
├── public/                 # Archivos estáticos
├── index.html              # HTML principal
├── vite.config.js          # Configuración de Vite
├── tailwind.config.js      # Configuración de Tailwind
├── package.json            # Dependencias
└── README.md              # Este archivo
```

## 🎯 Funcionalidades

### Gestión de Bienes
- ✅ Crear, editar y visualizar bienes
- ✅ Categorización por tipo
- ✅ Control de estados (disponible, asignado)
- ✅ Registro de valores y fechas de ingreso
- ✅ Búsqueda y filtrado avanzado

### Gestión de Cuentadantes
- ✅ Registro de cuentadantes
- ✅ Información de contacto
- ✅ Asignación de áreas y cargos
- ✅ Control de estado activo/inactivo

### Asignaciones
- ✅ Asignar múltiples bienes a cuentadantes
- ✅ Historial de asignaciones
- ✅ Desasignación de bienes
- ✅ Seguimiento de fechas

### Dashboard
- ✅ Estadísticas en tiempo real
- ✅ Últimos movimientos
- ✅ Alertas del sistema
- ✅ Gráficos y métricas

### Características Adicionales
- ✅ Modo oscuro/claro
- ✅ Multiidioma (ES/EN/PT)
- ✅ Notificaciones en tiempo real
- ✅ Diseño responsive
- ✅ Animaciones suaves

## 🔌 API Endpoints

### Bienes
- `GET /api/bienes` - Obtener todos los bienes
- `POST /api/bienes` - Crear nuevo bien
- `POST /api/bienes/:id/desasignar` - Desasignar bien

### Cuentadantes
- `GET /api/cuentadantes` - Obtener todos los cuentadantes
- `POST /api/cuentadantes` - Crear nuevo cuentadante

### Asignaciones
- `GET /api/asignaciones` - Obtener todas las asignaciones
- `POST /api/asignaciones` - Crear nueva asignación

## 🛠️ Scripts Disponibles

```bash
npm run dev          # Inicia el servidor de desarrollo
npm run build        # Construye para producción
npm run preview      # Previsualiza el build de producción
npm run server       # Inicia el servidor backend
```

## 🐛 Solución de Problemas

### Error de conexión a la base de datos

Verifica que:
- PostgreSQL esté corriendo
- Las credenciales en `.env` sean correctas
- La base de datos `bd_elementos` exista
- El usuario tenga permisos adecuados

### Puerto en uso

Si el puerto 3000 o 3001 está en uso:
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9
```

### Dependencias faltantes

```bash
rm -rf node_modules package-lock.json
npm install
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de uso educativo para el SENA.

## 👥 Autores

- **Desarrollador Principal** - [Tu Nombre](https://github.com/TU_USUARIO)

## 🙏 Agradecimientos

- SENA - Servicio Nacional de Aprendizaje
- Comunidad de React
- Contribuidores del proyecto

---

[[CONTRIBUTING|🤝 Guía de Contribución KALMIYA]] | [[06_docs/OneDrive_Docs/GitHub/proyecto_elementos/CHECKLIST_GITHUB|✅ Checklist GitHub]] | [[06_docs/OneDrive_Docs/GitHub/proyecto_elementos/INSTRUCCIONES_GITHUB|📤 Instrucciones GitHub]]

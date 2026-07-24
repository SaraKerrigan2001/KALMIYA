# 📁 Carpeta src/assets/js/

Esta carpeta contiene los componentes React en formato JavaScript (.js) del sistema SENA BIENES.

## 📋 Índice de Archivos

### 🔐 Autenticación y Seguridad
- **AuthScreen.js** - Pantalla de login y registro de usuarios
- **RecuperarPasswordModal.js** - Modal para recuperación de contraseña

### 📊 Dashboard y Navegación
- **Dashboard.js** - Componente principal del dashboard con gestión de vistas
- **Header.js** - Barra superior con fecha/hora, notificaciones y controles
- **Sidebar.js** - Menú lateral de navegación con opciones del sistema
- **StatsCards.js** - Tarjetas de estadísticas del dashboard

### 💻 Gestión de Bienes
- **BienesTable.js** - Tabla para listar y gestionar bienes tecnológicos
- **BienModal.js** - Modal para crear/editar bienes

### 👥 Gestión de Cuentadantes
- **CuentadantesTable.js** - Tabla para listar cuentadantes (responsables)
- **CuentadanteModal.js** - Modal para crear/editar cuentadantes

### 📋 Asignaciones
- **AsignacionesTable.js** - Historial de asignaciones de bienes
- **AsignacionModal.js** - Modal para realizar nuevas asignaciones

### 🔔 Notificaciones
- **NotificationCenter.js** - Centro de notificaciones con historial
- **NotificationContainer.js** - Contenedor de notificaciones toast

### ⚙️ Configuración y Perfil
- **ConfiguracionModal.js** - Modal de configuración del sistema
- **PerfilModal.js** - Modal para editar perfil de usuario
- **LanguageSelector.js** - Selector de idioma (ES/EN/PT)

### 🎨 UI/UX
- **LoadingScreen.js** - Pantalla de carga inicial del sistema

---

## 📝 Descripción Detallada de Archivos

### 🔐 AuthScreen.js
**Propósito:** Pantalla de autenticación del sistema

**Características:**
- Tabs para alternar entre Login y Registro
- Validación de formularios en tiempo real
- Integración con contexto de autenticación
- Enlace a recuperación de contraseña
- Animaciones y efectos visuales
- Partículas de fondo decorativas

**Props:**
- `onLogin` (Function): Callback ejecutado al iniciar sesión exitosamente

**Estados:**
- `isLogin`: Controla si muestra login (true) o registro (false)
- `formData`: Datos del formulario (correo, password, nombre, área, rol)
- `errors`: Errores de validación
- `isLoading`: Estado de carga durante autenticación

---

### 🔄 RecuperarPasswordModal.js
**Propósito:** Modal para recuperación de contraseña en 3 pasos

**Características:**
- Paso 1: Ingreso de correo electrónico
- Paso 2: Verificación de código de 6 dígitos
- Paso 3: Establecer nueva contraseña
- Validación en cada paso
- Modo demo con código visible

**Props:**
- `onClose` (Function): Callback para cerrar el modal

**Estados:**
- `step`: Paso actual (1-4)
- `formData`: Datos del formulario
- `codigoEnviado`: Código generado para verificación

---

### 📊 Dashboard.js
**Propósito:** Componente principal que orquesta todas las vistas del sistema

**Características:**
- Gestión de vistas (dashboard, bienes, cuentadantes, asignaciones)
- Control de modales (crear/editar)
- Sidebar responsive con overlay
- Renderizado condicional de contenido

**Props:**
- `onLogout` (Function): Callback para cerrar sesión

**Estados:**
- `activeView`: Vista actualmente seleccionada
- `showAsignacionModal`: Control de modal de asignaciones
- `showBienModal`: Control de modal de bienes
- `showCuentadanteModal`: Control de modal de cuentadantes
- `selectedBien`: Bien seleccionado para edición
- `selectedCuentadante`: Cuentadante seleccionado para edición
- `sidebarOpen`: Estado del sidebar (abierto/cerrado)

---

### 🎯 Header.js
**Propósito:** Barra superior del dashboard con información y controles

**Características:**
- Fecha y hora en tiempo real
- Estado del sistema y última sincronización
- Selector de idioma
- Botón de cambio de tema (claro/oscuro)
- Centro de notificaciones
- Botón hamburguesa para móviles

**Props:**
- `onMenuClick` (Function): Callback para abrir/cerrar sidebar en móviles

**Estados:**
- `currentDateTime`: Fecha y hora actual
- `lastSync`: Última sincronización
- `syncTimeAgo`: Tiempo transcurrido desde última sync

---

### 🗂️ Sidebar.js
**Propósito:** Menú lateral de navegación del sistema

**Características:**
- Logo y título SENA BIENES
- Información del usuario (clickeable para abrir perfil)
- Menú de navegación con 4 opciones
- Botones de configuración y cerrar sesión
- Responsive con overlay
- Indicador visual de vista activa

**Props:**
- `activeView` (String): Vista actualmente seleccionada
- `onViewChange` (Function): Callback para cambiar de vista
- `isOpen` (Boolean): Estado del sidebar
- `onClose` (Function): Callback para cerrar sidebar
- `onLogout` (Function): Callback para cerrar sesión

**Estados:**
- `showConfigModal`: Control de modal de configuración

**Menú de navegación:**
1. Dashboard - Vista general del sistema
2. Bienes - Gestión de bienes tecnológicos
3. Cuentadantes - Gestión de responsables
4. Asignaciones - Asignar bienes a cuentadantes

---

### 📈 StatsCards.js
**Propósito:** Tarjetas de estadísticas en el dashboard

**Características:**
- 4 tarjetas con métricas clave
- Iconos y colores diferenciados
- Animaciones al cargar
- Formato de números con separadores

**Props:**
- `stats` (Object): Objeto con estadísticas
  - `totalBienes`: Total de bienes registrados
  - `entradasHoy`: Nuevos ingresos del día
  - `salidasHoy`: Asignaciones del día
  - `alertas`: Notificaciones pendientes

**Tarjetas:**
1. Total Bienes (azul) - 💻
2. Entradas Hoy (verde) - 📥
3. Salidas Hoy (naranja) - 📤
4. Alertas (rojo) - ⚠️

---

### 💻 BienesTable.js
**Propósito:** Tabla para listar y gestionar bienes tecnológicos

**Características:**
- Búsqueda en tiempo real
- Filtro por estado (disponible, asignado, mantenimiento, baja)
- Badges de estado con colores
- Botón de editar
- Botón de desasignar (solo para bienes asignados)
- Información de asignación (cuentadante y fecha)
- Paginación con contador

**Props:**
- `onEdit` (Function): Callback para editar un bien

**Estados:**
- `searchTerm`: Término de búsqueda
- `filterEstado`: Filtro de estado seleccionado

**Columnas:**
- Código/Placa
- Descripción
- Categoría
- Estado
- Valor
- Fecha y Hora de Creación
- Ubicación
- Acciones

---

### ➕ BienModal.js
**Propósito:** Modal para crear o editar bienes

**Características:**
- Modo creación y edición
- Validación de formularios
- Campos: código, descripción, categoría, valor, ubicación, estado
- Categorías predefinidas
- Estados: disponible, asignado, mantenimiento, baja

**Props:**
- `bien` (Object|null): Bien a editar (null para crear nuevo)
- `onClose` (Function): Callback para cerrar modal

**Estados:**
- `formData`: Datos del formulario
- `errors`: Errores de validación
- `isLoading`: Estado de carga

---

### 👥 CuentadantesTable.js
**Propósito:** Tabla para listar cuentadantes (responsables de bienes)

**Características:**
- Búsqueda por nombre, cédula, cargo o área
- Badge de estado (activo/inactivo)
- Información de contacto (correo y teléfono)
- Botón de editar
- Fecha y hora de creación
- Contador de resultados

**Props:**
- `onEdit` (Function): Callback para editar un cuentadante

**Estados:**
- `searchTerm`: Término de búsqueda

**Columnas:**
- Cédula
- Nombre
- Cargo
- Área
- Contacto (correo y teléfono)
- Fecha y Hora de Creación
- Estado
- Acciones

---

### ➕ CuentadanteModal.js
**Propósito:** Modal para crear o editar cuentadantes

**Características:**
- Modo creación y edición
- Validación de formularios
- Validación de correo electrónico
- Campos: cédula, nombre, cargo, área, correo, teléfono
- Áreas predefinidas

**Props:**
- `cuentadante` (Object|null): Cuentadante a editar (null para crear)
- `onClose` (Function): Callback para cerrar modal

**Estados:**
- `formData`: Datos del formulario
- `errors`: Errores de validación
- `isLoading`: Estado de carga

---

### 📋 AsignacionesTable.js
**Propósito:** Historial de asignaciones de bienes a cuentadantes

**Características:**
- Búsqueda por cuentadante, descripción o bienes
- Formato de fecha en español
- Información detallada del cuentadante
- Lista de bienes asignados
- Descripción de la asignación
- Badge de estado "Completada"
- Estado vacío cuando no hay asignaciones

**Props:**
Ninguna

**Estados:**
- `searchTerm`: Término de búsqueda

**Información mostrada:**
- Fecha y hora de asignación
- Cuentadante (nombre, cargo, área, cédula)
- Bienes asignados (cantidad y lista)
- Descripción de la asignación

---

### ➕ AsignacionModal.js
**Propósito:** Modal para realizar nuevas asignaciones de bienes

**Características:**
- Selección de cuentadante con búsqueda inteligente
- Autocompletado de cuentadantes
- Selección múltiple de bienes disponibles
- Búsqueda de bienes por múltiples criterios
- Validación de formulario
- Contador de bienes seleccionados
- Solo muestra bienes disponibles

**Props:**
- `onClose` (Function): Callback para cerrar modal

**Estados:**
- `selectedCuentadante`: ID del cuentadante seleccionado
- `selectedBienes`: Array de IDs de bienes seleccionados
- `searchTerm`: Búsqueda de bienes
- `cuentadanteSearch`: Búsqueda de cuentadantes
- `showCuentadanteSuggestions`: Control de sugerencias
- `errors`: Errores de validación
- `isLoading`: Estado de carga

**Búsqueda inteligente:**
- Bienes: placa, descripción, modelo, serial, categoría, costo, fecha
- Cuentadantes: documento, nombre, área, cargo

---

### 🔔 NotificationCenter.js
**Propósito:** Centro de notificaciones con historial

**Características:**
- Panel desplegable
- Contador de notificaciones no leídas
- Iconos según tipo (success, error, warning, info)
- Tiempo relativo (hace X min/h/días)
- Botón para limpiar todas
- Botón para eliminar individual
- Estado vacío con mensaje
- Overlay para cerrar al hacer clic fuera

**Props:**
Ninguna

**Estados:**
- `isOpen`: Control de visibilidad del panel

**Tipos de notificación:**
- ✅ Success (verde)
- ❌ Error (rojo)
- ⚠️ Warning (amarillo)
- ℹ️ Info (azul)

---

### 🍞 NotificationContainer.js
**Propósito:** Contenedor de notificaciones toast (temporales)

**Características:**
- Notificaciones flotantes en esquina
- Auto-desaparición después de tiempo
- Iconos según tipo
- Hora de la notificación
- Botón para cerrar manualmente
- Animaciones de entrada/salida

**Props:**
Ninguna

**Tipos de notificación:**
- ✅ Success (verde)
- ❌ Error (rojo)
- ⚠️ Warning (amarillo)
- ℹ️ Info (azul)

---

### ⚙️ ConfiguracionModal.js
**Propósito:** Modal de configuración del sistema

**Características:**
- Configuración de apariencia (tema claro/oscuro/auto)
- Configuración de notificaciones
- Preferencias del sistema
- Guardado en localStorage
- Botón para restaurar valores predeterminados

**Props:**
- `onClose` (Function): Callback para cerrar modal

**Estados:**
- `config`: Objeto con todas las configuraciones
- `isLoading`: Estado de carga
- `successMessage`: Mensaje de éxito

**Secciones:**
1. **Apariencia**
   - Tema (claro/oscuro/auto)

2. **Notificaciones**
   - Notificaciones en pantalla
   - Sonido
   - Notificaciones por correo

3. **Preferencias**
   - Auto-guardado
   - Idioma (ES/EN/PT)
   - Ítems por página
   - Formato de fecha

---

### 👤 PerfilModal.js
**Propósito:** Modal para editar perfil de usuario

**Características:**
- Edición de información personal
- Validación de formularios
- Avatar del usuario
- Información de la cuenta (ID, rol, fecha de registro)
- Guardado con notificación

**Props:**
- `onClose` (Function): Callback para cerrar modal

**Estados:**
- `formData`: Datos del formulario
- `errors`: Errores de validación
- `isLoading`: Estado de carga
- `successMessage`: Mensaje de éxito

**Campos editables:**
- Nombre completo
- Correo electrónico
- Área
- Cargo
- Teléfono
- Dirección

**Información de cuenta (solo lectura):**
- ID de usuario
- Rol
- Fecha de registro

---

### 🌐 LanguageSelector.js
**Propósito:** Selector de idioma del sistema

**Características:**
- Menú desplegable con banderas
- 3 idiomas disponibles
- Indicador visual del idioma activo
- Checkmark en idioma seleccionado
- Cierre automático al seleccionar

**Props:**
Ninguna

**Estados:**
- `showMenu`: Control de visibilidad del menú

**Idiomas disponibles:**
- 🇪🇸 Español (es)
- 🇺🇸 English (en)
- 🇧🇷 Português (pt)

---

### ⏳ LoadingScreen.js
**Propósito:** Pantalla de carga inicial del sistema

**Características:**
- Logo animado
- Barra de progreso
- Mensajes de estado por etapas
- Partículas de fondo decorativas
- Indicadores de carga (dots animados)
- Información del sistema (versión)

**Props:**
Ninguna

**Estados:**
- `progress`: Progreso de carga (0-100)
- `status`: Mensaje de estado actual

**Etapas de carga:**
1. Inicializando módulos del sistema...
2. Cargando base de datos...
3. Verificando permisos...
4. Configurando interfaz...
5. Finalizando carga...

---

## 🎨 Convenciones de Código

### Estructura de Componentes
```javascript
// 1. Imports
import { useState } from 'react'
import { useContext } from '../contexts/...'

// 2. Definición del componente
const ComponentName = ({ props }) => {
  // 3. Hooks y estados
  const [state, setState] = useState(initialValue)
  
  // 4. Funciones auxiliares
  const handleFunction = () => {
    // lógica
  }
  
  // 5. Return con JSX
  return (
    <div>
      {/* Contenido */}
    </div>
  )
}

// 6. Export
export default ComponentName
```

### Nomenclatura
- **Componentes:** PascalCase (ej: `BienModal`)
- **Funciones:** camelCase (ej: `handleSubmit`)
- **Constantes:** camelCase (ej: `menuItems`)
- **CSS Classes:** kebab-case (ej: `bien-modal-container`)

### Comentarios
- Secciones principales con `// ============================================`
- Funciones importantes con JSDoc
- Comentarios inline para lógica compleja

---

## 🔗 Dependencias Principales

- **React** - Librería principal
- **lucide-react** - Iconos (usado en algunos componentes)
- **Contexts:**
  - `AuthContext` - Autenticación
  - `DataContext` - Datos del sistema
  - `ThemeContext` - Tema claro/oscuro
  - `LanguageContext` - Idioma
  - `NotificationContext` - Notificaciones

- **Hooks personalizados:**
  - `useNotifications` - Gestión de notificaciones
  - `useTranslation` - Traducciones

---

## 📦 Relación con otros archivos

```
src/
├── assets/
│   ├── js/          ← ESTA CARPETA (componentes en .js)
│   └── css/         ← Estilos CSS correspondientes
├── components/      ← Componentes en .jsx (usan los .js)
├── contexts/        ← Contextos de React
├── hooks/           ← Hooks personalizados
└── locales/         ← Archivos de traducción
```

**Nota:** Los archivos .jsx en `src/components/` importan los estilos CSS desde `src/assets/css/`, mientras que los archivos .js en esta carpeta son copias con rutas ajustadas.

---

## 🚀 Uso

Estos archivos son componentes React que se importan y utilizan en la aplicación principal. Cada archivo exporta un componente por defecto que puede ser importado así:

```javascript
import ComponentName from './assets/js/ComponentName'
```

---

## 📝 Notas Importantes

1. **Rutas de importación:** Los archivos en esta carpeta usan rutas relativas ajustadas (`../../contexts/`, `../../hooks/`, etc.)

2. **Estilos CSS:** Los componentes importan sus estilos desde `../css/NombreComponente.css`

3. **Validación:** Todos los formularios incluyen validación en tiempo real

4. **Responsive:** Todos los componentes son responsive y se adaptan a móviles

5. **Accesibilidad:** Se usan labels, títulos y alt text apropiados

6. **Internacionalización:** Muchos componentes usan el hook `useTranslation` para soporte multiidioma

---

**Última actualización:** Diciembre 2024
**Versión del sistema:** 2025.1
**Autor:** Sistema SENA BIENES

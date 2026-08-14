# Ejemplos de Uso de Componentes

[[INDEX|← Índice Principal]] | [[06_docs/OneDrive_Docs/GitHub/proyecto_elementos/README|📄 README proyecto]] | [[06_docs/OneDrive_Docs/GitHub/proyecto_elementos/CHECKLIST_GITHUB|✅ Checklist]] | [[06_docs/OneDrive_Docs/GitHub/proyecto_elementos/INSTRUCCIONES_GITHUB|📤 Instrucciones]]

Esta carpeta contiene archivos de ejemplo `App.jsx` para cada componente del sistema. Cada archivo muestra cómo usar un componente específico de forma independiente.

## 📋 Cómo usar estos ejemplos

### Método 1: Script Automático (Recomendado) ⚡

**Windows (PowerShell):**
```powershell
.\examples\cambiar-ejemplo.ps1 BienesTable
```

**Linux/Mac (Node.js):**
```bash
node examples/cambiar-ejemplo.js BienesTable
```

**Ver componentes disponibles:**
```powershell
.\examples\cambiar-ejemplo.ps1
```

**Restaurar App.jsx original:**
```powershell
.\examples\cambiar-ejemplo.ps1 restaurar
```

### Método 2: Manual

1. **Copia el contenido** del archivo de ejemplo que quieras probar
2. **Reemplaza** el contenido de `src/App.jsx` con el contenido copiado
3. **Guarda** el archivo
4. El navegador se recargará automáticamente mostrando el componente

### Método 3: Interfaz Visual

Abre `examples/index.html` en tu navegador para ver todos los ejemplos con una interfaz visual

## 📁 Archivos Disponibles

### Componentes de Autenticación

**`App-AuthScreen.jsx`**
- Pantalla de login y registro
- Incluye validación de formularios
- Cambio entre modo login/registro

**`App-LoadingScreen.jsx`**
- Pantalla de carga inicial del sistema
- Animaciones y barra de progreso
- Efectos visuales

### Componentes de Navegación

**`App-Header.jsx`**
- Encabezado con información del usuario
- Botón de cambio de tema (dark/light)
- Menú desplegable de usuario
- Notificaciones

**`App-Sidebar.jsx`**
- Menú lateral de navegación
- Cambio entre vistas
- Información del usuario
- Estado del sistema

### Componentes de Dashboard

**`App-Dashboard.jsx`**
- Panel principal completo
- Todas las vistas integradas
- Navegación entre secciones
- Gestión completa del sistema

**`App-StatsCards.jsx`**
- Tarjetas de estadísticas
- Métricas del sistema
- Diseño responsive

### Componentes de Bienes

**`App-BienesTable.jsx`**
- Tabla de bienes tecnológicos
- Búsqueda y filtros
- Paginación
- Acciones de edición

**`App-BienModal.jsx`**
- Modal para agregar/editar bienes
- Validación de formularios
- Categorías predefinidas
- Estados de bienes

### Componentes de Cuentadantes

**`App-CuentadantesTable.jsx`**
- Tabla de cuentadantes (responsables)
- Búsqueda por múltiples campos
- Información de contacto
- Estado activo/inactivo

**`App-CuentadanteModal.jsx`**
- Modal para agregar/editar cuentadantes
- Validación de correo y teléfono
- Áreas y cargos predefinidos

### Componentes de Asignación

**`App-AsignacionModal.jsx`**
- Modal para asignar bienes a cuentadantes
- Selección múltiple de bienes
- Búsqueda en tiempo real
- Validación de asignaciones

### Componentes de Notificaciones

**`App-NotificationContainer.jsx`**
- Sistema de notificaciones
- Diferentes tipos (success, error, warning, info)
- Auto-cierre y cierre manual
- Animaciones de entrada

## 🎯 Ejemplo de Uso

### Para probar el componente de Bienes:

1. Abre `examples/App-BienesTable.jsx`
2. Copia todo el contenido
3. Abre `src/App.jsx`
4. Reemplaza todo el contenido con lo copiado
5. Guarda el archivo
6. Ve al navegador y verás la tabla de bienes funcionando

### Para volver a la aplicación completa:

Simplemente restaura el contenido original de `src/App.jsx` o copia el contenido de `examples/App-Dashboard.jsx`

## 🔧 Estructura de los Ejemplos

Cada archivo de ejemplo incluye:

```jsx
// 1. Importaciones necesarias
import { ThemeProvider } from '../src/contexts/ThemeContext'
import ComponenteEjemplo from '../src/components/ComponenteEjemplo'

// 2. Función App con el componente
function App() {
  // Estados y funciones necesarias
  
  return (
    // Providers necesarios
    <ThemeProvider>
      <ComponenteEjemplo />
    </ThemeProvider>
  )
}

export default App
```

## 📝 Notas Importantes

- **Rutas de importación**: Los ejemplos asumen que están en la carpeta `examples/` y los componentes en `src/`
- **Contextos**: Cada ejemplo incluye solo los contextos (Providers) necesarios para ese componente
- **Datos de prueba**: Algunos ejemplos incluyen datos de ejemplo para demostración
- **Estilos**: Todos los ejemplos importan `./index.css` para mantener los estilos

## 🎨 Personalización

Puedes modificar estos ejemplos para:
- Probar diferentes estados del componente
- Agregar más datos de prueba
- Experimentar con diferentes props
- Combinar múltiples componentes

## 🚀 Componentes que Requieren Contextos

| Componente | ThemeProvider | AuthProvider | DataProvider |
|------------|---------------|--------------|--------------|
| AuthScreen | ✅ | ✅ | ❌ |
| Dashboard | ✅ | ✅ | ✅ |
| Header | ✅ | ✅ | ❌ |
| Sidebar | ✅ | ✅ | ❌ |
| BienesTable | ✅ | ❌ | ✅ |
| BienModal | ✅ | ❌ | ✅ |
| CuentadantesTable | ✅ | ❌ | ✅ |
| CuentadanteModal | ✅ | ❌ | ✅ |
| AsignacionModal | ✅ | ❌ | ✅ |
| StatsCards | ✅ | ❌ | ❌ |
| LoadingScreen | ❌ | ❌ | ❌ |
| NotificationContainer | ✅ | ❌ | ❌ |

## 💡 Tips

1. **Desarrollo aislado**: Usa estos ejemplos para desarrollar y probar componentes sin afectar el resto de la aplicación
2. **Debugging**: Facilita encontrar y corregir errores en componentes específicos
3. **Documentación**: Sirven como documentación viva de cómo usar cada componente
4. **Testing**: Útil para probar diferentes escenarios y casos de uso

## 🐛 Solución de Problemas

Si un ejemplo no funciona:
1. Verifica que las rutas de importación sean correctas
2. Asegúrate de que todos los contextos necesarios estén incluidos
3. Revisa la consola del navegador para errores
4. Verifica que el servidor de desarrollo esté corriendo (`npm run dev`)

---

[[06_docs/OneDrive_Docs/GitHub/proyecto_elementos/README|← README proyecto]] | [[CONTRIBUTING|🤝 Contribuir KALMIYA]]

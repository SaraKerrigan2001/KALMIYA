/**
 * EJEMPLO: Componente BienesTable
 * 
 * Este archivo demuestra cómo usar el componente BienesTable del sistema.
 * BienesTable es una tabla completa para gestionar los bienes tecnológicos
 * con funcionalidades de búsqueda, filtrado y edición.
 * 
 * CARACTERÍSTICAS:
 * - Listado completo de bienes con paginación
 * - Búsqueda en tiempo real por código, descripción, categoría o estado
 * - Filtros por categoría y estado
 * - Botón para agregar nuevos bienes
 * - Acciones de editar y eliminar por cada bien
 * - Diseño responsive con scroll horizontal en móviles
 * - Indicadores visuales de estado (Disponible, Asignado, Mantenimiento, Baja)
 * 
 * CONTEXTOS REQUERIDOS:
 * - ThemeProvider: Maneja el tema claro/oscuro
 * - DataProvider: Proporciona los datos de bienes y funciones CRUD
 * 
 * PROPS DEL COMPONENTE:
 * - onEdit: Función callback que se ejecuta al hacer clic en editar un bien
 *           Recibe el objeto del bien como parámetro
 */

// Importación de contextos necesarios
import { ThemeProvider } from '../src/contexts/ThemeContext'
import { DataProvider } from '../src/contexts/DataContext'

// Importación del componente de tabla de bienes
import BienesTable from '../src/components/BienesTable'

// Estilos globales de la aplicación
import './index.css'

function App() {
  // Manejador del evento de edición de un bien
  // Recibe el objeto completo del bien seleccionado
  const handleEdit = (bien) => {
    console.log('Editar bien:', bien)
    alert(`Editar: ${bien.descripcion}`)
    // En una aplicación real, aquí se abriría un modal de edición
  }

  return (
    // Envolver con los contextos necesarios
    <ThemeProvider>
      <DataProvider>
        {/* Contenedor principal con estilos responsive */}
        <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-6">
          {/* Título de la sección */}
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Tabla de Bienes
          </h1>
          {/* Componente de tabla con callback de edición */}
          <BienesTable onEdit={handleEdit} />
        </div>
      </DataProvider>
    </ThemeProvider>
  )
}

export default App

/**
 * EJEMPLO: Componente CuentadantesTable
 * 
 * Este archivo demuestra cómo usar el componente CuentadantesTable del sistema.
 * CuentadantesTable es una tabla completa para gestionar los cuentadantes
 * (personas responsables de los bienes) con funcionalidades de búsqueda y edición.
 * 
 * CARACTERÍSTICAS:
 * - Listado completo de cuentadantes con paginación
 * - Búsqueda en tiempo real por nombre, cédula, cargo o área
 * - Botón para agregar nuevos cuentadantes
 * - Acciones de editar y eliminar por cada cuentadante
 * - Muestra información de contacto (correo y teléfono)
 * - Indicador de estado activo/inactivo
 * - Diseño responsive con scroll horizontal en móviles
 * 
 * CONTEXTOS REQUERIDOS:
 * - ThemeProvider: Maneja el tema claro/oscuro
 * - DataProvider: Proporciona los datos de cuentadantes y funciones CRUD
 * 
 * PROPS DEL COMPONENTE:
 * - onEdit: Función callback que se ejecuta al hacer clic en editar un cuentadante
 *           Recibe el objeto del cuentadante como parámetro
 */

// Importación de contextos necesarios
import { ThemeProvider } from '../src/contexts/ThemeContext'
import { DataProvider } from '../src/contexts/DataContext'

// Importación del componente de tabla de cuentadantes
import CuentadantesTable from '../src/components/CuentadantesTable'

// Estilos globales de la aplicación
import './index.css'

function App() {
  // Manejador del evento de edición de un cuentadante
  // Recibe el objeto completo del cuentadante seleccionado
  const handleEdit = (cuentadante) => {
    console.log('Editar cuentadante:', cuentadante)
    alert(`Editar: ${cuentadante.nombre}`)
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
            Tabla de Cuentadantes
          </h1>
          {/* Componente de tabla con callback de edición */}
          <CuentadantesTable onEdit={handleEdit} />
        </div>
      </DataProvider>
    </ThemeProvider>
  )
}

export default App

/**
 * EJEMPLO: Componente AsignacionModal
 * 
 * Este archivo demuestra cómo usar el componente AsignacionModal del sistema.
 * AsignacionModal es un modal complejo para asignar bienes a cuentadantes responsables.
 * 
 * CARACTERÍSTICAS:
 * - Selección de cuentadante con información detallada
 * - Lista de bienes disponibles con búsqueda en tiempo real
 * - Selección múltiple de bienes (checkboxes)
 * - Validación: debe seleccionar cuentadante y al menos un bien
 * - Actualización automática de estados de bienes
 * - Registro de fecha de asignación
 * - Confirmación visual de asignación exitosa
 * - Diseño responsive con scroll en listas largas
 * - Animaciones de entrada y salida
 * 
 * CONTEXTOS REQUERIDOS:
 * - ThemeProvider: Maneja el tema claro/oscuro
 * - DataProvider: Proporciona datos de bienes, cuentadantes y función de asignación
 * 
 * PROPS DEL COMPONENTE:
 * - onClose: Función callback que se ejecuta al cerrar el modal
 * 
 * FLUJO DE USO:
 * 1. Usuario abre el modal
 * 2. Selecciona un cuentadante de la lista
 * 3. Busca y selecciona uno o más bienes disponibles
 * 4. Hace clic en "Realizar Asignación"
 * 5. El sistema actualiza los estados y registra la asignación
 */

// Importación del hook useState para manejar el estado del modal
import { useState } from 'react'

// Importación de contextos necesarios
import { ThemeProvider } from '../src/contexts/ThemeContext'
import { DataProvider } from '../src/contexts/DataContext'

// Importación del componente modal de asignación
import AsignacionModal from '../src/components/AsignacionModal'

// Estilos globales de la aplicación
import './index.css'

function App() {
  // Estado para controlar la visibilidad del modal
  const [showModal, setShowModal] = useState(false)

  return (
    // Envolver con los contextos necesarios
    <ThemeProvider>
      <DataProvider>
        {/* Contenedor principal */}
        <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-6">
          {/* Título de la sección */}
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Modal de Asignación de Bienes
          </h1>
          
          {/* Botón para abrir el modal de asignación */}
          <button
            onClick={() => setShowModal(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
          >
            Abrir Modal de Asignación
          </button>

          {/* Tarjeta con instrucciones de uso */}
          <div className="mt-6 bg-white dark:bg-gray-800 rounded-lg p-4">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Instrucciones:
            </h2>
            <ul className="list-disc list-inside text-gray-600 dark:text-gray-400 space-y-1">
              <li>Selecciona un cuentadante de la lista</li>
              <li>Busca y selecciona uno o más bienes disponibles</li>
              <li>Haz clic en "Realizar Asignación"</li>
            </ul>
          </div>

          {/* Renderizar el modal solo cuando showModal es true */}
          {showModal && (
            <AsignacionModal onClose={() => setShowModal(false)} />
          )}
        </div>
      </DataProvider>
    </ThemeProvider>
  )
}

export default App

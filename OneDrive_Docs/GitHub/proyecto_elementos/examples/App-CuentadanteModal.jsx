/**
 * EJEMPLO: Componente CuentadanteModal
 * 
 * Este archivo demuestra cómo usar el componente CuentadanteModal del sistema.
 * CuentadanteModal es un modal para agregar o editar cuentadantes (responsables de bienes).
 * 
 * CARACTERÍSTICAS:
 * - Formulario completo con validación de campos
 * - Modo agregar (cuando cuentadante es null) o editar (cuando tiene datos)
 * - Campos: cédula, nombre, cargo, área, correo, teléfono
 * - Validación de formato de correo y teléfono
 * - Validación en tiempo real
 * - Mensajes de error personalizados
 * - Botones de guardar y cancelar
 * - Cierre con tecla ESC o clic fuera del modal
 * - Animaciones de entrada y salida
 * 
 * CONTEXTOS REQUERIDOS:
 * - ThemeProvider: Maneja el tema claro/oscuro
 * - DataProvider: Proporciona funciones para agregar/editar cuentadantes
 * 
 * PROPS DEL COMPONENTE:
 * - cuentadante: Objeto del cuentadante a editar (null para agregar nuevo)
 * - onClose: Función callback que se ejecuta al cerrar el modal
 * 
 * ESTRUCTURA DEL OBJETO CUENTADANTE:
 * {
 *   id: number,
 *   cedula: string,
 *   nombre: string,
 *   cargo: string,
 *   area: string,
 *   correo: string (formato email),
 *   telefono: string
 * }
 */

// Importación del hook useState para manejar el estado del modal
import { useState } from 'react'

// Importación de contextos necesarios
import { ThemeProvider } from '../src/contexts/ThemeContext'
import { DataProvider } from '../src/contexts/DataContext'

// Importación del componente modal de cuentadantes
import CuentadanteModal from '../src/components/CuentadanteModal'

// Estilos globales de la aplicación
import './index.css'

function App() {
  // Estado para controlar la visibilidad del modal
  const [showModal, setShowModal] = useState(false)
  
  // Estado para almacenar el cuentadante seleccionado (null = agregar, objeto = editar)
  const [selectedCuentadante, setSelectedCuentadante] = useState(null)

  // Ejemplo de cuentadante para demostrar el modo de edición
  const cuentadanteEjemplo = {
    id: 1,
    cedula: '12345678',
    nombre: 'María González',
    cargo: 'Coordinadora Académica',
    area: 'Coordinación',
    correo: 'maria.gonzalez@sena.edu.co',
    telefono: '3001234567'
  }

  return (
    // Envolver con los contextos necesarios
    <ThemeProvider>
      <DataProvider>
        {/* Contenedor principal */}
        <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-6">
          {/* Título de la sección */}
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Modal de Cuentadantes
          </h1>
          
          {/* Botones para demostrar ambos modos del modal */}
          <div className="space-x-4">
            {/* Botón para abrir modal en modo AGREGAR (cuentadante = null) */}
            <button
              onClick={() => {
                setSelectedCuentadante(null)
                setShowModal(true)
              }}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg"
            >
              Agregar Nuevo Cuentadante
            </button>
            
            {/* Botón para abrir modal en modo EDITAR (cuentadante = objeto) */}
            <button
              onClick={() => {
                setSelectedCuentadante(cuentadanteEjemplo)
                setShowModal(true)
              }}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
            >
              Editar Cuentadante Ejemplo
            </button>
          </div>

          {/* Renderizar el modal solo cuando showModal es true */}
          {showModal && (
            <CuentadanteModal
              cuentadante={selectedCuentadante}  // null para agregar, objeto para editar
              onClose={() => {
                setShowModal(false)
                setSelectedCuentadante(null)
              }}
            />
          )}
        </div>
      </DataProvider>
    </ThemeProvider>
  )
}

export default App

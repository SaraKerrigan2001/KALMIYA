/**
 * EJEMPLO: Componente BienModal
 * 
 * Este archivo demuestra cómo usar el componente BienModal del sistema.
 * BienModal es un modal (ventana emergente) para agregar o editar bienes tecnológicos.
 * 
 * CARACTERÍSTICAS:
 * - Formulario completo con validación de campos
 * - Modo agregar (cuando bien es null) o editar (cuando bien tiene datos)
 * - Campos: código, descripción, categoría, estado, valor, ubicación
 * - Validación en tiempo real
 * - Mensajes de error personalizados
 * - Botones de guardar y cancelar
 * - Cierre con tecla ESC o clic fuera del modal
 * - Animaciones de entrada y salida
 * 
 * CONTEXTOS REQUERIDOS:
 * - ThemeProvider: Maneja el tema claro/oscuro
 * - DataProvider: Proporciona funciones para agregar/editar bienes
 * 
 * PROPS DEL COMPONENTE:
 * - bien: Objeto del bien a editar (null para agregar nuevo)
 * - onClose: Función callback que se ejecuta al cerrar el modal
 * 
 * ESTRUCTURA DEL OBJETO BIEN:
 * {
 *   id: number,
 *   codigo: string,
 *   descripcion: string,
 *   categoria: string,
 *   estado: 'disponible' | 'asignado' | 'mantenimiento' | 'baja',
 *   valor: number,
 *   ubicacion: string
 * }
 */

// Importación del hook useState para manejar el estado del modal
import { useState } from 'react'

// Importación de contextos necesarios
import { ThemeProvider } from '../src/contexts/ThemeContext'
import { DataProvider } from '../src/contexts/DataContext'

// Importación del componente modal de bienes
import BienModal from '../src/components/BienModal'

// Estilos globales de la aplicación
import './index.css'

function App() {
  // Estado para controlar la visibilidad del modal
  const [showModal, setShowModal] = useState(false)
  
  // Estado para almacenar el bien seleccionado (null = agregar, objeto = editar)
  const [selectedBien, setSelectedBien] = useState(null)

  // Ejemplo de bien para demostrar el modo de edición
  const bienEjemplo = {
    id: 1,
    codigo: 'HP-2024-001',
    descripcion: 'Computador HP EliteBook 840',
    categoria: 'Computadores',
    estado: 'disponible',
    valor: 2500000,
    ubicacion: 'Almacén Principal'
  }

  return (
    // Envolver con los contextos necesarios
    <ThemeProvider>
      <DataProvider>
        {/* Contenedor principal */}
        <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-6">
          {/* Título de la sección */}
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Modal de Bienes
          </h1>
          
          {/* Botones para demostrar ambos modos del modal */}
          <div className="space-x-4">
            {/* Botón para abrir modal en modo AGREGAR (bien = null) */}
            <button
              onClick={() => {
                setSelectedBien(null)
                setShowModal(true)
              }}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg"
            >
              Agregar Nuevo Bien
            </button>
            
            {/* Botón para abrir modal en modo EDITAR (bien = objeto) */}
            <button
              onClick={() => {
                setSelectedBien(bienEjemplo)
                setShowModal(true)
              }}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
            >
              Editar Bien Ejemplo
            </button>
          </div>

          {/* Renderizar el modal solo cuando showModal es true */}
          {showModal && (
            <BienModal
              bien={selectedBien}  // null para agregar, objeto para editar
              onClose={() => {
                setShowModal(false)
                setSelectedBien(null)
              }}
            />
          )}
        </div>
      </DataProvider>
    </ThemeProvider>
  )
}

export default App

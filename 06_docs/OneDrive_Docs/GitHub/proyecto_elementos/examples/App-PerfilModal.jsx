/**
 * EJEMPLO: Componente PerfilModal
 * 
 * Este archivo demuestra cómo usar el componente PerfilModal del sistema.
 * PerfilModal es un modal que permite al usuario ver y editar su información personal.
 * 
 * CARACTERÍSTICAS:
 * - Visualización de información del usuario autenticado
 * - Edición de datos personales (nombre, correo, teléfono)
 * - Actualización de información laboral (área, cargo)
 * - Validación de formularios en tiempo real
 * - Validación de formato de correo electrónico
 * - Guardado con confirmación visual
 * - Información de la cuenta (fecha de registro, último acceso)
 * - Avatar con iniciales del usuario
 * - Diseño responsive
 * 
 * CONTEXTOS REQUERIDOS:
 * - ThemeProvider: Maneja el tema claro/oscuro
 * - AuthProvider: Proporciona y actualiza la información del usuario
 * 
 * PROPS DEL COMPONENTE:
 * - onClose: Función callback que se ejecuta al cerrar el modal
 * 
 * DATOS DEL USUARIO:
 * Los datos se obtienen automáticamente del AuthContext y incluyen:
 * - Nombre completo
 * - Correo electrónico
 * - Teléfono
 * - Área de trabajo
 * - Cargo
 * - Fecha de registro
 * - Último acceso
 */

// Importación del hook useState para manejar el estado del modal
import { useState } from 'react'

// Importación de contextos necesarios
import { ThemeProvider } from '../src/contexts/ThemeContext'
import { AuthProvider } from '../src/contexts/AuthContext'

// Importación del componente modal de perfil
import PerfilModal from '../src/components/PerfilModal'

// Estilos globales de la aplicación
import '../src/index.css'

function App() {
  // Estado para controlar la visibilidad del modal (inicia visible para demo)
  const [showModal, setShowModal] = useState(true)

  return (
    // Envolver con los contextos necesarios
    <ThemeProvider>
      <AuthProvider>
        {/* Contenedor principal */}
        <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-6">
          {/* Título de la sección */}
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Modal de Perfil de Usuario
          </h1>
          
          {/* Tarjeta informativa con características */}
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 mb-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Características:
            </h2>
            <ul className="list-disc list-inside text-gray-600 dark:text-gray-400 space-y-2">
              <li>Editar información personal</li>
              <li>Actualizar correo y teléfono</li>
              <li>Cambiar área y cargo</li>
              <li>Validación de formularios</li>
              <li>Guardado con confirmación</li>
              <li>Información de la cuenta</li>
            </ul>
          </div>

          {/* Botón para abrir el modal */}
          <button
            onClick={() => setShowModal(true)}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg"
          >
            Abrir Modal de Perfil
          </button>

          {/* Renderizar el modal solo cuando showModal es true */}
          {showModal && (
            <PerfilModal onClose={() => setShowModal(false)} />
          )}
        </div>
      </AuthProvider>
    </ThemeProvider>
  )
}

export default App

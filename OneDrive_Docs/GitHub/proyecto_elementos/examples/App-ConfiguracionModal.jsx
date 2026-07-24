/**
 * EJEMPLO: Componente ConfiguracionModal
 * 
 * Este archivo demuestra cómo usar el componente ConfiguracionModal del sistema.
 * ConfiguracionModal es un modal completo para configurar las preferencias
 * del sistema y personalizar la experiencia del usuario.
 * 
 * CARACTERÍSTICAS:
 * - Cambio de tema (claro/oscuro/automático)
 * - Configuración de notificaciones (activar/desactivar)
 * - Control de sonidos del sistema
 * - Configuración de email para notificaciones
 * - Auto-guardado de cambios
 * - Selección de idioma de la interfaz
 * - Configuración de ítems por página en tablas
 * - Selección de formato de fecha
 * - Botón para restaurar valores predeterminados
 * - Persistencia de configuración en localStorage
 * - Organización por secciones (Apariencia, Notificaciones, General)
 * 
 * CONTEXTOS REQUERIDOS:
 * - ThemeProvider: Maneja el tema y aplica los cambios de configuración
 * 
 * PROPS DEL COMPONENTE:
 * - onClose: Función callback que se ejecuta al cerrar el modal
 * 
 * CONFIGURACIONES DISPONIBLES:
 * - Tema: light, dark, auto (según preferencia del sistema)
 * - Notificaciones: activadas/desactivadas
 * - Sonidos: activados/desactivados
 * - Email de notificaciones: dirección de correo
 * - Idioma: español, inglés, etc.
 * - Ítems por página: 10, 25, 50, 100
 * - Formato de fecha: DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD
 * 
 * NOTA: Todas las configuraciones se guardan automáticamente en localStorage
 */

// Importación del hook useState para manejar el estado del modal
import { useState } from 'react'

// Importación del contexto de tema
import { ThemeProvider } from '../src/contexts/ThemeContext'

// Importación del componente modal de configuración
import ConfiguracionModal from '../src/components/ConfiguracionModal'

// Estilos globales de la aplicación
import '../src/index.css'

function App() {
  // Estado para controlar la visibilidad del modal (inicia visible para demo)
  const [showModal, setShowModal] = useState(true)

  return (
    // Envolver con el contexto de tema
    <ThemeProvider>
      {/* Contenedor principal */}
      <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-6">
        {/* Título de la sección */}
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          Modal de Configuración del Sistema
        </h1>
        
        {/* Tarjeta informativa con características */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Características:
          </h2>
          <ul className="list-disc list-inside text-gray-600 dark:text-gray-400 space-y-2">
            <li>Cambiar tema (claro/oscuro/auto)</li>
            <li>Configurar notificaciones</li>
            <li>Activar/desactivar sonidos</li>
            <li>Configurar email de notificaciones</li>
            <li>Auto-guardado</li>
            <li>Seleccionar idioma</li>
            <li>Ítems por página</li>
            <li>Formato de fecha</li>
            <li>Restaurar valores predeterminados</li>
            <li>Persistencia en localStorage</li>
          </ul>
        </div>

        {/* Botón para abrir el modal de configuración */}
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
        >
          Abrir Configuración
        </button>

        {/* Renderizar el modal solo cuando showModal es true */}
        {showModal && (
          <ConfiguracionModal onClose={() => setShowModal(false)} />
        )}
      </div>
    </ThemeProvider>
  )
}

export default App

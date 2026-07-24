/**
 * EJEMPLO: Componente Sidebar
 * 
 * Este archivo demuestra cómo usar el componente Sidebar del sistema.
 * Sidebar es el menú lateral de navegación que permite cambiar entre
 * las diferentes secciones de la aplicación.
 * 
 * CARACTERÍSTICAS:
 * - Menú de navegación con iconos y etiquetas
 * - Indicador visual de la vista activa
 * - Opciones: Dashboard, Bienes, Cuentadantes, Asignaciones
 * - Efectos hover y transiciones suaves
 * - Diseño responsive (se oculta en móviles)
 * - Logo del SENA en la parte superior
 * - Colores del tema SENA (verde)
 * 
 * CONTEXTOS REQUERIDOS:
 * - ThemeProvider: Maneja el tema claro/oscuro
 * - AuthProvider: Proporciona información del usuario (opcional)
 * 
 * PROPS DEL COMPONENTE:
 * - activeView: String que indica la vista actualmente activa
 *               Valores: 'dashboard', 'bienes', 'cuentadantes', 'asignaciones'
 * - onViewChange: Función callback que se ejecuta al cambiar de vista
 *                 Recibe el nombre de la nueva vista como parámetro
 */

// Importación del hook useState para manejar la vista activa
import { useState } from 'react'

// Importación de contextos necesarios
import { ThemeProvider } from '../src/contexts/ThemeContext'
import { AuthProvider } from '../src/contexts/AuthContext'

// Importación del componente Sidebar
import Sidebar from '../src/components/Sidebar'

// Estilos globales de la aplicación
import './index.css'

function App() {
  // Estado para rastrear la vista actualmente activa
  const [activeView, setActiveView] = useState('dashboard')

  return (
    // Envolver con los contextos necesarios
    <ThemeProvider>
      <AuthProvider>
        {/* Contenedor flex para sidebar + contenido */}
        <div className="flex min-h-screen bg-gray-100 dark:bg-gray-900">
          {/* Componente Sidebar con vista activa y callback de cambio */}
          <Sidebar activeView={activeView} onViewChange={setActiveView} />
          
          {/* Área de contenido principal */}
          <div className="flex-1 p-6">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              Vista Activa: {activeView}
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              Haz clic en las opciones del menú lateral para cambiar de vista
            </p>
          </div>
        </div>
      </AuthProvider>
    </ThemeProvider>
  )
}

export default App

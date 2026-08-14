/**
 * EJEMPLO: Componente Header
 * 
 * Este archivo demuestra cómo usar el componente Header del sistema.
 * Header es la barra superior de navegación que muestra información del usuario
 * y opciones de configuración.
 * 
 * CARACTERÍSTICAS:
 * - Logo y título del sistema SENA
 * - Botón para alternar tema claro/oscuro
 * - Menú de usuario con dropdown
 * - Opciones: Perfil, Configuración, Cerrar sesión
 * - Avatar del usuario con iniciales
 * - Diseño responsive que se adapta a móviles
 * - Animaciones suaves en interacciones
 * 
 * CONTEXTOS REQUERIDOS:
 * - ThemeProvider: Maneja el tema claro/oscuro y el botón de alternancia
 * - AuthProvider: Proporciona información del usuario autenticado
 * 
 * PROPS DEL COMPONENTE:
 * - onLogout: Función callback que se ejecuta cuando el usuario cierra sesión
 */

// Importación de contextos necesarios
import { ThemeProvider } from '../src/contexts/ThemeContext'
import { AuthProvider } from '../src/contexts/AuthContext'

// Importación del componente Header
import Header from '../src/components/Header'

// Estilos globales de la aplicación
import './index.css'

function App() {
  // Manejador del evento de cierre de sesión
  // En una aplicación real, aquí se limpiaría el estado y se redirigiría al login
  const handleLogout = () => {
    console.log('Usuario cerró sesión')
    alert('Sesión cerrada')
  }

  return (
    // Envolver con los contextos necesarios
    <ThemeProvider>
      <AuthProvider>
        {/* Contenedor principal con altura completa */}
        <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
          {/* Componente Header con callback de logout */}
          <Header onLogout={handleLogout} />
          
          {/* Contenido de ejemplo debajo del header */}
          <div className="p-6">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              Contenido de la página
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              Este es un ejemplo del componente Header
            </p>
          </div>
        </div>
      </AuthProvider>
    </ThemeProvider>
  )
}

export default App

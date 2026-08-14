/**
 * EJEMPLO: Componente Dashboard
 * 
 * Este archivo demuestra cómo usar el componente Dashboard del sistema.
 * El Dashboard es el panel principal que muestra estadísticas, últimos movimientos
 * y alertas del sistema de gestión de bienes.
 * 
 * CARACTERÍSTICAS:
 * - Muestra tarjetas de estadísticas (total bienes, disponibles, asignados, cuentadantes)
 * - Lista de últimos movimientos de bienes
 * - Sistema de alertas y notificaciones
 * - Navegación rápida a otras secciones
 * 
 * CONTEXTOS REQUERIDOS:
 * - ThemeProvider: Maneja el tema claro/oscuro
 * - AuthProvider: Gestiona la autenticación del usuario
 * - DataProvider: Proporciona datos de bienes y cuentadantes
 * 
 * PROPS DEL COMPONENTE:
 * - onLogout: Función callback que se ejecuta cuando el usuario cierra sesión
 */

// Importación de contextos necesarios para el funcionamiento del Dashboard
import { ThemeProvider } from '../src/contexts/ThemeContext'
import { AuthProvider } from '../src/contexts/AuthContext'
import { DataProvider } from '../src/contexts/DataContext'

// Importación del componente Dashboard
import Dashboard from '../src/components/Dashboard'

// Estilos globales de la aplicación
import './index.css'

function App() {
  // Manejador del evento de cierre de sesión
  // En una aplicación real, aquí se limpiaría el localStorage, tokens, etc.
  const handleLogout = () => {
    console.log('Usuario cerró sesión')
    alert('Sesión cerrada')
  }

  return (
    // Envolver el Dashboard con todos los contextos necesarios
    // El orden de los providers es importante: Theme > Auth > Data
    <ThemeProvider>
      <AuthProvider>
        <DataProvider>
          {/* Componente Dashboard con callback de logout */}
          <Dashboard onLogout={handleLogout} />
        </DataProvider>
      </AuthProvider>
    </ThemeProvider>
  )
}

export default App

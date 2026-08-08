/**
 * EJEMPLO: Componente AuthScreen
 * 
 * Este archivo demuestra cómo usar el componente AuthScreen del sistema.
 * AuthScreen es la pantalla de autenticación que permite a los usuarios
 * iniciar sesión o registrarse en el sistema.
 * 
 * CARACTERÍSTICAS:
 * - Formulario de login con correo y contraseña
 * - Formulario de registro con validación
 * - Alternancia entre modo login y registro
 * - Validación de campos en tiempo real
 * - Mensajes de error personalizados
 * - Diseño responsive con animaciones
 * 
 * CONTEXTOS REQUERIDOS:
 * - ThemeProvider: Maneja el tema claro/oscuro de la interfaz
 * - AuthProvider: Gestiona el estado de autenticación y usuarios
 * 
 * PROPS DEL COMPONENTE:
 * - onLogin: Función callback que se ejecuta cuando el login es exitoso
 */

// Importación de contextos necesarios
import { ThemeProvider } from '../src/contexts/ThemeContext'
import { AuthProvider } from '../src/contexts/AuthContext'

// Importación del componente de autenticación
import AuthScreen from '../src/components/AuthScreen'

// Estilos globales de la aplicación
import './index.css'

function App() {
  // Manejador del evento de login exitoso
  // En una aplicación real, aquí se redigiría al usuario al dashboard
  // y se guardarían tokens de autenticación
  const handleLogin = () => {
    console.log('Usuario autenticado exitosamente')
    alert('¡Login exitoso!')
  }

  return (
    // Envolver AuthScreen con los contextos necesarios
    <ThemeProvider>
      <AuthProvider>
        {/* Componente de autenticación con callback de login */}
        <AuthScreen onLogin={handleLogin} />
      </AuthProvider>
    </ThemeProvider>
  )
}

export default App

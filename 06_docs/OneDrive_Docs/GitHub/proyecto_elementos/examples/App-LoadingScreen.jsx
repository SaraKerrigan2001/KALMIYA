/**
 * EJEMPLO: Componente LoadingScreen
 * 
 * Este archivo demuestra cómo usar el componente LoadingScreen del sistema.
 * LoadingScreen es la pantalla de carga inicial que se muestra mientras
 * la aplicación se inicializa o carga recursos.
 * 
 * CARACTERÍSTICAS:
 * - Animación de carga con logo del SENA
 * - Gradiente animado de fondo
 * - Efecto de pulso en el logo
 * - Mensaje de carga
 * - Diseño centrado y responsive
 * 
 * USO TÍPICO:
 * - Pantalla inicial mientras se cargan datos
 * - Durante la verificación de autenticación
 * - Mientras se inicializan contextos
 * - Transiciones entre secciones
 * 
 * NOTA: Este componente no requiere contextos ni props
 */

// Importación del componente de pantalla de carga
import LoadingScreen from '../src/components/LoadingScreen'

// Estilos globales de la aplicación
import './index.css'

function App() {
  return (
    <div>
      {/* Componente de pantalla de carga - No requiere props */}
      <LoadingScreen />
    </div>
  )
}

export default App

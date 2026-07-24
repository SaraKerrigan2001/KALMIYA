/**
 * EJEMPLO: Componente NotificationContainer
 * 
 * Este archivo demuestra cómo usar el componente NotificationContainer del sistema.
 * NotificationContainer es un contenedor que muestra notificaciones tipo toast
 * en la esquina superior derecha de la pantalla.
 * 
 * CARACTERÍSTICAS:
 * - Notificaciones tipo toast (emergentes)
 * - Posicionamiento fijo en esquina superior derecha
 * - Tipos: success (verde), error (rojo), warning (amarillo), info (azul)
 * - Auto-desaparición después de unos segundos
 * - Animaciones de entrada y salida suaves
 * - Botón de cierre manual
 * - Apilamiento de múltiples notificaciones
 * - Iconos representativos por tipo
 * 
 * CONTEXTOS REQUERIDOS:
 * - ThemeProvider: Maneja el tema claro/oscuro
 * 
 * PROPS DEL COMPONENTE:
 * - No requiere props, las notificaciones se gestionan internamente
 * 
 * USO TÍPICO:
 * - Confirmación de acciones (bien agregado, asignación exitosa)
 * - Mensajes de error (validación fallida, error de red)
 * - Advertencias (campos incompletos, límites alcanzados)
 * - Información general (sistema actualizado, recordatorios)
 * 
 * NOTA: Este componente genera notificaciones de ejemplo automáticamente
 * para demostración. En producción, las notificaciones se disparan
 * mediante eventos o funciones del contexto.
 */

// Importación del contexto de tema
import { ThemeProvider } from '../src/contexts/ThemeContext'

// Importación del componente contenedor de notificaciones
import NotificationContainer from '../src/components/NotificationContainer'

// Estilos globales de la aplicación
import './index.css'

function App() {
  return (
    // Envolver con el contexto de tema
    <ThemeProvider>
      {/* Contenedor principal */}
      <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-6">
        {/* Título de la sección */}
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          Sistema de Notificaciones
        </h1>
        
        {/* Tarjeta informativa */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-4">
          <p className="text-gray-600 dark:text-gray-400">
            Las notificaciones aparecerán en la esquina superior derecha.
            Espera unos segundos para verlas aparecer automáticamente.
          </p>
        </div>

        {/* Componente de notificaciones - Se posiciona fixed en la esquina */}
        <NotificationContainer />
      </div>
    </ThemeProvider>
  )
}

export default App

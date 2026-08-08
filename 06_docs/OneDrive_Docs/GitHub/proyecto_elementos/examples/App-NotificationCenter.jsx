/**
 * EJEMPLO: Componente NotificationCenter
 * 
 * Este archivo demuestra cómo usar el componente NotificationCenter del sistema.
 * NotificationCenter es un centro de notificaciones completo con panel desplegable
 * y notificaciones toast.
 * 
 * CARACTERÍSTICAS:
 * - Panel desplegable de notificaciones con historial
 * - Contador de notificaciones no leídas (badge)
 * - 4 tipos de notificaciones: Success, Error, Warning, Info
 * - Tiempo relativo (hace X minutos/horas)
 * - Eliminar notificaciones individuales
 * - Botón para limpiar todas las notificaciones
 * - Auto-cierre de notificaciones después de duración configurada
 * - Notificaciones toast en esquina superior derecha
 * - Integración con hook useNotifications para disparar notificaciones
 * - Persistencia opcional en localStorage
 * 
 * CONTEXTOS REQUERIDOS:
 * - ThemeProvider: Maneja el tema claro/oscuro
 * - NotificationProvider: Gestiona el estado global de notificaciones
 * 
 * COMPONENTES INCLUIDOS:
 * - NotificationCenter: Panel desplegable con historial
 * - NotificationContainer: Notificaciones toast flotantes
 * 
 * HOOK PERSONALIZADO:
 * - useNotifications: Proporciona funciones para crear notificaciones
 *   - bienCreado(codigo)
 *   - bienError(mensaje)
 *   - mantenimientoPendiente(cantidad)
 *   - sincronizacionCompleta()
 *   - asignacionExitosa(cantidad, cuentadante)
 *   - perfilActualizado()
 */

// Importación de contextos necesarios
import { ThemeProvider } from '../src/contexts/ThemeContext'
import { NotificationProvider } from '../src/contexts/NotificationContext'

// Importación del hook personalizado para notificaciones
import { useNotifications } from '../src/hooks/useNotifications'

// Importación de componentes de notificaciones
import NotificationCenter from '../src/components/NotificationCenter'
import NotificationContainer from '../src/components/NotificationContainer'

// Estilos globales de la aplicación
import '../src/index.css'

/**
 * Componente auxiliar con botones para demostrar diferentes tipos de notificaciones
 * Debe estar dentro del NotificationProvider para usar el hook useNotifications
 */
function DemoButtons() {
  // Hook que proporciona funciones para crear notificaciones
  const notifications = useNotifications()

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        Probar Notificaciones
      </h2>
      
      {/* Grid de botones para demostrar diferentes tipos de notificaciones */}
      <div className="grid grid-cols-2 gap-4">
        {/* Notificación de éxito: Bien creado */}
        <button
          onClick={() => notifications.bienCreado('HP-2024-001')}
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg"
        >
          ✅ Bien Creado
        </button>
        
        {/* Notificación de error */}
        <button
          onClick={() => notifications.bienError('No se pudo guardar el bien')}
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg"
        >
          ❌ Error
        </button>
        
        {/* Notificación de advertencia */}
        <button
          onClick={() => notifications.mantenimientoPendiente(5)}
          className="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg"
        >
          ⚠️ Advertencia
        </button>
        
        {/* Notificación informativa */}
        <button
          onClick={() => notifications.sincronizacionCompleta()}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
        >
          ℹ️ Información
        </button>
        
        {/* Notificación de asignación exitosa */}
        <button
          onClick={() => notifications.asignacionExitosa(3, 'María González')}
          className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg"
        >
          🔗 Asignación
        </button>
        
        {/* Notificación de perfil actualizado */}
        <button
          onClick={() => notifications.perfilActualizado()}
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg"
        >
          👤 Perfil
        </button>
      </div>
    </div>
  )
}

/**
 * Componente principal de la aplicación de ejemplo
 */
function App() {
  return (
    // Envolver con los contextos necesarios
    // IMPORTANTE: NotificationProvider debe estar dentro de ThemeProvider
    <ThemeProvider>
      <NotificationProvider>
        {/* Contenedor principal */}
        <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-6">
          
          {/* Header simulado con NotificationCenter */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 mb-6">
            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                Centro de Notificaciones
              </h1>
              {/* Componente NotificationCenter: icono de campana con badge */}
              <NotificationCenter />
            </div>
          </div>

          {/* Tarjeta informativa con características */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Características:
            </h2>
            <ul className="list-disc list-inside text-gray-600 dark:text-gray-400 space-y-2">
              <li>Panel desplegable de notificaciones</li>
              <li>Contador de notificaciones no leídas</li>
              <li>4 tipos: Success, Error, Warning, Info</li>
              <li>Tiempo relativo (hace X minutos)</li>
              <li>Eliminar notificaciones individuales</li>
              <li>Limpiar todas las notificaciones</li>
              <li>Auto-cierre después de duración</li>
              <li>Notificaciones toast en esquina</li>
            </ul>
          </div>

          {/* Tarjeta con botones de prueba */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <DemoButtons />
          </div>

          {/* Contenedor de notificaciones toast (esquina superior derecha) */}
          <NotificationContainer />
        </div>
      </NotificationProvider>
    </ThemeProvider>
  )
}

export default App

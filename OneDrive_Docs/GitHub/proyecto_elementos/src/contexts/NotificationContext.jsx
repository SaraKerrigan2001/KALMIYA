/**
 * ============================================
 * NotificationContext.jsx - Contexto de notificaciones
 * ============================================
 * 
 * Este contexto maneja el sistema de notificaciones de la aplicación.
 * 
 * Características:
 * - Notificaciones toast (temporales en esquina)
 * - Centro de notificaciones (historial persistente)
 * - 4 tipos: success, error, warning, info
 * - Auto-cierre configurable
 * - Métodos de conveniencia
 * 
 * Tipos de notificaciones:
 * - Toast: Aparecen temporalmente y desaparecen
 * - Persistentes: Se guardan en el centro de notificaciones
 * 
 * Uso:
 * ```javascript
 * const { success, error, warning, info } = useNotification()
 * success('Título', 'Mensaje', 5000)
 * ```
 */

import { createContext, useContext, useState, useCallback } from 'react'

// Crear el contexto
const NotificationContext = createContext()

/**
 * ============================================
 * useNotification - Hook para usar el contexto de notificaciones
 * ============================================
 * 
 * @returns {Object} Funciones y estado de notificaciones
 * @throws {Error} Si se usa fuera de NotificationProvider
 */
export const useNotification = () => {
  const context = useContext(NotificationContext)
  if (!context) {
    throw new Error('useNotification debe ser usado dentro de NotificationProvider')
  }
  return context
}

/**
 * ============================================
 * NotificationProvider - Proveedor del contexto de notificaciones
 * ============================================
 * 
 * @param {Object} props
 * @param {ReactNode} props.children - Componentes hijos
 */
export const NotificationProvider = ({ children }) => {
  // ============================================
  // ESTADOS
  // ============================================
  
  // Notificaciones persistentes (centro de notificaciones)
  const [notifications, setNotifications] = useState([])
  
  // Notificaciones temporales (toast en esquina)
  const [toastNotifications, setToastNotifications] = useState([])

  /**
   * ============================================
   * addNotification - Agregar nueva notificación
   * ============================================
   * 
   * Crea una notificación que puede ser:
   * - Toast temporal (desaparece automáticamente)
   * - Persistente (se guarda en el centro)
   * 
   * @param {Object} notification - Configuración de la notificación
   * @param {string} [notification.type='info'] - Tipo: success, error, warning, info
   * @param {string} [notification.title='Notificación'] - Título
   * @param {string} [notification.message=''] - Mensaje
   * @param {number} [notification.duration=5000] - Duración en ms (0 = permanente)
   * @param {boolean} [notification.persistent=true] - Si se guarda en el centro
   * 
   * @returns {number} ID de la notificación creada
   */
  const addNotification = useCallback((notification) => {
    // Generar ID único
    const id = Date.now() + Math.random()
    
    // Crear objeto de notificación con valores por defecto
    const newNotification = {
      id,
      type: notification.type || 'info',
      title: notification.title || 'Notificación',
      message: notification.message || '',
      duration: notification.duration || 5000,
      timestamp: Date.now(),
      persistent: notification.persistent !== false // Por defecto es persistente
    }

    // Agregar a notificaciones persistentes (centro de notificaciones)
    if (newNotification.persistent) {
      setNotifications(prev => [newNotification, ...prev])
    }

    // Agregar a notificaciones toast (temporales en esquina)
    setToastNotifications(prev => [...prev, newNotification])

    // Auto-remover del toast después de la duración especificada
    if (newNotification.duration > 0) {
      setTimeout(() => {
        removeToastNotification(id)
      }, newNotification.duration)
    }

    return id
  }, [])

  /**
   * ============================================
   * removeNotification - Remover del centro de notificaciones
   * ============================================
   * 
   * @param {number} id - ID de la notificación a remover
   */
  const removeNotification = useCallback((id) => {
    setNotifications(prev => prev.filter(notif => notif.id !== id))
  }, [])

  /**
   * ============================================
   * removeToastNotification - Remover notificación toast
   * ============================================
   * 
   * @param {number} id - ID de la notificación toast a remover
   */
  const removeToastNotification = useCallback((id) => {
    setToastNotifications(prev => prev.filter(notif => notif.id !== id))
  }, [])

  /**
   * ============================================
   * clearAll - Limpiar todas las notificaciones del centro
   * ============================================
   */
  const clearAll = useCallback(() => {
    setNotifications([])
  }, [])

  // ============================================
  // MÉTODOS DE CONVENIENCIA
  // Funciones simplificadas para cada tipo de notificación
  // ============================================

  /**
   * Notificación de éxito (verde)
   * @param {string} title - Título
   * @param {string} message - Mensaje
   * @param {number} [duration] - Duración en ms
   * @returns {number} ID de la notificación
   */
  const success = useCallback((title, message, duration) => {
    return addNotification({ type: 'success', title, message, duration })
  }, [addNotification])

  /**
   * Notificación de error (rojo)
   * @param {string} title - Título
   * @param {string} message - Mensaje
   * @param {number} [duration] - Duración en ms
   * @returns {number} ID de la notificación
   */
  const error = useCallback((title, message, duration) => {
    return addNotification({ type: 'error', title, message, duration })
  }, [addNotification])

  /**
   * Notificación de advertencia (amarillo)
   * @param {string} title - Título
   * @param {string} message - Mensaje
   * @param {number} [duration] - Duración en ms
   * @returns {number} ID de la notificación
   */
  const warning = useCallback((title, message, duration) => {
    return addNotification({ type: 'warning', title, message, duration })
  }, [addNotification])

  /**
   * Notificación informativa (azul)
   * @param {string} title - Título
   * @param {string} message - Mensaje
   * @param {number} [duration] - Duración en ms
   * @returns {number} ID de la notificación
   */
  const info = useCallback((title, message, duration) => {
    return addNotification({ type: 'info', title, message, duration })
  }, [addNotification])

  // ============================================
  // VALOR DEL CONTEXTO
  // ============================================
  const value = {
    notifications,              // Array de notificaciones persistentes
    toastNotifications,         // Array de notificaciones toast temporales
    addNotification,            // Función para agregar notificación
    removeNotification,         // Función para remover del centro
    removeToastNotification,    // Función para remover toast
    clearAll,                   // Función para limpiar todas
    success,                    // Método de conveniencia para éxito
    error,                      // Método de conveniencia para error
    warning,                    // Método de conveniencia para advertencia
    info                        // Método de conveniencia para info
  }

  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  )
}

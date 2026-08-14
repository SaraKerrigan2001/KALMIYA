/**
 * ============================================
 * useNotifications.js - Hook de notificaciones
 * ============================================
 * 
 * Este hook personalizado proporciona funciones predefinidas
 * para mostrar notificaciones comunes en el sistema.
 * 
 * Ventajas:
 * - Mensajes consistentes en toda la aplicación
 * - Fácil de usar (una línea de código)
 * - Duraciones predefinidas según el tipo de notificación
 * - Tipos: success, error, warning, info
 * 
 * Uso:
 * ```javascript
 * const notifications = useNotifications()
 * notifications.bienCreado('HP-2024-001')
 * ```
 */

import { useNotification } from '../contexts/NotificationContext'

export const useNotifications = () => {
  const notification = useNotification()

  return {
    // ============================================
    // NOTIFICACIONES DE BIENES
    // ============================================
    
    /**
     * Notificación cuando se crea un bien exitosamente
     * @param {string} codigo - Código del bien creado
     * Duración: 5 segundos
     */
    bienCreado: (codigo) => {
      notification.success(
        'Bien registrado',
        `El bien ${codigo} ha sido agregado exitosamente`,
        5000
      )
    },
    
    /**
     * Notificación cuando se actualiza un bien
     * @param {string} codigo - Código del bien actualizado
     * Duración: 4 segundos
     */
    bienActualizado: (codigo) => {
      notification.success(
        'Bien actualizado',
        `El bien ${codigo} ha sido actualizado correctamente`,
        4000
      )
    },
    
    /**
     * Notificación de error al procesar un bien
     * @param {string} mensaje - Mensaje de error personalizado
     * Duración: 6 segundos
     */
    bienError: (mensaje) => {
      notification.error(
        'Error al procesar bien',
        mensaje || 'No se pudo completar la operación',
        6000
      )
    },

    // ============================================
    // NOTIFICACIONES DE CUENTADANTES
    // ============================================
    
    /**
     * Notificación cuando se crea un cuentadante
     * @param {string} nombre - Nombre del cuentadante
     * Duración: 5 segundos
     */
    cuentadanteCreado: (nombre) => {
      notification.success(
        'Cuentadante registrado',
        `${nombre} ha sido agregado exitosamente`,
        5000
      )
    },
    
    /**
     * Notificación cuando se actualiza un cuentadante
     * @param {string} nombre - Nombre del cuentadante
     * Duración: 4 segundos
     */
    cuentadanteActualizado: (nombre) => {
      notification.success(
        'Cuentadante actualizado',
        `Los datos de ${nombre} han sido actualizados`,
        4000
      )
    },

    // ============================================
    // NOTIFICACIONES DE ASIGNACIONES
    // ============================================
    
    /**
     * Notificación cuando se completa una asignación
     * @param {number} cantidad - Cantidad de bienes asignados
     * @param {string} cuentadante - Nombre del cuentadante
     * Duración: 5 segundos
     */
    asignacionExitosa: (cantidad, cuentadante) => {
      notification.success(
        'Asignación completada',
        `${cantidad} bien(es) asignado(s) a ${cuentadante}`,
        5000
      )
    },
    
    /**
     * Notificación de error en asignación
     * Duración: 6 segundos
     */
    asignacionError: () => {
      notification.error(
        'Error en asignación',
        'No se pudo completar la asignación de bienes',
        6000
      )
    },

    // ============================================
    // NOTIFICACIONES DE PERFIL
    // ============================================
    
    /**
     * Notificación cuando se actualiza el perfil del usuario
     * Duración: 4 segundos
     */
    perfilActualizado: () => {
      notification.success(
        'Perfil actualizado',
        'Tu información ha sido guardada correctamente',
        4000
      )
    },

    // ============================================
    // NOTIFICACIONES DE CONFIGURACIÓN
    // ============================================
    
    /**
     * Notificación cuando se guarda la configuración
     * Duración: 4 segundos
     */
    configuracionGuardada: () => {
      notification.success(
        'Configuración guardada',
        'Tus preferencias han sido actualizadas',
        4000
      )
    },

    // ============================================
    // NOTIFICACIONES DE AUTENTICACIÓN
    // ============================================
    
    /**
     * Notificación de bienvenida al iniciar sesión
     * @param {string} nombre - Nombre del usuario
     * Duración: 3 segundos
     */
    loginExitoso: (nombre) => {
      notification.success(
        'Bienvenido',
        `Hola ${nombre}, sesión iniciada correctamente`,
        3000
      )
    },
    
    /**
     * Notificación al cerrar sesión
     * Duración: 3 segundos
     */
    logoutExitoso: () => {
      notification.info(
        'Sesión cerrada',
        'Has cerrado sesión correctamente',
        3000
      )
    },

    // ============================================
    // NOTIFICACIONES DE ADVERTENCIA
    // ============================================
    
    /**
     * Notificación de mantenimiento pendiente
     * @param {number} cantidad - Cantidad de equipos
     * Duración: 8 segundos (más tiempo para advertencias)
     */
    mantenimientoPendiente: (cantidad) => {
      notification.warning(
        'Mantenimiento pendiente',
        `${cantidad} equipo(s) requieren mantenimiento preventivo`,
        8000
      )
    },
    
    /**
     * Notificación de bienes sin asignar
     * @param {number} dias - Días sin asignar
     * Duración: 8 segundos
     */
    bienSinAsignar: (dias) => {
      notification.warning(
        'Bienes sin asignar',
        `Hay bienes disponibles sin asignar por más de ${dias} días`,
        8000
      )
    },

    // ============================================
    // NOTIFICACIONES INFORMATIVAS
    // ============================================
    
    /**
     * Notificación de sincronización completa
     * Duración: 3 segundos
     */
    sincronizacionCompleta: () => {
      notification.info(
        'Sincronización completa',
        'Los datos han sido actualizados',
        3000
      )
    },

    // ============================================
    // MÉTODO GENÉRICO
    // ============================================
    
    /**
     * Método genérico para notificaciones personalizadas
     * @param {string} type - Tipo: 'success', 'error', 'warning', 'info'
     * @param {string} title - Título de la notificación
     * @param {string} message - Mensaje de la notificación
     * @param {number} duration - Duración en milisegundos
     */
    custom: (type, title, message, duration) => {
      notification.addNotification({ type, title, message, duration })
    }
  }
}

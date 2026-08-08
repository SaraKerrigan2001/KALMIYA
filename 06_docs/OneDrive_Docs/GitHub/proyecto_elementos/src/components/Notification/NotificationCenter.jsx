import { useState } from 'react'
import { useNotification } from '../../contexts/NotificationContext'
import '../../assets/css/NotificationCenter.css'

const NotificationCenter = () => {
  const [isOpen, setIsOpen] = useState(false)
  const { notifications, removeNotification, clearAll } = useNotification()

  const unreadCount = notifications.length

  const getTimeAgo = (timestamp) => {
    const seconds = Math.floor((Date.now() - timestamp) / 1000)
    
    if (seconds < 60) return 'Ahora'
    if (seconds < 3600) return `Hace ${Math.floor(seconds / 60)} min`
    if (seconds < 86400) return `Hace ${Math.floor(seconds / 3600)} h`
    return `Hace ${Math.floor(seconds / 86400)} días`
  }

  const getNotificationIcon = (type) => {
    const icons = {
      success: '✅',
      error: '❌',
      warning: '⚠️',
      info: 'ℹ️'
    }
    return icons[type] || icons.info
  }

  const getNotificationClasses = (type) => {
    const classes = {
      success: {
        item: 'notification-item-success',
        title: 'notification-item-title-success'
      },
      error: {
        item: 'notification-item-error',
        title: 'notification-item-title-error'
      },
      warning: {
        item: 'notification-item-warning',
        title: 'notification-item-title-warning'
      },
      info: {
        item: 'notification-item-info',
        title: 'notification-item-title-info'
      }
    }
    return classes[type] || classes.info
  }

  return (
    <div className="notification-center-container">
      {/* Botón de notificaciones */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="notification-button"
        title="Notificaciones"
      >
        <span className="notification-icon">🔔</span>
        {unreadCount > 0 && (
          <span className="notification-badge">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {/* Panel de notificaciones */}
      {isOpen && (
        <>
          {/* Overlay para cerrar al hacer clic fuera */}
          <div
            className="notification-overlay"
            onClick={() => setIsOpen(false)}
          />

          {/* Panel */}
          <div className="notification-panel">
            {/* Header del panel */}
            <div className="notification-header">
              <div className="notification-header-content">
                <h3 className="notification-header-title">
                  Notificaciones
                </h3>
                {notifications.length > 0 && (
                  <button
                    onClick={clearAll}
                    className="notification-clear-button"
                  >
                    Limpiar todo
                  </button>
                )}
              </div>
              {notifications.length > 0 && (
                <p className="notification-header-subtitle">
                  Tienes {notifications.length} notificación{notifications.length !== 1 ? 'es' : ''}
                </p>
              )}
            </div>

            {/* Lista de notificaciones */}
            <div className="notification-list">
              {notifications.length === 0 ? (
                <div className="notification-empty">
                  <div className="notification-empty-icon">🔕</div>
                  <p className="notification-empty-text">
                    No hay notificaciones
                  </p>
                  <p className="notification-empty-subtext">
                    Te notificaremos cuando haya algo nuevo
                  </p>
                </div>
              ) : (
                <div className="notification-items">
                  {notifications.map((notification) => {
                    const classes = getNotificationClasses(notification.type)
                    
                    return (
                      <div
                        key={notification.id}
                        className={`notification-item ${classes.item}`}
                      >
                        <div className="notification-item-content">
                          <div className="notification-item-icon">
                            {getNotificationIcon(notification.type)}
                          </div>
                          
                          <div className="notification-item-body">
                            <div className="notification-item-header">
                              <div className="notification-item-text">
                                <h4 className={`notification-item-title ${classes.title}`}>
                                  {notification.title}
                                </h4>
                                <p className="notification-item-message">
                                  {notification.message}
                                </p>
                                <p className="notification-item-time">
                                  {getTimeAgo(notification.timestamp)}
                                </p>
                              </div>
                              
                              <button
                                onClick={() => removeNotification(notification.id)}
                                className="notification-item-close"
                              >
                                <span className="notification-item-close-icon">×</span>
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    )
                  })}
                </div>
              )}
            </div>

            {/* Footer */}
            {notifications.length > 0 && (
              <div className="notification-footer">
                <button
                  onClick={() => setIsOpen(false)}
                  className="notification-close-button"
                >
                  Cerrar
                </button>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  )
}

export default NotificationCenter

import { useNotification } from '../../contexts/NotificationContext'
import '../../assets/css/NotificationContainer.css'

const NotificationContainer = () => {
  const { toastNotifications, removeToastNotification } = useNotification()

  const getNotificationData = (type) => {
    const data = {
      success: {
        icon: '✅',
        classes: {
          item: 'toast-item-success',
          iconContainer: 'toast-icon-container-success',
          title: 'toast-title-success'
        }
      },
      error: {
        icon: '❌',
        classes: {
          item: 'toast-item-error',
          iconContainer: 'toast-icon-container-error',
          title: 'toast-title-error'
        }
      },
      warning: {
        icon: '⚠️',
        classes: {
          item: 'toast-item-warning',
          iconContainer: 'toast-icon-container-warning',
          title: 'toast-title-warning'
        }
      },
      info: {
        icon: 'ℹ️',
        classes: {
          item: 'toast-item-info',
          iconContainer: 'toast-icon-container-info',
          title: 'toast-title-info'
        }
      }
    }
    return data[type] || data.info
  }

  if (toastNotifications.length === 0) {
    return null
  }

  return (
    <div className="toast-container">
      <div className="toast-list">
        {toastNotifications.map((notification) => {
          const data = getNotificationData(notification.type)
          
          return (
            <div
              key={notification.id}
              className={`toast-item ${data.classes.item}`}
            >
              <div className="toast-content">
                <div className={`toast-icon-container ${data.classes.iconContainer}`}>
                  <span className="toast-icon">{data.icon}</span>
                </div>
                
                <div className="toast-body">
                  <h4 className={`toast-title ${data.classes.title}`}>
                    {notification.title}
                  </h4>
                  <p className="toast-message">
                    {notification.message}
                  </p>
                  <p className="toast-time">
                    {new Date(notification.timestamp).toLocaleTimeString()}
                  </p>
                </div>
                
                <button
                  onClick={() => removeToastNotification(notification.id)}
                  className="toast-close"
                >
                  <span className="toast-close-icon">×</span>
                </button>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default NotificationContainer
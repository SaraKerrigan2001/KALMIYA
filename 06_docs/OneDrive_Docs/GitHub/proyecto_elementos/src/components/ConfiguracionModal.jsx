import { useState, useEffect } from 'react'
import { useTheme } from '../contexts/ThemeContext'
import { useNotifications } from '../hooks/useNotifications'
import '../assets/css/ConfiguracionModal.css'

const ConfiguracionModal = ({ onClose }) => {
  const { isDark, toggleTheme } = useTheme()
  const notifications = useNotifications()
  const [config, setConfig] = useState({
    notificaciones: true,
    sonido: true,
    emailNotificaciones: true,
    autoGuardado: true,
    idioma: 'es',
    itemsPorPagina: 10,
    formatoFecha: 'DD/MM/YYYY',
    tema: isDark ? 'dark' : 'light'
  })
  const [isLoading, setIsLoading] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')

  useEffect(() => {
    // Cargar configuración guardada
    const savedConfig = localStorage.getItem('appConfig')
    if (savedConfig) {
      try {
        const parsed = JSON.parse(savedConfig)
        setConfig(prev => ({ ...prev, ...parsed }))
      } catch (error) {
        console.error('Error al cargar configuración:', error)
      }
    }
  }, [])

  const handleToggle = (key) => {
    setConfig(prev => ({
      ...prev,
      [key]: !prev[key]
    }))
  }

  const handleSelectChange = (e) => {
    const { name, value } = e.target
    setConfig(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleTemaChange = (nuevoTema) => {
    setConfig(prev => ({
      ...prev,
      tema: nuevoTema
    }))
    
    if ((nuevoTema === 'dark' && !isDark) || (nuevoTema === 'light' && isDark)) {
      toggleTheme()
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setSuccessMessage('')

    try {
      // Guardar en localStorage
      localStorage.setItem('appConfig', JSON.stringify(config))
      
      // Simular guardado en servidor
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      setSuccessMessage('Configuración guardada exitosamente')
      notifications.configuracionGuardada()
      
      setTimeout(() => {
        onClose()
      }, 1500)
    } catch (error) {
      console.error('Error al guardar configuración:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleRestaurar = () => {
    const defaultConfig = {
      notificaciones: true,
      sonido: true,
      emailNotificaciones: true,
      autoGuardado: true,
      idioma: 'es',
      itemsPorPagina: 10,
      formatoFecha: 'DD/MM/YYYY',
      tema: 'light'
    }
    setConfig(defaultConfig)
    localStorage.removeItem('appConfig')
    setSuccessMessage('Configuración restaurada a valores predeterminados')
  }

  return (
    <div className="config-modal-overlay">
      <div className="config-modal-container">
        {/* Header */}
        <div className="config-modal-header">
          <div className="config-modal-header-content">
            <div className="config-modal-header-left">
              <div className="config-modal-icon">
                <span className="config-modal-icon-emoji">⚙️</span>
              </div>
              <div>
                <h2 className="config-modal-title">
                  Configuración
                </h2>
                <p className="config-modal-subtitle">
                  Personaliza tu experiencia en el sistema
                </p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="config-modal-close"
            >
              <span className="config-modal-close-icon">×</span>
            </button>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="config-modal-form">
          {successMessage && (
            <div className="config-modal-success">
              {successMessage}
            </div>
          )}

          {/* Apariencia */}
          <div className="config-modal-section">
            <h3 className="config-modal-section-title">
              🎨 Apariencia
            </h3>
            
            <div className="config-modal-section-content">
              <div>
                <label className="config-label">
                  Tema
                </label>
                <div className="config-theme-grid">
                  <button
                    type="button"
                    onClick={() => handleTemaChange('light')}
                    className={`config-theme-button ${config.tema === 'light' ? 'active' : ''}`}
                  >
                    <span className="config-theme-button-emoji">☀️</span>
                    <span className="config-theme-button-text">Claro</span>
                  </button>
                  
                  <button
                    type="button"
                    onClick={() => handleTemaChange('dark')}
                    className={`config-theme-button ${config.tema === 'dark' ? 'active' : ''}`}
                  >
                    <span className="config-theme-button-emoji">🌙</span>
                    <span className="config-theme-button-text">Oscuro</span>
                  </button>
                  
                  <button
                    type="button"
                    onClick={() => handleTemaChange('auto')}
                    className={`config-theme-button ${config.tema === 'auto' ? 'active' : ''}`}
                  >
                    <span className="config-theme-button-emoji">🔄</span>
                    <span className="config-theme-button-text">Auto</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Notificaciones */}
          <div className="config-modal-section">
            <h3 className="config-modal-section-title">
              🔔 Notificaciones
            </h3>
            
            <div className="config-modal-section-content">
              <div className="config-toggle-item">
                <div className="config-toggle-info">
                  <p className="config-toggle-title">Notificaciones en pantalla</p>
                  <p className="config-toggle-description">Mostrar alertas en el sistema</p>
                </div>
                <button
                  type="button"
                  onClick={() => handleToggle('notificaciones')}
                  className={`config-toggle-switch ${config.notificaciones ? 'active' : 'inactive'}`}
                >
                  <span className="config-toggle-switch-circle" />
                </button>
              </div>

              <div className="config-toggle-item">
                <div className="config-toggle-info">
                  <p className="config-toggle-title">Sonido</p>
                  <p className="config-toggle-description">Reproducir sonidos de notificación</p>
                </div>
                <button
                  type="button"
                  onClick={() => handleToggle('sonido')}
                  className={`config-toggle-switch ${config.sonido ? 'active' : 'inactive'}`}
                >
                  <span className="config-toggle-switch-circle" />
                </button>
              </div>

              <div className="config-toggle-item">
                <div className="config-toggle-info">
                  <p className="config-toggle-title">Notificaciones por correo</p>
                  <p className="config-toggle-description">Recibir alertas por email</p>
                </div>
                <button
                  type="button"
                  onClick={() => handleToggle('emailNotificaciones')}
                  className={`config-toggle-switch ${config.emailNotificaciones ? 'active' : 'inactive'}`}
                >
                  <span className="config-toggle-switch-circle" />
                </button>
              </div>
            </div>
          </div>

          {/* Preferencias */}
          <div className="config-modal-section">
            <h3 className="config-modal-section-title">
              🎯 Preferencias
            </h3>
            
            <div className="config-modal-section-content">
              <div className="config-toggle-item">
                <div className="config-toggle-info">
                  <p className="config-toggle-title">Auto-guardado</p>
                  <p className="config-toggle-description">Guardar cambios automáticamente</p>
                </div>
                <button
                  type="button"
                  onClick={() => handleToggle('autoGuardado')}
                  className={`config-toggle-switch ${config.autoGuardado ? 'active' : 'inactive'}`}
                >
                  <span className="config-toggle-switch-circle" />
                </button>
              </div>

              <div className="config-field">
                <label htmlFor="idioma" className="config-label">
                  Idioma
                </label>
                <select
                  id="idioma"
                  name="idioma"
                  value={config.idioma}
                  onChange={handleSelectChange}
                  className="config-select"
                >
                  <option value="es">Español</option>
                  <option value="en">English</option>
                  <option value="pt">Português</option>
                </select>
              </div>

              <div className="config-field">
                <label htmlFor="itemsPorPagina" className="config-label">
                  Ítems por página
                </label>
                <select
                  id="itemsPorPagina"
                  name="itemsPorPagina"
                  value={config.itemsPorPagina}
                  onChange={handleSelectChange}
                  className="config-select"
                >
                  <option value="5">5</option>
                  <option value="10">10</option>
                  <option value="20">20</option>
                  <option value="50">50</option>
                  <option value="100">100</option>
                </select>
              </div>

              <div className="config-field">
                <label htmlFor="formatoFecha" className="config-label">
                  Formato de fecha
                </label>
                <select
                  id="formatoFecha"
                  name="formatoFecha"
                  value={config.formatoFecha}
                  onChange={handleSelectChange}
                  className="config-select"
                >
                  <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                  <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                  <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                </select>
              </div>
            </div>
          </div>

          {/* Buttons */}
          <div className="config-modal-footer">
            <button
              type="button"
              onClick={handleRestaurar}
              className="config-btn-restore"
            >
              Restaurar Predeterminados
            </button>
            
            <div className="config-modal-footer-right">
              <button
                type="button"
                onClick={onClose}
                className="config-btn-cancel"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="config-btn-submit"
              >
                {isLoading ? 'Guardando...' : 'Guardar Configuración'}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ConfiguracionModal

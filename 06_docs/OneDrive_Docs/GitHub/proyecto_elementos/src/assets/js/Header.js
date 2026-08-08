import { useState, useEffect } from 'react'
import { useTheme } from '../../contexts/ThemeContext'
import { useTranslation } from '../../hooks/useTranslation'
import NotificationCenter from '../../components/NotificationCenter'
import LanguageSelector from '../../components/LanguageSelector'
import '../css/Header.css'

const Header = ({ onMenuClick }) => {
  const [currentDateTime, setCurrentDateTime] = useState(new Date())
  const [lastSync, setLastSync] = useState(new Date())
  const [syncTimeAgo, setSyncTimeAgo] = useState('hace 0 min')
  const { isDark, toggleTheme } = useTheme()
  const { t } = useTranslation()

  // Actualizar fecha y hora cada segundo
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentDateTime(new Date())
    }, 1000)
    return () => clearInterval(timer)
  }, [])

  // Simular sincronización automática cada 2 minutos
  useEffect(() => {
    const syncTimer = setInterval(() => {
      setLastSync(new Date())
    }, 120000) // 2 minutos
    return () => clearInterval(syncTimer)
  }, [])

  // Actualizar el tiempo transcurrido desde la última sincronización
  useEffect(() => {
    const updateSyncTime = () => {
      const now = new Date()
      const diffMs = now - lastSync
      const diffMinutes = Math.floor(diffMs / 60000)
      const diffSeconds = Math.floor((diffMs % 60000) / 1000)

      if (diffMinutes === 0) {
        setSyncTimeAgo(`${t('header.hace')} ${diffSeconds} ${t('header.seg')}`)
      } else if (diffMinutes === 1) {
        setSyncTimeAgo(`${t('header.hace')} 1 ${t('header.min')}`)
      } else {
        setSyncTimeAgo(`${t('header.hace')} ${diffMinutes} ${t('header.min')}`)
      }
    }

    updateSyncTime()
    const timer = setInterval(updateSyncTime, 1000)
    return () => clearInterval(timer)
  }, [lastSync])

  // Formatear fecha y hora
  const formatDateTime = () => {
    const days = t('days')
    const months = t('months')
    
    const dayName = days[currentDateTime.getDay()]
    const day = currentDateTime.getDate()
    const month = months[currentDateTime.getMonth()]
    const year = currentDateTime.getFullYear()
    const hours = currentDateTime.getHours().toString().padStart(2, '0')
    const minutes = currentDateTime.getMinutes().toString().padStart(2, '0')
    const seconds = currentDateTime.getSeconds().toString().padStart(2, '0')
    
    return `${dayName}, ${day} de ${month} de ${year}, ${hours}:${minutes}:${seconds}`
  }

  return (
    <header className="header-container">
      <div className="header-content">
        <div className="header-main">
          {/* Botón hamburguesa (móvil) */}
          <button
            onClick={onMenuClick}
            className="header-hamburger-btn"
            title="Menú"
          >
            <span className="header-hamburger-icon">☰</span>
          </button>

          {/* Título y fecha */}
          <div className="header-title-section">
            <h1 className="header-title">{t('header.dashboardPrincipal')}</h1>
            <p className="header-datetime">{formatDateTime()}</p>
          </div>

          {/* Controles del header */}
          <div className="header-controls">
            {/* Estado del sistema */}
            <div className="header-system-status">
              <span className="header-status-dot"></span>
              <span className="header-status-text">{t('header.sistemaActivo')}</span>
              <span className="header-status-sync">{t('header.ultimaSync')}: {syncTimeAgo}</span>
            </div>

            {/* Selector de idioma */}
            <LanguageSelector />

            {/* Botón de tema */}
            <button
              onClick={toggleTheme}
              className="header-theme-btn"
              title={isDark ? t('header.cambiarTemaClaro') : t('header.cambiarTemaOscuro')}
            >
              <span className="header-theme-icon">
                {isDark ? '☀️' : '🌙'}
              </span>
            </button>

            {/* Notificaciones */}
            <NotificationCenter />
          </div>
        </div>
      </div>

    </header>
  )
}

export default Header

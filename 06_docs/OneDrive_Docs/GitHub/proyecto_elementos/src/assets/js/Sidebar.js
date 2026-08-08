/**
 * ============================================
 * SIDEBAR.JSX - Menú lateral de navegación
 * ============================================
 * 
 * Este componente muestra el menú lateral con:
 * - Logo y título SENA BIENES
 * - Información del usuario actual
 * - Menú de navegación (Dashboard, Bienes, Cuentadantes, Asignaciones)
 * - Información del sistema (versión y estado)
 * 
 * Características:
 * - Responsive con menú hamburguesa
 * - Colapsable en todas las resoluciones
 * - Overlay oscuro al abrir
 * 
 * @param {string} activeView - Vista actualmente seleccionada
 * @param {Function} onViewChange - Función para cambiar de vista
 * @param {boolean} isOpen - Estado del sidebar (abierto/cerrado)
 * @param {Function} onClose - Función para cerrar el sidebar
 */

import { useState } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { useNotifications } from '../../hooks/useNotifications'
import { useTranslation } from '../../hooks/useTranslation'
import PerfilModal from '../../components/PerfilModal'
import ConfiguracionModal from '../../components/ConfiguracionModal'
import '../css/Sidebar.css'

const Sidebar = ({ activeView, onViewChange, isOpen, onClose, onLogout }) => {
  const { user, logout } = useAuth()
  const notifications = useNotifications()
  const { t } = useTranslation()
  const [showPerfilModal, setShowPerfilModal] = useState(false)
  const [showConfigModal, setShowConfigModal] = useState(false)

  const handleLogout = () => {
    notifications.logoutExitoso()
    setTimeout(() => {
      logout()
      onLogout()
    }, 500)
  }

  // ============================================
  // ITEMS DEL MENÚ DE NAVEGACIÓN
  // ============================================
  const menuItems = [
    {
      id: 'dashboard',
      name: t('sidebar.dashboard'),
      icon: '📊',
      description: t('sidebar.dashboardDesc')
    },
    {
      id: 'bienes',
      name: t('sidebar.bienes'),
      icon: '💻',
      description: t('sidebar.bienesDesc')
    },
    {
      id: 'cuentadantes',
      name: t('sidebar.cuentadantes'),
      icon: '👥',
      description: t('sidebar.cuentadantesDesc')
    },
    {
      id: 'asignaciones',
      name: t('sidebar.asignaciones'),
      icon: '📋',
      description: t('sidebar.asignacionesDesc')
    }
  ]

  return (
    <>
      {/* ============================================
          OVERLAY - Fondo oscuro cuando el sidebar está abierto
          Al hacer clic en el overlay, se cierra el sidebar
          ============================================ */}
      {isOpen && (
        <div 
          className="sidebar-overlay"
          onClick={onClose}
        />
      )}
      
      {/* ============================================
          SIDEBAR CONTAINER - Contenedor principal del menú
          Clase 'sidebar-open' se agrega cuando está abierto
          ============================================ */}
      <div className={`sidebar-container ${isOpen ? 'sidebar-open' : ''}`}>
      {/* Logo y título */}
      <div className="sidebar-logo-section">
        <div className="sidebar-logo-content">
          <img 
            src="/sena-logo.png (2).png" 
            alt="Logo SENA" 
            className="sidebar-logo-img"
          />
          <div>
            <h1 className="dashboard-title text-lg font-bold text-gray-900 dark:text-white">
              {t('sidebar.title')}
            </h1>
            <p className="dashboard-subtitle text-xs text-gray-600 dark:text-gray-400">
              {t('sidebar.subtitle')}
            </p>
          </div>
        </div>
      </div>

      {/* Información del usuario */}
      <div className="sidebar-user-section">
        <div className="sidebar-user-content">
          <img 
            src="/sena-logo-perfil.png.webp.webp" 
            alt="Perfil" 
            className="sidebar-user-avatar"
          />
          <div className="sidebar-user-info">
            <p className="dashboard-text sidebar-user-name">
              {user?.nombre || 'Usuario'}
            </p>
            <p className="dashboard-subtitle sidebar-user-area">
              {user?.area || 'Área no definida'}
            </p>
          </div>
        </div>
      </div>

      {/* Menú de navegación */}
      <nav className="sidebar-nav">
        <ul className="sidebar-menu-list">
          {menuItems.map((item) => (
            <li key={item.id}>
              <button
                onClick={() => onViewChange(item.id)}
                className={`sidebar-menu-item ${activeView === item.id ? 'active' : ''}`}
              >
                <span className="sidebar-menu-icon">{item.icon}</span>
                <div className="sidebar-menu-text">
                  <p className="dashboard-text sidebar-menu-name">{item.name}</p>
                  <p className="dashboard-subtitle sidebar-menu-description">{item.description}</p>
                </div>
              </button>
            </li>
          ))}
        </ul>
      </nav>

      {/* Sección de perfil y logout */}
      <div className="sidebar-bottom-section">
        {/* Perfil del usuario */}
        <div className="sidebar-profile-card" onClick={() => setShowPerfilModal(true)} style={{ cursor: 'pointer' }}>
          <div className="sidebar-profile-avatar-wrapper">
            <img 
              src="/sena-logo-perfil.png.webp.webp" 
              alt="Perfil" 
              className="sidebar-profile-avatar-large"
            />
          </div>
          <div className="sidebar-profile-info">
            <p className="sidebar-profile-name">
              {user?.nombre || 'Usuario'}
            </p>
            <p className="sidebar-profile-role">
              {user?.area || 'Administrador'}
            </p>
          </div>
        </div>

        {/* Botones de acción */}
        <div className="sidebar-action-buttons">
          <button
            onClick={() => setShowConfigModal(true)}
            className="sidebar-config-button"
          >
            <span className="sidebar-config-icon">⚙️</span>
            <span className="sidebar-config-text">{t('sidebar.configuracion')}</span>
          </button>

          <button
            onClick={handleLogout}
            className="sidebar-logout-button"
          >
            <span className="sidebar-logout-icon">🚪</span>
            <span className="sidebar-logout-text">{t('sidebar.cerrarSesion')}</span>
          </button>
        </div>
      </div>
    </div>

    {/* Modales */}
    {showPerfilModal && (
      <PerfilModal onClose={() => setShowPerfilModal(false)} />
    )}

    {showConfigModal && (
      <ConfiguracionModal onClose={() => setShowConfigModal(false)} />
    )}
    </>
  )
}

export default Sidebar

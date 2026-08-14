/**
 * ============================================
 * DASHBOARD.JSX - Panel principal del sistema
 * ============================================
 * 
 * Este componente es el contenedor principal de la aplicación
 * después del login. Incluye:
 * 
 * - Sidebar: Menú lateral de navegación
 * - Header: Barra superior con usuario y controles
 * - Contenido dinámico: Dashboard, Bienes, Cuentadantes, Asignaciones
 * - Modales: Para agregar/editar bienes, cuentadantes y asignaciones
 * 
 * @param {Function} onLogout - Función para cerrar sesión
 */

import { useState } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { useData } from '../../contexts/DataContext'
import { useTranslation } from '../../hooks/useTranslation'
import Sidebar from '../../components/Sidebar'
import Header from '../../components/Header'
import StatsCards from '../../components/StatsCards'
import BienesTable from '../../components/BienesTable'
import CuentadantesTable from '../../components/CuentadantesTable'
import AsignacionesTable from '../../components/AsignacionesTable'
import AsignacionModal from '../../components/AsignacionModal'
import BienModal from '../../components/BienModal'
import CuentadanteModal from '../../components/CuentadanteModal'
import '../css/Dashboard.css'

const Dashboard = ({ onLogout }) => {
  // ============================================
  // ESTADOS DEL COMPONENTE
  // ============================================
  
  // Vista activa actual (dashboard, bienes, cuentadantes, asignaciones)
  const [activeView, setActiveView] = useState('dashboard')
  
  // Control de visibilidad de modales
  const [showAsignacionModal, setShowAsignacionModal] = useState(false)
  const [showBienModal, setShowBienModal] = useState(false)
  const [showCuentadanteModal, setShowCuentadanteModal] = useState(false)
  
  // Elementos seleccionados para edición
  const [selectedBien, setSelectedBien] = useState(null)
  const [selectedCuentadante, setSelectedCuentadante] = useState(null)
  
  // Control del sidebar (abierto/cerrado)
  const [sidebarOpen, setSidebarOpen] = useState(false)

  // ============================================
  // HOOKS DE CONTEXTO
  // ============================================
  const { user } = useAuth() // Información del usuario actual
  const { stats } = useData() // Estadísticas del sistema
  const { t } = useTranslation() // Hook de traducción

  // ============================================
  // FUNCIONES DE MANEJO
  // ============================================
  
  /**
   * Abre el modal de edición de bien
   * @param {Object} bien - Bien a editar
   */
  const handleEditBien = (bien) => {
    setSelectedBien(bien)
    setShowBienModal(true)
  }

  /**
   * Abre el modal de edición de cuentadante
   * @param {Object} cuentadante - Cuentadante a editar
   */
  const handleEditCuentadante = (cuentadante) => {
    setSelectedCuentadante(cuentadante)
    setShowCuentadanteModal(true)
  }

  /**
   * ============================================
   * RENDERIZADO DE CONTENIDO DINÁMICO
   * ============================================
   * Muestra el contenido según la vista activa seleccionada
   * en el sidebar (Dashboard, Bienes, Cuentadantes, Asignaciones)
   */
  const renderContent = () => {
    switch (activeView) {
      // Vista principal con estadísticas y resumen
      case 'dashboard':
        return (
          <div className="dashboard-section">
            <div>
              <h1 className="dashboard-title text-2xl font-bold text-gray-900 dark:text-white">
                {t('sidebar.dashboard')}
              </h1>
              <p className="dashboard-subtitle text-gray-600 dark:text-gray-400">
                {t('dashboard.bienvenido')}, {user?.nombre}
              </p>
            </div>
            <StatsCards stats={stats} />
            <div className="dashboard-cards-grid">
              <div className="dashboard-card">
                <h3 className="dashboard-card-title">
                  {t('dashboard.ultimosMovimientos')}
                </h3>
                <div className="dashboard-card-content">
                  <div className="dashboard-movement-item">
                    <div>
                      <p className="dashboard-text dashboard-movement-title">Entrada - HP-2024-001</p>
                      <p className="dashboard-subtitle dashboard-movement-description">Computador HP EliteBook</p>
                    </div>
                    <span className="dashboard-text dashboard-movement-time dashboard-movement-time-today">{t('dashboard.hoy')}</span>
                  </div>
                  <div className="dashboard-movement-item">
                    <div>
                      <p className="dashboard-text dashboard-movement-title">Asignación - EPSON-2023-045</p>
                      <p className="dashboard-subtitle dashboard-movement-description">A María González</p>
                    </div>
                    <span className="dashboard-text dashboard-movement-time dashboard-movement-time-yesterday">{t('dashboard.ayer')}</span>
                  </div>
                </div>
              </div>
              <div className="dashboard-card">
                <h3 className="dashboard-card-title">
                  {t('dashboard.alertasSistema')}
                </h3>
                <div className="dashboard-card-content">
                  <div className="dashboard-alert-item dashboard-alert-warning">
                    <div className="dashboard-alert-dot">
                      <div className="dashboard-alert-dot-inner dashboard-alert-dot-warning"></div>
                    </div>
                    <div className="dashboard-alert-content">
                      <p className="dashboard-text dashboard-alert-text dashboard-alert-text-warning">
                        3 {t('dashboard.bienesMantenimiento')}
                      </p>
                    </div>
                  </div>
                  <div className="dashboard-alert-item dashboard-alert-error">
                    <div className="dashboard-alert-dot">
                      <div className="dashboard-alert-dot-inner dashboard-alert-dot-error"></div>
                    </div>
                    <div className="dashboard-alert-content">
                      <p className="dashboard-text dashboard-alert-text dashboard-alert-text-error">
                        2 {t('dashboard.bienesSinAsignar')}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )
      case 'bienes':
        return (
          <div className="dashboard-section">
            <div className="dashboard-header">
              <h1 className="dashboard-title text-2xl font-bold text-gray-900 dark:text-white">
                {t('bienes.titulo')}
              </h1>
              <button
                onClick={() => {
                  setSelectedBien(null)
                  setShowBienModal(true)
                }}
                className="dashboard-text dashboard-btn dashboard-btn-green"
              >
                {t('bienes.agregar')}
              </button>
            </div>
            <BienesTable onEdit={handleEditBien} />
          </div>
        )
      case 'cuentadantes':
        return (
          <div className="dashboard-section">
            <div className="dashboard-header">
              <h1 className="dashboard-title text-2xl font-bold text-gray-900 dark:text-white">
                {t('cuentadantes.titulo')}
              </h1>
              <button
                onClick={() => {
                  setSelectedCuentadante(null)
                  setShowCuentadanteModal(true)
                }}
                className="dashboard-text dashboard-btn dashboard-btn-green"
              >
                {t('cuentadantes.agregar')}
              </button>
            </div>
            <CuentadantesTable onEdit={handleEditCuentadante} />
          </div>
        )
      case 'asignaciones':
        return (
          <div className="dashboard-section">
            <div className="dashboard-header">
              <h1 className="dashboard-title text-2xl font-bold text-gray-900 dark:text-white">
                {t('asignaciones.titulo')}
              </h1>
              <button
                onClick={() => setShowAsignacionModal(true)}
                className="dashboard-text dashboard-btn dashboard-btn-blue"
              >
                {t('asignaciones.nueva')}
              </button>
            </div>
            <AsignacionesTable />
          </div>
        )
      default:
        return null
    }
  }

  return (
    <div className="dashboard-container">
      <Sidebar 
        activeView={activeView} 
        onViewChange={setActiveView}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onLogout={onLogout}
      />
      
      <div className="dashboard-main-wrapper">
        <Header 
          onLogout={onLogout}
          onMenuClick={() => setSidebarOpen(!sidebarOpen)}
        />
        
        <main className="dashboard-main-content">
          {renderContent()}
        </main>
      </div>

      {/* Modales */}
      {showAsignacionModal && (
        <AsignacionModal
          onClose={() => setShowAsignacionModal(false)}
        />
      )}

      {showBienModal && (
        <BienModal
          bien={selectedBien}
          onClose={() => {
            setShowBienModal(false)
            setSelectedBien(null)
          }}
        />
      )}

      {showCuentadanteModal && (
        <CuentadanteModal
          cuentadante={selectedCuentadante}
          onClose={() => {
            setShowCuentadanteModal(false)
            setSelectedCuentadante(null)
          }}
        />
      )}
    </div>
  )
}

export default Dashboard

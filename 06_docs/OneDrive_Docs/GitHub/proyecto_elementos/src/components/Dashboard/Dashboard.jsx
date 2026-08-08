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
import Sidebar from '../Sidebar/Sidebar'
import Header from '../Header'
import StatsCards from '../StatsCards'
import BienesTable from '../Bienes/BienesTable'
import PersonasTable from '../Personas/PersonasTable'
import AsignacionesTable from '../Asignaciones/AsignacionesTable'
import RolesTable from '../Roles/RolesTable'
import SedesTable from '../Sedes/SedesTable'
import AsignacionModal from '../Asignaciones/AsignacionModal'
import BienModal from '../Bienes/BienModal'
import PersonasModal from '../Personas/PersonasModal'
import RolModal from '../Roles/RolModal'
import SedeModal from '../Sedes/SedeModal'
import '../../assets/css/Dashboard.css'

const Dashboard = ({ onLogout }) => {
  // ============================================
  // ESTADOS DEL COMPONENTE
  // ============================================
  
  // Vista activa actual (dashboard, bienes, cuentadantes, asignaciones)
  const [activeView, setActiveView] = useState('dashboard')
  
  // Control de visibilidad de modales
  const [showAsignacionModal, setShowAsignacionModal] = useState(false)
  const [showBienModal, setShowBienModal] = useState(false)
  const [showPersonaModal, setShowPersonaModal] = useState(false)
  const [showRolModal, setShowRolModal] = useState(false)
  const [showSedeModal, setShowSedeModal] = useState(false)
  
  // Elementos seleccionados para edición
  const [selectedBien, setSelectedBien] = useState(null)
  const [selectedPersona, setSelectedPersona] = useState(null)
  const [selectedRol, setSelectedRol] = useState(null)
  const [selectedSede, setSelectedSede] = useState(null)
  
  // Control del sidebar (abierto/cerrado)
  const [sidebarOpen, setSidebarOpen] = useState(false)

  // ============================================
  // HOOKS DE CONTEXTO
  // ============================================
  const { user } = useAuth() // Información del usuario actual
  const { stats, refreshData } = useData() // Estadísticas del sistema
  const { t } = useTranslation() // Hook de traducción
  
  // Estado para forzar recarga de tablas
  const [refreshKey, setRefreshKey] = useState(0)

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
   * Abre el modal de edición de persona
   * @param {Object} persona - Persona a editar
   */
  const handleEditPersona = (persona) => {
    setSelectedPersona(persona)
    setShowPersonaModal(true)
  }

  /**
   * Abre el modal de edición de rol
   * @param {Object} rol - Rol a editar
   */
  const handleEditRol = (rol) => {
    setSelectedRol(rol)
    setShowRolModal(true)
  }

  /**
   * Abre el modal de edición de sede
   * @param {Object} sede - Sede a editar
   */
  const handleEditSede = (sede) => {
    setSelectedSede(sede)
    setShowSedeModal(true)
  }

  /**
   * ============================================
   * RENDERIZADO DE CONTENIDO DINÁMICO
   * ============================================
   * Muestra el contenido según la vista activa seleccionada
   * en el sidebar (Dashboard, Bienes, Cuentadantes, Asignaciones, Roles, Sedes)
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
      case 'personas':
        return (
          <div className="dashboard-section">
            <div className="dashboard-header">
              <h1 className="dashboard-title text-2xl font-bold text-gray-900 dark:text-white">
                Gestión de Personas
              </h1>
              <button
                onClick={() => {
                  setSelectedPersona(null)
                  setShowPersonaModal(true)
                }}
                className="dashboard-text dashboard-btn dashboard-btn-green"
              >
                Crear Persona
              </button>
            </div>
            <PersonasTable key={`personas-${refreshKey}`} onEdit={handleEditPersona} />
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
      case 'roles':
        return (
          <div className="dashboard-section">
            <div className="dashboard-header">
              <h1 className="dashboard-title text-2xl font-bold text-gray-900 dark:text-white">
                Gestión de Roles
              </h1>
              <button
                onClick={() => {
                  setSelectedRol(null)
                  setShowRolModal(true)
                }}
                className="dashboard-text dashboard-btn dashboard-btn-green"
              >
                Crear Rol
              </button>
            </div>
            <RolesTable key={`roles-${refreshKey}`} onEdit={handleEditRol} />
          </div>
        )
      case 'sedes':
        return (
          <div className="dashboard-section">
            <div className="dashboard-header">
              <h1 className="dashboard-title text-2xl font-bold text-gray-900 dark:text-white">
                Gestión de Sedes
              </h1>
              <button
                onClick={() => {
                  setSelectedSede(null)
                  setShowSedeModal(true)
                }}
                className="dashboard-text dashboard-btn dashboard-btn-green"
              >
                Crear Sede
              </button>
            </div>
            <SedesTable key={`sedes-${refreshKey}`} onEdit={handleEditSede} />
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
          activeView={activeView}
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

      {showPersonaModal && (
        <PersonasModal
          persona={selectedPersona}
          onClose={() => {
            setShowPersonaModal(false)
            setSelectedPersona(null)
          }}
          onSuccess={() => {
            // Recargar datos de personas
            refreshData()
            setRefreshKey(prev => prev + 1)
          }}
        />
      )}

      {showRolModal && (
        <RolModal
          rol={selectedRol}
          onClose={() => {
            setShowRolModal(false)
            setSelectedRol(null)
          }}
          onSuccess={() => {
            // Recargar la tabla de roles
            setRefreshKey(prev => prev + 1)
          }}
        />
      )}

      {showSedeModal && (
        <SedeModal
          sede={selectedSede}
          onClose={() => {
            setShowSedeModal(false)
            setSelectedSede(null)
          }}
          onSuccess={() => {
            // Recargar la tabla de sedes
            setRefreshKey(prev => prev + 1)
          }}
        />
      )}
    </div>
  )
}

export default Dashboard
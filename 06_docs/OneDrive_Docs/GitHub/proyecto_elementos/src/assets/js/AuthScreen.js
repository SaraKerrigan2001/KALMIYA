/**
 * ============================================
 * AUTHSCREEN.JSX - Pantalla de autenticación
 * ============================================
 * 
 * Este componente maneja el login y registro de usuarios.
 * Incluye:
 * - Tabs para cambiar entre Login y Registro
 * - Formularios con validación
 * - Enlace para recuperar contraseña
 * - Animaciones y efectos visuales
 * 
 * @param {Function} onLogin - Función que se ejecuta al iniciar sesión exitosamente
 */

import { useState } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { useNotifications } from '../../hooks/useNotifications'
import RecuperarPasswordModal from '../../components/RecuperarPasswordModal'
import '../css/AuthScreen.css'

const AuthScreen = ({ onLogin }) => {
  // ============================================
  // ESTADOS DEL COMPONENTE
  // ============================================
  const notifications = useNotifications()
  
  // Controla si está en modo Login (true) o Registro (false)
  const [isLogin, setIsLogin] = useState(true)
  
  // Controla la visibilidad del modal de recuperar contraseña
  const [showRecuperarPassword, setShowRecuperarPassword] = useState(false)
  
  // Datos del formulario
  const [formData, setFormData] = useState({
    correo: '',
    password: '',
    nombre: '',
    area: '',
    rol: ''
  })
  
  // Errores de validación
  const [errors, setErrors] = useState({})
  
  // Estado de carga durante el envío del formulario
  const [isLoading, setIsLoading] = useState(false)

  // ============================================
  // HOOKS DE CONTEXTO
  // ============================================
  const { login, register } = useAuth() // Funciones de autenticación

  /**
   * ============================================
   * MANEJO DE CAMBIOS EN LOS INPUTS
   * ============================================
   * Actualiza el estado del formulario y limpia errores
   */
  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    // Limpiar error del campo cuando el usuario empieza a escribir
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }))
    }
  }

  const validateForm = () => {
    const newErrors = {}

    if (!formData.correo.trim()) {
      newErrors.correo = 'El correo es requerido'
    } else if (!/\S+@\S+\.\S+/.test(formData.correo)) {
      newErrors.correo = 'El correo no es válido'
    }

    if (!formData.password.trim()) {
      newErrors.password = 'La contraseña es requerida'
    } else if (formData.password.length < 6) {
      newErrors.password = 'La contraseña debe tener al menos 6 caracteres'
    }

    if (!isLogin) {
      if (!formData.nombre.trim()) {
        newErrors.nombre = 'El nombre es requerido'
      }
      if (!formData.area) {
        newErrors.area = 'El área es requerida'
      }
      if (!formData.rol) {
        newErrors.rol = 'El rol es requerido'
      }
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) return

    setIsLoading(true)

    try {
      if (isLogin) {
        const result = await login(formData)
        if (result.success) {
          notifications.loginExitoso(result.user.nombre)
          setTimeout(() => {
            onLogin()
          }, 500)
        }
      } else {
        const result = await register(formData)
        if (result.success) {
          notifications.loginExitoso(result.user.nombre)
          setTimeout(() => {
            onLogin()
          }, 500)
        }
      }
    } catch (error) {
      setErrors({ general: 'Error al procesar la solicitud. Intente nuevamente.' })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="auth-screen-container">
      
      {/* Partículas de fondo */}
      <div className="auth-particles">
        <div className="auth-particle-1"></div>
        <div className="auth-particle-2"></div>
      </div>

      <div className="auth-content-wrapper">
        {/* Logo y título */}
        <div className="auth-logo-section">
          <img 
            src="/sena-logo.png.png" 
            alt="Logo SENA" 
            className="auth-logo-img"
          />
          <h1 className="epic-title auth-font text-4xl font-extrabold mb-2">
            SENA BIENES
          </h1>
          <p className="auth-font auth-subtitle">
            Sistema Integral de Control de Bienes
          </p>
        </div>

        {/* Formulario */}
        <div className="auth-form-card">
          <div className="auth-tabs-container">
            <button
              type="button"
              onClick={() => setIsLogin(true)}
              className={`auth-font auth-tab-button ${isLogin ? 'active' : 'inactive'}`}
            >
              Iniciar Sesión
            </button>
            <button
              type="button"
              onClick={() => setIsLogin(false)}
              className={`auth-font auth-tab-button ${!isLogin ? 'active' : 'inactive'}`}
            >
              Registrarse
            </button>
          </div>

          <form onSubmit={handleSubmit} className="auth-form">
            {errors.general && (
              <div className="auth-error-message">
                {errors.general}
              </div>
            )}

            {!isLogin && (
              <div className="auth-field">
                <label htmlFor="nombre" className="auth-label">
                  Nombre Completo
                </label>
                <input
                  id="nombre"
                  name="nombre"
                  type="text"
                  value={formData.nombre}
                  onChange={handleInputChange}
                  className={`auth-input ${errors.nombre ? 'error' : ''}`}
                  placeholder="Tu nombre completo"
                />
                {errors.nombre && <p className="auth-error-text">{errors.nombre}</p>}
              </div>
            )}

            <div className="auth-field">
              <label htmlFor="correo" className="auth-label">
                Correo Electrónico
              </label>
              <input
                id="correo"
                name="correo"
                type="email"
                value={formData.correo}
                onChange={handleInputChange}
                className={`auth-input ${errors.correo ? 'error' : ''}`}
                placeholder="correo@sena.edu.co"
              />
              {errors.correo && <p className="auth-error-text">{errors.correo}</p>}
            </div>

            <div className="auth-field">
              <label htmlFor="password" className="auth-label">
                Contraseña
              </label>
              <input
                id="password"
                name="password"
                type="password"
                value={formData.password}
                onChange={handleInputChange}
                className={`auth-input ${errors.password ? 'error' : ''}`}
                placeholder="••••••••"
              />
              {errors.password && <p className="auth-error-text">{errors.password}</p>}
            </div>

            {!isLogin && (
              <>
                <div className="auth-field">
                  <label htmlFor="area" className="auth-label">
                    Área
                  </label>
                  <select
                    id="area"
                    name="area"
                    value={formData.area}
                    onChange={handleInputChange}
                    className={`auth-input ${errors.area ? 'error' : ''}`}
                  >
                    <option value="">Seleccione un área</option>
                    <option value="Administración">Administración</option>
                    <option value="Coordinación">Coordinación</option>
                    <option value="Sistemas">Sistemas</option>
                    <option value="Contabilidad">Contabilidad</option>
                    <option value="Recursos Humanos">Recursos Humanos</option>
                    <option value="Almacén">Almacén</option>
                  </select>
                  {errors.area && <p className="auth-error-text">{errors.area}</p>}
                </div>

                <div className="auth-field">
                  <label htmlFor="rol" className="auth-label">
                    Rol
                  </label>
                  <select
                    id="rol"
                    name="rol"
                    value={formData.rol}
                    onChange={handleInputChange}
                    className={`auth-input ${errors.rol ? 'error' : ''}`}
                  >
                    <option value="">Seleccione un rol</option>
                    <option value="Administrador">Administrador</option>
                    <option value="Coordinador">Coordinador</option>
                    <option value="Almacenista">Almacenista</option>
                    <option value="Usuario">Usuario</option>
                  </select>
                  {errors.rol && <p className="auth-error-text">{errors.rol}</p>}
                </div>
              </>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="auth-submit-button"
            >
              {isLoading ? 'Procesando...' : (isLogin ? 'Iniciar Sesión' : 'Registrarse')}
            </button>
          </form>

          {isLogin && (
            <div className="auth-forgot-password">
              <button
                type="button"
                onClick={() => setShowRecuperarPassword(true)}
                className="auth-forgot-password-button"
              >
                ¿Olvidaste tu contraseña?
              </button>
            </div>
          )}
        </div>

        {/* Información adicional */}
        <div className="auth-footer-info">
          <p>Sistema SENA | Versión 2025.1</p>
          <p>© 2025 Todos los derechos reservados</p>
        </div>
      </div>

      {/* Modal de Recuperar Contraseña */}
      {showRecuperarPassword && (
        <RecuperarPasswordModal onClose={() => setShowRecuperarPassword(false)} />
      )}
    </div>
  )
}

export default AuthScreen

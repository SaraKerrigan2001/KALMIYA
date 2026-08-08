import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useNotifications } from '../hooks/useNotifications'
import '../assets/css/PerfilModal.css'

const PerfilModal = ({ onClose }) => {
  const { user, updateProfile } = useAuth()
  const notifications = useNotifications()
  const [formData, setFormData] = useState({
    nombre: '',
    correo: '',
    area: '',
    cargo: '',
    telefono: '',
    direccion: ''
  })
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')

  useEffect(() => {
    if (user) {
      setFormData({
        nombre: user.nombre || '',
        correo: user.correo || '',
        area: user.area || '',
        cargo: user.cargo || '',
        telefono: user.telefono || '',
        direccion: user.direccion || ''
      })
    }
  }, [user])

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }))
    }
  }

  const validateForm = () => {
    const newErrors = {}

    if (!formData.nombre.trim()) {
      newErrors.nombre = 'El nombre es requerido'
    }
    if (!formData.correo.trim()) {
      newErrors.correo = 'El correo es requerido'
    } else if (!/\S+@\S+\.\S+/.test(formData.correo)) {
      newErrors.correo = 'El correo no es válido'
    }
    if (!formData.area) {
      newErrors.area = 'El área es requerida'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) return

    setIsLoading(true)
    setSuccessMessage('')

    try {
      await updateProfile(formData)
      setSuccessMessage('Perfil actualizado exitosamente')
      notifications.perfilActualizado()
      
      setTimeout(() => {
        onClose()
      }, 1500)
    } catch (error) {
      setErrors({ general: 'Error al actualizar el perfil. Intente nuevamente.' })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="perfil-modal-overlay">
      <div className="perfil-modal-container">
        {/* Header */}
        <div className="perfil-modal-header">
          <div className="perfil-modal-header-content">
            <div className="perfil-modal-header-info">
              <img 
                src="/sena-logo.png (2).png" 
                alt="Perfil" 
                className="perfil-modal-avatar"
              />
              <div>
                <h2 className="perfil-modal-title">
                  Mi Perfil
                </h2>
                <p className="perfil-modal-subtitle">
                  Actualiza tu información personal
                </p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="perfil-modal-close"
            >
              <span className="perfil-modal-close-icon">×</span>
            </button>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="perfil-modal-form">
          {errors.general && (
            <div className="perfil-modal-alert perfil-modal-alert-error">
              {errors.general}
            </div>
          )}

          {successMessage && (
            <div className="perfil-modal-alert perfil-modal-alert-success">
              {successMessage}
            </div>
          )}

          <div className="perfil-modal-grid">
            {/* Nombre */}
            <div>
              <label htmlFor="nombre" className="perfil-modal-field-label">
                Nombre Completo *
              </label>
              <input
                id="nombre"
                name="nombre"
                type="text"
                value={formData.nombre}
                onChange={handleInputChange}
                className={`perfil-modal-input ${errors.nombre ? 'perfil-modal-input-error' : ''}`}
                placeholder="Tu nombre completo"
              />
              {errors.nombre && <p className="perfil-modal-error-text">{errors.nombre}</p>}
            </div>

            {/* Correo */}
            <div>
              <label htmlFor="correo" className="perfil-modal-field-label">
                Correo Electrónico *
              </label>
              <input
                id="correo"
                name="correo"
                type="email"
                value={formData.correo}
                onChange={handleInputChange}
                className={`perfil-modal-input ${errors.correo ? 'perfil-modal-input-error' : ''}`}
                placeholder="correo@sena.edu.co"
              />
              {errors.correo && <p className="perfil-modal-error-text">{errors.correo}</p>}
            </div>

            {/* Área */}
            <div>
              <label htmlFor="area" className="perfil-modal-field-label">
                Área *
              </label>
              <select
                id="area"
                name="area"
                value={formData.area}
                onChange={handleInputChange}
                className={`perfil-modal-input ${errors.area ? 'perfil-modal-input-error' : ''}`}
              >
                <option value="">Seleccione un área</option>
                <option value="Administración">Administración</option>
                <option value="Coordinación">Coordinación</option>
                <option value="Sistemas">Sistemas</option>
                <option value="Contabilidad">Contabilidad</option>
                <option value="Recursos Humanos">Recursos Humanos</option>
                <option value="Almacén">Almacén</option>
              </select>
              {errors.area && <p className="perfil-modal-error-text">{errors.area}</p>}
            </div>

            {/* Cargo */}
            <div>
              <label htmlFor="cargo" className="perfil-modal-field-label">
                Cargo
              </label>
              <input
                id="cargo"
                name="cargo"
                type="text"
                value={formData.cargo}
                onChange={handleInputChange}
                className="perfil-modal-input"
                placeholder="Tu cargo"
              />
            </div>

            {/* Teléfono */}
            <div>
              <label htmlFor="telefono" className="perfil-modal-field-label">
                Teléfono
              </label>
              <input
                id="telefono"
                name="telefono"
                type="tel"
                value={formData.telefono}
                onChange={handleInputChange}
                className="perfil-modal-input"
                placeholder="3001234567"
              />
            </div>

            {/* Dirección */}
            <div>
              <label htmlFor="direccion" className="perfil-modal-field-label">
                Dirección
              </label>
              <input
                id="direccion"
                name="direccion"
                type="text"
                value={formData.direccion}
                onChange={handleInputChange}
                className="perfil-modal-input"
                placeholder="Tu dirección"
              />
            </div>
          </div>

          {/* Información adicional */}
          <div className="perfil-modal-info-box">
            <h4 className="perfil-modal-info-title">
              Información de la Cuenta
            </h4>
            <div className="perfil-modal-info-content">
              <p><strong>ID de Usuario:</strong> {user?.id}</p>
              <p><strong>Rol:</strong> {user?.rol || 'Usuario'}</p>
              <p><strong>Fecha de Registro:</strong> {new Date().toLocaleDateString()}</p>
            </div>
          </div>

          {/* Buttons */}
          <div className="perfil-modal-footer">
            <button
              type="button"
              onClick={onClose}
              className="perfil-modal-button perfil-modal-button-cancel"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="perfil-modal-button perfil-modal-button-submit"
            >
              {isLoading ? 'Guardando...' : 'Guardar Cambios'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default PerfilModal

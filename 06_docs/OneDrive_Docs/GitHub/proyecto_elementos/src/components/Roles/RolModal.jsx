import { useState, useEffect } from 'react'
import { useNotifications } from '../../hooks/useNotifications'
import '../../assets/css/PersonasModal.css'

const RolModal = ({ rol, onClose, onSuccess }) => {
  const notifications = useNotifications()
  const [formData, setFormData] = useState({
    rol_nombre: ''
  })
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)

  const isEditing = !!rol

  useEffect(() => {
    if (rol) {
      setFormData({
        rol_nombre: rol.rol_nombre || ''
      })
    }
  }, [rol])

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

    if (!formData.rol_nombre.trim()) {
      newErrors.rol_nombre = 'El nombre del rol es requerido'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) return

    setIsLoading(true)

    try {
      const url = isEditing 
        ? `http://localhost:3001/api/roles/${rol.rol_id}`
        : 'http://localhost:3001/api/roles'
      
      const method = isEditing ? 'PUT' : 'POST'
      
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        notifications.custom(
          'success',
          isEditing ? 'Rol actualizado' : 'Rol creado',
          isEditing 
            ? `El rol "${formData.rol_nombre}" ha sido actualizado exitosamente`
            : `El rol "${formData.rol_nombre}" ha sido creado exitosamente`,
          4000
        )
        if (onSuccess) onSuccess()
        setTimeout(() => {
          onClose()
        }, 500)
      } else {
        throw new Error('Error al guardar el rol')
      }
    } catch (error) {
      console.error('Error:', error)
      setErrors({ general: 'Error al guardar el rol. Intente nuevamente.' })
      notifications.custom('error', 'Error', error.message || 'Error al guardar el rol', 5000)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="personas-modal-overlay">
      <div className="personas-modal-container">
        {/* Header */}
        <div className="personas-modal-header">
          <div className="personas-modal-header-content">
            <h2 className="personas-modal-title">
              {isEditing ? 'Editar Rol' : 'Crear Nuevo Rol'}
            </h2>
            <button
              onClick={onClose}
              className="personas-modal-close"
            >
              <span className="personas-modal-close-icon">×</span>
            </button>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="personas-modal-form">
          {errors.general && (
            <div className="personas-modal-error">
              {errors.general}
            </div>
          )}

          <div className="personas-modal-field">
            <label htmlFor="rol_nombre" className="personas-modal-label">
              Nombre del Rol *
            </label>
            <input
              id="rol_nombre"
              name="rol_nombre"
              type="text"
              value={formData.rol_nombre}
              onChange={handleInputChange}
              className={`personas-modal-input ${errors.rol_nombre ? 'error' : ''}`}
              placeholder="Ej: Administrador, Coordinador, Instructor"
              autoFocus
            />
            {errors.rol_nombre && <p className="personas-modal-error-text">{errors.rol_nombre}</p>}
          </div>

          {/* Buttons */}
          <div className="personas-modal-footer">
            <button
              type="button"
              onClick={onClose}
              className="personas-modal-btn-cancel"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="personas-modal-btn-submit"
            >
              {isLoading ? 'Guardando...' : (isEditing ? 'Actualizar' : 'Crear')}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default RolModal

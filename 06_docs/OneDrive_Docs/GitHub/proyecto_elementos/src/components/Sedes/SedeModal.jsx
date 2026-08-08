import { useState, useEffect } from 'react'
import { useNotifications } from '../../hooks/useNotifications'
import '../../assets/css/PersonasModal.css'

const SedeModal = ({ sede, onClose, onSuccess }) => {
  const notifications = useNotifications()
  const [formData, setFormData] = useState({
    sede_nombre: ''
  })
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)

  const isEditing = !!sede

  useEffect(() => {
    if (sede) {
      setFormData({
        sede_nombre: sede.sede_nombre || ''
      })
    }
  }, [sede])

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

    if (!formData.sede_nombre.trim()) {
      newErrors.sede_nombre = 'El nombre de la sede es requerido'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) return

    setIsLoading(true)
    setErrors({})

    try {
      const url = isEditing 
        ? `http://localhost:3001/api/sedes/${sede.sede_id}`
        : 'http://localhost:3001/api/sedes'
      
      const method = isEditing ? 'PUT' : 'POST'
      
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      const data = await response.json()

      if (response.ok) {
        notifications.custom(
          'success',
          isEditing ? 'Sede actualizada' : 'Sede creada',
          isEditing 
            ? `La sede "${formData.sede_nombre}" ha sido actualizada exitosamente`
            : `La sede "${formData.sede_nombre}" ha sido creada exitosamente`,
          4000
        )
        if (onSuccess) onSuccess()
        setTimeout(() => {
          onClose()
        }, 500)
      } else {
        throw new Error(data.error || 'Error al guardar la sede')
      }
    } catch (error) {
      console.error('Error:', error)
      setErrors({ general: error.message || 'Error al guardar la sede. Intente nuevamente.' })
      notifications.custom('error', 'Error', error.message || 'Error al guardar la sede', 5000)
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
              {isEditing ? 'Editar Sede' : 'Crear Nueva Sede'}
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
            <label htmlFor="sede_nombre" className="personas-modal-label">
              Nombre de la Sede *
            </label>
            <input
              id="sede_nombre"
              name="sede_nombre"
              type="text"
              value={formData.sede_nombre}
              onChange={handleInputChange}
              className={`personas-modal-input ${errors.sede_nombre ? 'error' : ''}`}
              placeholder="Ej: Sede Principal, Sede Norte, Sede Centro"
              autoFocus
            />
            {errors.sede_nombre && <p className="personas-modal-error-text">{errors.sede_nombre}</p>}
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

export default SedeModal

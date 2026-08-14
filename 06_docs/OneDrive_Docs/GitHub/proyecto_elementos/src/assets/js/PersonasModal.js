import { useState, useEffect } from 'react'
import { useData } from '../../contexts/DataContext'
import { useNotifications } from '../../hooks/useNotifications'
import '../css/personaModal.css'

const personaModal = ({ persona, onClose }) => {
  const { addpersona } = useData()
  const notifications = useNotifications()
  const [formData, setFormData] = useState({
    cedula: '',
    nombre: '',
    cargo: '',
    area: '',
    correo: '',
    telefono: ''
  })
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)

  const isEditing = !!persona

  useEffect(() => {
    if (persona) {
      setFormData({
        cedula: persona.cedula,
        nombre: persona.nombre,
        cargo: persona.cargo,
        area: persona.area,
        correo: persona.correo,
        telefono: persona.telefono
      })
    }
  }, [persona])

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    // Limpiar error del campo
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }))
    }
  }

  const validateForm = () => {
    const newErrors = {}

    if (!formData.cedula.trim()) {
      newErrors.cedula = 'La cédula es requerida'
    }
    if (!formData.nombre.trim()) {
      newErrors.nombre = 'El nombre es requerido'
    }
    if (!formData.cargo.trim()) {
      newErrors.cargo = 'El cargo es requerido'
    }
    if (!formData.area.trim()) {
      newErrors.area = 'El área es requerida'
    }
    if (!formData.correo.trim()) {
      newErrors.correo = 'El correo es requerido'
    } else if (!/\S+@\S+\.\S+/.test(formData.correo)) {
      newErrors.correo = 'El correo no es válido'
    }
    if (!formData.telefono.trim()) {
      newErrors.telefono = 'El teléfono es requerido'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) return

    setIsLoading(true)

    try {
      if (isEditing) {
        // Aquí iría la lógica para actualizar persona
        console.log('Actualizar persona:', formData)
        notifications.personaActualizado(formData.nombre)
      } else {
        addpersona(formData)
        notifications.personaCreado(formData.nombre)
      }

      setTimeout(() => {
        onClose()
      }, 500)
    } catch (error) {
      setErrors({ general: 'Error al guardar el persona. Intente nuevamente.' })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="persona-modal-overlay">
      <div className="persona-modal-container">
        {/* Header */}
        <div className="persona-modal-header">
          <div className="persona-modal-header-content">
            <h2 className="persona-modal-title">
              {isEditing ? 'Editar persona' : 'Agregar Nuevo persona'}
            </h2>
            <button
              onClick={onClose}
              className="persona-modal-close"
            >
              <span className="persona-modal-close-icon">×</span>
            </button>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="persona-modal-form">
          {errors.general && (
            <div className="persona-modal-error">
              {errors.general}
            </div>
          )}

          <div className="persona-modal-field">
            <label htmlFor="cedula" className="persona-modal-label">
              Cédula *
            </label>
            <input
              id="cedula"
              name="cedula"
              type="text"
              value={formData.cedula}
              onChange={handleInputChange}
              className={`persona-modal-input ${errors.cedula ? 'error' : ''}`}
              placeholder="Número de cédula"
            />
            {errors.cedula && <p className="persona-modal-error-text">{errors.cedula}</p>}
          </div>

          <div className="persona-modal-field">
            <label htmlFor="nombre" className="persona-modal-label">
              Nombre Completo *
            </label>
            <input
              id="nombre"
              name="nombre"
              type="text"
              value={formData.nombre}
              onChange={handleInputChange}
              className={`persona-modal-input ${errors.nombre ? 'error' : ''}`}
              placeholder="Nombre completo del persona"
            />
            {errors.nombre && <p className="persona-modal-error-text">{errors.nombre}</p>}
          </div>

          <div className="persona-modal-field">
            <label htmlFor="cargo" className="persona-modal-label">
              Cargo *
            </label>
            <input
              id="cargo"
              name="cargo"
              type="text"
              value={formData.cargo}
              onChange={handleInputChange}
              className={`persona-modal-input ${errors.cargo ? 'error' : ''}`}
              placeholder="Cargo en la institución"
            />
            {errors.cargo && <p className="persona-modal-error-text">{errors.cargo}</p>}
          </div>

          <div className="persona-modal-field">
            <label htmlFor="area" className="persona-modal-label">
              Área *
            </label>
            <select
              id="area"
              name="area"
              value={formData.area}
              onChange={handleInputChange}
              className={`persona-modal-select ${errors.area ? 'error' : ''}`}
            >
              <option value="">Seleccione un área</option>
              <option value="Administración">Administración</option>
              <option value="Coordinación">Coordinación</option>
              <option value="Sistemas">Sistemas</option>
              <option value="Contabilidad">Contabilidad</option>
              <option value="Recursos Humanos">Recursos Humanos</option>
              <option value="Almacén">Almacén</option>
            </select>
            {errors.area && <p className="persona-modal-error-text">{errors.area}</p>}
          </div>

          <div className="persona-modal-field">
            <label htmlFor="correo" className="persona-modal-label">
              Correo Electrónico *
            </label>
            <input
              id="correo"
              name="correo"
              type="email"
              value={formData.correo}
              onChange={handleInputChange}
              className={`persona-modal-input ${errors.correo ? 'error' : ''}`}
              placeholder="correo@sena.edu.co"
            />
            {errors.correo && <p className="persona-modal-error-text">{errors.correo}</p>}
          </div>

          <div className="persona-modal-field">
            <label htmlFor="telefono" className="persona-modal-label">
              Teléfono *
            </label>
            <input
              id="telefono"
              name="telefono"
              type="tel"
              value={formData.telefono}
              onChange={handleInputChange}
              className={`persona-modal-input ${errors.telefono ? 'error' : ''}`}
              placeholder="Número de teléfono"
            />
            {errors.telefono && <p className="persona-modal-error-text">{errors.telefono}</p>}
          </div>

          {/* Buttons */}
          <div className="persona-modal-footer">
            <button
              type="button"
              onClick={onClose}
              className="persona-modal-btn-cancel"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="persona-modal-btn-submit"
            >
              {isLoading ? 'Guardando...' : (isEditing ? 'Actualizar' : 'Crear')}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default personaModal

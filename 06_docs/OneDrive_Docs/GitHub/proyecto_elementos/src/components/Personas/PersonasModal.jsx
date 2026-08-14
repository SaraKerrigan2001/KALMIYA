import { useState, useEffect } from 'react'
import { useData } from '../../contexts/DataContext'
import { useNotifications } from '../../hooks/useNotifications'
import '../../assets/css/PersonasModal.css'

const PersonasModal = ({ persona, onClose, onSuccess }) => {
  const { addCuentadante } = useData()
  const notifications = useNotifications()
  const [formData, setFormData] = useState({
    pers_documento: '',
    pers_nombres: '',
    pers_apellidos: '',
    pers_direccion: '',
    pers_telefono: '',
    pers_tipodoc: 'CC',
    pers_correo: '',
    rol_id: ''
  })
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)
  const [roles, setRoles] = useState([])

  const isEditing = !!persona

  // Cargar roles disponibles
  useEffect(() => {
    const loadRoles = async () => {
      try {
        const rolesRes = await fetch('http://localhost:3001/api/roles')
        const rolesData = await rolesRes.json()
        setRoles(rolesData)
      } catch (error) {
        console.error('Error al cargar roles:', error)
      }
    }
    loadRoles()
  }, [])

  useEffect(() => {
    if (persona) {
      setFormData({
        pers_documento: persona.pers_documento || '',
        pers_nombres: persona.pers_nombres || '',
        pers_apellidos: persona.pers_apellidos || '',
        pers_direccion: persona.pers_direccion || '',
        pers_telefono: persona.pers_telefono || '',
        pers_tipodoc: persona.pers_tipodoc || 'CC',
        pers_correo: persona.pers_correo || '',
        rol_id: persona.rol_id || ''
      })
    }
  }, [persona])

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

    if (!formData.pers_documento.toString().trim()) {
      newErrors.pers_documento = 'El documento es requerido'
    }
    if (!formData.pers_nombres.trim()) {
      newErrors.pers_nombres = 'Los nombres son requeridos'
    }
    if (!formData.pers_apellidos.trim()) {
      newErrors.pers_apellidos = 'Los apellidos son requeridos'
    }
    if (!formData.pers_direccion.trim()) {
      newErrors.pers_direccion = 'La dirección es requerida'
    }
    if (!formData.pers_telefono.toString().trim()) {
      newErrors.pers_telefono = 'El teléfono es requerido'
    }
    if (!formData.pers_tipodoc.trim()) {
      newErrors.pers_tipodoc = 'El tipo de documento es requerido'
    }
    if (!formData.pers_correo.trim()) {
      newErrors.pers_correo = 'El correo es requerido'
    } else if (!/\S+@\S+\.\S+/.test(formData.pers_correo)) {
      newErrors.pers_correo = 'El correo no es válido'
    }
    if (!formData.rol_id) {
      newErrors.rol_id = 'El rol es requerido'
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
        console.log('Actualizar persona:', formData)
        notifications.cuentadanteActualizado(`${formData.pers_nombres} ${formData.pers_apellidos}`)
      } else {
        await addCuentadante(formData)
        notifications.cuentadanteCreado(`${formData.pers_nombres} ${formData.pers_apellidos}`)
      }

      if (onSuccess) {
        onSuccess()
      }

      setTimeout(() => {
        onClose()
      }, 500)
    } catch (error) {
      setErrors({ general: 'Error al guardar la persona. Intente nuevamente.' })
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
              {isEditing ? 'Editar Persona' : 'Agregar Nueva Persona'}
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
            <label htmlFor="pers_tipodoc" className="personas-modal-label">
              Tipo de Documento *
            </label>
            <select
              id="pers_tipodoc"
              name="pers_tipodoc"
              value={formData.pers_tipodoc}
              onChange={handleInputChange}
              className={`personas-modal-input ${errors.pers_tipodoc ? 'error' : ''}`}
            >
              <option value="CC">Cédula de Ciudadanía</option>
              <option value="CE">Cédula de Extranjería</option>
              <option value="TI">Tarjeta de Identidad</option>
              <option value="PAS">Pasaporte</option>
            </select>
            {errors.pers_tipodoc && <p className="personas-modal-error-text">{errors.pers_tipodoc}</p>}
          </div>

          <div className="personas-modal-field">
            <label htmlFor="pers_documento" className="personas-modal-label">
              Número de Documento *
            </label>
            <input
              id="pers_documento"
              name="pers_documento"
              type="number"
              value={formData.pers_documento}
              onChange={handleInputChange}
              className={`personas-modal-input ${errors.pers_documento ? 'error' : ''}`}
              placeholder="Número de documento"
            />
            {errors.pers_documento && <p className="personas-modal-error-text">{errors.pers_documento}</p>}
          </div>

          <div className="personas-modal-field">
            <label htmlFor="pers_nombres" className="personas-modal-label">
              Nombres *
            </label>
            <input
              id="pers_nombres"
              name="pers_nombres"
              type="text"
              value={formData.pers_nombres}
              onChange={handleInputChange}
              className={`personas-modal-input ${errors.pers_nombres ? 'error' : ''}`}
              placeholder="Nombres de la persona"
              maxLength="45"
            />
            {errors.pers_nombres && <p className="personas-modal-error-text">{errors.pers_nombres}</p>}
          </div>

          <div className="personas-modal-field">
            <label htmlFor="pers_apellidos" className="personas-modal-label">
              Apellidos *
            </label>
            <input
              id="pers_apellidos"
              name="pers_apellidos"
              type="text"
              value={formData.pers_apellidos}
              onChange={handleInputChange}
              className={`personas-modal-input ${errors.pers_apellidos ? 'error' : ''}`}
              placeholder="Apellidos de la persona"
              maxLength="45"
            />
            {errors.pers_apellidos && <p className="personas-modal-error-text">{errors.pers_apellidos}</p>}
          </div>

          <div className="personas-modal-field">
            <label htmlFor="pers_direccion" className="personas-modal-label">
              Dirección *
            </label>
            <input
              id="pers_direccion"
              name="pers_direccion"
              type="text"
              value={formData.pers_direccion}
              onChange={handleInputChange}
              className={`personas-modal-input ${errors.pers_direccion ? 'error' : ''}`}
              placeholder="Dirección de residencia"
              maxLength="45"
            />
            {errors.pers_direccion && <p className="personas-modal-error-text">{errors.pers_direccion}</p>}
          </div>

          <div className="personas-modal-field">
            <label htmlFor="pers_telefono" className="personas-modal-label">
              Teléfono *
            </label>
            <input
              id="pers_telefono"
              name="pers_telefono"
              type="number"
              value={formData.pers_telefono}
              onChange={handleInputChange}
              className={`personas-modal-input ${errors.pers_telefono ? 'error' : ''}`}
              placeholder="Número de teléfono"
            />
            {errors.pers_telefono && <p className="personas-modal-error-text">{errors.pers_telefono}</p>}
          </div>

          <div className="personas-modal-field">
            <label htmlFor="pers_correo" className="personas-modal-label">
              Correo Electrónico *
            </label>
            <input
              id="pers_correo"
              name="pers_correo"
              type="email"
              value={formData.pers_correo}
              onChange={handleInputChange}
              className={`personas-modal-input ${errors.pers_correo ? 'error' : ''}`}
              placeholder="correo@sena.edu.co"
              maxLength="100"
            />
            {errors.pers_correo && <p className="personas-modal-error-text">{errors.pers_correo}</p>}
          </div>

          <div className="personas-modal-field">
            <label htmlFor="rol_id" className="personas-modal-label">
              Rol *
            </label>
            <select
              id="rol_id"
              name="rol_id"
              value={formData.rol_id}
              onChange={handleInputChange}
              className={`personas-modal-input ${errors.rol_id ? 'error' : ''}`}
            >
              <option value="">Seleccione un rol</option>
              {roles.map(rol => (
                <option key={rol.rol_id} value={rol.rol_id}>
                  {rol.rol_nombre}
                </option>
              ))}
            </select>
            {errors.rol_id && <p className="personas-modal-error-text">{errors.rol_id}</p>}
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

export default PersonasModal

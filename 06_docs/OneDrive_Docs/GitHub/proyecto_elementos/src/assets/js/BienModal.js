import { useState, useEffect } from 'react'
import { useData } from '../../contexts/DataContext'
import { useNotifications } from '../../hooks/useNotifications'
import '../css/BienModal.css'

const BienModal = ({ bien, onClose }) => {
  const { addBien, updateBien } = useData()
  const notifications = useNotifications()
  const [formData, setFormData] = useState({
    codigo: '',
    descripcion: '',
    categoria: '',
    valor: '',
    ubicacion: '',
    estado: 'disponible'
  })
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)

  const isEditing = !!bien

  useEffect(() => {
    if (bien) {
      setFormData({
        codigo: bien.codigo,
        descripcion: bien.descripcion,
        categoria: bien.categoria,
        valor: bien.valor.toString(),
        ubicacion: bien.ubicacion,
        estado: bien.estado
      })
    }
  }, [bien])

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

    if (!formData.codigo.trim()) {
      newErrors.codigo = 'El código es requerido'
    }
    if (!formData.descripcion.trim()) {
      newErrors.descripcion = 'La descripción es requerida'
    }
    if (!formData.categoria.trim()) {
      newErrors.categoria = 'La categoría es requerida'
    }
    if (!formData.valor || isNaN(formData.valor) || parseFloat(formData.valor) <= 0) {
      newErrors.valor = 'El valor debe ser un número mayor a 0'
    }
    if (!formData.ubicacion.trim()) {
      newErrors.ubicacion = 'La ubicación es requerida'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) return

    setIsLoading(true)

    try {
      const bienData = {
        ...formData,
        valor: parseFloat(formData.valor)
      }

      if (isEditing) {
        updateBien(bien.id, bienData)
        notifications.bienActualizado(bienData.codigo)
      } else {
        addBien(bienData)
        notifications.bienCreado(bienData.codigo)
      }

      setTimeout(() => {
        onClose()
      }, 500)
    } catch (error) {
      setErrors({ general: 'Error al guardar el bien. Intente nuevamente.' })
      notifications.bienError('Error al guardar el bien. Intente nuevamente.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="bien-modal-overlay">
      <div className="bien-modal-container">
        {/* Header */}
        <div className="bien-modal-header">
          <div className="bien-modal-header-content">
            <h2 className="bien-modal-title">
              {isEditing ? 'Editar Bien' : 'Agregar Nuevo Bien'}
            </h2>
            <button
              onClick={onClose}
              className="bien-modal-close"
            >
              <span className="bien-modal-close-icon">×</span>
            </button>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="bien-modal-form">
          {errors.general && (
            <div className="bien-modal-error">
              {errors.general}
            </div>
          )}

          <div className="bien-modal-field">
            <label htmlFor="codigo" className="bien-modal-label">
              Código *
            </label>
            <input
              id="codigo"
              name="codigo"
              type="text"
              value={formData.codigo}
              onChange={handleInputChange}
              className={`bien-modal-input ${errors.codigo ? 'error' : ''}`}
              placeholder="Ej: HP-2024-001"
            />
            {errors.codigo && <p className="bien-modal-error-text">{errors.codigo}</p>}
          </div>

          <div className="bien-modal-field">
            <label htmlFor="descripcion" className="bien-modal-label">
              Descripción *
            </label>
            <textarea
              id="descripcion"
              name="descripcion"
              value={formData.descripcion}
              onChange={handleInputChange}
              rows={3}
              className={`bien-modal-textarea ${errors.descripcion ? 'error' : ''}`}
              placeholder="Descripción detallada del bien"
            />
            {errors.descripcion && <p className="bien-modal-error-text">{errors.descripcion}</p>}
          </div>

          <div className="bien-modal-field">
            <label htmlFor="categoria" className="bien-modal-label">
              Categoría *
            </label>
            <select
              id="categoria"
              name="categoria"
              value={formData.categoria}
              onChange={handleInputChange}
              className={`bien-modal-select ${errors.categoria ? 'error' : ''}`}
            >
              <option value="">Seleccione una categoría</option>
              <option value="Computadores">Computadores</option>
              <option value="Impresoras">Impresoras</option>
              <option value="Proyectores">Proyectores</option>
              <option value="Tablets">Tablets</option>
              <option value="Monitores">Monitores</option>
              <option value="Equipos de Red">Equipos de Red</option>
              <option value="Otros">Otros</option>
            </select>
            {errors.categoria && <p className="bien-modal-error-text">{errors.categoria}</p>}
          </div>

          <div className="bien-modal-field">
            <label htmlFor="valor" className="bien-modal-label">
              Valor *
            </label>
            <input
              id="valor"
              name="valor"
              type="number"
              value={formData.valor}
              onChange={handleInputChange}
              className={`bien-modal-input ${errors.valor ? 'error' : ''}`}
              placeholder="Valor en pesos colombianos"
            />
            {errors.valor && <p className="bien-modal-error-text">{errors.valor}</p>}
          </div>

          <div className="bien-modal-field">
            <label htmlFor="ubicacion" className="bien-modal-label">
              Ubicación *
            </label>
            <input
              id="ubicacion"
              name="ubicacion"
              type="text"
              value={formData.ubicacion}
              onChange={handleInputChange}
              className={`bien-modal-input ${errors.ubicacion ? 'error' : ''}`}
              placeholder="Ej: Almacén Principal, Aula 201"
            />
            {errors.ubicacion && <p className="bien-modal-error-text">{errors.ubicacion}</p>}
          </div>

          <div className="bien-modal-field">
            <label htmlFor="estado" className="bien-modal-label">
              Estado
            </label>
            <select
              id="estado"
              name="estado"
              value={formData.estado}
              onChange={handleInputChange}
              className="bien-modal-select"
            >
              <option value="disponible">Disponible</option>
              <option value="asignado">Asignado</option>
              <option value="mantenimiento">Mantenimiento</option>
              <option value="baja">Dado de Baja</option>
            </select>
          </div>

          {/* Buttons */}
          <div className="bien-modal-footer">
            <button
              type="button"
              onClick={onClose}
              className="bien-modal-btn-cancel"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="bien-modal-btn-submit"
            >
              {isLoading ? 'Guardando...' : (isEditing ? 'Actualizar' : 'Crear')}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default BienModal

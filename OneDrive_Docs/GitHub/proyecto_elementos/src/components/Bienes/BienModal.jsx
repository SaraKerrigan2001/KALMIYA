import { useState, useEffect } from 'react'
import { useData } from '../../contexts/DataContext'
import { useNotifications } from '../../hooks/useNotifications'
import '../../assets/css/BienModal.css'

const BienModal = ({ bien, onClose }) => {
  const { addBien, updateBien } = useData()
  const notifications = useNotifications()
  const [formData, setFormData] = useState({
    codigo: '',
    descripcion: '',
    modelo: '',
    categoria: '',
    serial: '',
    fechaCompra: '',
    vidaUtil: '',
    costo: ''
  })
  const [marcas, setMarcas] = useState([])
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)

  const isEditing = !!bien

  // Cargar marcas desde la API
  useEffect(() => {
    const loadMarcas = async () => {
      try {
        const response = await fetch('http://localhost:3001/api/marcas')
        if (response.ok) {
          const data = await response.json()
          setMarcas(data)
        } else {
          console.error('Error al cargar marcas')
          setErrors(prev => ({ ...prev, general: 'Error al cargar las categorías' }))
        }
      } catch (error) {
        console.error('Error al cargar marcas:', error)
        setErrors(prev => ({ ...prev, general: 'Error al cargar las categorías' }))
      }
    }
    
    loadMarcas()
  }, [])

  // Cargar datos del bien en modo edición
  useEffect(() => {
    if (bien) {
      // Formatear fecha al formato YYYY-MM-DD para el input date
      let fechaFormateada = ''
      if (bien.fechaIngreso || bien.fechaCreacion) {
        const fecha = new Date(bien.fechaIngreso || bien.fechaCreacion)
        if (!isNaN(fecha.getTime())) {
          fechaFormateada = fecha.toISOString().split('T')[0]
        }
      }

      setFormData({
        codigo: bien.codigo || '',
        descripcion: bien.descripcion || '',
        modelo: bien.modelo || '',
        categoria: bien.categoriaId || bien.marc_id || '',
        serial: bien.serial || '',
        fechaCompra: fechaFormateada,
        vidaUtil: bien.vidaUtil ? bien.vidaUtil.toString() : '',
        costo: bien.costo ? bien.costo.toString() : (bien.valor ? bien.valor.toString() : '')
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
      newErrors.codigo = 'El código/placa es requerido'
    }
    if (!formData.descripcion.trim()) {
      newErrors.descripcion = 'La descripción es requerida'
    }
    if (!formData.modelo.trim()) {
      newErrors.modelo = 'El modelo es requerido'
    }
    if (!formData.categoria) {
      newErrors.categoria = 'La categoría es requerida'
    }
    if (!formData.serial.trim()) {
      newErrors.serial = 'El serial es requerido'
    }
    if (formData.costo && (isNaN(formData.costo) || parseInt(formData.costo) <= 0)) {
      newErrors.costo = 'El costo debe ser un número válido'
    }
    if (formData.vidaUtil && (isNaN(formData.vidaUtil) || parseInt(formData.vidaUtil) <= 0 || !Number.isInteger(parseFloat(formData.vidaUtil)))) {
      newErrors.vidaUtil = 'La vida útil debe ser un número entero'
    }
    if (formData.fechaCompra && isNaN(new Date(formData.fechaCompra).getTime())) {
      newErrors.fechaCompra = 'La fecha de compra debe ser válida'
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
        codigo: formData.codigo,
        descripcion: formData.descripcion,
        modelo: formData.modelo,
        categoria: parseInt(formData.categoria),
        serial: formData.serial,
        fechaCompra: formData.fechaCompra || null,
        vidaUtil: formData.vidaUtil ? parseInt(formData.vidaUtil) : null,
        costo: formData.costo ? parseInt(formData.costo) : null
      }

      if (isEditing) {
        await updateBien(bien.id, bienData)
        notifications.bienActualizado(bienData.codigo)
      } else {
        await addBien(bienData)
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
              Código/Placa *
            </label>
            <input
              id="codigo"
              name="codigo"
              type="text"
              value={formData.codigo}
              onChange={handleInputChange}
              className={`bien-modal-input ${errors.codigo ? 'error' : ''}`}
              placeholder="Ej: HP-2024-001"
              disabled={isEditing}
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
            <label htmlFor="modelo" className="bien-modal-label">
              Modelo *
            </label>
            <input
              id="modelo"
              name="modelo"
              type="text"
              value={formData.modelo}
              onChange={handleInputChange}
              className={`bien-modal-input ${errors.modelo ? 'error' : ''}`}
              placeholder="Ej: EliteBook 840 G8"
            />
            {errors.modelo && <p className="bien-modal-error-text">{errors.modelo}</p>}
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
              {marcas.length === 0 ? (
                <option value="" disabled>No hay marcas disponibles</option>
              ) : (
                marcas.map(marca => (
                  <option key={marca.marc_id} value={marca.marc_id}>
                    {marca.marc_nombre}
                  </option>
                ))
              )}
            </select>
            {errors.categoria && <p className="bien-modal-error-text">{errors.categoria}</p>}
          </div>

          <div className="bien-modal-field">
            <label htmlFor="serial" className="bien-modal-label">
              Serial *
            </label>
            <input
              id="serial"
              name="serial"
              type="text"
              value={formData.serial}
              onChange={handleInputChange}
              className={`bien-modal-input ${errors.serial ? 'error' : ''}`}
              placeholder="Ej: SN001HP2024"
            />
            {errors.serial && <p className="bien-modal-error-text">{errors.serial}</p>}
          </div>

          <div className="bien-modal-field">
            <label htmlFor="fechaCompra" className="bien-modal-label">
              Fecha de Compra
            </label>
            <input
              id="fechaCompra"
              name="fechaCompra"
              type="date"
              value={formData.fechaCompra}
              onChange={handleInputChange}
              className={`bien-modal-input ${errors.fechaCompra ? 'error' : ''}`}
            />
            {errors.fechaCompra && <p className="bien-modal-error-text">{errors.fechaCompra}</p>}
          </div>

          <div className="bien-modal-field">
            <label htmlFor="vidaUtil" className="bien-modal-label">
              Vida Útil (años)
            </label>
            <input
              id="vidaUtil"
              name="vidaUtil"
              type="number"
              value={formData.vidaUtil}
              onChange={handleInputChange}
              className={`bien-modal-input ${errors.vidaUtil ? 'error' : ''}`}
              placeholder="Ej: 5"
              min="1"
            />
            {errors.vidaUtil && <p className="bien-modal-error-text">{errors.vidaUtil}</p>}
          </div>

          <div className="bien-modal-field">
            <label htmlFor="costo" className="bien-modal-label">
              Costo
            </label>
            <input
              id="costo"
              name="costo"
              type="number"
              value={formData.costo}
              onChange={handleInputChange}
              className={`bien-modal-input ${errors.costo ? 'error' : ''}`}
              placeholder="Valor en pesos colombianos"
              min="0"
            />
            {errors.costo && <p className="bien-modal-error-text">{errors.costo}</p>}
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
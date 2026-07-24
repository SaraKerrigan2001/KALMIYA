import { useState } from 'react'
import { useData } from '../../contexts/DataContext'
import { useNotifications } from '../../hooks/useNotifications'
import '../css/AsignacionesModal.css'

const AsignacionModal = ({ onClose }) => {
  const { bienes, cuentadantes, assignBienes } = useData()
  const notifications = useNotifications()
  const [selectedCuentadante, setSelectedCuentadante] = useState('')
  const [selectedBienes, setSelectedBienes] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [cuentadanteSearch, setCuentadanteSearch] = useState('')
  const [showCuentadanteSuggestions, setShowCuentadanteSuggestions] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [errors, setErrors] = useState({})

  // Filtrar solo bienes disponibles
  const bienesDisponibles = bienes.filter(bien => bien.estado === 'disponible')
  
  // Filtrar bienes con búsqueda inteligente
  const filteredBienes = bienesDisponibles.filter(bien => {
    if (!searchTerm.trim()) return true
    
    const searchLower = searchTerm.toLowerCase()
    const searchTerms = searchLower.split(' ').filter(term => term.length > 0)
    
    return searchTerms.every(term => {
      // Buscar en placa/código
      const matchPlaca = bien.codigo?.toLowerCase().includes(term)
      
      // Buscar en descripción
      const matchDescripcion = bien.descripcion?.toLowerCase().includes(term)
      
      // Buscar en modelo
      const matchModelo = bien.modelo?.toLowerCase().includes(term)
      
      // Buscar en serial
      const matchSerial = bien.serial?.toLowerCase().includes(term)
      
      // Buscar en categoría/marca
      const matchCategoria = bien.categoria?.toLowerCase().includes(term)
      
      // Buscar en costo (si es número)
      const matchCosto = bien.valor?.toString().includes(term)
      
      // Buscar en fecha de compra (si parece una fecha)
      const matchFecha = bien.fechaIngreso?.toString().includes(term)
      
      return matchPlaca || matchDescripcion || matchModelo || matchSerial || 
             matchCategoria || matchCosto || matchFecha
    })
  })

  // Filtrar cuentadantes con búsqueda inteligente
  const filteredCuentadantes = cuentadantes.filter(c => {
    if (!c.activo) return false
    if (!cuentadanteSearch.trim()) return true
    
    const searchLower = cuentadanteSearch.toLowerCase()
    const searchTerms = searchLower.split(' ').filter(term => term.length > 0)
    
    return searchTerms.every(term => {
      // Buscar en documento (cédula)
      const matchDocumento = c.cedula?.toString().includes(term)
      
      // Buscar en nombre completo
      const matchNombre = c.nombre?.toLowerCase().includes(term)
      
      // Buscar en área (que puede ser el rol)
      const matchArea = c.area?.toLowerCase().includes(term)
      
      // Buscar en cargo
      const matchCargo = c.cargo?.toLowerCase().includes(term)
      
      return matchDocumento || matchNombre || matchArea || matchCargo
    })
  })

  const handleBienToggle = (bienId) => {
    setSelectedBienes(prev => {
      if (prev.includes(bienId)) {
        return prev.filter(id => id !== bienId)
      } else {
        return [...prev, bienId]
      }
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    const newErrors = {}
    
    if (!selectedCuentadante) {
      newErrors.cuentadante = 'Debe seleccionar un cuentadante'
    }
    
    if (selectedBienes.length === 0) {
      newErrors.bienes = 'Debe seleccionar al menos un bien'
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    setIsLoading(true)

    try {
      const success = assignBienes(selectedBienes, parseInt(selectedCuentadante))
      
      if (success) {
        const cuentadante = cuentadantes.find(c => c.id === parseInt(selectedCuentadante))
        notifications.asignacionExitosa(selectedBienes.length, cuentadante?.nombre || 'cuentadante')
        setTimeout(() => {
          onClose()
        }, 500)
      } else {
        setErrors({ general: 'Error al realizar la asignación' })
        notifications.asignacionError()
      }
    } catch (error) {
      setErrors({ general: 'Error al realizar la asignación. Intente nuevamente.' })
    } finally {
      setIsLoading(false)
    }
  }

  const selectedCuentadanteData = cuentadantes.find(c => c.id === parseInt(selectedCuentadante))

  return (
    <div className="asignacion-modal-overlay">
      <div className="asignacion-modal-container">
        {/* Header */}
        <div className="asignacion-modal-header">
          <div className="asignacion-modal-header-content">
            <h2 className="asignacion-modal-title">
              Nueva Asignación de Bienes
            </h2>
            <button
              onClick={onClose}
              className="asignacion-modal-close"
            >
              <span className="asignacion-modal-close-icon">×</span>
            </button>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="asignacion-modal-form">
          {errors.general && (
            <div className="asignacion-modal-error">
              {errors.general}
            </div>
          )}

          <div className="asignacion-modal-grid">
            {/* Selección de Cuentadante */}
            <div className="asignacion-modal-section">
              <h3 className="asignacion-modal-section-title">
                1. Seleccionar Cuentadante
              </h3>
              
              <div className="asignacion-modal-section-content">
                <label htmlFor="cuentadante" className="asignacion-modal-label">
                  Cuentadante *
                </label>
                <div style={{ position: 'relative' }}>
                  <input
                    id="cuentadante"
                    type="text"
                    placeholder="🔍 Buscar por nombre, documento o área..."
                    value={cuentadanteSearch}
                    onChange={(e) => {
                      setCuentadanteSearch(e.target.value)
                      setShowCuentadanteSuggestions(true)
                      if (errors.cuentadante) {
                        setErrors(prev => ({ ...prev, cuentadante: '' }))
                      }
                    }}
                    onFocus={() => setShowCuentadanteSuggestions(true)}
                    className={`asignacion-modal-search ${errors.cuentadante ? 'error' : ''}`}
                    autoComplete="off"
                  />
                  
                  {showCuentadanteSuggestions && filteredCuentadantes.length > 0 && (
                    <div style={{
                      position: 'absolute',
                      top: '100%',
                      left: 0,
                      right: 0,
                      backgroundColor: 'white',
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px',
                      marginTop: '4px',
                      maxHeight: '300px',
                      overflowY: 'auto',
                      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                      zIndex: 1000
                    }}>
                      {filteredCuentadantes.map(cuentadante => (
                        <div
                          key={cuentadante.id}
                          onClick={() => {
                            setSelectedCuentadante(cuentadante.id)
                            setCuentadanteSearch(`${cuentadante.nombre} - ${cuentadante.cedula}`)
                            setShowCuentadanteSuggestions(false)
                            if (errors.cuentadante) {
                              setErrors(prev => ({ ...prev, cuentadante: '' }))
                            }
                          }}
                          style={{
                            padding: '12px 16px',
                            cursor: 'pointer',
                            borderBottom: '1px solid #f3f4f6',
                            transition: 'background-color 0.2s'
                          }}
                          onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#f9fafb'}
                          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'white'}
                        >
                          <div style={{ fontWeight: '600', color: '#111827', marginBottom: '4px' }}>
                            {cuentadante.nombre}
                          </div>
                          <div style={{ fontSize: '14px', color: '#6b7280' }}>
                            CC: {cuentadante.cedula} • {cuentadante.area || cuentadante.cargo}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
                {errors.cuentadante && <p className="asignacion-modal-error-text">{errors.cuentadante}</p>}

                {selectedCuentadanteData && (
                  <div className="asignacion-modal-info-box">
                    <h4 className="asignacion-modal-info-title">Información del Cuentadante</h4>
                    <p className="asignacion-modal-info-text">
                      <strong>Nombre:</strong> {selectedCuentadanteData.nombre}
                    </p>
                    <p className="asignacion-modal-info-text">
                      <strong>Documento:</strong> {selectedCuentadanteData.cedula}
                    </p>
                    <p className="asignacion-modal-info-text">
                      <strong>Área:</strong> {selectedCuentadanteData.area}
                    </p>
                    <p className="asignacion-modal-info-text">
                      <strong>Correo:</strong> {selectedCuentadanteData.correo}
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Selección de Bienes */}
            <div className="asignacion-modal-section">
              <h3 className="asignacion-modal-section-title">
                2. Seleccionar Bienes
              </h3>
              
              <div className="asignacion-modal-section-content">
                <div>
                  <label htmlFor="search" className="asignacion-modal-label">
                    Buscar bienes
                  </label>
                  <input
                    id="search"
                    type="text"
                    placeholder="🔍 Buscar por placa, modelo, marca, serial, costo o fecha..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="asignacion-modal-search"
                    autoComplete="off"
                  />
                </div>

                {errors.bienes && <p className="asignacion-modal-error-text">{errors.bienes}</p>}

                <div className="asignacion-modal-bienes-container">
                  {filteredBienes.length === 0 ? (
                    <div className="asignacion-modal-bienes-empty">
                      {bienesDisponibles.length === 0 
                        ? 'No hay bienes disponibles para asignar'
                        : 'No se encontraron bienes con ese criterio de búsqueda'
                      }
                    </div>
                  ) : (
                    <div className="asignacion-modal-bienes-list">
                      {filteredBienes.map(bien => (
                        <label
                          key={bien.id}
                          className="asignacion-modal-bien-item"
                        >
                          <input
                            type="checkbox"
                            checked={selectedBienes.includes(bien.id)}
                            onChange={() => handleBienToggle(bien.id)}
                            className="asignacion-modal-bien-checkbox"
                          />
                          <div className="asignacion-modal-bien-info">
                            <div className="asignacion-modal-bien-code">
                              {bien.codigo}
                            </div>
                            <div className="asignacion-modal-bien-description">
                              {bien.descripcion}
                            </div>
                            <div className="asignacion-modal-bien-details">
                              {bien.categoria} • ${bien.valor?.toLocaleString() || '0'}
                              {bien.modelo && ` • Modelo: ${bien.modelo}`}
                              {bien.serial && ` • Serial: ${bien.serial}`}
                            </div>
                            {bien.fechaIngreso && (
                              <div style={{ fontSize: '12px', color: '#9ca3af', marginTop: '4px' }}>
                                Compra: {new Date(bien.fechaIngreso).toLocaleDateString('es-CO')}
                              </div>
                            )}
                          </div>
                        </label>
                      ))}
                    </div>
                  )}
                </div>

                {selectedBienes.length > 0 && (
                  <div className="asignacion-modal-success-box">
                    <p className="asignacion-modal-success-text">
                      {selectedBienes.length} bien(es) seleccionado(s)
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Buttons */}
          <div className="asignacion-modal-footer">
            <button
              type="button"
              onClick={onClose}
              className="asignacion-modal-btn-cancel"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="asignacion-modal-btn-submit"
            >
              {isLoading ? 'Asignando...' : 'Realizar Asignación'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default AsignacionModal

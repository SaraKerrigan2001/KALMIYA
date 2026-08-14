import { useState } from 'react'
import { useData } from '../../contexts/DataContext'
import { Calendar, User, Package, FileText } from 'lucide-react'
import '../../assets/css/AsignacionesTable.css'

const AsignacionesTable = () => {
  const { movimientos } = useData()
  const [searchTerm, setSearchTerm] = useState('')

  // Filtrar solo movimientos de asignación
  const asignaciones = movimientos.filter(m => m.tipo === 'asignacion')

  // Filtrar por búsqueda
  const filteredAsignaciones = asignaciones.filter(asignacion =>
    asignacion.cuentadante?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    asignacion.descripcion?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    asignacion.bienesInfo?.some(info => info.toLowerCase().includes(searchTerm.toLowerCase()))
  )

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('es-CO', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="asignaciones-container">
      {/* Header con búsqueda */}
      <div className="asignaciones-header">
        <div className="asignaciones-header-content">
          <div>
            <h2 className="asignaciones-title">
              Historial de Asignaciones
            </h2>
            <p className="asignaciones-count">
              {filteredAsignaciones.length} asignación(es) registrada(s)
            </p>
          </div>
          <div className="asignaciones-search-wrapper">
            <input
              type="text"
              placeholder="Buscar asignaciones..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="asignaciones-search-input"
            />
          </div>
        </div>
      </div>

      {/* Tabla */}
      <div className="asignaciones-table-wrapper">
        {filteredAsignaciones.length === 0 ? (
          <div className="asignaciones-empty-state">
            <Package className="asignaciones-empty-icon" />
            <p className="asignaciones-empty-text">
              {asignaciones.length === 0 
                ? 'No hay asignaciones registradas'
                : 'No se encontraron asignaciones con ese criterio de búsqueda'
              }
            </p>
          </div>
        ) : (
          <div className="asignaciones-list">
            {filteredAsignaciones.map((asignacion) => (
              <div key={asignacion.id} className="asignacion-item">
                <div className="asignacion-content">
                  {/* Información principal */}
                  <div className="asignacion-info">
                    {/* Fecha */}
                    <div className="asignacion-date">
                      <Calendar className="asignacion-date-icon" />
                      {formatDate(asignacion.fecha)}
                    </div>

                    {/* Cuentadante */}
                    <div className="asignacion-section">
                      <User className="asignacion-icon asignacion-icon-blue" />
                      <div>
                        <p className="asignacion-name">
                          {asignacion.cuentadante}
                        </p>
                        {asignacion.cuentadanteInfo && (
                          <div className="asignacion-details">
                            <p>{asignacion.cuentadanteInfo.cargo} - {asignacion.cuentadanteInfo.area}</p>
                            <p>CC: {asignacion.cuentadanteInfo.cedula}</p>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Bienes asignados */}
                    <div className="asignacion-section">
                      <Package className="asignacion-icon asignacion-icon-green" />
                      <div className="asignacion-bienes-wrapper">
                        <p className="asignacion-bienes-title">
                          {asignacion.bienes.length} bien(es) asignado(s):
                        </p>
                        <div className="asignacion-bienes-list">
                          {asignacion.bienesInfo?.map((info, index) => (
                            <div key={index} className="asignacion-bien-item">
                              {info}
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>

                    {/* Descripción */}
                    <div className="asignacion-section">
                      <FileText className="asignacion-icon asignacion-icon-gray" />
                      <p className="asignacion-description">
                        {asignacion.descripcion}
                      </p>
                    </div>
                  </div>

                  {/* Badge de estado */}
                  <div className="asignacion-status-wrapper">
                    <span className="asignacion-status-badge">
                      Completada
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default AsignacionesTable

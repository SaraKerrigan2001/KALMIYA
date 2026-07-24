import { useState, useEffect } from 'react'
import { useNotifications } from '../../hooks/useNotifications'
import '../../assets/css/PersonasTable.css'

const SedesTable = ({ onEdit }) => {
  const notifications = useNotifications()
  const [sedes, setSedes] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadSedes()
  }, [])

  const loadSedes = async () => {
    try {
      setLoading(true)
      const response = await fetch('http://localhost:3001/api/sedes')
      const data = await response.json()
      setSedes(data)
    } catch (error) {
      console.error('Error al cargar sedes:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredSedes = sedes.filter(sede => {
    return sede.sede_nombre?.toLowerCase().includes(searchTerm.toLowerCase())
  })

  return (
    <div className="personas-table-container">
      {/* Filtros */}
      <div className="personas-filters">
        <div className="personas-filters-wrapper">
          <div className="personas-search-wrapper">
            <input
              type="text"
              placeholder="Buscar sede..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="personas-search-input"
            />
          </div>
        </div>
      </div>

      {/* Tabla */}
      <div className="personas-table-wrapper">
        <table className="personas-table">
          <thead className="personas-table-head">
            <tr>
              <th className="personas-table-th">ID</th>
              <th className="personas-table-th">Nombre de la Sede</th>
              <th className="personas-table-th">Acciones</th>
            </tr>
          </thead>
          <tbody className="personas-table-body">
            {loading ? (
              <tr>
                <td colSpan="3" className="personas-empty-state">
                  Cargando sedes...
                </td>
              </tr>
            ) : filteredSedes.length === 0 ? (
              <tr>
                <td colSpan="3" className="personas-empty-state">
                  No se encontraron sedes
                </td>
              </tr>
            ) : (
              filteredSedes.map((sede) => (
                <tr key={sede.sede_id} className="personas-table-row">
                  <td className="personas-table-td personas-table-td-cedula">
                    {sede.sede_id}
                  </td>
                  <td className="personas-table-td personas-table-td-nombre">
                    {sede.sede_nombre}
                  </td>
                  <td className="personas-table-td personas-table-td-actions">
                    <button
                      onClick={() => onEdit(sede)}
                      className="personas-btn-edit"
                    >
                      Editar
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Paginación */}
      <div className="personas-pagination">
        <div className="personas-pagination-content">
          <p className="personas-pagination-text">
            Mostrando {filteredSedes.length} de {sedes.length} sedes
          </p>
        </div>
      </div>
    </div>
  )
}

export default SedesTable

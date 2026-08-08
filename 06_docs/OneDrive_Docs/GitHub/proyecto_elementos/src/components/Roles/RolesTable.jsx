import { useState, useEffect } from 'react'
import { useNotifications } from '../../hooks/useNotifications'
import '../../assets/css/PersonasTable.css'

const RolesTable = ({ onEdit }) => {
  const notifications = useNotifications()
  const [roles, setRoles] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadRoles()
  }, [])

  const loadRoles = async () => {
    try {
      setLoading(true)
      const response = await fetch('http://localhost:3001/api/roles')
      const data = await response.json()
      setRoles(data)
    } catch (error) {
      console.error('Error al cargar roles:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredRoles = roles.filter(rol => {
    return rol.rol_nombre?.toLowerCase().includes(searchTerm.toLowerCase())
  })

  return (
    <div className="personas-table-container">
      {/* Filtros */}
      <div className="personas-filters">
        <div className="personas-filters-wrapper">
          <div className="personas-search-wrapper">
            <input
              type="text"
              placeholder="Buscar rol..."
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
              <th className="personas-table-th">Nombre del Rol</th>
              <th className="personas-table-th">Acciones</th>
            </tr>
          </thead>
          <tbody className="personas-table-body">
            {loading ? (
              <tr>
                <td colSpan="3" className="personas-empty-state">
                  Cargando roles...
                </td>
              </tr>
            ) : filteredRoles.length === 0 ? (
              <tr>
                <td colSpan="3" className="personas-empty-state">
                  No se encontraron roles
                </td>
              </tr>
            ) : (
              filteredRoles.map((rol) => (
                <tr key={rol.rol_id} className="personas-table-row">
                  <td className="personas-table-td personas-table-td-cedula">
                    {rol.rol_id}
                  </td>
                  <td className="personas-table-td personas-table-td-nombre">
                    {rol.rol_nombre}
                  </td>
                  <td className="personas-table-td personas-table-td-actions">
                    <button
                      onClick={() => onEdit(rol)}
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
            Mostrando {filteredRoles.length} de {roles.length} roles
          </p>
        </div>
      </div>
    </div>
  )
}

export default RolesTable

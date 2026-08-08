import { useState } from 'react'
import { useData } from '../../contexts/DataContext'
import { useTranslation } from '../../hooks/useTranslation'
import '../../assets/css/PersonasTable.css'

const PersonasTable = ({ onEdit }) => {
  const { cuentadantes } = useData()
  const { t } = useTranslation()
  const [searchTerm, setSearchTerm] = useState('')

  const filteredPersonas = cuentadantes.filter(persona => {
    return (
      persona.pers_nombres?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      persona.pers_apellidos?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      persona.pers_documento?.toString().includes(searchTerm) ||
      persona.pers_telefono?.toString().includes(searchTerm)
    )
  })

  return (
    <div className="personas-table-container">
      {/* Filtros */}
      <div className="personas-filters">
        <div className="personas-filters-wrapper">
          <div className="personas-search-wrapper">
            <input
              type="text"
              placeholder="Buscar persona..."
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
              <th className="personas-table-th">Documento</th>
              <th className="personas-table-th">Nombres</th>
              <th className="personas-table-th">Apellidos</th>
              <th className="personas-table-th">Teléfono</th>
              <th className="personas-table-th">Roles</th>
              <th className="personas-table-th">Acciones</th>
            </tr>
          </thead>
          <tbody className="personas-table-body">
            {filteredPersonas.length === 0 ? (
              <tr>
                <td colSpan="6" className="personas-empty-state">
                  No se encontraron personas
                </td>
              </tr>
            ) : (
              filteredPersonas.map((persona) => (
                <tr key={persona.id} className="personas-table-row">
                  <td className="personas-table-td personas-table-td-cedula">
                    {persona.pers_tipodoc} {persona.pers_documento}
                  </td>
                  <td className="personas-table-td personas-table-td-nombre">
                    {persona.pers_nombres}
                  </td>
                  <td className="personas-table-td personas-table-td-apellidos">
                    {persona.pers_apellidos}
                  </td>
                  <td className="personas-table-td personas-table-td-telefono">
                    {persona.pers_telefono}
                  </td>
                  <td className="personas-table-td personas-table-td-roles">
                    {persona.roles ? persona.roles.join(', ') : 'Sin rol'}
                  </td>
                  <td className="personas-table-td personas-table-td-actions">
                    <button
                      onClick={() => onEdit(persona)}
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
            Mostrando {filteredPersonas.length} de {cuentadantes.length} personas
          </p>
        </div>
      </div>
    </div>
  )
}

export default PersonasTable

import { useState } from 'react'
import { useData } from '../../contexts/DataContext'
import { useTranslation } from '../../hooks/useTranslation'
import '../css/personasTable.css'

const personasTable = ({ onEdit }) => {
  const { personas } = useData()
  const { t } = useTranslation()
  const [searchTerm, setSearchTerm] = useState('')

  const filteredpersonas = personas.filter(persona => {
    return (
      persona.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
      persona.cedula.includes(searchTerm) ||
      persona.cargo.toLowerCase().includes(searchTerm.toLowerCase()) ||
      persona.area.toLowerCase().includes(searchTerm.toLowerCase())
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
              placeholder={t('personas.buscar')}
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
              <th className="personas-table-th">{t('personas.cedula')}</th>
              <th className="personas-table-th">{t('personas.nombre')}</th>
              <th className="personas-table-th">{t('personas.cargo')}</th>
              <th className="personas-table-th">{t('personas.area')}</th>
              <th className="personas-table-th">{t('personas.contacto')}</th>
              <th className="personas-table-th">{t('personas.fechaHoraCreacion')}</th>
              <th className="personas-table-th">{t('personas.estado')}</th>
              <th className="personas-table-th">{t('personas.acciones')}</th>
            </tr>
          </thead>
          <tbody className="personas-table-body">
            {filteredpersonas.length === 0 ? (
              <tr>
                <td colSpan="8" className="personas-empty-state">
                  {t('personas.noEncontrados')}
                </td>
              </tr>
            ) : (
              filteredpersonas.map((persona) => (
                <tr key={persona.id} className="personas-table-row">
                  <td className="personas-table-td personas-table-td-cedula">
                    {persona.cedula}
                  </td>
                  <td className="personas-table-td personas-table-td-nombre">
                    {persona.nombre}
                  </td>
                  <td className="personas-table-td personas-table-td-cargo">
                    {persona.cargo}
                  </td>
                  <td className="personas-table-td personas-table-td-area">
                    {persona.area}
                  </td>
                  <td className="personas-table-td personas-table-td-contacto">
                    <div className="personas-contact-email">{persona.correo}</div>
                    <div className="personas-contact-phone">
                      {persona.telefono}
                    </div>
                  </td>
                  <td className="personas-table-td personas-table-td-fecha">
                    {persona.fechaCreacion ? (
                      <>
                        <div className="personas-fecha">
                          {new Date(persona.fechaCreacion).toLocaleDateString('es-CO')}
                        </div>
                        <div className="personas-hora">
                          {persona.horaCreacion || new Date(persona.fechaCreacion).toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' })}
                        </div>
                      </>
                    ) : (
                      <span className="personas-no-fecha">{t('personas.noRegistrada')}</span>
                    )}
                  </td>
                  <td className="personas-table-td">
                    <span className={`personas-badge ${
                      persona.activo
                        ? 'personas-badge-activo'
                        : 'personas-badge-inactivo'
                    }`}>
                      {persona.activo ? t('personas.activo') : t('personas.inactivo')}
                    </span>
                  </td>
                  <td className="personas-table-td personas-table-td-actions">
                    <button
                      onClick={() => onEdit(persona)}
                      className="personas-btn-edit"
                    >
                      {t('personas.editar')}
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
            {t('personas.mostrando')} {filteredpersonas.length} {t('personas.de')} {personas.length} {t('sidebar.personas').toLowerCase()}
          </p>
        </div>
      </div>
    </div>
  )
}

export default personasTable

import { useState } from 'react'
import { useData } from '../../contexts/DataContext'
import { useNotifications } from '../../hooks/useNotifications'
import { useTranslation } from '../../hooks/useTranslation'
import '../css/BienesTable.css'

const BienesTable = ({ onEdit }) => {
  const { bienes, desasignarBien } = useData()
  const notifications = useNotifications()
  const { t } = useTranslation()
  const [searchTerm, setSearchTerm] = useState('')
  const [filterEstado, setFilterEstado] = useState('todos')

  const filteredBienes = bienes.filter(bien => {
    const matchesSearch = 
      bien.codigo.toLowerCase().includes(searchTerm.toLowerCase()) ||
      bien.descripcion.toLowerCase().includes(searchTerm.toLowerCase()) ||
      bien.categoria.toLowerCase().includes(searchTerm.toLowerCase())
    
    const matchesEstado = filterEstado === 'todos' || bien.estado === filterEstado

    return matchesSearch && matchesEstado
  })

  const handleDesasignar = (bien) => {
    if (window.confirm(`${t('bienes.confirmarDesasignar')} ${bien.codigo}?`)) {
      desasignarBien(bien.id)
      notifications.success(t('notifications.bienDesasignado'))
    }
  }

  const getEstadoBadge = (estado) => {
    const badges = {
      disponible: {
        className: 'bienes-badge bienes-badge-disponible',
        label: t('bienes.disponible')
      },
      asignado: {
        className: 'bienes-badge bienes-badge-asignado',
        label: t('bienes.asignado')
      },
      mantenimiento: {
        className: 'bienes-badge bienes-badge-mantenimiento',
        label: t('bienes.mantenimiento')
      },
      baja: {
        className: 'bienes-badge bienes-badge-baja',
        label: t('bienes.baja')
      }
    }
    const badge = badges[estado] || badges.disponible
    return (
      <span className={badge.className}>
        {badge.label}
      </span>
    )
  }

  return (
    <div className="bienes-table-container">
      {/* Filtros */}
      <div className="bienes-filters">
        <div className="bienes-filters-wrapper">
          <div className="bienes-search-wrapper">
            <input
              type="text"
              placeholder={t('bienes.buscar')}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bienes-search-input"
            />
          </div>
          <div>
            <select
              value={filterEstado}
              onChange={(e) => setFilterEstado(e.target.value)}
              className="bienes-filter-select"
            >
              <option value="todos">{t('bienes.todosEstados')}</option>
              <option value="disponible">{t('bienes.disponible')}</option>
              <option value="asignado">{t('bienes.asignado')}</option>
              <option value="mantenimiento">{t('bienes.mantenimiento')}</option>
              <option value="baja">{t('bienes.baja')}</option>
            </select>
          </div>
        </div>
      </div>

      {/* Tabla */}
      <div className="bienes-table-wrapper">
        <table className="bienes-table">
          <thead className="bienes-table-head">
            <tr>
              <th className="bienes-table-th">{t('bienes.codigo')}</th>
              <th className="bienes-table-th">{t('bienes.descripcion')}</th>
              <th className="bienes-table-th">{t('bienes.categoria')}</th>
              <th className="bienes-table-th">{t('bienes.estado')}</th>
              <th className="bienes-table-th">{t('bienes.valor')}</th>
              <th className="bienes-table-th">{t('bienes.fechaHoraCreacion')}</th>
              <th className="bienes-table-th">{t('bienes.ubicacion')}</th>
              <th className="bienes-table-th">{t('bienes.acciones')}</th>
            </tr>
          </thead>
          <tbody className="bienes-table-body">
            {filteredBienes.length === 0 ? (
              <tr>
                <td colSpan="8" className="bienes-empty-state">
                  {t('bienes.noEncontrados')}
                </td>
              </tr>
            ) : (
              filteredBienes.map((bien) => (
                <tr key={bien.id} className="bienes-table-row">
                  <td className="bienes-table-td bienes-table-td-code">
                    {bien.codigo}
                  </td>
                  <td className="bienes-table-td bienes-table-td-description">
                    {bien.descripcion}
                  </td>
                  <td className="bienes-table-td bienes-table-td-category">
                    {bien.categoria}
                  </td>
                  <td className="bienes-table-td">
                    {getEstadoBadge(bien.estado)}
                  </td>
                  <td className="bienes-table-td bienes-table-td-value">
                    ${bien.valor.toLocaleString()}
                  </td>
                  <td className="bienes-table-td bienes-table-td-fecha">
                    {bien.fechaCreacion ? (
                      <>
                        <div className="bienes-fecha">
                          {new Date(bien.fechaCreacion).toLocaleDateString('es-CO')}
                        </div>
                        <div className="bienes-hora">
                          {bien.horaCreacion || new Date(bien.fechaCreacion).toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' })}
                        </div>
                      </>
                    ) : (
                      <span className="bienes-no-fecha">{t('bienes.noRegistrada')}</span>
                    )}
                  </td>
                  <td className="bienes-table-td bienes-table-td-location">
                    {bien.ubicacion}
                    {bien.cuentadante && (
                      <div className="bienes-location-assigned">
                        {t('bienes.asignadoA')}: {bien.cuentadante}
                      </div>
                    )}
                    {bien.fechaAsignacion && (
                      <div className="bienes-location-date">
                        {t('bienes.desde')}: {new Date(bien.fechaAsignacion).toLocaleDateString('es-CO')}
                      </div>
                    )}
                  </td>
                  <td className="bienes-table-td bienes-table-td-actions">
                    <div className="bienes-actions-wrapper">
                      <button
                        onClick={() => onEdit(bien)}
                        className="bienes-btn-edit"
                      >
                        {t('bienes.editar')}
                      </button>
                      {bien.estado === 'asignado' && (
                        <button
                          onClick={() => handleDesasignar(bien)}
                          className="bienes-btn-unassign"
                        >
                          {t('bienes.desasignar')}
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Paginación */}
      <div className="bienes-pagination">
        <div className="bienes-pagination-content">
          <p className="bienes-pagination-text">
            {t('bienes.mostrando')} {filteredBienes.length} {t('bienes.de')} {bienes.length} {t('sidebar.bienes').toLowerCase()}
          </p>
        </div>
      </div>
    </div>
  )
}

export default BienesTable

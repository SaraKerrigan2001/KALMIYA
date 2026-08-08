import '../assets/css/StatsCards.css'

const StatsCards = ({ stats }) => {
  const cards = [
    {
      title: 'Total Bienes',
      value: stats.totalBienes,
      icon: '💻',
      color: 'blue',
      description: 'Bienes registrados en el sistema'
    },
    {
      title: 'Entradas Hoy',
      value: stats.entradasHoy,
      icon: '📥',
      color: 'green',
      description: 'Nuevos ingresos del día'
    },
    {
      title: 'Salidas Hoy',
      value: stats.salidasHoy,
      icon: '📤',
      color: 'orange',
      description: 'Asignaciones realizadas hoy'
    },
    {
      title: 'Alertas',
      value: stats.alertas,
      icon: '⚠️',
      color: 'red',
      description: 'Notificaciones pendientes'
    }
  ]

  const getColorClasses = (color) => {
    const colors = {
      blue: {
        card: 'stats-card-blue',
        text: 'stats-card-text-blue',
        icon: 'stats-card-icon-blue'
      },
      green: {
        card: 'stats-card-green',
        text: 'stats-card-text-green',
        icon: 'stats-card-icon-green'
      },
      orange: {
        card: 'stats-card-orange',
        text: 'stats-card-text-orange',
        icon: 'stats-card-icon-orange'
      },
      red: {
        card: 'stats-card-red',
        text: 'stats-card-text-red',
        icon: 'stats-card-icon-red'
      }
    }
    return colors[color] || colors.blue
  }

  return (
    <div className="stats-cards-container">
      {cards.map((card, index) => {
        const colorClasses = getColorClasses(card.color)
        
        return (
          <div
            key={index}
            className={`stats-card ${colorClasses.card}`}
          >
            <div className="stats-card-content">
              <div className="stats-card-info">
                <p className="stats-card-title dashboard-text">
                  {card.title}
                </p>
                <p className={`stats-card-value dashboard-title ${colorClasses.text}`}>
                  {card.value.toLocaleString()}
                </p>
                <p className="stats-card-description dashboard-subtitle">
                  {card.description}
                </p>
              </div>
              <div className={`stats-card-icon-container ${colorClasses.icon}`}>
                <span className="stats-card-icon">{card.icon}</span>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}

export default StatsCards
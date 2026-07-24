import { useEffect, useState } from 'react'
import '../css/LoadingScreen.css'

const LoadingScreen = () => {
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState('Inicializando módulos del sistema...')

  const loadingSteps = [
    'Inicializando módulos del sistema...',
    'Cargando base de datos...',
    'Verificando permisos...',
    'Configurando interfaz...',
    'Finalizando carga...'
  ]

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress(prev => {
        const newProgress = prev + 2
        const stepIndex = Math.floor((newProgress / 100) * loadingSteps.length)
        if (stepIndex < loadingSteps.length) {
          setStatus(loadingSteps[stepIndex])
        }
        return newProgress > 100 ? 100 : newProgress
      })
    }, 60)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="loading-screen-container">
      
      {/* Partículas de fondo */}
      <div className="loading-particles">
        <div className="loading-particle-1"></div>
        <div className="loading-particle-2"></div>
        <div className="loading-particle-3"></div>
      </div>

      <div className="loading-content epic-loader">
        {/* Logo animado */}
        <div className="loading-logo-container">
          <img 
            src="/sena-logo.png.png" 
            alt="Logo SENA" 
            className="loading-logo epic-loader"
          />
        </div>
        
        {/* Título principal */}
        <h1 className="loading-title epic-title auth-font">
          SENA BIENES
        </h1>
        
        {/* Subtítulos */}
        <p className="loading-subtitle-1 auth-font">
          Gestión de Entradas y Salidas
        </p>
        
        <p className="loading-subtitle-2 auth-font">
          Sistema Integral de Control de Objetos Tecnológicos
        </p>
        
        <p className="loading-status">
          {status}
        </p>
        
        {/* Barra de progreso */}
        <div className="loading-progress-container">
          <div className="loading-progress-bg">
            <div 
              className="loading-progress-bar"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
        
        {/* Indicadores de carga */}
        <div className="loading-dots">
          <div className="loading-dot loading-dot-1"></div>
          <div className="loading-dot loading-dot-2"></div>
          <div className="loading-dot loading-dot-3"></div>
        </div>
        
        {/* Información del sistema */}
        <div className="loading-system-info">
          <div className="loading-system-status">
            <div className="loading-system-indicator"></div>
            <span>Sistema SENA | Versión 2025.1</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LoadingScreen

import { useState } from 'react'
import { useNotifications } from '../../hooks/useNotifications'
import { Mail, CheckCircle, AlertCircle } from 'lucide-react'
import '../../assets/css/RecuperarPasswordModal.css'

const RecuperarPasswordModal = ({ onClose }) => {
  const notifications = useNotifications()
  const [step, setStep] = useState(1) // 1: email, 2: código, 3: nueva contraseña, 4: éxito
  const [formData, setFormData] = useState({
    correo: '',
    codigo: '',
    nuevaPassword: '',
    confirmarPassword: ''
  })
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)
  const [codigoEnviado, setCodigoEnviado] = useState('')

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }))
    }
  }

  const generarCodigoAleatorio = () => {
    return Math.floor(100000 + Math.random() * 900000).toString()
  }

  const handleEnviarCodigo = async (e) => {
    e.preventDefault()
    
    const newErrors = {}
    if (!formData.correo.trim()) {
      newErrors.correo = 'El correo es requerido'
    } else if (!/\S+@\S+\.\S+/.test(formData.correo)) {
      newErrors.correo = 'El correo no es válido'
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    setIsLoading(true)

    // Simular envío de código
    setTimeout(() => {
      const codigo = generarCodigoAleatorio()
      setCodigoEnviado(codigo)
      console.log('Código de recuperación:', codigo) // En producción, esto se enviaría por email
      notifications.success(`Código enviado a ${formData.correo}`)
      setStep(2)
      setIsLoading(false)
    }, 1500)
  }

  const handleVerificarCodigo = async (e) => {
    e.preventDefault()
    
    const newErrors = {}
    if (!formData.codigo.trim()) {
      newErrors.codigo = 'El código es requerido'
    } else if (formData.codigo !== codigoEnviado) {
      newErrors.codigo = 'El código es incorrecto'
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    setIsLoading(true)

    // Simular verificación
    setTimeout(() => {
      notifications.success('Código verificado correctamente')
      setStep(3)
      setIsLoading(false)
    }, 1000)
  }

  const handleCambiarPassword = async (e) => {
    e.preventDefault()
    
    const newErrors = {}
    if (!formData.nuevaPassword.trim()) {
      newErrors.nuevaPassword = 'La contraseña es requerida'
    } else if (formData.nuevaPassword.length < 6) {
      newErrors.nuevaPassword = 'La contraseña debe tener al menos 6 caracteres'
    }

    if (!formData.confirmarPassword.trim()) {
      newErrors.confirmarPassword = 'Debe confirmar la contraseña'
    } else if (formData.nuevaPassword !== formData.confirmarPassword) {
      newErrors.confirmarPassword = 'Las contraseñas no coinciden'
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    setIsLoading(true)

    // Simular cambio de contraseña
    setTimeout(() => {
      notifications.success('Contraseña actualizada exitosamente')
      setStep(4)
      setIsLoading(false)
      
      // Cerrar modal después de 2 segundos
      setTimeout(() => {
        onClose()
      }, 2000)
    }, 1500)
  }

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <form onSubmit={handleEnviarCodigo} className="recuperar-password-form">
            <div className="recuperar-password-step-header">
              <div className="recuperar-password-icon-container recuperar-password-icon-blue">
                <Mail className="h-8 w-8 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="recuperar-password-step-title">
                Recuperar Contraseña
              </h3>
              <p className="recuperar-password-step-description">
                Ingresa tu correo electrónico y te enviaremos un código de verificación
              </p>
            </div>

            <div>
              <label htmlFor="correo" className="recuperar-password-field-label">
                Correo Electrónico
              </label>
              <input
                id="correo"
                name="correo"
                type="email"
                value={formData.correo}
                onChange={handleInputChange}
                className={`recuperar-password-input ${errors.correo ? 'recuperar-password-input-error' : ''}`}
                placeholder="correo@sena.edu.co"
                autoFocus
              />
              {errors.correo && <p className="recuperar-password-error-text">{errors.correo}</p>}
            </div>

            <div className="recuperar-password-buttons">
              <button
                type="button"
                onClick={onClose}
                className="recuperar-password-button recuperar-password-button-cancel"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="recuperar-password-button recuperar-password-button-submit"
              >
                {isLoading ? 'Enviando...' : 'Enviar Código'}
              </button>
            </div>
          </form>
        )

      case 2:
        return (
          <form onSubmit={handleVerificarCodigo} className="recuperar-password-form">
            <div className="recuperar-password-step-header">
              <div className="recuperar-password-icon-container recuperar-password-icon-green">
                <Mail className="h-8 w-8 text-green-600 dark:text-green-400" />
              </div>
              <h3 className="recuperar-password-step-title">
                Verificar Código
              </h3>
              <p className="recuperar-password-step-description">
                Hemos enviado un código de 6 dígitos a <strong>{formData.correo}</strong>
              </p>
              <div className="recuperar-password-demo-alert">
                <p className="recuperar-password-demo-text">
                  <strong>Modo Demo:</strong> El código es <strong>{codigoEnviado}</strong>
                </p>
              </div>
            </div>

            <div>
              <label htmlFor="codigo" className="recuperar-password-field-label">
                Código de Verificación
              </label>
              <input
                id="codigo"
                name="codigo"
                type="text"
                maxLength="6"
                value={formData.codigo}
                onChange={handleInputChange}
                className={`recuperar-password-input recuperar-password-input-code ${errors.codigo ? 'recuperar-password-input-error' : ''}`}
                placeholder="000000"
                autoFocus
              />
              {errors.codigo && <p className="recuperar-password-error-text">{errors.codigo}</p>}
            </div>

            <div className="recuperar-password-buttons">
              <button
                type="button"
                onClick={() => setStep(1)}
                className="recuperar-password-button recuperar-password-button-cancel"
              >
                Atrás
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="recuperar-password-button recuperar-password-button-submit"
              >
                {isLoading ? 'Verificando...' : 'Verificar'}
              </button>
            </div>
          </form>
        )

      case 3:
        return (
          <form onSubmit={handleCambiarPassword} className="recuperar-password-form">
            <div className="recuperar-password-step-header">
              <div className="recuperar-password-icon-container recuperar-password-icon-purple">
                <CheckCircle className="h-8 w-8 text-purple-600 dark:text-purple-400" />
              </div>
              <h3 className="recuperar-password-step-title">
                Nueva Contraseña
              </h3>
              <p className="recuperar-password-step-description">
                Ingresa tu nueva contraseña
              </p>
            </div>

            <div>
              <label htmlFor="nuevaPassword" className="recuperar-password-field-label">
                Nueva Contraseña
              </label>
              <input
                id="nuevaPassword"
                name="nuevaPassword"
                type="password"
                value={formData.nuevaPassword}
                onChange={handleInputChange}
                className={`recuperar-password-input ${errors.nuevaPassword ? 'recuperar-password-input-error' : ''}`}
                placeholder="••••••••"
                autoFocus
              />
              {errors.nuevaPassword && <p className="recuperar-password-error-text">{errors.nuevaPassword}</p>}
            </div>

            <div>
              <label htmlFor="confirmarPassword" className="recuperar-password-field-label">
                Confirmar Contraseña
              </label>
              <input
                id="confirmarPassword"
                name="confirmarPassword"
                type="password"
                value={formData.confirmarPassword}
                onChange={handleInputChange}
                className={`recuperar-password-input ${errors.confirmarPassword ? 'recuperar-password-input-error' : ''}`}
                placeholder="••••••••"
              />
              {errors.confirmarPassword && <p className="recuperar-password-error-text">{errors.confirmarPassword}</p>}
            </div>

            <div className="recuperar-password-buttons">
              <button
                type="button"
                onClick={onClose}
                className="recuperar-password-button recuperar-password-button-cancel"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="recuperar-password-button recuperar-password-button-submit"
              >
                {isLoading ? 'Actualizando...' : 'Cambiar Contraseña'}
              </button>
            </div>
          </form>
        )

      case 4:
        return (
          <div className="recuperar-password-success">
            <div className="recuperar-password-icon-container recuperar-password-icon-green">
              <CheckCircle className="h-8 w-8 text-green-600 dark:text-green-400" />
            </div>
            <h3 className="recuperar-password-step-title">
              ¡Contraseña Actualizada!
            </h3>
            <p className="recuperar-password-step-description">
              Tu contraseña ha sido cambiada exitosamente. Ya puedes iniciar sesión con tu nueva contraseña.
            </p>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="recuperar-password-overlay">
      <div className="recuperar-password-container">
        {/* Header */}
        {step !== 4 && (
          <div className="recuperar-password-header">
            <div className="recuperar-password-header-content">
              <div className="recuperar-password-step-indicator">
                Paso {step} de 3
              </div>
              <button
                onClick={onClose}
                className="recuperar-password-close"
              >
                <span className="recuperar-password-close-icon">×</span>
              </button>
            </div>
          </div>
        )}

        {/* Content */}
        <div className="recuperar-password-content">
          {renderStep()}
        </div>
      </div>
    </div>
  )
}

export default RecuperarPasswordModal

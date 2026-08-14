/**
 * ============================================
 * SELECTOR DE IDIOMA
 * ============================================
 * 
 * Componente que permite al usuario cambiar el idioma de la aplicación.
 * Muestra un botón con icono de globo y un menú desplegable con los
 * idiomas disponibles.
 * 
 * Idiomas soportados:
 * - 🇪🇸 Español (es)
 * - 🇺🇸 English (en)
 * - 🇧🇷 Português (pt)
 * 
 * Características:
 * - Menú desplegable con banderas
 * - Indicador visual del idioma activo
 * - Estilo consistente con el header
 * - Cierre automático al seleccionar
 * 
 * @module components/LanguageSelector
 */

import { useState } from 'react'
import { useLanguage } from '../contexts/LanguageContext'
import '../assets/css/LanguageSelector.css'

const LanguageSelector = () => {
  const { language, changeLanguage } = useLanguage()
  const [showMenu, setShowMenu] = useState(false)

  // Lista de idiomas disponibles
  const languages = [
    { code: 'es', name: 'Español', flag: '🇪🇸' },
    { code: 'en', name: 'English', flag: '🇺🇸' },
    { code: 'pt', name: 'Português', flag: '🇧🇷' }
  ]

  // Obtener el idioma actual
  const currentLanguage = languages.find(lang => lang.code === language)

  /**
   * Maneja el cambio de idioma
   * @param {string} code - Código del idioma seleccionado
   */
  const handleLanguageChange = (code) => {
    changeLanguage(code)
    setShowMenu(false)
  }

  return (
    <div className="language-selector">
      {/* Botón principal con icono de globo */}
      <button
        onClick={() => setShowMenu(!showMenu)}
        className="language-selector-btn"
        title="Cambiar idioma"
      >
        <span className="language-selector-icon">🌐</span>
      </button>

      {/* Menú desplegable de idiomas */}
      {showMenu && (
        <div className="language-selector-menu">
          {languages.map((lang) => (
            <button
              key={lang.code}
              onClick={() => handleLanguageChange(lang.code)}
              className={`language-selector-item ${language === lang.code ? 'active' : ''}`}
            >
              <span className="language-selector-item-flag">{lang.flag}</span>
              <span className="language-selector-item-name">{lang.name}</span>
              {/* Checkmark para el idioma activo */}
              {language === lang.code && (
                <span className="language-selector-check">✓</span>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

export default LanguageSelector

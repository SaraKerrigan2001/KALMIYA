/**
 * ============================================
 * CONTEXTO DE IDIOMA (i18n)
 * ============================================
 * 
 * Contexto global para manejar el idioma de la aplicación.
 * Proporciona funcionalidad de internacionalización (i18n).
 * 
 * Características:
 * - Persistencia en localStorage
 * - Cambio dinámico de idioma
 * - Idiomas soportados: es, en, pt
 * 
 * @module contexts/LanguageContext
 * 
 * @example
 * // En App.jsx
 * <LanguageProvider>
 *   <App />
 * </LanguageProvider>
 * 
 * // En componentes
 * const { language, changeLanguage } = useLanguage()
 * changeLanguage('en') // Cambiar a inglés
 */

import { createContext, useContext, useState, useEffect } from 'react'

// Crear el contexto
const LanguageContext = createContext()

/**
 * Hook para acceder al contexto de idioma
 * @returns {Object} Objeto con el idioma actual y función para cambiarlo
 * @throws {Error} Si se usa fuera del LanguageProvider
 */
export const useLanguage = () => {
  const context = useContext(LanguageContext)
  if (!context) {
    throw new Error('useLanguage debe ser usado dentro de LanguageProvider')
  }
  return context
}

/**
 * Proveedor del contexto de idioma
 * @param {Object} props - Props del componente
 * @param {React.ReactNode} props.children - Componentes hijos
 */
export const LanguageProvider = ({ children }) => {
  // Estado del idioma actual, inicializado desde localStorage o 'es' por defecto
  const [language, setLanguage] = useState(() => {
    return localStorage.getItem('language') || 'es'
  })

  // Guardar el idioma en localStorage cuando cambie
  useEffect(() => {
    localStorage.setItem('language', language)
  }, [language])

  /**
   * Función para cambiar el idioma
   * @param {string} newLanguage - Nuevo idioma ('es', 'en', 'pt')
   */
  const changeLanguage = (newLanguage) => {
    setLanguage(newLanguage)
  }

  // Valor del contexto
  const value = {
    language,        // Idioma actual
    changeLanguage   // Función para cambiar idioma
  }

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  )
}

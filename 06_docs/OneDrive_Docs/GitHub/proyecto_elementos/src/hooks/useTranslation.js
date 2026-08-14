/**
 * ============================================
 * HOOK DE TRADUCCIÓN (i18n)
 * ============================================
 * 
 * Hook personalizado para manejar las traducciones de la aplicación.
 * Proporciona acceso a las traducciones según el idioma seleccionado.
 * 
 * Idiomas soportados:
 * - es: Español
 * - en: English
 * - pt: Português
 * 
 * @module hooks/useTranslation
 * 
 * @example
 * const { t, language } = useTranslation()
 * 
 * // Usar traducciones
 * <h1>{t('sidebar.title')}</h1>
 * <p>{t('dashboard.bienvenido')}</p>
 * 
 * // Obtener idioma actual
 * console.log(language) // 'es', 'en', o 'pt'
 */

import { useLanguage } from '../contexts/LanguageContext'
import { es } from '../locales/es'
import { en } from '../locales/en'
import { pt } from '../locales/pt'

// Objeto con todas las traducciones disponibles
const translations = {
  es,
  en,
  pt
}

/**
 * Hook para acceder a las traducciones
 * @returns {Object} Objeto con función t() y el idioma actual
 */
export const useTranslation = () => {
  const { language } = useLanguage()

  /**
   * Función para obtener una traducción
   * @param {string} key - Clave de la traducción en formato 'seccion.clave'
   * @returns {string|Array} Traducción correspondiente o la clave si no existe
   * 
   * @example
   * t('sidebar.title') // 'SENA BIENES'
   * t('bienes.agregar') // 'Agregar Bien'
   */
  const t = (key) => {
    const keys = key.split('.')
    let value = translations[language]

    // Navegar por el objeto de traducciones
    for (const k of keys) {
      value = value?.[k]
    }

    // Retornar la traducción o la clave si no existe
    return value || key
  }

  return { t, language }
}

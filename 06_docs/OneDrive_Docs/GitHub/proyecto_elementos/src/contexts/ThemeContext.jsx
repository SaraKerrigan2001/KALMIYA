/**
 * ============================================
 * ThemeContext.jsx - Contexto de tema (claro/oscuro)
 * ============================================
 * 
 * Este contexto maneja el tema de la aplicación (modo claro/oscuro).
 * 
 * Características:
 * - Detecta preferencia del sistema operativo
 * - Guarda preferencia en localStorage
 * - Aplica clase 'dark' al HTML para CSS
 * - Proporciona función para cambiar tema
 * 
 * Uso:
 * ```javascript
 * const { isDark, toggleTheme } = useTheme()
 * ```
 */

import { createContext, useContext, useState, useEffect } from 'react'

// Crear el contexto
const ThemeContext = createContext()

/**
 * ============================================
 * useTheme - Hook para usar el contexto de tema
 * ============================================
 * 
 * @returns {Object} { isDark, toggleTheme }
 * @throws {Error} Si se usa fuera de ThemeProvider
 */
export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme debe ser usado dentro de ThemeProvider')
  }
  return context
}

/**
 * ============================================
 * ThemeProvider - Proveedor del contexto de tema
 * ============================================
 * 
 * Envuelve la aplicación para proporcionar acceso al tema
 * 
 * @param {Object} props
 * @param {ReactNode} props.children - Componentes hijos
 */
export const ThemeProvider = ({ children }) => {
  // Estado del tema (false = claro, true = oscuro)
  const [isDark, setIsDark] = useState(false)

  /**
   * ============================================
   * EFECTO: Cargar tema al iniciar
   * ============================================
   * 
   * 1. Verifica si hay tema guardado en localStorage
   * 2. Si no hay, detecta preferencia del sistema
   * 3. Aplica el tema correspondiente
   */
  useEffect(() => {
    // Verificar preferencia guardada en localStorage
    const savedTheme = localStorage.getItem('theme')
    
    // Detectar preferencia del sistema operativo
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

    // Aplicar tema oscuro si está guardado o si el sistema lo prefiere
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
      setIsDark(true)
      document.documentElement.classList.add('dark') // Agregar clase al HTML
    }
  }, [])

  /**
   * ============================================
   * toggleTheme - Cambiar entre tema claro y oscuro
   * ============================================
   * 
   * Acciones:
   * 1. Cambia el estado isDark
   * 2. Agrega/quita clase 'dark' del HTML
   * 3. Guarda preferencia en localStorage
   */
  const toggleTheme = () => {
    setIsDark(prev => {
      const newTheme = !prev
      
      if (newTheme) {
        // Activar modo oscuro
        document.documentElement.classList.add('dark')
        localStorage.setItem('theme', 'dark')
      } else {
        // Activar modo claro
        document.documentElement.classList.remove('dark')
        localStorage.setItem('theme', 'light')
      }
      
      return newTheme
    })
  }

  // Valor que se proporciona a los componentes
  const value = {
    isDark,      // Estado actual del tema (boolean)
    toggleTheme  // Función para cambiar tema
  }

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  )
}

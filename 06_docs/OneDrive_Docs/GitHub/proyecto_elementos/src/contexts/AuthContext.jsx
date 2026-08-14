/**
 * ============================================
 * AuthContext.jsx - Contexto de autenticación
 * ============================================
 * 
 * Este contexto maneja la autenticación y sesión del usuario.
 * 
 * Características:
 * - Login y registro de usuarios
 * - Gestión del estado de autenticación
 * - Información del usuario actual
 * - Actualización de perfil
 * - Cierre de sesión
 * 
 * Nota: Actualmente usa datos simulados (mock).
 * En producción, conectar con API real.
 * 
 * Uso:
 * ```javascript
 * const { user, isAuthenticated, login, logout } = useAuth()
 * ```
 */

import { createContext, useContext, useState } from 'react'

// Crear el contexto
const AuthContext = createContext()

/**
 * ============================================
 * useAuth - Hook para usar el contexto de autenticación
 * ============================================
 * 
 * @returns {Object} { user, isAuthenticated, login, register, logout, updateProfile }
 * @throws {Error} Si se usa fuera de AuthProvider
 */
export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de AuthProvider')
  }
  return context
}

/**
 * ============================================
 * AuthProvider - Proveedor del contexto de autenticación
 * ============================================
 * 
 * Envuelve la aplicación para proporcionar acceso a la autenticación
 * 
 * @param {Object} props
 * @param {ReactNode} props.children - Componentes hijos
 */
export const AuthProvider = ({ children }) => {
  // ============================================
  // ESTADOS
  // ============================================
  
  // Información del usuario actual (null si no está autenticado)
  const [user, setUser] = useState(null)
  
  // Estado de autenticación (true si hay sesión activa)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  /**
   * ============================================
   * login - Iniciar sesión
   * ============================================
   * 
   * Simula el proceso de autenticación con un servidor.
   * En producción, reemplazar con llamada a API real.
   * 
   * @param {Object} credentials - Credenciales del usuario
   * @param {string} credentials.correo - Email del usuario
   * @param {string} credentials.password - Contraseña
   * @param {string} [credentials.nombre] - Nombre (opcional)
   * @param {string} [credentials.area] - Área (opcional)
   * @param {string} [credentials.rol] - Rol (opcional)
   * 
   * @returns {Promise<Object>} { success: boolean, user: Object }
   */
  const login = async (credentials) => {
    // Simular llamada a API (1.5 segundos)
    return new Promise((resolve) => {
      setTimeout(() => {
        // Crear usuario mock
        const mockUser = {
          id: 1,
          nombre: credentials.nombre || 'Admin SENA',
          correo: credentials.correo,
          area: credentials.area || 'Administración',
          rol: credentials.rol || 'Administrador'
        }
        
        // Actualizar estado
        setUser(mockUser)
        setIsAuthenticated(true)
        
        // Resolver promesa
        resolve({ success: true, user: mockUser })
      }, 1500)
    })
  }

  /**
   * ============================================
   * register - Registrar nuevo usuario
   * ============================================
   * 
   * Simula el registro de un nuevo usuario.
   * En producción, reemplazar con llamada a API real.
   * 
   * @param {Object} userData - Datos del nuevo usuario
   * @param {string} userData.nombre - Nombre completo
   * @param {string} userData.correo - Email
   * @param {string} userData.password - Contraseña
   * @param {string} userData.area - Área de trabajo
   * @param {string} userData.rol - Rol en el sistema
   * 
   * @returns {Promise<Object>} { success: boolean, user: Object }
   */
  const register = async (userData) => {
    // Simular llamada a API (2 segundos)
    return new Promise((resolve) => {
      setTimeout(() => {
        // Crear nuevo usuario con ID único
        const newUser = {
          id: Date.now(), // Usar timestamp como ID único
          ...userData
        }
        
        // Actualizar estado (auto-login después del registro)
        setUser(newUser)
        setIsAuthenticated(true)
        
        // Resolver promesa
        resolve({ success: true, user: newUser })
      }, 2000)
    })
  }

  /**
   * ============================================
   * logout - Cerrar sesión
   * ============================================
   * 
   * Limpia el estado de autenticación y usuario.
   * En producción, también invalidar token en el servidor.
   */
  const logout = () => {
    setUser(null)
    setIsAuthenticated(false)
    // TODO: En producción, invalidar token en el servidor
  }

  /**
   * ============================================
   * updateProfile - Actualizar perfil del usuario
   * ============================================
   * 
   * Actualiza la información del usuario actual.
   * En producción, reemplazar con llamada a API real.
   * 
   * @param {Object} profileData - Datos a actualizar
   * @returns {Promise<Object>} { success: boolean, user: Object }
   */
  const updateProfile = async (profileData) => {
    // Simular llamada a API (1 segundo)
    return new Promise((resolve) => {
      setTimeout(() => {
        // Combinar datos existentes con nuevos datos
        const updatedUser = {
          ...user,
          ...profileData
        }
        
        // Actualizar estado
        setUser(updatedUser)
        
        // Resolver promesa
        resolve({ success: true, user: updatedUser })
      }, 1000)
    })
  }

  // ============================================
  // VALOR DEL CONTEXTO
  // ============================================
  const value = {
    user,              // Usuario actual (Object | null)
    isAuthenticated,   // Estado de autenticación (boolean)
    login,             // Función para iniciar sesión
    register,          // Función para registrarse
    logout,            // Función para cerrar sesión
    updateProfile      // Función para actualizar perfil
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

import { useState, useEffect } from 'react'
import { ThemeProvider } from './contexts/ThemeContext'
import { AuthProvider } from './contexts/AuthContext'
import { DataProvider } from './contexts/DataContext'
import { NotificationProvider } from './contexts/NotificationContext'
import { LanguageProvider } from './contexts/LanguageContext'
import LoadingScreen from './components/LoadingScreen'
import AuthScreen from './components/Auth/AuthScreen'
import Dashboard from './components/Dashboard/Dashboard'
import NotificationContainer from './components/Notification/NotificationContainer'

function App() {
  const [isLoading, setIsLoading] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  useEffect(() => {
    // Simular carga inicial
    const timer = setTimeout(() => {
      setIsLoading(false)
    }, 3000)

    return () => clearTimeout(timer)
  }, [])

  const handleLogin = () => {
    setIsAuthenticated(true)
  }

  const handleLogout = () => {
    setIsAuthenticated(false)
  }

  if (isLoading) {
    return <LoadingScreen />
  }

  return (
    <LanguageProvider>
      <ThemeProvider>
        <AuthProvider>
          <DataProvider>
            <NotificationProvider>
              <div className="min-h-screen">
                {!isAuthenticated ? (
                  <AuthScreen onLogin={handleLogin} />
                ) : (
                  <Dashboard onLogout={handleLogout} />
                )}
                <NotificationContainer />
              </div>
            </NotificationProvider>
          </DataProvider>
        </AuthProvider>
      </ThemeProvider>
    </LanguageProvider>
  )
}

export default App
/**
 * EJEMPLO: Componente StatsCards
 * 
 * Este archivo demuestra cómo usar el componente StatsCards del sistema.
 * StatsCards muestra tarjetas de estadísticas con información resumida
 * del sistema de gestión de bienes.
 * 
 * CARACTERÍSTICAS:
 * - Grid responsive de tarjetas de estadísticas
 * - Iconos representativos para cada métrica
 * - Colores diferenciados por tipo de estadística
 * - Animaciones de entrada (fade-in)
 * - Diseño adaptable: 1 columna en móvil, 2-4 en desktop
 * - Números grandes y etiquetas descriptivas
 * 
 * CONTEXTOS REQUERIDOS:
 * - ThemeProvider: Maneja el tema claro/oscuro
 * 
 * PROPS DEL COMPONENTE:
 * - stats: Objeto con las estadísticas a mostrar
 * 
 * ESTRUCTURA DEL OBJETO STATS:
 * {
 *   totalBienes: number,    // Total de bienes en el sistema
 *   entradasHoy: number,    // Bienes ingresados hoy
 *   salidasHoy: number,     // Bienes asignados hoy
 *   alertas: number         // Alertas o notificaciones pendientes
 * }
 * 
 * NOTA: Los valores pueden ser personalizados según las necesidades
 */

// Importación del contexto de tema
import { ThemeProvider } from '../src/contexts/ThemeContext'

// Importación del componente de tarjetas de estadísticas
import StatsCards from '../src/components/StatsCards'

// Estilos globales de la aplicación
import './index.css'

function App() {
  // Objeto con estadísticas de ejemplo
  // En una aplicación real, estos datos vendrían de una API o contexto
  const stats = {
    totalBienes: 156,    // Total de bienes registrados
    entradasHoy: 12,     // Bienes ingresados hoy
    salidasHoy: 8,       // Bienes asignados hoy
    alertas: 5           // Alertas pendientes
  }

  return (
    // Envolver con el contexto de tema
    <ThemeProvider>
      {/* Contenedor principal */}
      <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-6">
        {/* Título de la sección */}
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          Estadísticas del Sistema
        </h1>
        {/* Componente de tarjetas con las estadísticas */}
        <StatsCards stats={stats} />
      </div>
    </ThemeProvider>
  )
}

export default App

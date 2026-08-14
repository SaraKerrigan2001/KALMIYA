/** @type {import('tailwindcss').Config} */
export default {
  // Define los archivos donde Tailwind buscará las clases CSS utilizadas
  // Esto permite la eliminación de CSS no utilizado en producción (tree-shaking)
  content: [
    "./index.html",                    // Archivo HTML principal
    "./src/**/*.{js,ts,jsx,tsx}",     // Todos los archivos JS, TS, JSX y TSX dentro de src
  ],
  
  // Configuración del modo oscuro usando la estrategia 'class'
  // Requiere agregar la clase 'dark' al elemento HTML para activar el modo oscuro
  darkMode: 'class',
  
  // Configuración del tema de Tailwind
  theme: {
    // Extiende el tema por defecto sin sobrescribirlo
    extend: {
      // Paleta de colores personalizada
      colors: {
        primary: {
          50: '#f0fdf4',   // Verde muy claro (para fondos)
          500: '#059669',  // Verde medio (color principal)
          600: '#047857',  // Verde oscuro (hover states)
          700: '#065f46',  // Verde más oscuro (estados activos)
        }
      },
      
      // Animaciones personalizadas que pueden usarse con la clase animate-*
      animation: {
        'fade-in-up': 'fadeInUp 0.6s ease-out',           // Aparece desde abajo con fade
        'slide-in-left': 'slideInLeft 0.5s ease-out',     // Desliza desde la izquierda
        'slide-in-right': 'slideInRight 0.5s ease-out',   // Desliza desde la derecha
        'pulse-custom': 'pulse 2s infinite',              // Pulso continuo personalizado
        'bounce-custom': 'bounce 2s infinite',            // Rebote continuo personalizado
        'spin-slow': 'spin 3s linear infinite',           // Rotación lenta continua
        'glow': 'glow 2s ease-in-out infinite',           // Efecto de brillo pulsante
      },
      
      // Definición de los keyframes para las animaciones personalizadas
      keyframes: {
        // Animación de deslizamiento desde la izquierda
        slideInLeft: {
          from: { transform: 'translateX(-100%)', opacity: '0' },
          to: { transform: 'translateX(0)', opacity: '1' }
        },
        // Animación de deslizamiento desde la derecha
        slideInRight: {
          from: { transform: 'translateX(100%)', opacity: '0' },
          to: { transform: 'translateX(0)', opacity: '1' }
        },
        // Animación de aparición desde abajo con fade
        fadeInUp: {
          from: { transform: 'translateY(30px)', opacity: '0' },
          to: { transform: 'translateY(0)', opacity: '1' }
        },
        // Animación de brillo pulsante con sombras
        glow: {
          '0%, 100%': { boxShadow: '0 0 5px rgba(57, 169, 0, 0.3)' },
          '50%': { boxShadow: '0 0 20px rgba(57, 169, 0, 0.6), 0 0 30px rgba(57, 169, 0, 0.4)' }
        }
      }
    },
  },
  
  // Array de plugins de Tailwind (actualmente vacío)
  // Aquí se pueden agregar plugins como @tailwindcss/forms, @tailwindcss/typography, etc.
  plugins: [],
}
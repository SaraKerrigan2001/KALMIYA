// Importa la función defineConfig de Vite para configuración con autocompletado y validación de tipos
import { defineConfig } from 'vite'
// Importa el plugin oficial de React para Vite que habilita Fast Refresh y JSX
import react from '@vitejs/plugin-react'

// Exporta la configuración de Vite usando defineConfig
export default defineConfig({
  // Array de plugins que extienden la funcionalidad de Vite
  plugins: [react()], // Plugin de React para soporte de JSX y Fast Refresh durante el desarrollo
  
  // Configuración del servidor de desarrollo
  server: {
    port: 3000,        // Puerto en el que se ejecutará el servidor de desarrollo (por defecto es 5173)
    open: true         // Abre automáticamente el navegador al iniciar el servidor
  }
})
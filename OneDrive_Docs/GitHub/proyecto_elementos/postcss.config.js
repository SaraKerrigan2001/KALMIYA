// Configuración de PostCSS - Herramienta para transformar CSS con plugins de JavaScript
export default {
  // Lista de plugins de PostCSS que se ejecutarán en orden
  plugins: {
    // Plugin de Tailwind CSS: procesa las directivas de Tailwind (@tailwind, @apply, etc.)
    // y genera las clases CSS basadas en la configuración de tailwind.config.js
    tailwindcss: {},
    
    // Autoprefixer: agrega automáticamente prefijos de navegador (-webkit-, -moz-, -ms-)
    // a las propiedades CSS para garantizar compatibilidad cross-browser
    // Usa la base de datos de Can I Use para determinar qué prefijos son necesarios
    autoprefixer: {},
  },
}
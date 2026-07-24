#!/usr/bin/env node

/**
 * Script para cambiar rápidamente entre ejemplos de componentes
 * Uso: node examples/cambiar-ejemplo.js [nombre-componente]
 * Ejemplo: node examples/cambiar-ejemplo.js BienesTable
 */

const fs = require('fs');
const path = require('path');

const ejemplos = {
  'AuthScreen': 'App-AuthScreen.jsx',
  'LoadingScreen': 'App-LoadingScreen.jsx',
  'Header': 'App-Header.jsx',
  'Sidebar': 'App-Sidebar.jsx',
  'Dashboard': 'App-Dashboard.jsx',
  'BienesTable': 'App-BienesTable.jsx',
  'BienModal': 'App-BienModal.jsx',
  'CuentadantesTable': 'App-CuentadantesTable.jsx',
  'CuentadanteModal': 'App-CuentadanteModal.jsx',
  'AsignacionModal': 'App-AsignacionModal.jsx',
  'StatsCards': 'App-StatsCards.jsx',
  'NotificationContainer': 'App-NotificationContainer.jsx',
  'NotificationCenter': 'App-NotificationCenter.jsx',
  'PerfilModal': 'App-PerfilModal.jsx',
  'ConfiguracionModal': 'App-ConfiguracionModal.jsx'
};

function mostrarAyuda() {
  console.log('\n📚 Cambiar Ejemplo de Componente\n');
  console.log('Uso: node examples/cambiar-ejemplo.js [componente]\n');
  console.log('Componentes disponibles:');
  Object.keys(ejemplos).forEach((nombre, index) => {
    console.log(`  ${index + 1}. ${nombre}`);
  });
  console.log('\nEjemplo: node examples/cambiar-ejemplo.js BienesTable\n');
}

function cambiarEjemplo(nombreComponente) {
  const archivoEjemplo = ejemplos[nombreComponente];
  
  if (!archivoEjemplo) {
    console.error(`❌ Error: Componente "${nombreComponente}" no encontrado`);
    mostrarAyuda();
    process.exit(1);
  }

  const rutaEjemplo = path.join(__dirname, archivoEjemplo);
  const rutaApp = path.join(__dirname, '..', 'src', 'App.jsx');

  try {
    // Leer el archivo de ejemplo
    const contenidoEjemplo = fs.readFileSync(rutaEjemplo, 'utf8');
    
    // Hacer backup del App.jsx actual
    const backupPath = path.join(__dirname, '..', 'src', 'App.jsx.backup');
    if (fs.existsSync(rutaApp)) {
      fs.copyFileSync(rutaApp, backupPath);
      console.log('💾 Backup creado: src/App.jsx.backup');
    }
    
    // Escribir el nuevo contenido
    fs.writeFileSync(rutaApp, contenidoEjemplo, 'utf8');
    
    console.log(`✅ Ejemplo cambiado exitosamente a: ${nombreComponente}`);
    console.log(`📄 Archivo: ${archivoEjemplo}`);
    console.log('\n🔄 El navegador se recargará automáticamente');
    console.log('💡 Para restaurar: node examples/cambiar-ejemplo.js restaurar\n');
  } catch (error) {
    console.error('❌ Error al cambiar ejemplo:', error.message);
    process.exit(1);
  }
}

function restaurarBackup() {
  const backupPath = path.join(__dirname, '..', 'src', 'App.jsx.backup');
  const rutaApp = path.join(__dirname, '..', 'src', 'App.jsx');

  if (!fs.existsSync(backupPath)) {
    console.error('❌ No se encontró backup para restaurar');
    process.exit(1);
  }

  try {
    fs.copyFileSync(backupPath, rutaApp);
    console.log('✅ App.jsx restaurado desde backup');
    console.log('🔄 El navegador se recargará automáticamente\n');
  } catch (error) {
    console.error('❌ Error al restaurar backup:', error.message);
    process.exit(1);
  }
}

// Procesar argumentos
const args = process.argv.slice(2);

if (args.length === 0) {
  mostrarAyuda();
  process.exit(0);
}

const comando = args[0];

if (comando === 'restaurar' || comando === 'restore') {
  restaurarBackup();
} else if (comando === 'ayuda' || comando === 'help' || comando === '-h' || comando === '--help') {
  mostrarAyuda();
} else {
  cambiarEjemplo(comando);
}

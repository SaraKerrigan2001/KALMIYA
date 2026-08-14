/**
 * ============================================
 * ENGLISH TRANSLATIONS
 * ============================================
 * 
 * This file contains all application translations
 * in English (en).
 * 
 * Structure:
 * - sidebar: Side menu texts
 * - header: Top bar texts
 * - dashboard: Main panel texts
 * - bienes: Assets management texts
 * - cuentadantes: Accountants management texts
 * - asignaciones: Assets assignment texts
 * - days: Day names
 * - months: Month names
 * - notifications: Notification messages
 * - auth: Authentication texts
 * 
 * @module locales/en
 */

export const en = {
  // ============================================
  // SIDEBAR - Side navigation menu
  // ============================================
  sidebar: {
    title: 'SENA ASSETS',
    subtitle: 'Management System',
    dashboard: 'Dashboard',
    dashboardDesc: 'System overview',
    bienes: 'Assets',
    bienesDesc: 'Technology assets management',
    cuentadantes: 'Accountants',
    cuentadantesDesc: 'Responsible management',
    asignaciones: 'Assignments',
    asignacionesDesc: 'Assign assets to accountants',
    perfilUsuario: 'User Profile',
    configuracion: 'Settings',
    cerrarSesion: 'Sign Out',
    sistemaActivo: 'System Active',
    version: 'Version 2025.1'
  },

  // Header
  header: {
    dashboardPrincipal: 'Main Dashboard',
    sistemaActivo: 'System Active',
    ultimaSync: 'Last sync',
    hace: 'ago',
    min: 'min',
    seg: 'sec',
    cambiarTemaClaro: 'Switch to light theme',
    cambiarTemaOscuro: 'Switch to dark theme'
  },

  // Dashboard
  dashboard: {
    bienvenido: 'Welcome',
    ultimosMovimientos: 'Recent Movements',
    alertasSistema: 'System Alerts',
    entrada: 'Entry',
    asignacion: 'Assignment',
    hoy: 'Today',
    ayer: 'Yesterday',
    bienesMantenimiento: 'assets due for maintenance',
    bienesSinAsignar: 'assets unassigned for more than 30 days'
  },

  // Bienes
  bienes: {
    titulo: 'Assets Management',
    agregar: 'Add Asset',
    buscar: 'Search by code, description or category...',
    todosEstados: 'All statuses',
    disponible: 'Available',
    asignado: 'Assigned',
    mantenimiento: 'Maintenance',
    baja: 'Decommissioned',
    modelo: 'Model',
    descripcion: 'Description',
    serial: 'Serial',
    estado: 'Status',
    costo: 'Cost',
    fechaCompra: 'Purchase Date',
    vidaUtil: 'Useful Life',
    sede: 'Location',
    acciones: 'Actions',
    editar: 'Edit',
    desasignar: 'Unassign',
    asignadoA: 'Assigned to',
    desde: 'Since',
    noEncontrados: 'No assets found',
    mostrando: 'Showing',
    de: 'of',
    noRegistrada: 'Not registered',
    confirmarDesasignar: 'Are you sure you want to unassign the asset'
  },

  // Cuentadantes
  cuentadantes: {
    titulo: 'Accountants Management',
    agregar: 'Add Accountant',
    buscar: 'Search by name, ID, position or area...',
    cedula: 'ID',
    nombre: 'Name',
    cargo: 'Position',
    area: 'Area',
    contacto: 'Contact',
    fechaHoraCreacion: 'Creation Date/Time',
    estado: 'Status',
    acciones: 'Actions',
    activo: 'Active',
    inactivo: 'Inactive',
    editar: 'Edit',
    noEncontrados: 'No accountants found',
    mostrando: 'Showing',
    de: 'of',
    noRegistrada: 'Not registered'
  },

  // Asignaciones
  asignaciones: {
    titulo: 'Assets Assignment',
    nueva: 'New Assignment',
    fecha: 'Date',
    cuentadante: 'Accountant',
    bienes: 'Assets',
    descripcion: 'Description',
    noEncontradas: 'No assignments found',
    mostrando: 'Showing',
    de: 'of'
  },

  // Días de la semana
  days: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],

  // Meses
  months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],

  // Notificaciones
  notifications: {
    loginExitoso: 'Login successful',
    logoutExitoso: 'Session closed successfully',
    bienAgregado: 'Asset added successfully',
    bienActualizado: 'Asset updated successfully',
    bienDesasignado: 'Asset unassigned successfully',
    cuentadanteAgregado: 'Accountant added successfully',
    cuentadanteActualizado: 'Accountant updated successfully',
    asignacionExitosa: 'Assignment completed successfully',
    error: 'An error has occurred',
    success: 'Operation successful'
  },

  // Auth
  auth: {
    iniciarSesion: 'Sign In',
    correo: 'Email',
    contrasena: 'Password',
    olvidoContrasena: 'Forgot your password?',
    ingresar: 'Sign In',
    recuperarContrasena: 'Recover Password',
    enviarEnlace: 'Send Link',
    volver: 'Back to sign in'
  }
}

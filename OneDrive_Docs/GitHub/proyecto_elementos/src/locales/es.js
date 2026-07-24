/**
 * ============================================
 * TRADUCCIONES EN ESPAÑOL
 * ============================================
 * 
 * Este archivo contiene todas las traducciones de la aplicación
 * en idioma español (es).
 * 
 * Estructura:
 * - sidebar: Textos del menú lateral
 * - header: Textos de la barra superior
 * - dashboard: Textos del panel principal
 * - bienes: Textos de gestión de bienes
 * - cuentadantes: Textos de gestión de cuentadantes
 * - asignaciones: Textos de asignación de bienes
 * - days: Nombres de los días de la semana
 * - months: Nombres de los meses
 * - notifications: Mensajes de notificación
 * - auth: Textos de autenticación
 * 
 * @module locales/es
 */

export const es = {
  // ============================================
  // SIDEBAR - Menú lateral de navegación
  // ============================================
  sidebar: {
    title: 'SENA BIENES',
    subtitle: 'Sistema de Gestión',
    dashboard: 'Dashboard',
    dashboardDesc: 'Vista general del sistema',
    bienes: 'Bienes',
    bienesDesc: 'Gestión de bienes tecnológicos',
    cuentadantes: 'Cuentadantes',
    cuentadantesDesc: 'Gestión de responsables',
    asignaciones: 'Asignaciones',
    asignacionesDesc: 'Asignar bienes a cuentadantes',
    perfilUsuario: 'Perfil Usuario',
    configuracion: 'Configuración',
    cerrarSesion: 'Cerrar Sesión',
    sistemaActivo: 'Sistema Activo',
    version: 'Versión 2025.1'
  },

  // ============================================
  // HEADER - Barra superior
  // ============================================
  header: {
    dashboardPrincipal: 'Dashboard Principal',
    sistemaActivo: 'Sistema Activo',
    ultimaSync: 'Última sync',
    hace: 'hace',
    min: 'min',
    seg: 'seg',
    cambiarTemaClaro: 'Cambiar a tema claro',
    cambiarTemaOscuro: 'Cambiar a tema oscuro'
  },

  // ============================================
  // DASHBOARD - Panel principal
  // ============================================
  dashboard: {
    bienvenido: 'Bienvenido',
    ultimosMovimientos: 'Últimos Movimientos',
    alertasSistema: 'Alertas del Sistema',
    entrada: 'Entrada',
    asignacion: 'Asignación',
    hoy: 'Hoy',
    ayer: 'Ayer',
    bienesMantenimiento: 'bienes próximos a mantenimiento',
    bienesSinAsignar: 'bienes sin asignar por más de 30 días'
  },

  // ============================================
  // BIENES - Gestión de bienes tecnológicos
  // ============================================
  bienes: {
    titulo: 'Gestión de Bienes',
    agregar: 'Agregar Bien',
    buscar: 'Buscar por código, descripción o categoría...',
    todosEstados: 'Todos los estados',
    disponible: 'Disponible',
    asignado: 'Asignado',
    mantenimiento: 'Mantenimiento',
    baja: 'Dado de Baja',
    modelo: 'Modelo',
    descripcion: 'Descripción',
    serial: 'Serial',
    estado: 'Estado',
    costo: 'Costo',
    fechaCompra: 'Fecha de Compra',
    vidaUtil: 'Vida Útil',
    sede: 'Sede',
    acciones: 'Acciones',
    editar: 'Editar',
    desasignar: 'Desasignar',
    asignadoA: 'Asignado a',
    desde: 'Desde',
    noEncontrados: 'No se encontraron bienes',
    mostrando: 'Mostrando',
    de: 'de',
    noRegistrada: 'No registrada',
    confirmarDesasignar: '¿Está seguro de desasignar el bien'
  },

  // ============================================
  // CUENTADANTES - Gestión de responsables
  // ============================================
  cuentadantes: {
    titulo: 'Gestión de Cuentadantes',
    agregar: 'Agregar Cuentadante',
    buscar: 'Buscar por nombre, cédula, cargo o área...',
    cedula: 'Cédula',
    nombre: 'Nombre',
    cargo: 'Cargo',
    area: 'Área',
    contacto: 'Contacto',
    fechaHoraCreacion: 'Fecha/Hora Creación',
    estado: 'Estado',
    acciones: 'Acciones',
    activo: 'Activo',
    inactivo: 'Inactivo',
    editar: 'Editar',
    noEncontrados: 'No se encontraron cuentadantes',
    mostrando: 'Mostrando',
    de: 'de',
    noRegistrada: 'No registrada'
  },

  // ============================================
  // ASIGNACIONES - Asignación de bienes
  // ============================================
  asignaciones: {
    titulo: 'Asignación de Bienes',
    nueva: 'Nueva Asignación',
    fecha: 'Fecha',
    cuentadante: 'Cuentadante',
    bienes: 'Bienes',
    descripcion: 'Descripción',
    noEncontradas: 'No se encontraron asignaciones',
    mostrando: 'Mostrando',
    de: 'de'
  },

  // ============================================
  // DÍAS DE LA SEMANA
  // ============================================
  days: ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'],

  // ============================================
  // MESES DEL AÑO
  // ============================================
  months: ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'],

  // ============================================
  // NOTIFICACIONES - Mensajes del sistema
  // ============================================
  notifications: {
    loginExitoso: 'Inicio de sesión exitoso',
    logoutExitoso: 'Sesión cerrada exitosamente',
    bienAgregado: 'Bien agregado exitosamente',
    bienActualizado: 'Bien actualizado exitosamente',
    bienDesasignado: 'Bien desasignado exitosamente',
    cuentadanteAgregado: 'Cuentadante agregado exitosamente',
    cuentadanteActualizado: 'Cuentadante actualizado exitosamente',
    asignacionExitosa: 'Asignación realizada exitosamente',
    error: 'Ha ocurrido un error',
    success: 'Operación exitosa'
  },

  // ============================================
  // AUTH - Autenticación y login
  // ============================================
  auth: {
    iniciarSesion: 'Iniciar Sesión',
    correo: 'Correo Electrónico',
    contrasena: 'Contraseña',
    olvidoContrasena: '¿Olvidó su contraseña?',
    ingresar: 'Ingresar',
    recuperarContrasena: 'Recuperar Contraseña',
    enviarEnlace: 'Enviar Enlace',
    volver: 'Volver al inicio de sesión'
  }
}

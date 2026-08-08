/**
 * ============================================
 * TRADUÇÕES EM PORTUGUÊS
 * ============================================
 * 
 * Este arquivo contém todas as traduções da aplicação
 * em português (pt).
 * 
 * Estrutura:
 * - sidebar: Textos do menu lateral
 * - header: Textos da barra superior
 * - dashboard: Textos do painel principal
 * - bienes: Textos de gestão de bens
 * - cuentadantes: Textos de gestão de responsáveis
 * - asignaciones: Textos de atribuição de bens
 * - days: Nomes dos dias da semana
 * - months: Nomes dos meses
 * - notifications: Mensagens de notificação
 * - auth: Textos de autenticação
 * 
 * @module locales/pt
 */

export const pt = {
  // ============================================
  // SIDEBAR - Menu lateral de navegação
  // ============================================
  sidebar: {
    title: 'SENA BENS',
    subtitle: 'Sistema de Gestão',
    dashboard: 'Painel',
    dashboardDesc: 'Visão geral do sistema',
    bienes: 'Bens',
    bienesDesc: 'Gestão de bens tecnológicos',
    cuentadantes: 'Responsáveis',
    cuentadantesDesc: 'Gestão de responsáveis',
    asignaciones: 'Atribuições',
    asignacionesDesc: 'Atribuir bens aos responsáveis',
    perfilUsuario: 'Perfil do Usuário',
    configuracion: 'Configurações',
    cerrarSesion: 'Sair',
    sistemaActivo: 'Sistema Ativo',
    version: 'Versão 2025.1'
  },

  // Header
  header: {
    dashboardPrincipal: 'Painel Principal',
    sistemaActivo: 'Sistema Ativo',
    ultimaSync: 'Última sinc',
    hace: 'há',
    min: 'min',
    seg: 'seg',
    cambiarTemaClaro: 'Mudar para tema claro',
    cambiarTemaOscuro: 'Mudar para tema escuro'
  },

  // Dashboard
  dashboard: {
    bienvenido: 'Bem-vindo',
    ultimosMovimientos: 'Últimos Movimentos',
    alertasSistema: 'Alertas do Sistema',
    entrada: 'Entrada',
    asignacion: 'Atribuição',
    hoy: 'Hoje',
    ayer: 'Ontem',
    bienesMantenimiento: 'bens próximos à manutenção',
    bienesSinAsignar: 'bens não atribuídos há mais de 30 dias'
  },

  // Bienes
  bienes: {
    titulo: 'Gestão de Bens',
    agregar: 'Adicionar Bem',
    buscar: 'Buscar por código, descrição ou categoria...',
    todosEstados: 'Todos os status',
    disponible: 'Disponível',
    asignado: 'Atribuído',
    mantenimiento: 'Manutenção',
    baja: 'Baixado',
    modelo: 'Modelo',
    descripcion: 'Descrição',
    serial: 'Serial',
    estado: 'Status',
    costo: 'Custo',
    fechaCompra: 'Data de Compra',
    vidaUtil: 'Vida Útil',
    sede: 'Localização',
    acciones: 'Ações',
    editar: 'Editar',
    desasignar: 'Desatribuir',
    asignadoA: 'Atribuído a',
    desde: 'Desde',
    noEncontrados: 'Nenhum bem encontrado',
    mostrando: 'Mostrando',
    de: 'de',
    noRegistrada: 'Não registrada',
    confirmarDesasignar: 'Tem certeza de que deseja desatribuir o bem'
  },

  // Cuentadantes
  cuentadantes: {
    titulo: 'Gestão de Responsáveis',
    agregar: 'Adicionar Responsável',
    buscar: 'Buscar por nome, CPF, cargo ou área...',
    cedula: 'CPF',
    nombre: 'Nome',
    cargo: 'Cargo',
    area: 'Área',
    contacto: 'Contato',
    fechaHoraCreacion: 'Data/Hora de Criação',
    estado: 'Status',
    acciones: 'Ações',
    activo: 'Ativo',
    inactivo: 'Inativo',
    editar: 'Editar',
    noEncontrados: 'Nenhum responsável encontrado',
    mostrando: 'Mostrando',
    de: 'de',
    noRegistrada: 'Não registrada'
  },

  // Asignaciones
  asignaciones: {
    titulo: 'Atribuição de Bens',
    nueva: 'Nova Atribuição',
    fecha: 'Data',
    cuentadante: 'Responsável',
    bienes: 'Bens',
    descripcion: 'Descrição',
    noEncontradas: 'Nenhuma atribuição encontrada',
    mostrando: 'Mostrando',
    de: 'de'
  },

  // Días de la semana
  days: ['domingo', 'segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado'],

  // Meses
  months: ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'],

  // Notificaciones
  notifications: {
    loginExitoso: 'Login bem-sucedido',
    logoutExitoso: 'Sessão encerrada com sucesso',
    bienAgregado: 'Bem adicionado com sucesso',
    bienActualizado: 'Bem atualizado com sucesso',
    bienDesasignado: 'Bem desatribuído com sucesso',
    cuentadanteAgregado: 'Responsável adicionado com sucesso',
    cuentadanteActualizado: 'Responsável atualizado com sucesso',
    asignacionExitosa: 'Atribuição realizada com sucesso',
    error: 'Ocorreu um erro',
    success: 'Operação bem-sucedida'
  },

  // Auth
  auth: {
    iniciarSesion: 'Entrar',
    correo: 'E-mail',
    contrasena: 'Senha',
    olvidoContrasena: 'Esqueceu sua senha?',
    ingresar: 'Entrar',
    recuperarContrasena: 'Recuperar Senha',
    enviarEnlace: 'Enviar Link',
    volver: 'Voltar ao login'
  }
}

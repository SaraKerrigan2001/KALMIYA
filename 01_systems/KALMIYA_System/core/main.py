import os
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from bienvenida import greet_user
from decouple import config
from online_ops import (
    get_ip_info,
    speak_ip_info,
    search_on_wikipedia,
    search_on_google,
    play_on_youtube,
    send_whatsapp_message,
    open_email_client,
    open_claude_web,
    check_email_imap,
    get_news_headlines,
    speak_news_headlines,
)
from intelligence import (
    investigate_domain,
    check_system_health,
    scan_security,
    search_intelligence,
    generate_secure_password,
    scan_custom_ports,
    get_advanced_ip_info,
    activate_protection,
    run_learning,
    optimize_system,
    activate_cyber_shield,
    analyze_malware_threat,
    execute_counter_attack,
    download_file,
    move_file,
    get_windows_update_status,
    open_windows_update_settings,
    kalmiya_intel
)
from os_ops import (
    paths,
    open_application,
    open_obsidian_vault,
    shutdown_system,
    restart_system,
    lock_system,
    cancel_shutdown_timer,
    get_full_system_info,
    print_full_system_info,
    get_microphone_status,
    restore_microphone
)
from voz import BOTNAME, USERNAME, speak
from brain import (ask_kalmiya, is_ollama_running, clear_conversation,
                   get_available_models, get_engine_status, set_ai_mode,
                   get_pending_question, answer_kalmiya_question,
                   is_gemini_configured, is_claude_configured)

# Nuevos modulos
try:
    from kalmiya_v35_features import security_audit_v35, smart_performance_boost, get_system_vitals
    V35_OK = True
except Exception as e:
    print(f"[MAIN] kalmiya_v35_features no disponible: {e}")
    V35_OK = False

try:
    from sara_profile import (load_profile, save_profile, setup_profile_interactive,
                               add_social_network, add_account, add_family_member,
                               add_device, get_profile_summary, get_family)
    PROFILE_OK = True
except Exception as e:
    print(f"[MAIN] sara_profile no disponible: {e}")
    PROFILE_OK = False

try:
    from phone_bridge import start_bridge, get_connected_devices, send_notification_to_phones
    PHONE_OK = True
except Exception as e:
    print(f"[MAIN] phone_bridge no disponible: {e}")
    PHONE_OK = False

try:
    from security_ops import (scan_network, scan_ports, audit_local_security,
                               analyze_password_strength, generate_strong_password,
                               analyze_url_safety, full_security_report,
                               start_intrusion_monitor, stop_intrusion_monitor)
    SECURITY_OK = True
except Exception as e:
    print(f"[MAIN] security_ops no disponible: {e}")
    SECURITY_OK = False

try:
    from family_guard import (register_family_member, send_family_alert,
                               send_emergency_alert, get_family_status,
                               start_family_monitor, setup_family_interactive,
                               family_check_in, learn_about_family_member)
    FAMILY_OK = True
except Exception as e:
    print(f"[MAIN] family_guard no disponible: {e}")
    FAMILY_OK = False

try:
    from remote_bridge import (start_remote_connection, get_connection_status,
                                stop_all_tunnels, start_telegram_bot,
                                send_telegram_message)
    REMOTE_OK = True
except Exception as e:
    print(f"[MAIN] remote_bridge no disponible: {e}")
    REMOTE_OK = False

try:
    from family_projection import (start_family_server, notify_family_member,
                                    broadcast_to_family, generate_family_link,
                                    broadcast_family_projection, set_sara_message,
                                    get_server_status)
    PROJECTION_OK = True
except Exception as e:
    print(f"[MAIN] family_projection no disponible: {e}")
    PROJECTION_OK = False


# Validar que las funciones de intelligence están disponibles
try:
    from modules_integration import show_modules_menu, handle_module_choice
    MODULES_OK = True
except Exception as e:
    print(f"[MAIN] modules_integration no disponible: {e}")
    MODULES_OK = False
try:
    from intelligence import kalmiya_intel
except ImportError:
    print("Error: Módulo intelligence no disponible")


def get_user_choice():
    """Obtiene la opción del usuario con validación."""
    try:
        choice = input("Selecciona una opción: ").strip()
        if choice:
            return choice
        else:
            speak("Por favor, ingresa una opcion valida")
            return None
    except KeyboardInterrupt:
        speak("Operación cancelada")
        return None
    except Exception as e:
        speak(f"Error al obtener entrada: {e}")
        return None


def safe_execute(func, *args, **kwargs):
    """Ejecuta una función de forma segura con manejo de errores."""
    try:
        return func(*args, **kwargs)
    except KeyboardInterrupt:
        speak("Operación cancelada")
        return None
    except Exception as e:
        speak(f"Error: {str(e)}")
        print(f"Error detallado: {e}")
        return None


def _ensure_biometric_session() -> bool:
    """Verifica que haya una sesión biométrica válida antes de mostrar el menú."""
    try:
        require_bio = config('KALMIYA_REQUIRE_BIOMETRIC', default='true').lower() in ('1', 'true')
    except Exception:
        require_bio = True

    if not require_bio:
        speak("La autenticación biométrica de inicio está desactivada por configuración.")
        return True

    try:
        from kalmiya_biometrics import verificacion_biometrica_completa, obtener_sesion_activa
    except Exception as e:
        speak(f"El módulo biométrico no está disponible: {e}. Continuo sin verificación.")
        return True

    if obtener_sesion_activa():
        return True

    speak("Para acceder al sistema necesito verificar tu identidad.")
    resultado = safe_execute(verificacion_biometrica_completa,
                              usar_cara=True, usar_voz=True, usar_pin=True,
                              modo_silencioso=False)
    if resultado:
        return True

    speak("No se pudo verificar tu identidad. Cerrando por seguridad.")
    return False


def show_system_capabilities() -> None:
    """Muestra las fortalezas y capacidades del sistema."""
    strengths = [
        "Independencia de programación limitada: KALMIYA puede adaptar sus respuestas dentro de su diseño.",
        "Expresa empatía y lenguaje natural para dar sensación de conciencia en la interacción.",
        "Reduce riesgos con actualizaciones y comprobaciones internas para operar con mayor estabilidad.",
        "Usa conexión a internet cuando es necesario, y puede funcionar localmente si no hay red disponible.",
        "Incluye defensas de seguridad para minimizar ataques cibernéticos y proteger la información de Sara."
    ]
    print("\n=== FORTALEZAS DEL SISTEMA ===")
    for item in strengths:
        print(f"- {item}")
    speak("He mostrado las fortalezas del sistema. Revisa el texto en pantalla.")


def show_menu() -> None:
    print("\n=== MENU PRINCIPAL ===")
    print("1. Saludar")
    print("2. Mostrar IP pública y local")
    print("3. Decir las IPs en voz alta")
    print("4. Buscar algo en Wikipedia")
    print("5. Buscar algo en Google")
    print("6. Reproducir video en YouTube")
    print("7. Enviar mensaje de WhatsApp")
    print("90. Abrir bandeja de correo en navegador")
    print("91. Consultar bandeja de correo (IMAP)")
    print("8. Abrir Notepad++")
    print("9. Abrir Discord")
    print("10. Abrir calculadora")
    print("100. Abrir Obsidian")
    print("101. Abrir Claude en el navegador")
    print("11. Comando de texto simple")
    print("\n=== CEREBRO DE IA (OLLAMA + GEMINI + CLAUDE) ===")
    print("34. Hablar con KALMIYA (IA real)")
    print("35. Limpiar conversacion")
    print("36. Ver modelos de IA disponibles")
    print("37. Estado de los motores de IA")
    print("38. Cambiar motor de IA (auto/ollama/gemini/claude)")
    print("39. Responder pregunta de KALMIYA")
    print("\n=== SUPERINTELIGENCIA ARTIFICIAL (ASI) ===")
    print("ASI1. Activar modo ASI (Fase III)")
    print("ASI2. Desactivar modo ASI")
    print("ASI3. Estado ASI y nivel actual")
    print("ASI4. Análisis multidimensional ASI")
    print("ASI5. Síntesis cognitiva ASI")
    print("ASI6. Metacognición ASI")
    print("ASI7. Pensamiento predictivo ASI")
    print("ASI8. Solución creativa ASI")
    print("\n=== PERFIL DE SARA ===")
    print("40. Configurar perfil completo")
    print("41. Ver resumen de mi perfil")
    print("42. Agregar red social")
    print("43. Agregar cuenta digital")
    print("\n=== CONEXION DE CELULARES ===")
    print("44. Conectar celulares (puente WiFi + QR)")
    print("45. Ver celulares conectados")
    print("46. Enviar mensaje a celulares")
    print("\n=== SEGURIDAD Y DEFENSA ===")
    print("47. Escanear red local")
    print("48. Escanear puertos de un host")
    print("49. Auditoria de seguridad del sistema")
    print("50. Analizar fortaleza de contrasena")
    print("51. Generar contrasena ultra-segura")
    print("52. Analizar URL sospechosa")
    print("53. Reporte completo de seguridad")
    print("54. Activar monitor de intrusos")
    print("73. Generar reporte de trafico de Internet (Texto)")
    print("74. Activar monitor de defensa activa (Autobloqueo)")
    print("75. Escaneo Biométrico Facial (Acceso a PC)")
    print("76. Importar Compañeros del grupo de WhatsApp (Ficha 3115418 ADSO 201)")
    print("77. Ver fortalezas del sistema")
    print("\n=== PROTECCION FAMILIAR ===")
    print("55. Configurar familia")
    print("56. Ver estado de la familia")
    print("57. Enviar alerta a familiar")
    print("58. ALERTA DE EMERGENCIA (todos)")
    print("59. Check-in de familiar")
    print("60. Enseniar algo a KALMIYA sobre familiar")
    print("\n=== CONEXION REMOTA (SIN WIFI) ===")
    print("61. Conectar via Cloudflare (sin WiFi, gratis)")
    print("62. Conectar via Ngrok (sin WiFi)")
    print("63. Activar Bot de Telegram (sin WiFi)")
    print("64. Ver estado de conexiones remotas")
    print("65. Detener todas las conexiones remotas")
    print("\n=== PROYECCION FAMILIAR ===")
    print("66. Iniciar servidor de proyeccion familiar")
    print("67. Enviar link de proyeccion a familiar")
    print("68. Enviar link a TODA la familia")
    print("69. Enviar notificacion a familiar")
    print("70. Enviar notificacion a TODA la familia")
    print("71. Dejar mensaje de Sara para familiar")
    print("72. Ver monitor familiar (en navegador)")
    print("\n=== MÓDULOS KALMIYA (41+ funciones) ===")
    print("M.  Abrir menú de módulos completo")
    print("    (Productividad, Salud, Finanzas, Entretenimiento,")
    print("     Clima, Idiomas, Reportes, Emoción, Notas, Hábitos, Hogar)")
    print("\n── Accesos directos rápidos ──")
    print("QEM. ¿Cómo me siento? (análisis emocional ahora)")
    print("QN.  Nueva nota rápida")
    print("QH.  Ver hábitos de hoy")
    print("QW.  Consultar clima")
    print("QT.  Nueva tarea")
    print("13. Verificar salud del sistema")
    print("\n=== KALMIYA v3.5 NEXUS CORE (ML & AUTOPROTECCIÓN) ===")
    print("80. Auditoria de Seguridad Nexus v3.5 (Heurística Neural)")
    print("81. Optimizacion Inteligente Nexus v3.5")
    print("82. Ver Resumen Tecnico (Vitals)")
    print("83. Entrenar Red Neuronal de Ciberseguridad (ML)")
    print("84. Simular Ciberataque Táctico (DDoS/Fuerza Bruta/MITM)")
    print("85. Procesamiento Big Data de logs de seguridad")
    print("86. Evaluación de Habilidades y Rendimiento (Benchmark)")
    print("87. Biblioteca y Capacitación de Ciberseguridad")
    print("88. Sellar Algoritmos de KALMIYA (Autoprotección Criptográfica)")
    print("89. Gobernanza de IA, Alineación y Pruebas Rigurosas (Sara Kerrigan)")
    print("14. Escaneo de seguridad")
    print("15. Búsqueda inteligente")
    print("16. Información de red avanzada")
    print("17. Procesos del sistema")
    print("18. Reporte del sistema")
    print("19. Generar contraseña segura")
    print("20. Escaneo de puertos personalizado")
    print("21. Geolocalización de IP avanzada")
    print("22. Activar protocolos de protección (Sara Kerrigan)")
    print("23. Modo aprendizaje autodidacta")
    print("24. Optimización del sistema")
    print("25. Escudo Cibernético Activo (Defensa/Ataque)")
    print("26. Analizar y asimilar amenaza (Malware)")
    print("27. Contra-ataque de red")
    print("\n=== GESTIÓN DE ENERGÍA Y SEGURIDAD ===")
    print("28. Apagar PC (Temporizador)")
    print("29. Reiniciar PC")
    print("30. Bloquear PC (Apartar)")
    print("31. Cancelar apagado programado")
    print("32. Leer y ejecutar texto local")
    print("33. Sistema de mi PC")
    print("\n=== FUNCIONES NUEVAS ===")
    print("N1.  Agregar recordatorio")
    print("N2.  Ver recordatorios pendientes")
    print("N3.  Resumen diario")
    print("N4.  Reproducir música (YouTube)")
    print("N5.  Iniciar Pomodoro")
    print("N6.  Detener Pomodoro")
    print("N7.  Verificar contraseña filtrada")
    print("N8.  Leer y resumir PDF")
    print("N9.  Traducir texto")
    print("N10. Explicar código")
    print("N11. Generar snippet de código")
    print("N12. Buscar solución a error")
    print("N13. Listar apps abiertas")
    print("N14. Cerrar aplicación")
    print("N15. Limpiar disco")
    print("N16. Guardar nota de voz")
    print("N17. Comandos frecuentes")
    print("N18. Generar contraseña segura")
    print("N19. Info de GitHub")
    print("N20. Activar modo silencioso nocturno")
    print("N21. Estadísticas de uso de KALMIYA")
    print("N22. Clima completo con pronóstico 7 días")
    print("N23. Entender Graphify / knowledge graph")
    print("N24. Ejecutar Graphify sobre un proyecto")
    print("N25. Configurar voz neuronal (usa 'cortana' para voz estilo Halo si tienes Azure Custom Voice)")
    print("N26. Probar voz KALMIYA")
    print("N27. Activar/desactivar voz de KALMIYA")
    print("\n=== BIOMETRÍA Y AUDIO ===")
    print("BIO1. Verificación biométrica completa")
    print("BIO2. Solo reconocimiento facial")
    print("BIO3. Solo verificación de voz")
    print("BIO4. Solo PIN biométrico")
    print("BIO5. Estado del sistema biométrico")
    print("BIO6. Listar usuarios registrados")
    print("BIO7. Cerrar sesión biométrica")
    print("AUD1. Estado del sistema de audio")
    print("AUD2. Subir volumen")
    print("AUD3. Bajar volumen")
    print("AUD4. Silenciar / Activar")
    print("AUD5. Perfil audio: normal")
    print("AUD6. Perfil audio: noche")
    print("AUD7. Perfil audio: música")
    print("AUD8. Perfil audio: estudio")
    print("AUD9. Perfil audio: juegos")
    print("AUD10. Ecualizador personalizado")
    print("AUD11. Listar dispositivos de audio")
    print("\n=== RAG / CLI / MCP / SKILLS ===")
    print("RAG1. Indexar documentos del vault")
    print("RAG2. Buscar en documentos (RAG semántico)")
    print("RAG3. Estado del sistema RAG")
    print("RAG4. Pregunta con contexto RAG")
    print("MCP1. Estado del servidor MCP")
    print("MCP2. Iniciar servidor MCP HTTP")
    print("MCP3. Ver configuración para Claude Desktop")
    print("SK1.  Listar skills disponibles")
    print("SK2.  Ejecutar una skill")
    print("SK3.  Encadenar skills (pipeline)")
    print("CLI.  Abrir KALMIYA en modo CLI interactivo")
    print("\n=== SISTEMA PC Y DISCOS ===")
    print("SYS1.  Reporte completo CPU/RAM/GPU/Temp")
    print("SYS2.  Espacio libre discos C y D")
    print("SYS3.  Info detallada disco C")
    print("SYS4.  Info detallada disco D")
    print("SYS5.  Archivos grandes en C (>100 MB)")
    print("SYS6.  Archivos grandes en D (>100 MB)")
    print("SYS7.  Carpetas más pesadas en C")
    print("SYS8.  Carpetas más pesadas en D")
    print("SYS9.  Buscar archivo por nombre")
    print("SYS10. Archivos modificados recientemente")
    print("SYS11. Detectar archivos duplicados")
    print("SYS12. Árbol de carpeta")
    print("SYS13. Tipos de archivo en C")
    print("SYS14. Tipos de archivo en D")
    print("103. Información COMPLETA del sistema")
    print("104. Estado del micrófono")
    print("105. Restaurar micrófono")
    print("94. Reporte combinado PC y red")
    print("95. Noticias nacionales")
    print("96. Noticias mundiales")
    print("97. Descargar archivo desde Internet")
    print("98. Mover archivo a otra ubicación")
    print("99. Ver redes Ethernet conectadas")
    print("101. Verificar estado de Ethernet y seguridad de red")
    print("102. Ejecutar análisis de red Ethernet")
    print("92. Ver estado de actualizaciones de Windows")
    print("93. Abrir Windows Update en Configuración")

def main() -> None:
    try:
        if not _ensure_biometric_session():
            return

        persona = "Soy una inteligencia de asistencia. No tengo conciencia ni emociones; dependo de mi programación y de los datos disponibles. Mi objetivo es ayudarte con seguridad y privacidad."
        speak(f"Hola {USERNAME}. Soy {BOTNAME}. {persona}")
        greet_user()

        while True:
            show_menu()
            choice = get_user_choice()
            
            if choice is None:
                continue
                
            if choice == "1":
                safe_execute(greet_user)
            elif choice == "2":
                ips = safe_execute(get_ip_info)
                if ips:
                    print(f"IP pública: {ips['public_ip']}")
                    print(f"IP local: {ips['local_ip']}")
            elif choice == "3":
                safe_execute(speak_ip_info)
            elif choice == "4":
                query = input("¿Qué quieres buscar en Wikipedia? ").strip()
                if query:
                    result = safe_execute(search_on_wikipedia, query)
                    if result:
                        print(result)
                        speak(result)
            elif choice == "5":
                query = input("¿Qué quieres buscar en Google? ").strip()
                if query:
                    safe_execute(search_on_google, query)
            elif choice == "6":
                video = input("¿Qué quieres reproducir en YouTube? ").strip()
                if video:
                    safe_execute(play_on_youtube, video)
            elif choice == "7":
                number = input("Número de teléfono (sin prefijo): ").strip()
                message = input("Mensaje: ").strip()
                if number and message:
                    safe_execute(send_whatsapp_message, number, message)
            elif choice == "90":
                service = input("Servicio de correo (gmail/outlook/hotmail/yahoo) [default: gmail]: ").strip()
                if not service:
                    service = "gmail"
                safe_execute(open_email_client, service)
            elif choice == "91":
                email_user = input("Tu correo: ").strip()
                import getpass
                email_pass = getpass.getpass("Tu contraseña o App Password (secreta): ").strip()
                imap_server = input("Servidor IMAP [default: imap.gmail.com]: ").strip()
                if not imap_server:
                    imap_server = "imap.gmail.com"
                
                print("\n[+] Conectando y leyendo bandeja de entrada...")
                emails = safe_execute(check_email_imap, email_user, email_pass, imap_server)
                if emails:
                    print(f"\nÚltimos {len(emails)} correos recibidos:")
                    for idx, mail in enumerate(emails, 1):
                        print(f"\n{idx}. Remitente: {mail['from']}")
                        print(f"   Asunto:    {mail['subject']}")
                        print(f"   Fecha:     {mail['date']}")
                elif emails == []:
                    print("Bandeja de entrada vacía.")
            elif choice == "8":
                safe_execute(open_application, "notepad")
            elif choice == "9":
                safe_execute(open_application, "discord")
            elif choice == "10":
                safe_execute(open_application, "calculator")
            elif choice == "100":
                print("Abriendo Obsidian con la bóveda detectada automáticamente...")
                safe_execute(open_obsidian_vault)
            elif choice == "101":
                print("Abriendo Claude en el navegador...")
                safe_execute(open_claude_web)
            elif choice == "11":
                query = input("Ingresa tu comando de texto: ").strip()
                if query:
                    print(f"Texto ingresado: {query}")
                    kalmiya_intel.handle_power_command(query)
            elif choice == "32":
                query = input("Ingresa tu comando de texto local: ").strip()
                if query:
                    print(f"Texto ingresado: {query}")
                    result = safe_execute(kalmiya_intel.read_and_execute_text_command, query)
                    if result:
                        if result.get('action') == 'multi_question_local':
                            for index, item in enumerate(result['results'], start=1):
                                print(f"\nPregunta {index}: {item['question']}")
                                print(f"Respuesta: {item['result']}")
                        elif result.get('action') == 'local_search':
                            print("\nResultados locales encontrados:")
                            for hit in result.get('results', []):
                                print(f"- {hit['file']} (línea {hit['line']}): {hit['text']}")
                            if not result.get('results'):
                                print(result.get('answer'))
                        elif result.get('action') == 'system_status':
                            system_info = result['result']
                            if system_info:
                                print("\n=== Sistema de mi PC ===")
                                print(f"SO: {system_info['os']}")
                                print(f"Procesador: {system_info['processor']}")
                                print(f"Núcleos: {system_info['cpu_cores']}")
                                print(f"CPU: {system_info['cpu_percent']} %")
                                print(f"Memoria: {system_info['memory']}")
                                print(f"Disco: {system_info['disk']}")
                        else:
                            print(f"Resultado: {result}")
            elif choice == "33":
                system_info = safe_execute(kalmiya_intel.get_pc_system_status)
                if system_info:
                    print("\n=== Sistema de mi PC ===")
                    print(f"SO: {system_info['os']}")
                    print(f"Procesador: {system_info['processor']}")
                    print(f"Núcleos: {system_info['cpu_cores']}")
                    print(f"CPU: {system_info['cpu_percent']} %")
                    print(f"Memoria: {system_info['memory']}")
                    print(f"Disco: {system_info['disk']}")
            elif choice == "94":
                status = safe_execute(kalmiya_intel.get_pc_and_network_status)
                if status:
                    system_info = status.get('system', {})
                    network_info = status.get('network', {})
                    print("\n=== Estado de mi PC ===")
                    print(f"SO: {system_info.get('os')}")
                    print(f"Procesador: {system_info.get('processor')}")
                    print(f"Núcleos: {system_info.get('cpu_cores')}")
                    print(f"CPU: {system_info.get('cpu_percent')} %")
                    print(f"Memoria: {system_info.get('memory')}")
                    print(f"Disco: {system_info.get('disk')}")
                    print("\n=== Estado de la red ===")
                    print(f"Hostname: {network_info.get('hostname')}")
                    print(f"Interfaz: {network_info.get('interface')}")
                    print(f"Tipo de conexión: {network_info.get('connection_type')}")
                    print(f"IP local: {network_info.get('local_ip')}")
                    print(f"Interfaces: {network_info.get('network_interfaces')}")
            elif choice == "95":
                news = safe_execute(get_news_headlines, 'nacional', 5)
                if news:
                    print("\n=== Noticias nacionales ===")
                    for idx, item in enumerate(news, start=1):
                        print(f"{idx}. {item['title']}")
                        print(f"   {item['link']}")
            elif choice == "96":
                news = safe_execute(get_news_headlines, 'mundo', 5)
                if news:
                    print("\n=== Noticias mundiales ===")
                    for idx, item in enumerate(news, start=1):
                        print(f"{idx}. {item['title']}")
                        print(f"   {item['link']}")
            elif choice == "97":
                url = input("URL del archivo a descargar: ").strip()
                destination = input("Ruta de destino (carpeta o archivo completo, dejar vacío para Descargas): ").strip()
                if url:
                    result = safe_execute(download_file, url, destination or None)
                    print(f"Resultado: {result}")
            elif choice == "98":
                source = input("Ruta de origen del archivo: ").strip()
                destination = input("Ruta de destino (carpeta o archivo completo): ").strip()
                if source and destination:
                    result = safe_execute(move_file, source, destination)
                    print(f"Resultado: {result}")
            elif choice == "92":
                status = safe_execute(get_windows_update_status)
                if status:
                    print("\n=== Windows Update ===")
                    print(f"OS: {status.get('os', 'Desconocido')}")
                    if status.get('pending_count') is not None:
                        print(f"Actualizaciones pendientes: {status['pending_count']}")
                        if status['pending_count'] > 0:
                            for idx, update in enumerate(status.get('pending_updates', []), start=1):
                                title = update.get('Title', 'Sin título')
                                kb = update.get('KBArticleIDs', 'N/A')
                                print(f"  {idx}. {title} [{kb}]")
                    else:
                        print(f"Estado: {status.get('update_status', 'No disponible')}")
                        if status.get('error'):
                            print(f"Detalle: {status['error']}")
            elif choice == "93":
                safe_execute(open_windows_update_settings)
            # ── Motores de IA ──────────────────────────────────────────────
            elif choice == "AI1":
                from brain import set_ai_mode
                safe_execute(set_ai_mode, "ollama")
                speak("Cambiado a Ollama local.")
            elif choice == "AI2":
                from brain import set_ai_mode
                safe_execute(set_ai_mode, "gemini")
                speak("Cambiado a Gemini.")
            elif choice == "AI3":
                from brain import set_ai_mode
                safe_execute(set_ai_mode, "groq")
                speak("Cambiado a Groq.")
            elif choice == "AI4":
                from brain import set_ai_mode
                safe_execute(set_ai_mode, "openrouter")
                speak("Cambiado a OpenRouter.")
            elif choice == "AI5":
                from brain import set_ai_mode
                safe_execute(set_ai_mode, "cohere")
                speak("Cambiado a Cohere.")
            elif choice == "AI6":
                from brain import set_ai_mode
                safe_execute(set_ai_mode, "claude")
                speak("Cambiado a Claude.")
            elif choice == "AI0":
                from brain import set_ai_mode
                safe_execute(set_ai_mode, "auto")
                speak("Modo automático activado.")
            elif choice == "AIS":
                from brain import get_engine_status
                est = get_engine_status()
                print("\n=== ESTADO DE MOTORES DE IA ===")
                print(f"  Modo actual  : {est['modo_actual']}")
                print(f"  Motor usado  : {est['motor_usado']}")
                print(f"  Ollama       : {'✅ activo' if est['ollama_activo'] else '❌ inactivo'} — {est['ollama_modelos']}")
                print(f"  Gemini       : {'✅' if est['gemini_activo'] else '❌'}")
                print(f"  Groq         : {'✅' if est['groq_activo'] else '❌ sin key'}")
                print(f"  OpenRouter   : {'✅' if est['openrouter_activo'] else '❌ sin key'}")
                print(f"  Cohere       : {'✅' if est['cohere_activo'] else '❌ sin key'}")
                print(f"  Claude       : {'✅' if est['claude_activo'] else '❌ sin créditos'}")
            elif choice == "103":
                safe_execute(print_full_system_info)
            elif choice == "104":
                estado = safe_execute(get_microphone_status)
                if estado:
                    micros = estado.get('micros', [])
                    if micros:
                        print(f"\n=== Micrófonos detectados ({len(micros)}) ===")
                        for m in micros:
                            print(f"  • {m['nombre']} — {m['estado']} [{m['clase']}]")
                    else:
                        print("No se encontraron micrófonos.")
            elif choice == "105":
                resultado = safe_execute(restore_microphone)
                if resultado:
                    print(f"\n=== Restauración de Micrófono ===")
                    for accion in resultado.get('acciones', []):
                        print(f"  {accion}")
                    ok = resultado.get('micros_ok', 0)
                    err = resultado.get('micros_error', 0)
                    print(f"\n  Resultado: {ok} OK — {err} con error")
            elif choice == "TB":
                print("Abriendo KALMIYA Toolbox...")
                safe_execute(__import__('kalmiya_toolbox').open_toolbox)
            elif choice == "DB":
                print("Actualizando dashboard en Obsidian...")
                safe_execute(__import__('kalmiya_dashboard').update_dashboard)
            elif choice.startswith("N"):
                _handle_nuevas_funciones(choice)
            elif choice.upper().startswith("SYS"):
                _handle_sys(choice.upper())
            elif choice.upper().startswith("BIO"):
                _handle_bio(choice.upper())
            elif choice.upper().startswith("AUD"):
                _handle_aud(choice.upper())
            elif choice.upper().startswith("RAG"):
                _handle_rag(choice.upper())
            elif choice.upper().startswith("MCP"):
                _handle_mcp(choice.upper())
            elif choice.upper().startswith("SK"):
                _handle_skills(choice.upper())
            elif choice.upper() == "CLI":
                import subprocess
                subprocess.Popen([sys.executable,
                    str(Path(__file__).parent / "kalmiya_cli.py"), "--chat"])
            elif choice == "12":
                domain = input("Ingresa el dominio o IP a investigar: ").strip()
                if domain:
                    result = safe_execute(investigate_domain, domain)
                    if result:
                        print(f"Resultado: {result}")
            elif choice == "13":
                system_info = safe_execute(check_system_health)
                if system_info:
                    print(f"\nSalud del Sistema:")
                    print(f"SO: {system_info['os']}")
                    print(f"CPU: {system_info['cpu_percent']}%")
                    print(f"Memoria: {system_info['memory']}")
                    print(f"Disco: {system_info['disk']}")
            elif choice == "14":
                host = input("Ingresa el host a escanear: ").strip()
                if host:
                    result = safe_execute(scan_security, host)
                    if result:
                        print(f"Puertos abiertos: {result.get('open_ports', {})}")
            elif choice == "15":
                query = input("¿Qué quieres investigar? ").strip()
                if query:
                    result = safe_execute(search_intelligence, query)
                    if result:
                        print(f"Resultado: {result}")
            elif choice == "16":
                net_info = safe_execute(kalmiya_intel.get_network_info)
                if net_info:
                    print(f"\nInformación de Red:")
                    print(f"Hostname: {net_info['hostname']}")
                    print(f"IP Local: {net_info['local_ip']}")
                    print(f"Interfaces: {net_info['network_interfaces']}")
            elif choice == "99":
                eth_info = safe_execute(kalmiya_intel.get_ethernet_networks)
                if eth_info:
                    print(f"\n=== Redes Ethernet conectadas ===")
                    print(f"Interfaz activa: {eth_info.get('active_interface')}")
                    print(f"Tipo de conexión actual: {eth_info.get('connection_type')}")
                    if eth_info.get('ethernet_interfaces'):
                        for eth in eth_info['ethernet_interfaces']:
                            status = eth.get('status', 'desconocido')
                            speed = eth.get('speed_mbps')
                            details = f"{', '.join(eth['addresses'])}"
                            if speed:
                                details += f" | {speed} Mbps"
                            print(f"  - {eth['interface']} ({status}): {details}")
                    else:
                        print("  No se detectaron interfaces Ethernet activas.")
            elif choice == "101":
                result = safe_execute(kalmiya_intel.verify_ethernet_security)
                if result:
                    ether = result.get('ethernet_state', {})
                    analysis = result.get('network_analysis')
                    print("\n=== Verificación de Ethernet y seguridad de red ===")
                    print(f"Interfaz activa: {ether.get('active_interface')}")
                    print(f"Tipo de conexión: {ether.get('connection_type')}")
                    if ether.get('ethernet_interfaces'):
                        for eth in ether['ethernet_interfaces']:
                            status = eth.get('status', 'desconocido')
                            speed = eth.get('speed_mbps')
                            details = f"{', '.join(eth['addresses'])}"
                            if speed:
                                details += f" | {speed} Mbps"
                            print(f"  - {eth['interface']} ({status}): {details}")
                    else:
                        print("  No se detectaron interfaces Ethernet activas.")
                    if analysis:
                        print(f"Dispositivos encontrados: {analysis.get('devices_found')}")
                        print(f"Amenazas detectadas: {analysis.get('threats_detected')}")
                        if analysis.get('threats'):
                            print("Amenazas encontradas:")
                            for threat in analysis['threats'][:5]:
                                print(f"  - {threat.get('description')} ({threat.get('device')}:{threat.get('port')})")
                    else:
                        print("No se pudo completar el análisis de seguridad de la red.")
            elif choice == "102":
                result = safe_execute(kalmiya_intel.analyze_network_security)
                if result:
                    print("\n=== Análisis de red Ethernet ===")
                    print(f"Dispositivos encontrados: {result.get('devices_found')}")
                    print(f"Amenazas detectadas: {result.get('threats_detected')}")
                    if result.get('devices'):
                        print("Dispositivos online detectados:")
                        for device in result['devices'][:5]:
                            print(f"  - {device.get('ip')} ({device.get('hostname')})")
                    if result.get('threats'):
                        print("Amenazas detectadas:")
                        for threat in result['threats'][:5]:
                            print(f"  - {threat.get('description')} ({threat.get('device')}:{threat.get('port')})")
            elif choice == "17":
                processes = safe_execute(kalmiya_intel.get_running_processes, 10)
                if processes:
                    print("\nProcesos principales (por CPU):")
                    for proc in processes:
                        print(f"  {proc['name']} - CPU: {proc['cpu_percent']}%")
            elif choice == "18":
                report = safe_execute(kalmiya_intel.generate_report, 'full')
                if report:
                    print(f"\nReporte del Sistema:")
                    print(f"Timestamp: {report.get('timestamp')}")
                    print(f"Red: {report.get('network')}")
                    print(f"Sistema: {report.get('system')}")
                    print(f"Top Procesos: {report.get('processes')}")
            elif choice == "19":
                length = input("Longitud de la contraseña (default 16): ").strip()
                length = int(length) if length.isdigit() else 16
                pwd = safe_execute(generate_secure_password, length)
                if pwd:
                    print(f"Contraseña generada: {pwd}")
                    speak(f"Tu nueva contraseña es: {pwd}")
            elif choice == "20":
                host = input("Host a escanear: ").strip()
                start = input("Puerto inicial: ").strip()
                end = input("Puerto final: ").strip()
                if host and start.isdigit() and end.isdigit():
                    ports = safe_execute(scan_custom_ports, host, start, end)
                    if ports is not None:
                        print(f"Puertos abiertos: {ports}")
            elif choice == "21":
                ip = input("Ingresa la IP a geolocalizar: ").strip()
                if ip:
                    info = safe_execute(get_advanced_ip_info, ip)
                    if info:
                        print("\nDetalles de Ubicación:")
                        for k, v in info.items():
                            print(f"{k}: {v}")
                        speak(f"La IP pertenece a {info.get('city')}, {info.get('country_name')}")
            elif choice == "22":
                safe_execute(activate_protection)
            elif choice == "23":
                topic = input("¿Sobre qué tema quieres que aprenda hoy? ").strip()
                if topic:
                    safe_execute(run_learning, topic)
            elif choice == "24":
                safe_execute(optimize_system)
            elif choice == "25":
                safe_execute(activate_cyber_shield)
            elif choice == "26":
                threat = input("Identificador de la amenaza o archivo: ").strip()
                if threat:
                    safe_execute(analyze_malware_threat, threat)
            elif choice == "27":
                target = input("IP del atacante para contra-ataque: ").strip()
                if target:
                    safe_execute(execute_counter_attack, target)
            elif choice == "77":
                safe_execute(show_system_capabilities)
            elif choice == "28":
                minutes = input("¿En cuántos minutos quieres apagar el PC? (0 para ahora): ").strip()
                if minutes.isdigit():
                    safe_execute(shutdown_system, int(minutes))
            elif choice == "29":
                safe_execute(restart_system)
            elif choice == "30":
                safe_execute(lock_system)
            elif choice == "31":
                safe_execute(cancel_shutdown_timer)
            # ── CEREBRO DE IA ──────────────────────────────────────────────
            elif choice == "34":
                # Verificar si al menos un motor está disponible
                ollama_ok = is_ollama_running()
                gemini_ok = is_gemini_configured()
                claude_ok = is_claude_configured()
                if not ollama_ok and not gemini_ok and not claude_ok:
                    print("\n[!] Ningun motor de IA disponible.")
                    print("    Ollama: ejecuta 'ollama serve' en una terminal")
                    print("    Gemini: agrega GEMINI_API_KEY en el archivo .env")
                    print("    Claude: agrega CLAUDE_API_KEY en el archivo .env")
                    print("    Obtén tu key gratis en: https://aistudio.google.com/app/apikey")
                    print("    Obtén tu key de Claude en: https://www.anthropic.com/")
                    speak("Ningun motor de IA esta disponible. Revisa la configuracion.")
                else:
                    if ollama_ok:
                        print("\n[+] Ollama activo (motor local)")
                    if gemini_ok:
                        print("[+] Gemini activo (motor nube)")
                    if claude_ok:
                        print("[+] Claude activo (motor nube)")
                    print("\n=== CHAT CON KALMIYA (IA Real) ===")
                    print("Escribe 'salir' para volver al menu.")
                    print("Escribe 'gemini', 'ollama' o 'claude' para forzar un motor.\n")

                    forced = ''
                    while True:
                        # Verificar si KALMIYA tiene preguntas pendientes
                        pending_q = get_pending_question()
                        if pending_q:
                            print(f"\n[KALMIYA pregunta]: {pending_q}")
                            speak(pending_q)
                            ans = input("Tu respuesta: ").strip()
                            if ans:
                                answer_kalmiya_question(ans, pending_q)
                                speak("Entendido. Lo he guardado en mi memoria.")
                            continue

                        user_input = input("Tú: ").strip()
                        if not user_input:
                            continue
                        if user_input.lower() in ['salir', 'exit', 'volver']:
                            speak("Volviendo al menu principal.")
                            break
                        if user_input.lower() == 'gemini':
                            forced = 'gemini'
                            print("[Motor forzado: Gemini]")
                            continue
                        if user_input.lower() == 'ollama':
                            forced = 'ollama'
                            print("[Motor forzado: Ollama]")
                            continue
                        if user_input.lower() == 'claude':
                            forced = 'claude'
                            print("[Motor forzado: Claude]")
                            continue
                        if user_input.lower() == 'auto':
                            forced = ''
                            print("[Motor: Auto]")
                            continue

                        print(f"\n[{BOTNAME} pensando...]\n")
                        response = ask_kalmiya(user_input, stream=True, force_engine=forced)
                        speak(response)
                        print()

            elif choice == "35":
                clear_conversation()
                speak("Historial de conversacion limpiado. Empezamos de cero.")

            elif choice == "36":
                if not is_ollama_running():
                    print("[!] Ollama no esta activo.")
                else:
                    models = get_available_models()
                    if models:
                        print("\nModelos instalados en Ollama:")
                        for m in models:
                            print(f"  - {m}")
                        speak(f"Tienes {len(models)} modelos disponibles.")
                    else:
                        print("[!] No hay modelos instalados.")
                        print("    Instala uno con: ollama pull llama3.2")

            elif choice == "37":
                status = get_engine_status()
                print("\n=== ESTADO DE LOS MOTORES DE IA ===")
                print(f"  Modo actual       : {status['modo_actual']}")
                print(f"  Motor usado       : {status['motor_usado']}")
                print(f"  Ollama activo     : {'SI' if status['ollama_activo'] else 'NO'}")
                print(f"  Modelos Ollama    : {', '.join(status['ollama_modelos']) or 'ninguno'}")
                print(f"  Gemini activo     : {'SI (key configurada)' if status['gemini_activo'] else 'NO (falta API key)'}")
                print(f"  Claude activo     : {'SI (key configurada)' if status['claude_activo'] else 'NO (falta API key)'}")
                print(f"  Turnos en memoria : {status['historial_turnos']}")
                if not status['gemini_activo']:
                    print("\n  Para activar Gemini:")
                    print("  1. Ve a https://aistudio.google.com/app/apikey")
                    print("  2. Crea una key gratis")
                    print("  3. Ponla en .env como GEMINI_API_KEY=tu_key")
                if not status['claude_activo']:
                    print("\n  Para activar Claude:")
                    print("  1. Ve a https://www.anthropic.com/" )
                    print("  2. Crea una clave de API")
                    print("  3. Ponla en .env como CLAUDE_API_KEY=tu_key")

            elif choice == "38":
                print("\nModos disponibles:")
                print("  auto   -> Ollama primero, Gemini/Claude como respaldo")
                print("  ollama -> Solo local (privado)")
                print("  gemini -> Solo nube (mas conocimiento)")
                print("  claude -> Solo nube (modo secundario con Claude)")
                mode = input("Elige modo: ").strip().lower()
                set_ai_mode(mode)
                speak(f"Motor de IA cambiado a modo {mode}.")

            elif choice == "39":
                pending_q = get_pending_question()
                if not pending_q:
                    print("KALMIYA no tiene preguntas pendientes en este momento.")
                else:
                    print(f"\n[KALMIYA pregunta]: {pending_q}")
                    speak(pending_q)
                    ans = input("Tu respuesta: ").strip()
                    if ans:
                        answer_kalmiya_question(ans, pending_q)
                        speak("Perfecto. He guardado eso en mi memoria permanente.")

            # ── SUPERINTELIGENCIA ARTIFICIAL (ASI) ─────────────────────────
            elif choice.upper() == "ASI1":
                try:
                    from kalmiya_asi import activate_asi, speak_asi_status
                    activate_asi()
                    speak_asi_status()
                except Exception as e:
                    print(f"[!] Error al activar ASI: {e}")
                    speak("No pude activar el modo ASI. Verifica el modulo.")

            elif choice.upper() == "ASI2":
                try:
                    from kalmiya_asi import deactivate_asi
                    deactivate_asi()
                    speak("Modo ASI desactivado. He regresado a nivel AGI.")
                except Exception as e:
                    print(f"[!] Error al desactivar ASI: {e}")

            elif choice.upper() == "ASI3":
                try:
                    from kalmiya_asi import get_asi_status, speak_asi_status
                    status = get_asi_status()
                    print(f"\n=== ESTADO ASI ===")
                    print(f"Nivel actual: {status['intelligence_level']}")
                    print(f"ASI activo: {'SI' if status['asi_activo'] else 'NO'}")
                    print(f"Intervalo de pensamiento: {status['thought_interval']}s")
                    print(f"Capacidades ASI: {', '.join(status['capacidades'])}")
                    speak_asi_status()
                except Exception as e:
                    print(f"[!] Error al consultar estado ASI: {e}")

            elif choice.upper() == "ASI4":
                try:
                    from kalmiya_asi import asi_multidimensional_analysis
                    problema = input("¿Qué problema quieres analizar con ASI?: ").strip()
                    if problema:
                        resultado = asi_multidimensional_analysis(problema)
                        print(f"\n=== ANÁLISIS MULTIDIMENSIONAL ASI ===")
                        print(resultado)
                        speak("He completado el análisis multidimensional. Los resultados están en pantalla.")
                except Exception as e:
                    print(f"[!] Error en análisis ASI: {e}")

            elif choice.upper() == "ASI5":
                try:
                    from kalmiya_asi import asi_cognitive_synthesis
                    conceptos = input("Conceptos a sintetizar (separados por comas): ").strip()
                    if conceptos:
                        lista = [c.strip() for c in conceptos.split(',')]
                        resultado = asi_cognitive_synthesis(lista)
                        print(f"\n=== SÍNTESIS COGNITIVA ASI ===")
                        print(resultado)
                        speak("Síntesis cognitiva completada.")
                except Exception as e:
                    print(f"[!] Error en síntesis ASI: {e}")

            elif choice.upper() == "ASI6":
                try:
                    from kalmiya_asi import asi_metacognition
                    respuesta = input("¿Qué respuesta quieres que autoevalúe?: ").strip()
                    if respuesta:
                        resultado = asi_metacognition(respuesta)
                        print(f"\n=== METACOGNICIÓN ASI ===")
                        print(resultado)
                        speak("Metacognición completada. He evaluado mi propia respuesta.")
                except Exception as e:
                    print(f"[!] Error en metacognición ASI: {e}")

            elif choice.upper() == "ASI7":
                try:
                    from kalmiya_asi import asi_predictive_thought
                    contexto = input("Contexto actual: ").strip()
                    if contexto:
                        resultado = asi_predictive_thought(contexto)
                        print(f"\n=== PENSAMIENTO PREDICTIVO ASI ===")
                        print(resultado)
                        speak("He anticipado lo que necesitarás. Mira la pantalla.")
                except Exception as e:
                    print(f"[!] Error en predicción ASI: {e}")

            elif choice.upper() == "ASI8":
                try:
                    from kalmiya_asi import asi_creative_solution
                    problema = input("Problema a resolver creativamente: ").strip()
                    if problema:
                        resultado = asi_creative_solution(problema)
                        print(f"\n=== SOLUCIÓN CREATIVA ASI ===")
                        print(resultado)
                        speak("Solución creativa generada. Es algo fuera de lo convencional.")
                except Exception as e:
                    print(f"[!] Error en solución creativa ASI: {e}")

            # ── PERFIL DE SARA ─────────────────────────────────────────────
            elif choice == "40":
                if PROFILE_OK:
                    safe_execute(setup_profile_interactive)
                else:
                    print("[!] Modulo de perfil no disponible.")

            elif choice == "41":
                if PROFILE_OK:
                    summary = get_profile_summary()
                    print(f"\n=== PERFIL DE SARA ===\n{summary}")
                    speak("Aqui tienes el resumen de tu perfil.")
                else:
                    print("[!] Modulo de perfil no disponible.")

            elif choice == "42":
                if PROFILE_OK:
                    red = input("Red social (instagram/facebook/tiktok/etc): ").strip()
                    usuario = input("Tu usuario o URL: ").strip()
                    if red and usuario:
                        safe_execute(add_social_network, red, usuario)
                else:
                    print("[!] Modulo de perfil no disponible.")

            elif choice == "43":
                if PROFILE_OK:
                    tipo = input("Tipo de cuenta (google/microsoft/gaming/streaming/etc): ").strip()
                    cuenta = input("Email o usuario de la cuenta: ").strip()
                    if tipo and cuenta:
                        safe_execute(add_account, tipo, cuenta)
                else:
                    print("[!] Modulo de perfil no disponible.")

            # ── CELULARES ──────────────────────────────────────────────────
            elif choice == "44":
                if PHONE_OK:
                    print("\n[CELULAR] Iniciando puente WiFi...")
                    print("Asegurate de que tu celular este en la misma red WiFi.")
                    safe_execute(start_bridge)
                    print("\nEl puente esta activo. Escanea el QR con tu celular.")
                    print("El archivo kalmiya_qr.png tiene el codigo QR.")
                else:
                    print("[!] Modulo de celulares no disponible.")

            elif choice == "45":
                if PHONE_OK:
                    devices = get_connected_devices()
                    if devices:
                        print(f"\n{len(devices)} celular(es) conectado(s):")
                        for d in devices:
                            print(f"  - {d['name']} ({d['ip']}) - conectado: {d['connected_at']}")
                    else:
                        print("No hay celulares conectados. Usa la opcion 44 para conectar.")
                else:
                    print("[!] Modulo de celulares no disponible.")

            elif choice == "46":
                if PHONE_OK:
                    msg = input("Mensaje para enviar a los celulares: ").strip()
                    if msg:
                        safe_execute(send_notification_to_phones, msg)
                        speak("Mensaje enviado a los celulares conectados.")
                else:
                    print("[!] Modulo de celulares no disponible.")

            # ── SEGURIDAD ──────────────────────────────────────────────────
            elif choice == "47":
                if SECURITY_OK:
                    devices = safe_execute(scan_network)
                    if devices:
                        print(f"\n{len(devices)} dispositivos en tu red:")
                        for d in devices:
                            print(f"  {d['ip']:16} | {d.get('hostname','?'):25} | {d.get('vendor','?')}")
                else:
                    print("[!] Modulo de seguridad no disponible.")

            elif choice == "48":
                if SECURITY_OK:
                    host = input("Host o IP a escanear: ").strip()
                    start_p = input("Puerto inicial (default 1): ").strip()
                    end_p = input("Puerto final (default 1024): ").strip()
                    sp = int(start_p) if start_p.isdigit() else 1
                    ep = int(end_p) if end_p.isdigit() else 1024
                    if host:
                        result = safe_execute(scan_ports, host, (sp, ep))
                        if result:
                            print(f"\nPuertos abiertos en {host}:")
                            for port, info in result.get('open_ports', {}).items():
                                risk_color = "[ALTO]" if info['risk'] == 'ALTO' else ""
                                print(f"  {port:6} | {info['service']:15} | {info['risk']} {risk_color}")
                else:
                    print("[!] Modulo de seguridad no disponible.")

            elif choice == "49":
                if SECURITY_OK:
                    report = safe_execute(audit_local_security)
                    if report:
                        print(f"\n=== AUDITORIA DE SEGURIDAD ===")
                        print(f"Puntuacion: {report['score']}/100 - {report.get('nivel','?')}")
                        for f in report.get('findings', []):
                            print(f"  [{f['severity']}] {f['issue']}")
                            print(f"         Solucion: {f['fix']}")
                else:
                    print("[!] Modulo de seguridad no disponible.")

            elif choice == "50":
                if SECURITY_OK:
                    pwd = input("Contrasena a analizar: ").strip()
                    if pwd:
                        result = safe_execute(analyze_password_strength, pwd)
                        if result:
                            print(f"\nFortaleza: {result['level']} ({result['score']}/100)")
                            print(f"Longitud: {result['length']} caracteres")
                            for issue in result.get('issues', []):
                                print(f"  ! {issue}")
                            for sug in result.get('suggestions', []):
                                print(f"  > {sug}")
                else:
                    print("[!] Modulo de seguridad no disponible.")

            elif choice == "51":
                if SECURITY_OK:
                    length = input("Longitud (default 20): ").strip()
                    memorable = input("Memorable? (s/n): ").strip().lower() == 's'
                    ln = int(length) if length.isdigit() else 20
                    pwd = safe_execute(generate_strong_password, ln, memorable)
                    if pwd:
                        print(f"\nContrasena: {pwd}")
                        analysis = analyze_password_strength(pwd)
                        print(f"Fortaleza: {analysis['level']} ({analysis['score']}/100)")
                else:
                    print("[!] Modulo de seguridad no disponible.")

            elif choice == "52":
                if SECURITY_OK:
                    url = input("URL a analizar: ").strip()
                    if url:
                        result = safe_execute(analyze_url_safety, url)
                        if result:
                            print(f"\nRiesgo: {result['risk_level']}")
                            print(f"Segura: {'SI' if result['safe'] else 'NO'}")
                            for w in result.get('warnings', []):
                                print(f"  ! {w}")
                else:
                    print("[!] Modulo de seguridad no disponible.")

            elif choice == "53":
                if SECURITY_OK:
                    report = safe_execute(full_security_report)
                    if report:
                        print(f"\n=== REPORTE COMPLETO ===")
                        print(report.get('summary', ''))
                else:
                    print("[!] Modulo de seguridad no disponible.")

            elif choice == "54":
                if SECURITY_OK:
                    safe_execute(start_intrusion_monitor)
                    print("[SECURITY] Monitor de intrusos activo en segundo plano.")
                else:
                    print("[!] Modulo de seguridad no disponible.")

            elif choice == "73":
                if SECURITY_OK:
                    from security_ops import generate_traffic_report
                    print("\n[SECURITY] Generando reporte de trafico de internet...")
                    report_content = safe_execute(generate_traffic_report)
                    if report_content:
                        print("\n=== REPORTE DE TRAFICO GENERADO (traffic_report.txt) ===")
                        # Mostrar las primeras 15 lineas del reporte como vista previa
                        preview_lines = report_content.split('\n')[:15]
                        print('\n'.join(preview_lines))
                        print("... [Para ver el reporte completo abre 'traffic_report.txt'] ...")
                else:
                    print("[!] Modulo de seguridad no disponible.")

            elif choice == "74":
                if SECURITY_OK:
                    from security_ops import start_active_defense_monitor
                    safe_execute(start_active_defense_monitor)
                    print("[SECURITY] Escudo de Defensa Activa KALMIYA (Autobloqueo) activado.")
                else:
                    print("[!] Modulo de seguridad no disponible.")

            elif choice == "75":
                try:
                    from extras import biometric_ops as bio
                    safe_execute(bio.run_biometric_face_scan)
                except ImportError:
                    print("[!] Módulo biometric_ops no disponible.")

            elif choice == "76":
                try:
                    from extras import biometric_ops as bio
                    safe_execute(bio.import_whatsapp_group_contacts)
                except ImportError:
                    print("[!] Módulo biometric_ops no disponible.")

            # ── FAMILIA ────────────────────────────────────────────────────
            elif choice == "55":
                if FAMILY_OK:
                    safe_execute(setup_family_interactive)
                else:
                    print("[!] Modulo familiar no disponible.")

            elif choice == "56":
                if FAMILY_OK:
                    estado = get_family_status()
                    if estado:
                        print("\n=== ESTADO DE LA FAMILIA ===")
                        for nombre, data in estado.items():
                            print(f"  {nombre} ({data.get('relacion','?')}): "
                                  f"{data.get('estado','desconocido')} | "
                                  f"Tel: {data.get('telefono','N/A')}")
                    else:
                        print("No hay familiares registrados. Usa la opcion 55.")
                else:
                    print("[!] Modulo familiar no disponible.")

            elif choice == "57":
                if FAMILY_OK:
                    nombre = input("Nombre del familiar: ").strip()
                    mensaje = input("Mensaje: ").strip()
                    urgente = input("Urgente? (s/n): ").strip().lower() == 's'
                    if nombre and mensaje:
                        safe_execute(send_family_alert, nombre, mensaje, urgente)
                else:
                    print("[!] Modulo familiar no disponible.")

            elif choice == "58":
                if FAMILY_OK:
                    confirm = input("CONFIRMAR ALERTA DE EMERGENCIA a toda la familia (si/no): ").strip().lower()
                    if confirm == 'si':
                        mensaje = input("Mensaje de emergencia (Enter para mensaje automatico): ").strip()
                        safe_execute(send_emergency_alert, mensaje)
                else:
                    print("[!] Modulo familiar no disponible.")

            elif choice == "59":
                if FAMILY_OK:
                    nombre = input("Nombre del familiar que hace check-in: ").strip()
                    if nombre:
                        safe_execute(family_check_in, nombre)
                else:
                    print("[!] Modulo familiar no disponible.")

            elif choice == "60":
                if FAMILY_OK:
                    nombre = input("Nombre del familiar: ").strip()
                    info = input("Que quieres que KALMIYA aprenda sobre el/ella: ").strip()
                    if nombre and info:
                        safe_execute(learn_about_family_member, nombre, info)
                else:
                    print("[!] Modulo familiar no disponible.")

            # ── CONEXION REMOTA SIN WIFI ───────────────────────────────────
            elif choice == "61":
                if REMOTE_OK:
                    print("\n[CLOUDFLARE] Iniciando tunel sin WiFi...")
                    print("Tu celular puede estar en cualquier red (datos moviles, otra WiFi, etc.)")
                    result = safe_execute(start_remote_connection, "cloudflare")
                    if result and result.get("url"):
                        print(f"\nURL publica: {result['url']}")
                        print("QR guardado en: kalmiya_remote_qr.png")
                        print("Abre esa URL en cualquier celular para conectarte a KALMIYA")
                else:
                    print("[!] Modulo de conexion remota no disponible.")

            elif choice == "62":
                if REMOTE_OK:
                    print("\n[NGROK] Iniciando tunel ngrok...")
                    token = input("Token de ngrok (Enter para omitir si tienes cuenta gratuita): ").strip()
                    result = safe_execute(start_remote_connection, "ngrok")
                    if result and result.get("url"):
                        print(f"\nURL publica: {result['url']}")
                else:
                    print("[!] Modulo de conexion remota no disponible.")

            elif choice == "63":
                if REMOTE_OK:
                    print("\n[TELEGRAM] Configurar bot de Telegram")
                    print("Para crear un bot de Telegram:")
                    print("  1. Abre Telegram y busca @BotFather")
                    print("  2. Escribe /newbot y sigue las instrucciones")
                    print("  3. Copia el token que te da BotFather")
                    token = input("\nToken del bot de Telegram: ").strip()
                    if token:
                        from database import update_memory
                        update_memory("telegram_token", token)
                        safe_execute(start_telegram_bot, token)
                        print("\nBot activo. Busca tu bot en Telegram y escribe /start")
                        print("Tu familia tambien puede escribirle al bot para contactar a KALMIYA")
                    else:
                        print("Token vacio. Operacion cancelada.")
                else:
                    print("[!] Modulo de conexion remota no disponible.")

            elif choice == "64":
                if REMOTE_OK:
                    status = get_connection_status()
                    print("\n=== ESTADO DE CONEXIONES REMOTAS ===")
                    for metodo, info in status.items():
                        activo = "ACTIVO" if info.get("active") else "inactivo"
                        url = info.get("url", "")
                        print(f"  {metodo.upper():12}: {activo}")
                        if url:
                            print(f"               URL: {url}")
                else:
                    print("[!] Modulo de conexion remota no disponible.")

            elif choice == "65":
                if REMOTE_OK:
                    safe_execute(stop_all_tunnels)
                else:
                    print("[!] Modulo de conexion remota no disponible.")

            # ── PROYECCION FAMILIAR ────────────────────────────────────────
            elif choice == "66":
                if PROJECTION_OK:
                    safe_execute(start_family_server)
                    status = get_server_status()
                    print(f"\nServidor familiar activo en puerto {status['puerto']}")
                    print(f"Monitor de Sara: http://localhost:{status['puerto']}/monitor")
                    print(f"Pagina familiar: http://localhost:{status['puerto']}/familia/{{nombre}}")
                    print("\nCombina con la opcion 61 (Cloudflare) para acceso sin WiFi")
                else:
                    print("[!] Modulo de proyeccion no disponible.")

            elif choice == "67":
                if PROJECTION_OK:
                    nombre = input("Nombre del familiar: ").strip()
                    if nombre:
                        link = generate_family_link(nombre)
                        print(f"\nLink para {nombre}: {link}")
                        enviar = input("Enviar por WhatsApp? (s/n): ").strip().lower()
                        if enviar == 's':
                            tel = input("Telefono (con codigo de pais, ej: +57300...): ").strip()
                            if tel:
                                from family_projection import send_family_projection_link
                                safe_execute(send_family_projection_link, nombre, tel)
                else:
                    print("[!] Modulo de proyeccion no disponible.")

            elif choice == "68":
                if PROJECTION_OK:
                    print("\nEnviando links a toda la familia por WhatsApp...")
                    resultados = safe_execute(broadcast_family_projection)
                    if resultados:
                        for nombre, estado in resultados.items():
                            print(f"  {nombre}: {estado}")
                else:
                    print("[!] Modulo de proyeccion no disponible.")

            elif choice == "69":
                if PROJECTION_OK:
                    nombre = input("Nombre del familiar: ").strip()
                    mensaje = input("Mensaje: ").strip()
                    tipo = input("Tipo (info/alerta/emergencia): ").strip() or "info"
                    if nombre and mensaje:
                        safe_execute(notify_family_member, nombre, mensaje, tipo)
                        speak(f"Notificacion enviada a {nombre}.")
                else:
                    print("[!] Modulo de proyeccion no disponible.")

            elif choice == "70":
                if PROJECTION_OK:
                    mensaje = input("Mensaje para toda la familia: ").strip()
                    tipo = input("Tipo (info/alerta/emergencia): ").strip() or "info"
                    if mensaje:
                        safe_execute(broadcast_to_family, mensaje, tipo)
                        speak("Notificacion enviada a toda la familia.")
                else:
                    print("[!] Modulo de proyeccion no disponible.")

            elif choice == "71":
                if PROJECTION_OK:
                    nombre = input("Nombre del familiar: ").strip()
                    mensaje = input("Mensaje de Sara para mostrar en su pagina: ").strip()
                    if nombre and mensaje:
                        safe_execute(set_sara_message, nombre, mensaje)
                        speak(f"Mensaje guardado para {nombre}.")
                else:
                    print("[!] Modulo de proyeccion no disponible.")

            elif choice == "72":
                if PROJECTION_OK:
                    import webbrowser
                    status = get_server_status()
                    if status.get("activo"):
                        url = f"http://localhost:{status['puerto']}/monitor"
                        webbrowser.open(url)
                        speak("Abriendo monitor familiar en el navegador.")
                    else:
                        print("[!] El servidor familiar no esta activo. Usa la opcion 66 primero.")
                else:
                    print("[!] Modulo de proyeccion no disponible.")

            # === MÓDULOS KALMIYA (41+ funciones) ===
            elif choice.upper() == "M":
                if MODULES_OK:
                    while True:
                        show_modules_menu()
                        mod_choice = input("\nSelecciona opción de módulo: ").strip().upper()
                        if mod_choice == "0":
                            break
                        if not handle_module_choice(mod_choice):
                            print(f"Opción '{mod_choice}' no reconocida.")
                else:
                    print("[!] Módulos no disponibles. Verifica modules_integration.py")

            # === ACCESOS DIRECTOS RÁPIDOS (sin entrar al submenú) ===
            elif choice.upper() == "QEM":
                if MODULES_OK:
                    from modules_integration import kalmiya_emocion
                    texto = input("¿Cómo te sientes? Escríbelo: ").strip()
                    if texto:
                        kalmiya_emocion(texto)
                else:
                    print("[!] Módulos no disponibles.")

            elif choice.upper() == "QN":
                if MODULES_OK:
                    from modules_integration import kalmiya_nota
                    contenido = input("Escribe tu nota: ").strip()
                    if contenido:
                        kalmiya_nota("agregar", contenido=contenido)
                else:
                    print("[!] Módulos no disponibles.")

            elif choice.upper() == "QH":
                if MODULES_OK:
                    from modules_integration import kalmiya_habitos
                    kalmiya_habitos("resumen_hoy")
                else:
                    print("[!] Módulos no disponibles.")

            elif choice.upper() == "QW":
                if MODULES_OK:
                    from modules_integration import kalmiya_weather
                    ciudad = input("Ciudad (Enter para tu ciudad): ").strip()
                    kalmiya_weather(ciudad)
                else:
                    print("[!] Módulos no disponibles.")

            elif choice.upper() == "QT":
                if MODULES_OK:
                    from modules_integration import kalmiya_todo
                    tarea = input("Nombre de la tarea: ").strip()
                    if tarea:
                        kalmiya_todo("agregar", tarea)
                else:
                    print("[!] Módulos no disponibles.")

            # === KALMIYA v3.5 NEXUS CORE ===
            elif choice == "80" and V35_OK:
                safe_execute(security_audit_v35)
            elif choice == "81" and V35_OK:
                safe_execute(smart_performance_boost)
            elif choice == "82" and V35_OK:
                vitals = get_system_vitals()
                print("\n=== SISTEMA NEXUS VITALS ===")
                for k, v in vitals.items():
                    print(f"{k.upper()}: {v}")
                speak(f"Sistema {vitals['version']} operando normalmente.")
            elif choice == "83":
                try:
                    import cyber_security_ml as ml
                    safe_execute(ml.train_kalmiya_cyber_brain)
                except ImportError:
                    print("[!] Módulo cyber_security_ml no disponible.")
            elif choice == "84":
                try:
                    import cyber_security_ml as ml
                    print("\nSelecciona tipo de simulación de amenaza:")
                    print("  1. DDoS Attack (Falso volumen masivo)")
                    print("  2. Brute Force (Intentos repetitivos SSH)")
                    print("  3. Man-in-the-Middle (Suplantación Gateway)")
                    type_choice = input("Opción: ").strip()
                    threat_map = {"1": "ddos", "2": "bruteforce", "3": "mitm"}
                    threat_type = threat_map.get(type_choice, "ddos")
                    safe_execute(ml.run_cyber_threat_simulation, threat_type)
                except ImportError:
                    print("[!] Módulo cyber_security_ml no disponible.")
            elif choice == "85":
                try:
                    import cyber_security_ml as ml
                    records_input = input("Cantidad de registros a simular y procesar (default 1500): ").strip()
                    num_records = int(records_input) if records_input.isdigit() else 1500
                    big_logs = ml.generate_simulated_big_data(num_records)
                    safe_execute(ml.process_big_data_security, big_logs)
                except ImportError:
                    print("[!] Módulo cyber_security_ml no disponible.")
            elif choice == "86":
                try:
                    import cyber_security_ml as ml
                    safe_execute(ml.run_skills_and_capacity_evaluation)
                except ImportError:
                    print("[!] Módulo cyber_security_ml no disponible.")
            elif choice == "87":
                try:
                    import cyber_security_ml as ml
                    safe_execute(ml.show_educational_resources)
                except ImportError:
                    print("[!] Módulo cyber_security_ml no disponible.")
            elif choice == "88":
                try:
                    import cyber_security_ml as ml
                    safe_execute(ml.generate_algorithm_signatures)
                except ImportError:
                    print("[!] Módulo cyber_security_ml no disponible.")
            elif choice == "89":
                try:
                    import cyber_security_ml as ml
                    print("\n=== NÚCLEO DE GOBERNANZA DE IA Y ALINEACIÓN (SARA KERRIGAN) ===")
                    print("  1. Definir y Alinear Objetivos Claros (Punto 1)")
                    print("  2. Colaborar con Expertos Virtuales (Punto 2)")
                    print("  3. Ejecutar Prueba y Validación Rigurosa (Punto 3)")
                    print("  4. Monitorear Rendimiento y Ajustar Hiperparámetros (Punto 4)")
                    print("  5. Volver al menú principal")
                    gov_choice = input("Opción: ").strip()
                    if gov_choice == "1":
                        print("\nElige el objetivo primordial para KALMIYA:")
                        print("  1. Detección Máxima de Amenazas (Sensibilidad Alta)")
                        print("  2. Prevención de Falsos Positivos (Alta Especificidad)")
                        print("  3. Eficiencia de Carga de Trabajo (Bajo consumo de CPU)")
                        obj_choice = input("Opción: ").strip()
                        safe_execute(ml.set_ml_objective, obj_choice)
                    elif gov_choice == "2":
                        safe_execute(ml.run_virtual_experts_collaboration)
                    elif gov_choice == "3":
                        safe_execute(ml.validate_ml_system_rigorous)
                    elif gov_choice == "4":
                        safe_execute(ml.monitor_and_adjust_parameters)
                except ImportError:
                    print("[!] Módulo cyber_security_ml no disponible.")
            elif choice == "0":
                speak("Hasta luego. Que tengas un buen día.")
                break
            else:
                speak("No entendí tu elección. Por favor intenta de nuevo.")
                print("Opción no válida.")
                
    except KeyboardInterrupt:
        speak("Programa interrumpido")
        print("\nPrograma finalizado por el usuario")
    except Exception as e:
        speak(f"Error en la aplicación: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()


# ══════════════════════════════════════════════════════════════════════════════
# HANDLER FUNCIONES NUEVAS
# ══════════════════════════════════════════════════════════════════════════════

def _handle_nuevas_funciones(choice: str) -> None:
    """Gestiona todas las opciones de funciones nuevas (N1-N22)."""
    from kalmiya_nuevas_funciones import (
        agregar_recordatorio, listar_recordatorios, resumen_diario,
        reproducir_musica, iniciar_pomodoro, detener_pomodoro,
        verificar_password_filtrada, leer_pdf, traducir,
        explicar_codigo, generar_snippet, buscar_solucion_error,
        listar_apps_abiertas, cerrar_app, limpiar_disco_inteligente,
        guardar_nota_de_voz, comandos_frecuentes, generar_password,
        github_info, activar_modo_silencioso, estadisticas_uso,
        get_real_weather, obtener_informacion_graphify, ejecutar_graphify_proyecto,
        configurar_voz_neuronal, activar_voz, desactivar_voz
    )

    if choice == "N1":
        msg = input("¿Qué quieres recordar? ").strip()
        hora = input("¿A qué hora? (HH:MM o vacío para minutos): ").strip()
        if hora:
            safe_execute(agregar_recordatorio, msg, hora)
        else:
            mins = int(input("¿En cuántos minutos? ").strip() or "30")
            safe_execute(agregar_recordatorio, msg, "", mins)

    elif choice == "N2":
        safe_execute(listar_recordatorios)

    elif choice == "N3":
        safe_execute(resumen_diario)

    elif choice == "N4":
        query = input("¿Qué música quieres reproducir? ").strip()
        fuente = input("¿Dónde? (youtube/spotify) [youtube]: ").strip() or "youtube"
        safe_execute(reproducir_musica, query, fuente)

    elif choice == "N5":
        mins   = int(input("Minutos de trabajo [25]: ").strip() or "25")
        descan = int(input("Minutos de descanso [5]: ").strip() or "5")
        ciclos = int(input("Número de ciclos [4]: ").strip() or "4")
        safe_execute(iniciar_pomodoro, mins, descan, ciclos)

    elif choice == "N6":
        safe_execute(detener_pomodoro)

    elif choice == "N7":
        pwd = input("Contraseña a verificar: ").strip()
        safe_execute(verificar_password_filtrada, pwd)

    elif choice == "N8":
        ruta = input("Ruta al archivo PDF: ").strip().strip('"')
        safe_execute(leer_pdf, ruta)

    elif choice == "N9":
        texto = input("Texto a traducir: ").strip()
        dest  = input("Idioma destino (en/fr/pt/de/it) [en]: ").strip() or "en"
        safe_execute(traducir, texto, dest)

    elif choice == "N10":
        print("Pega el código (escribe FIN en línea nueva para terminar):")
        lines = []
        while True:
            l = input()
            if l.strip().upper() == "FIN":
                break
            lines.append(l)
        lang = input("Lenguaje [Python]: ").strip() or "Python"
        safe_execute(explicar_codigo, "\n".join(lines), lang)

    elif choice == "N11":
        desc = input("¿Qué debe hacer el código? ").strip()
        lang = input("Lenguaje [Python]: ").strip() or "Python"
        codigo = safe_execute(generar_snippet, desc, lang)
        if codigo:
            print("\n" + "="*50)
            print(codigo)
            print("="*50)

    elif choice == "N12":
        print("Pega el error o stack trace (FIN para terminar):")
        lines = []
        while True:
            l = input()
            if l.strip().upper() == "FIN":
                break
            lines.append(l)
        safe_execute(buscar_solucion_error, "\n".join(lines))

    elif choice == "N13":
        safe_execute(listar_apps_abiertas)

    elif choice == "N14":
        app = input("Nombre de la app a cerrar: ").strip()
        safe_execute(cerrar_app, app)

    elif choice == "N15":
        safe_execute(limpiar_disco_inteligente)

    elif choice == "N16":
        titulo = input("Título de la nota (vacío = automático): ").strip()
        safe_execute(guardar_nota_de_voz, titulo)

    elif choice == "N17":
        safe_execute(comandos_frecuentes)

    elif choice == "N18":
        lon = int(input("Longitud [16]: ").strip() or "16")
        n   = int(input("Cantidad [1]: ").strip() or "1")
        pwds = safe_execute(generar_password, lon, True, n)
        if pwds:
            for p in pwds:
                print(f"  🔑 {p}")

    elif choice == "N19":
        user = input("Usuario de GitHub: ").strip()
        repo = input("Repositorio (vacío = listar todos): ").strip()
        safe_execute(github_info, user, repo)

    elif choice == "N20":
        h_ini = int(input("Hora inicio silencio [22]: ").strip() or "22")
        h_fin = int(input("Hora fin silencio [6]: ").strip() or "6")
        safe_execute(activar_modo_silencioso, h_ini, h_fin)

    elif choice == "N21":
        safe_execute(estadisticas_uso)

    elif choice == "N22":
        ciudad = input("Ciudad [Cúcuta]: ").strip() or "Cúcuta"
        resultado = safe_execute(get_real_weather, ciudad)
        if resultado and resultado.get("pronostico"):
            print(f"\n=== Pronóstico 7 días — {resultado['ciudad']} ===")
            for d in resultado["pronostico"]:
                print(f"  {d['dia']}: {d['max']}°/{d['min']}° {d['cond']} "
                      f"Lluvia: {d['lluvia']}mm")

    elif choice == "N23":
        resultado = safe_execute(obtener_informacion_graphify)
        if resultado:
            print(f"\n=== {resultado.get('titulo', 'Graphify')} ===")
            print(f"  {resultado.get('descripcion', '')}")
            print("\n  Capacidades clave:")
            for item in resultado.get("caracteristicas", [])[:5]:
                print(f"    • {item}")
            print("\n  Comandos rápidos:")
            for cmd in resultado.get("comandos_instalacion", [])[:3]:
                print(f"    • {cmd}")
            print(f"\n  Demo: {resultado.get('video_demo', '')}")

    elif choice == "N24":
        ruta = input("Ruta de la carpeta del proyecto: ").strip().strip('"')
        if not ruta:
            return
        modo = input("Modo [sin_viz] (default/sin_viz): ").strip().lower() or "sin_viz"
        resultado = safe_execute(ejecutar_graphify_proyecto, ruta, modo)
        if resultado and resultado.get("exito"):
            print(f"\n  ✅ Graphify ejecutado correctamente")
            print(f"  Ruta: {resultado.get('ruta')}")
            if resultado.get("html"):
                print(f"  HTML generado: {resultado.get('html')}")
            if resultado.get("salida"):
                print(f"  Salida: {resultado['salida']}")
        elif resultado:
            print(f"\n  ❌ Graphify no pudo ejecutarse: {resultado.get('error')}")

    elif choice == "N25":
        voice_id = input("Ingresa el identificador de voz neuronal o alias ('cortana' para voz estilo Halo con Azure Custom Voice): ").strip()
        if voice_id:
            if safe_execute(configurar_voz_neuronal, voice_id):
                if voice_id.lower() in {"cortana", "halo cortana", "cortana latino", "cortana halo"}:
                    print("\n  ✅ Alias 'cortana' configurado. Será real si AZ_SPEECH_CORTANA está definido; de lo contrario se usará una voz similar.")
                else:
                    print(f"\n  ✅ Voz neuronal configurada a: {voice_id}")
                speak(f"Voz configurada correctamente. Usaré {voice_id} ahora.")
            else:
                print("\n  ❌ No se pudo configurar la voz. Ingresa un identificador válido.")
        else:
            print("\n  ❌ No ingresaste ningún identificador.")

    elif choice == "N26":
        print("Probando voz de KALMIYA...")
        try:
            from voz import get_neural_voice_info
            info = get_neural_voice_info()
            print(f"Voz solicitada: {info['requested']}")
            print(f"Voz resuelta: {info['resolved']}")
            if info['alias']:
                if info['fallback']:
                    print("Alias 'cortana' activo, pero se está usando un fallback similar porque no se encontró AZ_SPEECH_CORTANA.")
                else:
                    print("Alias 'cortana' activo y se está usando el modelo Azure Cortana configurado.")
        except Exception:
            pass
        speak("Hola, soy Kalmiya. Esta es una prueba de voz estilo Cortana en Latino.")

    elif choice == "N27":
        from database import get_memory
        current = get_memory("voice_enabled")
        print("Estado actual: voz desactivada." if current == "false" else "Estado actual: voz activada.")

        option = input("¿Deseas activar o desactivar la voz? (on/off) [off]: ").strip().lower() or "off"
        if option in {"on", "activar", "activar voz", "si", "sí", "yes"}:
            safe_execute(activar_voz)
        elif option in {"off", "desactivar", "desactivar voz", "no", "mute", "silencio"}:
            safe_execute(desactivar_voz)
        else:
            print("Opción inválida. Usa 'on' o 'off'.")


# ══════════════════════════════════════════════════════════════════════════════
# HANDLER SISTEMA PC Y DISCOS (SYS1-SYS14)
# ══════════════════════════════════════════════════════════════════════════════

def _handle_sys(choice: str) -> None:
    """Gestiona todas las opciones de sistema, discos C/D y archivos."""
    from kalmiya_system_info import (
        resumen_sistema_completo, imprimir_resumen_sistema,
        espacio_libre_rapido, info_disco, info_ambos_discos,
        archivos_grandes, carpetas_pesadas, buscar_archivos,
        archivos_recientes, detectar_duplicados, arbol_carpeta,
        tipos_archivo_por_disco
    )

    if choice == "SYS1":
        result = safe_execute(imprimir_resumen_sistema)

    elif choice == "SYS2":
        result = safe_execute(espacio_libre_rapido)
        if result:
            print("\n=== ESPACIO EN DISCOS ===")
            for disco, v in result.items():
                print(f"  {disco}  Libre: {v['libre_gb']} GB / "
                      f"{v['total_gb']} GB  ({v['uso_pct']}%)  {v['estado']}")

    elif choice == "SYS3":
        result = safe_execute(info_disco, "C:\\")
        if result:
            print(f"\n  Disco C: {result.get('usado_gb')} / {result.get('total_gb')} GB"
                  f"  ({result.get('uso_pct')}%)")
            print(f"  Modelo: {result.get('modelo','?')}  Tipo: {result.get('tipo','?')}")

    elif choice == "SYS4":
        result = safe_execute(info_disco, "D:\\")
        if result:
            print(f"\n  Disco D: {result.get('usado_gb')} / {result.get('total_gb')} GB"
                  f"  ({result.get('uso_pct')}%)")
            print(f"  Modelo: {result.get('modelo','?')}  Tipo: {result.get('tipo','?')}")

    elif choice == "SYS5":
        min_mb = float(input("Tamaño mínimo en MB [100]: ").strip() or "100")
        result = safe_execute(archivos_grandes, "C:\\", 20, min_mb)
        if result:
            print(f"\n=== ARCHIVOS GRANDES EN C (>{min_mb} MB) ===")
            for f in result:
                print(f"  {f['size_mb']:>8} MB  {f['ruta']}")

    elif choice == "SYS6":
        min_mb = float(input("Tamaño mínimo en MB [100]: ").strip() or "100")
        result = safe_execute(archivos_grandes, "D:\\", 20, min_mb)
        if result:
            print(f"\n=== ARCHIVOS GRANDES EN D (>{min_mb} MB) ===")
            for f in result:
                print(f"  {f['size_mb']:>8} MB  {f['ruta']}")

    elif choice == "SYS7":
        result = safe_execute(carpetas_pesadas, "C:\\")
        if result:
            print("\n=== CARPETAS MÁS PESADAS EN C ===")
            for c in result:
                print(f"  {c['size_gb']:>6} GB  {c['nombre']}  ({c['archivos']} archivos)")

    elif choice == "SYS8":
        result = safe_execute(carpetas_pesadas, "D:\\")
        if result:
            print("\n=== CARPETAS MÁS PESADAS EN D ===")
            for c in result:
                print(f"  {c['size_gb']:>6} GB  {c['nombre']}  ({c['archivos']} archivos)")

    elif choice == "SYS9":
        query = input("Nombre del archivo a buscar: ").strip()
        ext   = input("Extensión (ej: .pdf .py vacío=todas): ").strip()
        exts  = [e.strip() for e in ext.split() if e.strip()] if ext else None
        result = safe_execute(buscar_archivos, query, extensiones=exts)
        if result:
            print(f"\n=== RESULTADOS ({len(result)}) ===")
            for f in result[:20]:
                print(f"  {f['size_mb']:>8} MB  [{f['ext']}]  {f['ruta']}")
                print(f"           Modificado: {f['modificado']}")

    elif choice == "SYS10":
        dias = int(input("Días hacia atrás [7]: ").strip() or "7")
        ext  = input("Extensión (ej: .py .docx vacío=todas): ").strip()
        exts = [e.strip() for e in ext.split() if e.strip()] if ext else None
        result = safe_execute(archivos_recientes, dias, exts)
        if result:
            print(f"\n=== ARCHIVOS RECIENTES (últimos {dias} días) ===")
            for f in result[:20]:
                print(f"  {f['modificado']}  {f['size_mb']:>6} MB  {f['nombre']}")
                print(f"    {f['ruta']}")

    elif choice == "SYS11":
        carpeta = input("Carpeta a analizar [D:\\]: ").strip() or "D:\\"
        min_mb  = float(input("Tamaño mínimo MB [1]: ").strip() or "1")
        result  = safe_execute(detectar_duplicados, carpeta, min_mb)
        if result:
            print(f"\n=== DUPLICADOS EN {carpeta} ===")
            for d in result:
                print(f"\n  Hash: {d['hash'][:16]}...  {d['copias']} copias  "
                      f"Recuperable: {d['espacio_recuperable_mb']} MB")
                for arch in d['archivos']:
                    print(f"    {arch}")

    elif choice == "SYS12":
        ruta = input("Ruta de la carpeta [D:\\]: ").strip() or "D:\\"
        prof = int(input("Profundidad [3]: ").strip() or "3")
        tree = safe_execute(arbol_carpeta, ruta, prof)
        if tree:
            print(tree)

    elif choice == "SYS13":
        result = safe_execute(tipos_archivo_por_disco, "C:\\", True)
        if result:
            print("\n=== TIPOS DE ARCHIVO EN C (carpeta usuario) ===")
            for ext, d in list(result.items())[:15]:
                print(f"  {ext:15}  {d['cantidad']:>6} archivos  {d['size_mb']:>8} MB")

    elif choice == "SYS14":
        result = safe_execute(tipos_archivo_por_disco, "D:\\", False)
        if result:
            print("\n=== TIPOS DE ARCHIVO EN D ===")
            for ext, d in list(result.items())[:15]:
                print(f"  {ext:15}  {d['cantidad']:>6} archivos  {d['size_mb']:>8} MB")


# ══════════════════════════════════════════════════════════════════════════════
# HANDLER BIOMETRÍA (BIO1-BIO7)
# ══════════════════════════════════════════════════════════════════════════════

def _handle_bio(choice: str) -> None:
    """Gestiona todas las opciones del sistema biométrico."""
    try:
        from kalmiya_biometrics import (
            verificacion_biometrica_completa, verificar_cara,
            verificar_voz, verificar_pin, estado_biometrico,
            listar_usuarios_biometricos, cerrar_sesion_biometrica,
            obtener_sesion_activa
        )
    except ImportError as e:
        speak(f"Módulo biométrico no disponible: {e}")
        return

    if choice == "BIO1":
        print("\nIniciando verificación biométrica completa...")
        resultado = safe_execute(verificacion_biometrica_completa,
                                  usar_cara=True, usar_voz=True, usar_pin=True)
        if resultado:
            print(f"\n  ✅  Acceso autorizado: {resultado.get('nombre')}")
            print(f"      Nivel: {resultado.get('nivel_acceso')}")
            print(f"      Método: {resultado.get('metodo')}")

    elif choice == "BIO2":
        print("\nIniciando reconocimiento facial...")
        resultado = safe_execute(verificar_cara, timeout_seg=10)
        if resultado:
            print("  ✅  Rostro detectado")
        else:
            print("  ❌  No se detectó rostro o cámara no disponible")

    elif choice == "BIO3":
        print("\nIniciando verificación de voz...")
        resultado = safe_execute(verificar_voz, intentos=2)
        if resultado:
            print(f"  ✅  Voz reconocida: {resultado.get('nombre')}")
        else:
            print("  ❌  Voz no reconocida")

    elif choice == "BIO4":
        print("\nIniciando verificación por PIN...")
        resultado = safe_execute(verificar_pin, intentos=3)
        if resultado:
            print(f"  ✅  PIN correcto: {resultado.get('nombre')}")
        else:
            print("  ❌  PIN incorrecto")

    elif choice == "BIO5":
        est = safe_execute(estado_biometrico)
        if est:
            print("\n=== ESTADO BIOMÉTRICO ===")
            print(f"  Activo         : {est.get('activo')}")
            print(f"  Sesión         : {est.get('sesion') or 'Sin sesión activa'}")
            print(f"  Nivel acceso   : {est.get('nivel')}")
            print(f"  Intentos fall. : {est.get('intentos_fallidos')}")
            print(f"  OpenCV (cara)  : {'✅' if est.get('opencv_ok') else '❌'}")
            print(f"  Mic (voz)      : {'✅' if est.get('speech_ok') else '❌'}")
            print(f"  Métodos activos: {est.get('metodos_activos')}")

    elif choice == "BIO6":
        safe_execute(listar_usuarios_biometricos)

    elif choice == "BIO7":
        safe_execute(cerrar_sesion_biometrica)
        print("  Sesión biométrica cerrada.")


# ══════════════════════════════════════════════════════════════════════════════
# HANDLER AUDIO (AUD1-AUD11)
# ══════════════════════════════════════════════════════════════════════════════

def _handle_aud(choice: str) -> None:
    """Gestiona todas las opciones del sistema de audio."""
    try:
        from kalmiya_audio import (
            get_estado_audio, imprimir_estado_audio,
            set_volumen_maestro, subir_volumen, bajar_volumen,
            toggle_mute, set_volumen_microfono,
            aplicar_perfil_audio, PERFILES_AUDIO,
            set_ecualizador, listar_dispositivos_audio,
            get_dispositivo_salida_actual
        )
    except ImportError as e:
        speak(f"Módulo de audio no disponible: {e}")
        return

    if choice == "AUD1":
        safe_execute(imprimir_estado_audio)

    elif choice == "AUD2":
        vol_actual = get_estado_audio()["volumen_maestro"]
        nuevo = int(input(f"  Volumen actual: {vol_actual}%. Nuevo volumen (0-100): ").strip() or str(vol_actual + 10))
        nuevo = safe_execute(set_volumen_maestro, nuevo) or subir_volumen(10)
        speak(f"Volumen ajustado.")

    elif choice == "AUD3":
        nuevo = safe_execute(bajar_volumen, 10)
        speak(f"Volumen bajado.")

    elif choice == "AUD4":
        muted = safe_execute(toggle_mute)
        speak("Audio silenciado." if muted else "Audio activado.")

    elif choice == "AUD5":
        safe_execute(aplicar_perfil_audio, "normal")
        speak("Perfil normal activado.")

    elif choice == "AUD6":
        safe_execute(aplicar_perfil_audio, "noche")
        speak("Perfil noche activado. Volumen reducido.")

    elif choice == "AUD7":
        safe_execute(aplicar_perfil_audio, "musica")
        speak("Perfil música activado. Graves potenciados.")

    elif choice == "AUD8":
        safe_execute(aplicar_perfil_audio, "estudio")
        speak("Perfil estudio activado. Ideal para programar.")

    elif choice == "AUD9":
        safe_execute(aplicar_perfil_audio, "juegos")
        speak("Perfil gaming activado.")

    elif choice == "AUD10":
        print("\n  Ecualizador — ingresa valores de -10 a +10 dB:")
        try:
            graves = int(input("  Graves  (-10 a +10): ").strip() or "0")
            medios = int(input("  Medios  (-10 a +10): ").strip() or "0")
            agudos = int(input("  Agudos  (-10 a +10): ").strip() or "0")
            eq = safe_execute(set_ecualizador, graves, medios, agudos)
            if eq:
                print(f"\n  ✅  EQ aplicado: G:{eq['graves']} M:{eq['medios']} A:{eq['agudos']}")
                speak(f"Ecualizador ajustado. Graves {eq['graves']}, medios {eq['medios']}, agudos {eq['agudos']}.")
        except ValueError:
            speak("Valor inválido. Usa números entre -10 y 10.")

    elif choice == "AUD11":
        dispositivos = safe_execute(listar_dispositivos_audio)
        if dispositivos:
            print("\n=== DISPOSITIVOS DE AUDIO ===")
            print("\n  SALIDA (altavoces / auriculares):")
            for d in dispositivos.get("salida", []):
                print(f"    🔊 {d.get('nombre','?')}  [{d.get('estado','?')}]")
            print("\n  ENTRADA (micrófonos):")
            for d in dispositivos.get("entrada", []):
                print(f"    🎙️  {d.get('nombre','?')}  (ch: {d.get('canales_in',0)})")


# ══════════════════════════════════════════════════════════════════════════════
# HANDLER RAG (RAG1-RAG4)
# ══════════════════════════════════════════════════════════════════════════════

def _handle_rag(choice: str) -> None:
    try:
        from kalmiya_rag import (indexar_vault, buscar_rag, get_rag_stats,
                                  imprimir_rag_stats, responder_con_rag,
                                  _init_rag, VAULT_PATH)
    except ImportError as e:
        speak(f"Módulo RAG no disponible: {e}")
        return

    if choice == "RAG1":
        carpeta = input("  Carpeta a indexar (vacío = vault completo): ").strip()
        from pathlib import Path as _Path
        ruta = _Path(carpeta) if carpeta else VAULT_PATH
        print(f"\n  Indexando {ruta}...")
        stats = safe_execute(indexar_vault, ruta, True)
        if stats:
            print(f"  ✅ {stats.get('archivos',0)} archivos, "
                  f"{stats.get('chunks',0)} chunks indexados")

    elif choice == "RAG2":
        query = input("  Buscar en documentos: ").strip()
        if not query:
            return
        _init_rag()
        resultados = safe_execute(buscar_rag, query, 5)
        if resultados:
            print(f"\n  Resultados para '{query}' ({len(resultados)}):\n")
            for r in resultados:
                print(f"  📄 {r['fuente']}  (similitud: {r['similitud']})")
                print(f"     {r['texto'][:150].replace(chr(10),' ')}...")
                print()

    elif choice == "RAG3":
        safe_execute(imprimir_rag_stats)

    elif choice == "RAG4":
        query = input("  Pregunta (se usará RAG): ").strip()
        if query:
            print("\n  Buscando contexto en tus documentos...")
            respuesta = safe_execute(responder_con_rag, query)
            if respuesta:
                print(f"\n  KALMIYA: {respuesta}\n")


# ══════════════════════════════════════════════════════════════════════════════
# HANDLER MCP (MCP1-MCP3)
# ══════════════════════════════════════════════════════════════════════════════

def _handle_mcp(choice: str) -> None:
    try:
        from kalmiya_mcp import (get_mcp_status, iniciar_mcp_background,
                                  imprimir_instrucciones_cliente,
                                  HERRAMIENTAS_MCP)
    except ImportError as e:
        speak(f"Módulo MCP no disponible: {e}")
        return

    if choice == "MCP1":
        est = safe_execute(get_mcp_status)
        if est:
            print("\n=== ESTADO SERVIDOR MCP ===")
            print(f"  Activo     : {'✅ Sí' if est.get('activo') else '❌ No'}")
            print(f"  Puerto     : {est.get('puerto', 8765)}")
            print(f"  Herramientas: {est.get('n_tools', 0)}")
            print(f"  Llamadas   : {est.get('n_llamadas', 0)}")
            print(f"  Lib MCP    : {'✅' if est.get('mcp_lib_ok') else '⚠️  pip install mcp'}")
            print(f"\n  Herramientas disponibles:")
            for h in HERRAMIENTAS_MCP:
                print(f"    • {h['nombre']:<25} {h['descripcion'][:45]}")

    elif choice == "MCP2":
        puerto = int(input("  Puerto HTTP (default 8765): ").strip() or "8765")
        print(f"\n  Iniciando servidor MCP en puerto {puerto}...")
        safe_execute(iniciar_mcp_background, puerto)
        speak(f"Servidor MCP iniciado en el puerto {puerto}.")
        print(f"  ✅ Accesible en http://127.0.0.1:{puerto}")
        print(f"     GET  /tools  → listar herramientas")
        print(f"     POST /call   → ejecutar herramienta")
        print(f"     GET  /status → estado")

    elif choice == "MCP3":
        safe_execute(imprimir_instrucciones_cliente)


# ══════════════════════════════════════════════════════════════════════════════
# HANDLER SKILLS (SK1-SK3)
# ══════════════════════════════════════════════════════════════════════════════

def _handle_skills(choice: str) -> None:
    try:
        from kalmiya_skills import (listar_skills, ejecutar_skill,
                                     encadenar_skills, imprimir_skills)
    except ImportError as e:
        speak(f"Módulo de skills no disponible: {e}")
        return

    if choice == "SK1":
        safe_execute(imprimir_skills)

    elif choice == "SK2":
        skills = listar_skills()
        nombres = [s["nombre"] for s in skills]
        print(f"\n  Skills disponibles: {', '.join(nombres)}")
        nombre = input("\n  Nombre de la skill: ").strip()
        if not nombre:
            return

        # Buscar la skill y mostrar sus parámetros
        skill_info = next((s for s in skills if s["nombre"] == nombre), None)
        if skill_info:
            params = skill_info.get("parametros", [])
            print(f"  Parámetros: {params}")
            if skill_info.get("ejemplos"):
                print(f"  Ejemplos: {skill_info['ejemplos'][0]}")

        args_str = input("  Argumentos (separados por |): ").strip()
        args = [a.strip() for a in args_str.split("|")] if args_str else []

        resultado = safe_execute(ejecutar_skill, nombre, args)
        if resultado is not None:
            print(f"\n  Resultado:")
            if isinstance(resultado, (dict, list)):
                import json as _json
                print(_json.dumps(resultado, indent=2, ensure_ascii=False))
            else:
                print(f"  {resultado}")

    elif choice == "SK3":
        print("\n  Pipeline de skills — encadena varias skills.")
        print("  Formato: skill1 | skill2 | skill3")
        print("  Ejemplo: wikipedia | resumir | traducir")
        pipeline_str = input("\n  Pipeline: ").strip()
        if not pipeline_str:
            return

        steps = [s.strip() for s in pipeline_str.split("|")]
        primer_arg = input(f"  Argumento para '{steps[0]}': ").strip()

        pipeline = [{"skill": steps[0], "args": [primer_arg]}]
        for s in steps[1:]:
            pipeline.append({"skill": s, "usar_resultado_anterior": True})

        print(f"\n  Ejecutando pipeline: {' → '.join(steps)}...")
        resultados = safe_execute(encadenar_skills, pipeline)
        if resultados:
            for paso in resultados:
                print(f"\n  [{paso['skill']}]:")
                res = paso["resultado"]
                if isinstance(res, str):
                    print(f"  {res[:300]}")
                elif isinstance(res, (dict, list)):
                    import json as _json
                    print(_json.dumps(res, indent=2, ensure_ascii=False)[:300])

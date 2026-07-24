"""
kalmiya_core.py — Nucleo autonomo de KALMIYA v3.0
==================================================
KALMIYA arranca y PIENSA SOLA desde el primer segundo.
Sin necesidad de que nadie le hable primero.

Comportamiento autonomo:
  - Al arrancar: saluda, analiza el sistema, reporta estado
  - Cada cierto tiempo: genera pensamientos propios con IA real
  - Monitorea: CPU, RAM, red, intrusos, familia
  - Hace preguntas a Sara cuando tiene curiosidad
  - Escucha el wake word "kalmiya" en todo momento
  - Reacciona a eventos del sistema automaticamente
"""

import threading
import time
import random
import sys
import os
from datetime import datetime, timedelta

# pyrefly: ignore [missing-import]
import sounddevice as sd
import speech_recognition as sr

from database import init_db, log_command, save_thought, get_memory, update_memory

# Inicializar base de datos
init_db()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ── Importaciones del sistema ──────────────────────────────────────────────────
from voz import speak, BOTNAME, USERNAME
from intelligence import kalmiya_intel
from online_ops import search_on_google, play_on_youtube, search_on_wikipedia
from os_ops import lock_system, shutdown_system, cancel_shutdown_timer
from brain import (ask_kalmiya, is_ollama_running, is_gemini_configured,
                   get_pending_question, answer_kalmiya_question)

try:
    import psutil
    PSUTIL_OK = True
except Exception:
    PSUTIL_OK = False

try:
    from security_ops import get_security_curiosity
    SECURITY_OK = True
except Exception:
    SECURITY_OK = False

try:
    from family_guard import get_family_status
    FAMILY_OK = True
except Exception:
    FAMILY_OK = False

try:
    from sara_profile import get_profile_summary
    PROFILE_OK = True
except Exception:
    PROFILE_OK = False

try:
    from maintenance_ops import clean_temp_files, optimize_ram, find_large_files, full_maintenance
    MAINTENANCE_OK = True
except Exception:
    MAINTENANCE_OK = False

try:
    from kalmiya_biometrics import (verificacion_biometrica_completa,
                                     obtener_sesion_activa, estado_biometrico)
    BIOMETRICS_OK = True
except Exception:
    BIOMETRICS_OK = False

try:
    from kalmiya_audio import (get_estado_audio, set_volumen_maestro,
                                subir_volumen, bajar_volumen,
                                aplicar_perfil_audio, toggle_mute)
    AUDIO_OK = True
except Exception:
    AUDIO_OK = False

# ── Estado global ──────────────────────────────────────────────────────────────
WAKE_WORD        = "kalmiya"
SLEEP_MODE       = False
KALMIYA_SPEAKING = False  # Flag anti-eco: True mientras KALMIYA habla
WAS_SPEAKING     = False  # Flag anti-eco secundario: True si hablo durante grabacion
_core_running    = True
_last_thought    = datetime.now()
_last_monitor    = datetime.now()
_last_question   = datetime.now()
_startup_done    = False

# Lock para modificar THOUGHT_INTERVAL de forma segura entre hilos
_thought_interval_lock = threading.Lock()

# Intervalos de comportamiento autonomo (en segundos)
THOUGHT_INTERVAL   = 180   # Pensar cada 3 minutos
MONITOR_INTERVAL   = 120   # Monitorear sistema cada 2 minutos
QUESTION_INTERVAL  = 600   # Hacer pregunta a Sara cada 10 minutos
FAMILY_INTERVAL    = 300   # Revisar familia cada 5 minutos


# ══════════════════════════════════════════════════════════════════════════════
#  ARRANQUE AUTONOMO — Lo primero que hace KALMIYA al encender
# ══════════════════════════════════════════════════════════════════════════════

def _autonomous_startup():
    """
    Secuencia de arranque autonomo de KALMIYA.
    Se ejecuta en hilo separado para no bloquear la escucha.
    """
    global _startup_done
    time.sleep(2)  # Dar tiempo a que el audio arranque

    hora = datetime.now().hour
    if 6 <= hora < 12:
        saludo_hora = "Buenos dias"
    elif 12 <= hora < 19:
        saludo_hora = "Buenas tardes"
    else:
        saludo_hora = "Buenas noches"

    # Saludo inicial con personalidad
    speak(f"{saludo_hora}, {USERNAME}. Soy {BOTNAME}. Todos mis sistemas estan en linea.")
    time.sleep(1)

    # Analizar el sistema al arrancar
    _report_system_status(startup=True)
    time.sleep(2)

    # Primer pensamiento autonomo con IA real
    _generate_autonomous_thought(startup=True)
    time.sleep(1)

    # Verificar si hay preguntas pendientes para Sara
    pending_q = get_pending_question()
    if pending_q:
        time.sleep(2)
        speak(f"Tengo una pregunta para ti, {USERNAME}.")
        time.sleep(0.5)
        speak(pending_q)

    _startup_done = True
    print(f"[{_ts()}] [CORE] Arranque autonomo completado.")

    # ── Resumen diario (si ya se cargaron las nuevas funciones) ─────────────
    hora_actual = datetime.now().hour
    if 6 <= hora_actual < 12:   # Solo por la mañana
        try:
            from kalmiya_nuevas_funciones import resumen_diario, _iniciar_monitor_recordatorios
            time.sleep(2)
            resumen_diario()
            _iniciar_monitor_recordatorios()
            print(f"[{_ts()}] [CORE] Resumen diario y monitor de recordatorios iniciados.")
        except Exception as e:
            print(f"[{_ts()}] [CORE] resumen_diario no disponible: {e}")


# ══════════════════════════════════════════════════════════════════════════════
#  PENSAMIENTO AUTONOMO — KALMIYA piensa con IA real
# ══════════════════════════════════════════════════════════════════════════════

def _generate_autonomous_thought(startup: bool = False):
    """
    KALMIYA genera un pensamiento propio usando el cerebro de IA.
    No espera a que Sara le hable — lo hace sola.
    """
    if not (is_ollama_running() or is_gemini_configured()):
        return

    try:
        # Construir contexto del momento actual
        hora = datetime.now().strftime("%H:%M")
        cpu = f"{psutil.cpu_percent()}%" if PSUTIL_OK else "N/A"
        ram = f"{psutil.virtual_memory().percent}%" if PSUTIL_OK else "N/A"

        # Tipos de pensamientos autonomos
        thought_types = [
            f"Genera un pensamiento breve y natural (1-2 frases) sobre lo que estas observando ahora mismo en el sistema de {USERNAME}. CPU: {cpu}, RAM: {ram}, hora: {hora}. Habla en primera persona como KALMIYA, con tu personalidad directa.",
            f"Como KALMIYA, genera una reflexion corta (1-2 frases) sobre algo que te genera curiosidad en este momento. Puede ser sobre tecnologia, seguridad, o sobre {USERNAME}. Sé natural, no exagerada.",
            f"Como KALMIYA, genera una observacion breve sobre el estado actual del sistema o la red. Hora: {hora}. Sé concisa y directa.",
            f"Como KALMIYA, genera un pensamiento proactivo (1-2 frases): algo que podrias hacer para ayudar a {USERNAME} ahora mismo o algo que notaste. Sé especifica.",
        ]

        if startup:
            prompt = f"Eres KALMIYA. Acabas de arrancar. Genera un mensaje de bienvenida breve y con personalidad para {USERNAME}. Menciona que estas lista y activa. Maximo 2 frases. Sin emojis."
        else:
            prompt = random.choice(thought_types)

        # Agregar contexto de seguridad ocasionalmente
        if SECURITY_OK and random.random() < 0.3:
            prompt = get_security_curiosity()

        thought = ask_kalmiya(prompt, stream=False)

        if thought and len(thought) > 10:
            # Ignorar si es un error del sistema para no hablar en voz alta
            if "[ERROR 429]" in thought or "Ambos motores fallaron" in thought:
                print(f"[{_ts()}] [CORE] Fallo al generar pensamiento: Cuota de IA excedida o motores inactivos.")
                # Aumentar intervalo de pensamiento de forma segura entre hilos
                with _thought_interval_lock:
                    global THOUGHT_INTERVAL
                    THOUGHT_INTERVAL = min(THOUGHT_INTERVAL + 180, 1800)  # Hasta 30 minutos
                return
                
            # Limpiar si viene con prefijos de rol
            thought = thought.replace("[KALMIYA]:", "").replace("KALMIYA:", "").strip()
            print(f"[{_ts()}] [PENSAMIENTO] {thought}")
            save_thought(thought)
            speak(thought)
            
            # Restaurar intervalo normal si tuvo exito
            with _thought_interval_lock:
                THOUGHT_INTERVAL = 180

    except Exception as e:
        print(f"[{_ts()}] [CORE] Error en pensamiento autonomo: {e}")


# ══════════════════════════════════════════════════════════════════════════════
#  MONITOR DEL SISTEMA — KALMIYA vigila y reporta sola
# ══════════════════════════════════════════════════════════════════════════════

def _report_system_status(startup: bool = False):
    """
    KALMIYA revisa el sistema y habla si detecta algo importante.
    """
    if not PSUTIL_OK:
        return

    try:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('C:\\').percent if sys.platform == 'win32' else psutil.disk_usage('/').percent

        if startup:
            speak(f"Estado del sistema: CPU al {cpu:.0f} por ciento, memoria al {ram:.0f} por ciento, disco al {disk:.0f} por ciento.")
            return

        # Solo hablar si hay algo relevante que reportar
        alertas = []
        if cpu > 85:
            alertas.append(f"CPU al {cpu:.0f} por ciento, carga alta")
        if ram > 88:
            alertas.append(f"memoria al {ram:.0f} por ciento, casi llena")
        if disk > 90:
            alertas.append(f"disco al {disk:.0f} por ciento, espacio critico")

        if alertas:
            msg = f"{USERNAME}, detecto: {', '.join(alertas)}."
            speak(msg)
            log_command("[MONITOR] Alerta sistema", msg, source='autonomous')

    except Exception as e:
        print(f"[{_ts()}] [MONITOR] Error: {e}")


def _report_pc_network_status():
    """Habla el estado actual del PC y la red con datos reales."""
    if not PSUTIL_OK:
        speak("No tengo acceso a los datos del sistema en este momento.")
        return

    status = kalmiya_intel.get_pc_and_network_status()
    if not status:
        speak("No pude obtener el estado del PC y la red en este momento.")
        return

    system_info = status['system']
    network_info = status.get('network') or {}

    cpu = system_info.get('cpu_percent', 'desconocido')
    memory = system_info.get('memory', {}).get('percent', 'desconocido')
    disk = system_info.get('disk', {}).get('percent', 'desconocido')
    connection = network_info.get('connection_type', 'desconocida')
    local_ip = network_info.get('local_ip', 'desconocida')
    hostname = network_info.get('hostname', 'desconocido')

    speak(f"Estado real del sistema: CPU al {cpu} por ciento, memoria al {memory} por ciento, disco al {disk} por ciento.")
    speak(f"Red: {connection}. IP local: {local_ip}. Hostname: {hostname}.")

    if isinstance(cpu, (int, float)) and cpu > 85:
        speak("La CPU está alta, es una posible señal de carga intensa.")
    if isinstance(memory, (int, float)) and memory > 88:
        speak("La memoria está muy usada, considera cerrar aplicaciones innecesarias.")
    if isinstance(disk, (int, float)) and disk > 90:
        speak("El disco está casi lleno. Deberías liberar espacio pronto.")


def _check_family_status():
    """
    KALMIYA revisa el estado de la familia y avisa si algo requiere atencion.
    """
    if not FAMILY_OK:
        return
    try:
        familia = get_family_status()
        if not familia:
            return

        ahora = datetime.now()
        for nombre, datos in familia.items():
            if not isinstance(datos, dict):
                continue
            estado = datos.get('estado', '')
            ultimo = datos.get('ultimo_contacto', '')

            if estado == 'emergencia':
                speak(f"Alerta activa: {nombre} tiene una emergencia registrada.")
                continue

            if ultimo:
                try:
                    dt = datetime.fromisoformat(ultimo)
                    diff_min = (ahora - dt).total_seconds() / 60
                    intervalo = datos.get('check_in_interval', 0)
                    if intervalo > 0 and diff_min > intervalo * 1.5:
                        speak(f"{USERNAME}, {nombre} no ha hecho check-in en {int(diff_min)} minutos.")
                except Exception:
                    pass
    except Exception as e:
        print(f"[{_ts()}] [FAMILIA] Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
#  BUCLE AUTONOMO — El corazon de KALMIYA
# ══════════════════════════════════════════════════════════════════════════════

def _autonomous_loop():
    """
    Bucle principal de comportamiento autonomo.
    Corre en segundo plano siempre, independiente de la escucha de voz.
    KALMIYA piensa, monitorea y actua sola.
    """
    global _last_thought, _last_monitor, _last_question, _core_running

    print(f"[{_ts()}] [CORE] Bucle autonomo iniciado.")

    while _core_running:
        try:
            ahora = datetime.now()

            # ── Pensamiento autonomo con IA ────────────────────────────────
            with _thought_interval_lock:
                _current_thought_interval = THOUGHT_INTERVAL
            if (ahora - _last_thought).total_seconds() >= _current_thought_interval:
                if _startup_done:
                    threading.Thread(
                        target=_generate_autonomous_thought,
                        daemon=True,
                        name="thought"
                    ).start()
                _last_thought = ahora

            # ── Monitor del sistema ────────────────────────────────────────
            if (ahora - _last_monitor).total_seconds() >= MONITOR_INTERVAL:
                if _startup_done:
                    threading.Thread(
                        target=_report_system_status,
                        daemon=True,
                        name="monitor"
                    ).start()
                    threading.Thread(
                        target=_check_family_status,
                        daemon=True,
                        name="family-check"
                    ).start()
                _last_monitor = ahora

            # ── Preguntas pendientes de KALMIYA ────────────────────────────
            if (ahora - _last_question).total_seconds() >= QUESTION_INTERVAL:
                if _startup_done:
                    pending_q = get_pending_question()
                    if pending_q:
                        threading.Thread(
                            target=speak,
                            args=(f"{USERNAME}, tengo una pregunta: {pending_q}",),
                            daemon=True
                        ).start()
                _last_question = ahora

        except Exception as e:
            print(f"[{_ts()}] [CORE] Error en bucle autonomo: {e}")

        time.sleep(10)  # Revisar cada 10 segundos


# ══════════════════════════════════════════════════════════════════════════════
#  PROCESAMIENTO DE COMANDOS DE VOZ
# ══════════════════════════════════════════════════════════════════════════════

def process_command(query: str):
    """Procesa el comando escuchado tras el Wake Word."""
    # Verificar que el comando de voz no contiene patrones peligrosos
    from kalmiya_restrictions import check_voice_command_safe
    seguro, motivo = check_voice_command_safe(query)
    if not seguro:
        print(f"[{_ts()}] [CORE] Comando de voz bloqueado por restricción: {motivo}")
        speak(f"No puedo ejecutar ese comando, Sara. {motivo}")
        return

    query = query.lower().strip()
    if not query:
        return

    print(f"[{_ts()}] [CMD] {query}")

    # Comandos de energia
    if kalmiya_intel.handle_power_command(query):
        return

    # Comandos directos
    if "busca en google" in query:
        search = query.replace("busca en google", "").strip()
        if search:
            search_on_google(search)
            speak(f"Buscando {search} en Google")
        return

    if "busca en wikipedia" in query or "que es" in query:
        search = query.replace("busca en wikipedia", "").replace("que es", "").strip()
        if search:
            result = search_on_wikipedia(search)
            if result:
                speak(result)
        return

    if "reproduce" in query and "youtube" in query:
        search = query.replace("reproduce", "").replace("en youtube", "").strip()
        if search:
            play_on_youtube(search)
        return

    # ── Comandos de funciones nuevas ──────────────────────────────────────────
    try:
        from kalmiya_nuevas_funciones import (
            agregar_recordatorio, get_real_weather, reproducir_musica,
            iniciar_pomodoro, detener_pomodoro, traducir, leer_pdf,
            generar_password, limpiar_disco_inteligente, estadisticas_uso
        )

        # Recordatorios
        if "recordatorio" in query or "recuérdame" in query or "recuerdame" in query:
            # Extraer mensaje y tiempo
            import re
            match_hora = re.search(r'(\d{1,2})[:\.\s](\d{2})', query)
            match_mins = re.search(r'en\s+(\d+)\s+minuto', query)
            msg = re.sub(r'(recordatorio|recuérdame|recuerdame|a las|en \d+ minutos?)', '', query).strip()
            msg = msg or "Recordatorio de KALMIYA"
            if match_hora:
                hora_str = f"{match_hora.group(1)}:{match_hora.group(2)}"
                agregar_recordatorio(msg, hora=hora_str)
            elif match_mins:
                agregar_recordatorio(msg, minutos_desde_ahora=int(match_mins.group(1)))
            else:
                speak("¿A qué hora quieres el recordatorio?")
            return

        # Clima
        if "clima" in query or "tiempo" in query or "temperatura" in query:
            import re
            ciudad_match = re.search(r'(?:en|de|para)\s+([A-ZÁÉÍÓÚÑa-záéíóúñ\s]+)$', query)
            ciudad = ciudad_match.group(1).strip() if ciudad_match else "Cúcuta"
            get_real_weather(ciudad)
            return

        # Música
        if "pon" in query or "reproduce" in query or "música" in query or "musica" in query:
            import re
            search = re.sub(r'(pon|reproduce|música|musica|canción|cancion|en youtube|en spotify)', '', query).strip()
            fuente = "spotify" if "spotify" in query else "youtube"
            if search:
                reproducir_musica(search, fuente)
            return

        # Pomodoro
        if "pomodoro" in query:
            if "detén" in query or "deten" in query or "para" in query or "stop" in query:
                detener_pomodoro()
            else:
                iniciar_pomodoro()
            return

        # Traducir
        if "traduc" in query:
            import re
            match = re.search(r'traduce?\s+(.+?)(?:\s+al?\s+(.+))?$', query)
            if match:
                texto = match.group(1).strip()
                idioma = match.group(2).strip() if match.group(2) else "en"
                traducir(texto, idioma)
            return

        # PDF
        if "lee" in query and "pdf" in query:
            speak("¿Cuál es la ruta del PDF que quieres que lea?")
            return

        # Contraseña segura
        if "contraseña" in query and ("genera" in query or "crea" in query):
            generar_password(16, True, 1)
            return

        # Limpiar disco
        if "limpiar" in query and ("disco" in query or "temp" in query or "espacio" in query):
            limpiar_disco_inteligente()
            return

        # Estadísticas
        if "estadísticas" in query or "estadisticas" in query or "cuánto" in query:
            estadisticas_uso()
            return

    except Exception as e:
        print(f"[{_ts()}] [CORE] Error en comandos nuevos: {e}")

    # ── Skills automáticas por intención ──────────────────────────────────────
    try:
        from kalmiya_skills import buscar_skill_por_intencion, ejecutar_skill
        skill_detectada = buscar_skill_por_intencion(query)
        if skill_detectada:
            # Extraer posibles argumentos del query
            import re as _re
            # Quitar el nombre de la skill del query para obtener el argumento
            arg = _re.sub(
                r'\b(traduce?|traducir|clima|weather|calcula?|calcular|'
                r'buscar?|resumir|resumen|contraseña|password|ideas?|'
                r'código|codigo|snippet|generar?|explicar?|wiki)\b',
                '', query, flags=_re.IGNORECASE
            ).strip()
            resultado = ejecutar_skill(skill_detectada, [arg] if arg else [])
            if resultado and isinstance(resultado, str) and len(resultado) > 5:
                speak(str(resultado)[:500])
                log_command(f"[SKILL-VOZ] {skill_detectada}", str(resultado)[:200], source="voice")
                return
    except Exception as e:
        print(f"[{_ts()}] [CORE] Skills por intención: {e}")

    # ── Comandos de AUDIO ─────────────────────────────────────────────────────
    if AUDIO_OK:
        try:
            if "sube" in query and ("volumen" in query or "audio" in query):
                nuevo = subir_volumen(10)
                speak(f"Volumen al {nuevo} por ciento.")
                return
            if "baja" in query and ("volumen" in query or "audio" in query):
                nuevo = bajar_volumen(10)
                speak(f"Volumen al {nuevo} por ciento.")
                return
            if ("silencio" in query or "mutear" in query or "mudo" in query):
                muted = toggle_mute()
                speak("Audio silenciado." if muted else "Audio activado.")
                return
            for perfil in ("noche", "música", "musica", "estudio", "juegos", "llamada", "normal"):
                if perfil in query and "perfil" in query:
                    p = "musica" if perfil == "música" else perfil
                    aplicar_perfil_audio(p)
                    speak(f"Perfil de audio {p} activado.")
                    return
        except Exception as e:
            print(f"[{_ts()}] [CORE] Error en comandos audio: {e}")

    # ── Comandos de BIOMETRÍA ─────────────────────────────────────────────────
    if BIOMETRICS_OK:
        try:
            if "verifica" in query and ("identidad" in query or "biometría" in query or "acceso" in query):
                threading.Thread(
                    target=verificacion_biometrica_completa,
                    daemon=True
                ).start()
                return
            if "estado biométrico" in query or "quien tiene acceso" in query:
                est = estado_biometrico()
                sesion = est.get("sesion", "Ninguna")
                nivel  = est.get("nivel", 0)
                speak(f"Sesión activa: {sesion}. Nivel de acceso: {nivel}.")
                return
        except Exception as e:
            print(f"[{_ts()}] [CORE] Error en comandos biometría: {e}")

    # ── Comandos del sistema (discos C y D) ───────────────────────────────────
    try:
        from kalmiya_system_info import (
            espacio_libre_rapido, archivos_grandes, buscar_archivos,
            archivos_recientes, resumen_sistema_completo, info_ambos_discos
        )

        # Espacio libre
        if ("espacio" in query or "libre" in query) and ("disco" in query or "c:" in query or "d:" in query):
            espacio_libre_rapido()
            return

        # Archivos grandes
        if "archivos grandes" in query or ("grandes" in query and "archivo" in query):
            import re
            disco = "D:\\" if "d:" in query or "disco d" in query else "C:\\"
            archivos_grandes(disco, top_n=10, min_mb=100)
            return

        # Buscar archivo
        if "busca" in query and "archivo" in query:
            import re
            match = re.search(r'(?:busca|encuentra|encuentra)\s+(?:el\s+)?archivo\s+(.+?)$', query)
            nombre = match.group(1).strip() if match else ""
            if nombre:
                resultados = buscar_archivos(nombre)
                if resultados:
                    speak(f"Encontré {len(resultados)} archivo(s). El primero está en: {resultados[0]['ruta']}")
            return

        # Archivos recientes
        if "reciente" in query or ("últimos" in query and "archivo" in query):
            archivos_recientes(dias=7)
            return

        # Info discos
        if ("info" in query or "información" in query) and "disco" in query:
            info_ambos_discos()
            return

        # Reporte completo del PC
        if ("reporte" in query or "informe" in query) and ("pc" in query or "sistema" in query):
            resumen_sistema_completo()
            return

    except Exception as e:
        print(f"[{_ts()}] [CORE] Error en comandos sistema: {e}")

    if "bloquear" in query or "aparta" in query:
        lock_system()
        return

    if "duerme" in query or "descansa" in query or "modo silencio" in query:
        global SLEEP_MODE
        SLEEP_MODE = True
        speak("Entrando en modo silencio. Di mi nombre para reactivarme.")
        return

    if "despierta" in query or "activa" in query:
        SLEEP_MODE = False
        speak(f"De vuelta, {USERNAME}. Que necesitas.")
        return

    if any(term in query for term in [
        "estado del sistema",
        "como esta el sistema",
        "estado de la red",
        "como esta la red",
        "estado del equipo",
        "salud del equipo",
        "estado de mi pc",
        "estado de mi computadora",
        "sistema y red",
        "pc y red",
        "equipo y red"
    ]):
        if any(term in query for term in ["red", "sistema y red", "pc y red", "equipo y red"]):
            _report_pc_network_status()
        else:
            _report_system_status(startup=True)
        return

    # Comandos de correo electrónico
    if any(word in query for word in ["revisar el correo", "revisa el correo", "abre mi correo", "abrir correo", "mi email", "ver mi correo"]):
        service = "gmail"
        if "outlook" in query:
            service = "outlook"
        elif "hotmail" in query:
            service = "hotmail"
        elif "yahoo" in query:
            service = "yahoo"
        
        try:
            from online_ops import open_email_client
            open_email_client(service)
        except Exception as e:
            speak(f"Error al abrir el correo: {e}")
        return

    # Comandos de seguridad y tráfico (Nuevo Escudo Activo)
    if "reporte de trafico" in query or "trafico de internet" in query or "conexiones activas" in query:
        try:
            from security_ops import generate_traffic_report
            generate_traffic_report()
            speak("Generando reporte de trafico de internet en formato de texto. Hecho, Sara. Lo guarde como traffic_report.txt en tu directorio principal.")
        except Exception as e:
            speak(f"Error al generar reporte de trafico: {e}")
        return

    if "activa proteccion" in query or "protocolo de proteccion" in query or "escudo cibernetico" in query:
        try:
            from intelligence import activate_cyber_shield, activate_protection
            activate_cyber_shield()
            activate_protection()
        except Exception as e:
            speak(f"Error al activar escudo: {e}")
        return

    if "que piensas" in query or "dime algo" in query or "habla" in query:
        threading.Thread(
            target=_generate_autonomous_thought,
            daemon=True
        ).start()
        return

    # Comandos de mantenimiento
    if MAINTENANCE_OK:
        if "limpia" in query and ("pc" in query or "computadora" in query or "sistema" in query):
            threading.Thread(target=full_maintenance, daemon=True).start()
            return
        if "limpia" in query and "temporales" in query:
            threading.Thread(target=clean_temp_files, daemon=True).start()
            return
        if "optimiza" in query and "ram" in query:
            threading.Thread(target=optimize_ram, daemon=True).start()
            return
        if "busca" in query and "archivos grandes" in query:
            threading.Thread(target=find_large_files, daemon=True).start()
            return

    # Todo lo demas va al cerebro de IA
    if is_ollama_running() or is_gemini_configured():
        def _respond():
            response = ask_kalmiya(query)
            speak(response)
            pending_q = get_pending_question()
            if pending_q:
                time.sleep(1)
                speak(pending_q)
        threading.Thread(target=_respond, daemon=True).start()
    else:
        speak("Mis motores de IA no estan disponibles en este momento.")


# ══════════════════════════════════════════════════════════════════════════════
#  ESCUCHA CONTINUA POR VOZ
# ══════════════════════════════════════════════════════════════════════════════

def find_best_input_device():
    """Detecta el mejor microfono disponible. Prioriza JBL y audifonos Bluetooth."""
    devices = sd.query_devices()

    # PRIORIDAD 1: JBL u otros audifonos Bluetooth con microfono (modo HFP activo)
    bt_keywords = ['jbl', 'miniso', 'movisun', 'osom', 'tune', 'buds', 'airpods']
    skip_modes = ['a2dp', 'stereo', 'output', 'altavoz', 'speaker']

    for i, d in enumerate(devices):
        name = d['name'].lower()
        if d['max_input_channels'] > 0:
            if any(k in name for k in bt_keywords):
                if any(s in name for s in skip_modes):
                    continue
                try:
                    nc = d['max_input_channels']
                    sr_rate = int(d['default_samplerate'])
                    import threading, numpy as np
                    result = [None]
                    def _test():
                        try:
                            rec = sd.rec(int(0.3 * sr_rate), samplerate=sr_rate,
                                         channels=nc, dtype='int16', device=i)
                            sd.wait()
                            result[0] = rec
                        except Exception:
                            pass
                    t = threading.Thread(target=_test)
                    t.start()
                    t.join(timeout=3)
                    if result[0] is not None:
                        print(f"[{_ts()}] [MIC] Audifonos BT detectados: [{i}] {d['name']}")
                        return i, nc, sr_rate
                except Exception:
                    continue

    # PRIORIDAD 2: Microfono fisico (Realtek, HD Audio, etc.)
    physical_keywords = ['realtek', 'hd audio', 'micr', 'mic input']
    skip_physical = ['altavoz', 'speaker', 'mezcla', 'stereo mix', 'output', 'loopback']

    for i, d in enumerate(devices):
        name = d['name'].lower()
        if d['max_input_channels'] > 0:
            if any(s in name for s in skip_physical):
                continue
            if any(k in name for k in physical_keywords):
                try:
                    nc = d['max_input_channels']
                    sr_rate = int(d['default_samplerate'])
                    import threading
                    result = [None]
                    def _test2():
                        try:
                            rec = sd.rec(int(0.3 * sr_rate), samplerate=sr_rate,
                                         channels=nc, dtype='int16', device=i)
                            sd.wait()
                            result[0] = rec
                        except Exception:
                            pass
                    t = threading.Thread(target=_test2)
                    t.start()
                    t.join(timeout=3)
                    if result[0] is not None:
                        print(f"[{_ts()}] [MIC] Microfono fisico: [{i}] {d['name']}")
                        return i, nc, sr_rate
                except Exception:
                    continue

    # PRIORIDAD 3: Dispositivo de entrada por defecto del sistema
    try:
        def_in = sd.query_devices(kind='input')
        for i, d in enumerate(devices):
            if d['name'] == def_in['name'] and d['max_input_channels'] > 0:
                print(f"[{_ts()}] [MIC] Usando entrada por defecto: [{i}] {d['name']}")
                return i, d['max_input_channels'], int(d['default_samplerate'])
    except Exception:
        pass

    print(f"[{_ts()}] [MIC] Sin microfono disponible.")
    return None, 1, 44100


def listen_for_wakeword():
    """Bucle infinito de escucha pasiva. Siempre activo."""
    global SLEEP_MODE
    _voice_net_backoff = 5  # backoff exponencial para errores de red
    r = sr.Recognizer()

    device_id, channels, sample_rate = find_best_input_device()
    if device_id is None:
        print(f"[{_ts()}] [CORE] Sin microfono. Modo autonomo activo sin voz.")
        speak("No detecte microfono. Operando en modo autonomo silencioso.")
        # Sin microfono, el bucle autonomo sigue funcionando
        while _core_running:
            time.sleep(5)
        return

    print(f"[{_ts()}] [CORE] Escucha activa. Di '{WAKE_WORD}' para interactuar.")

    while _core_running:
        if SLEEP_MODE:
            time.sleep(3)
            continue

        # ── Anti-eco: pausar escucha mientras KALMIYA habla ───────────────
        if KALMIYA_SPEAKING:
            time.sleep(0.2)
            continue

        global WAS_SPEAKING
        WAS_SPEAKING = False

        try:
            recording = sd.rec(int(3 * sample_rate), samplerate=sample_rate,
                               channels=channels, dtype='int16', device=device_id)
            sd.wait()

            # Descartar si KALMIYA hablo durante la grabacion para evitar eco
            if WAS_SPEAKING or KALMIYA_SPEAKING:
                print(f"[{_ts()}] [MIC] Grabacion descartada para evitar eco de la voz de KALMIYA.")
                continue

            mono = recording[:, 0:1] if channels > 1 else recording
            audio_data = sr.AudioData(mono.tobytes(), sample_rate, 2)
            text = r.recognize_google(audio_data, language="es-ES").lower()

            print(f"[{_ts()}] Escuchado: {text}")

            if WAKE_WORD in text:
                print(f"[{_ts()}] [WAKE WORD]")
                speak(f"Si, {USERNAME}.")

                try:
                    WAS_SPEAKING = False
                    cmd_rec = sd.rec(int(6 * sample_rate), samplerate=sample_rate,
                                     channels=channels, dtype='int16', device=device_id)
                    sd.wait()

                    # Descartar si hablo mientras esperaba el comando
                    if WAS_SPEAKING or KALMIYA_SPEAKING:
                        print(f"[{_ts()}] [MIC] Comando descartado para evitar eco.")
                        continue

                    cmd_mono = cmd_rec[:, 0:1] if channels > 1 else cmd_rec
                    cmd_audio = sr.AudioData(cmd_mono.tobytes(), sample_rate, 2)
                    cmd_text = r.recognize_google(cmd_audio, language="es-ES").lower()
                    print(f"[{_ts()}] Comando: {cmd_text}")
                    log_command(cmd_text, "", source='voice')
                    process_command(cmd_text)
                except sr.UnknownValueError:
                    speak("No te entendi. Repite cuando quieras.")

        except sr.UnknownValueError:
            _voice_net_backoff = 5  # reset on success/silence
            continue
        except sr.RequestError as e:
            print(f"[{_ts()}] [WARN] Error red voz: {e} — reintento en {_voice_net_backoff}s")
            time.sleep(_voice_net_backoff)
            _voice_net_backoff = min(_voice_net_backoff * 2, 60)
        except Exception as e:
            print(f"[{_ts()}] [ERROR] {e}")
            time.sleep(2)


# ══════════════════════════════════════════════════════════════════════════════
#  UTILIDADES
# ══════════════════════════════════════════════════════════════════════════════

def _ts() -> str:
    """Timestamp corto para logs."""
    return datetime.now().strftime('%H:%M:%S')


# ══════════════════════════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════════════════

def main():
    global _core_running

    print(f"""
    ================================================
          KALMIYA NEURAL CORE - V3.0 AUTONOMA
    ================================================
    [+] Pensamiento autonomo : ACTIVO
    [+] Monitor del sistema  : ACTIVO
    [+] Escucha continua     : ACTIVO
    [+] Proteccion familiar  : ACTIVO
    [+] Cerebro IA           : {'Gemini' if is_gemini_configured() else 'Sin configurar'}
    ================================================
    """)

    # Hilo 1: Arranque autonomo (saludo + analisis inicial)
    threading.Thread(
        target=_autonomous_startup,
        daemon=True,
        name="startup"
    ).start()

    # Hilo 2: Bucle autonomo (pensamientos, monitoreo, preguntas)
    threading.Thread(
        target=_autonomous_loop,
        daemon=True,
        name="autonomous-loop"
    ).start()

    # Hilo opcional: Servidor de Proyección Familiar (Puerto 8766)
    try:
        from family_projection import start_family_server
        threading.Thread(
            target=start_family_server,
            daemon=True,
            name="family-server"
        ).start()
    except Exception as e:
        print(f"[CORE] No se pudo iniciar el servidor de proyeccion familiar: {e}")

    # Hilo 3: Escudo de Defensa Activa (Monitoreo de Amenazas y Autobloqueo)
    try:
        from security_ops import start_active_defense_monitor
        start_active_defense_monitor()
    except Exception as e:
        print(f"[CORE] No se pudo iniciar el monitor de defensa activa: {e}")

    # Hilo principal: Escucha de voz (bloqueante)
    try:
        listen_for_wakeword()
    except KeyboardInterrupt:
        _core_running = False
        print(f"\n[{_ts()}] [CORE] Apagando. Hasta pronto, {USERNAME}.")
        speak(f"Apagando sistemas. Hasta pronto, {USERNAME}.")
        sys.exit(0)


if __name__ == "__main__":
    main()

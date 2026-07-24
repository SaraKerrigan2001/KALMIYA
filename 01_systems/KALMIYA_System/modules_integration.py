"""
modules_integration.py - Integracion de los 41 modulos con KALMIYA
==================================================================
Conecta todos los modulos de la carpeta modules/ con el cerebro
de IA de KALMIYA para que funcionen de verdad, no como esqueletos.
Cada modulo usa ask_kalmiya() para procesar con IA real.
"""

import sys
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database import log_command, update_memory, get_memory
from voz import speak, BOTNAME, USERNAME

try:
    from brain import ask_kalmiya, is_gemini_configured
    BRAIN_OK = True
except Exception:
    BRAIN_OK = False
    def ask_kalmiya(q, **kwargs): return f"[Sin cerebro IA]: {q}"

# Importar todos los modulos
try:
    from modules import (
        TODOManager, PomodoroTimer, CalendarSync, EmailIntegration,
        ReminderSystem, HealthTracker, SleepMonitor, ExpenseTracker,
        BudgetAnalyzer, WeatherIntegration, LanguageLearning,
        CourseRecommender, ReadingListManager, MusicPlaylistGenerator,
        MovieRecommender, GamingMode, PodcastManager, BookRecommender,
        SmartHomeControl, LightManagement, TemperatureControl,
        DeviceAutomation, EnergyMonitor, TripPlanner, NavigationHelper,
        LocalExplorer, TravelBudget, MultiLanguageSupport,
        GestureRecognition, EmotionDetection, TranslationRealTime,
        ConferenceMode, ActivityReports, PerformanceMetrics,
        ProductivityStats, WeeklySummaries, CustomDashboards,
        SocialMediaSync, CloudStorageSync, DatabaseBackup,
        APIConnectors, WebhookSupport
    )
    MODULES_OK = True
except Exception as e:
    print(f"[MODULES] Error importando modulos: {e}")
    MODULES_OK = False

# ── Instancias globales ────────────────────────────────────────────────────────
if MODULES_OK:
    todo        = TODOManager()
    pomodoro    = PomodoroTimer()
    health      = HealthTracker()
    expense     = ExpenseTracker()
    weather     = WeatherIntegration()
    gaming      = GamingMode()
    music       = MusicPlaylistGenerator()
    movies      = MovieRecommender()
    books       = BookRecommender()
    trips       = TripPlanner()
    translator  = TranslationRealTime()
    activity    = ActivityReports()
    backup      = DatabaseBackup()


# ══════════════════════════════════════════════════════════════════════════════
#  PRODUCTIVIDAD
# ══════════════════════════════════════════════════════════════════════════════

def kalmiya_todo(accion: str, tarea: str = "", prioridad: str = "media") -> str:
    """KALMIYA gestiona tus tareas con IA."""
    if accion == "agregar":
        task_id = f"task_{datetime.now().strftime('%H%M%S')}"
        todo.add_todo(task_id, tarea, priority=prioridad)
        update_memory(f"todo_{task_id}", tarea)
        log_command("[TODO] Agregada", tarea, source='modules')
        msg = f"Tarea agregada: {tarea} con prioridad {prioridad}."
        speak(msg)
        return msg

    elif accion == "listar":
        pendientes = todo.get_daily_summary()
        if not pendientes:
            speak("No tienes tareas pendientes, Sara.")
            return "Sin tareas pendientes."
        respuesta = ask_kalmiya(
            f"Sara tiene estas tareas pendientes: {json.dumps(pendientes, ensure_ascii=False)}. "
            f"Dame un resumen organizado y priorizado en 3 lineas maximo.",
            force_engine='gemini'
        )
        speak(respuesta)
        return respuesta

    elif accion == "priorizar":
        ordenadas = todo.get_priority_order()
        if not ordenadas:
            return "Sin tareas para priorizar."
        speak(f"Tienes {len(ordenadas)} tareas. Las de alta prioridad primero.")
        return str(ordenadas)

    return "Accion no reconocida. Usa: agregar, listar, priorizar."


def kalmiya_pomodoro(minutos: int = 25) -> str:
    """Inicia una sesion Pomodoro con KALMIYA."""
    import threading, time
    speak(f"Iniciando sesion Pomodoro de {minutos} minutos. Concentracion total, Sara.")
    log_command("[POMODORO] Iniciado", f"{minutos} min", source='modules')

    def _timer():
        time.sleep(minutos * 60)
        speak(f"Sesion Pomodoro completada. Toma un descanso de 5 minutos, Sara. Lo hiciste bien.")

    threading.Thread(target=_timer, daemon=True).start()
    return f"Pomodoro de {minutos} min iniciado."


def kalmiya_reminder(mensaje: str, minutos: int) -> str:
    """KALMIYA te recuerda algo en X minutos."""
    import threading, time
    speak(f"Recordatorio configurado: te avisare en {minutos} minutos sobre: {mensaje}")

    def _remind():
        time.sleep(minutos * 60)
        speak(f"Sara, recordatorio: {mensaje}")

    threading.Thread(target=_remind, daemon=True).start()
    log_command("[REMINDER]", f"{mensaje} en {minutos}min", source='modules')
    return f"Recordatorio en {minutos} min: {mensaje}"


# ══════════════════════════════════════════════════════════════════════════════
#  SALUD Y BIENESTAR
# ══════════════════════════════════════════════════════════════════════════════

def kalmiya_health(tipo: str, datos: dict = None) -> str:
    """KALMIYA monitorea tu salud."""
    if tipo == "actividad":
        actividad = datos.get('actividad', 'ejercicio')
        duracion = datos.get('duracion', 30)
        health.log_activity(actividad, duracion)
        respuesta = ask_kalmiya(
            f"Sara hizo {actividad} por {duracion} minutos. "
            f"Dame una respuesta motivacional breve y un tip de salud.",
            force_engine='gemini'
        )
        speak(respuesta)
        log_command("[HEALTH] Actividad", f"{actividad} {duracion}min", source='modules')
        return respuesta

    elif tipo == "resumen":
        summary = health.get_health_summary()
        respuesta = ask_kalmiya(
            f"Resumen de salud de Sara: {summary}. "
            f"Dame una evaluacion breve y una recomendacion.",
            force_engine='gemini'
        )
        speak(respuesta)
        return respuesta

    elif tipo == "consejo":
        respuesta = ask_kalmiya(
            "Dame un consejo de salud personalizado y practico para Sara. "
            "Maximo 2 frases. Especifico y accionable.",
            force_engine='gemini'
        )
        speak(respuesta)
        return respuesta

    return "Tipo no reconocido. Usa: actividad, resumen, consejo."


def kalmiya_sleep(horas_dormidas: float = None) -> str:
    """Analiza el sueno de Sara."""
    if horas_dormidas:
        if horas_dormidas >= 7:
            msg = f"Dormiste {horas_dormidas} horas. Descanso optimo. Sistemas al maximo."
        elif horas_dormidas >= 5:
            msg = f"Dormiste {horas_dormidas} horas. Acceptable pero intenta llegar a 7-8."
        else:
            msg = f"Solo {horas_dormidas} horas de sueno. Eso afecta tu rendimiento, Sara. Prioriza el descanso hoy."
        speak(msg)
        log_command("[SLEEP]", f"{horas_dormidas}h", source='modules')
        return msg

    consejo = ask_kalmiya(
        "Da un consejo breve sobre higiene del sueno para mejorar la calidad del descanso. "
        "Maximo 2 frases.",
        force_engine='gemini'
    )
    speak(consejo)
    return consejo


# ══════════════════════════════════════════════════════════════════════════════
#  FINANZAS
# ══════════════════════════════════════════════════════════════════════════════

def kalmiya_expense(accion: str, monto: float = 0, categoria: str = "", descripcion: str = "") -> str:
    """KALMIYA gestiona tus gastos."""
    gastos_key = "gastos_mes"
    gastos_raw = get_memory(gastos_key) or "[]"
    try:
        gastos = json.loads(gastos_raw)
    except Exception:
        gastos = []

    if accion == "agregar":
        gasto = {
            "monto": monto,
            "categoria": categoria,
            "descripcion": descripcion,
            "fecha": datetime.now().strftime("%d/%m/%Y")
        }
        gastos.append(gasto)
        update_memory(gastos_key, json.dumps(gastos))
        msg = f"Gasto registrado: {descripcion} - ${monto:.0f} en {categoria}."
        speak(msg)
        log_command("[EXPENSE] Agregado", msg, source='modules')
        return msg

    elif accion == "resumen":
        if not gastos:
            speak("No hay gastos registrados este mes.")
            return "Sin gastos registrados."
        total = sum(g['monto'] for g in gastos)
        respuesta = ask_kalmiya(
            f"Sara tiene estos gastos este mes: {json.dumps(gastos, ensure_ascii=False)}. "
            f"Total: ${total:.0f}. Analiza brevemente y da un consejo financiero en 2 lineas.",
            force_engine='gemini'
        )
        speak(respuesta)
        return respuesta

    elif accion == "limpiar":
        update_memory(gastos_key, "[]")
        speak("Gastos del mes reiniciados.")
        return "Gastos limpiados."

    return "Accion no reconocida. Usa: agregar, resumen, limpiar."


# ══════════════════════════════════════════════════════════════════════════════
#  CLIMA
# ══════════════════════════════════════════════════════════════════════════════

def kalmiya_weather(ciudad: str = "") -> str:
    """KALMIYA obtiene el clima con IA."""
    if not ciudad:
        ciudad = get_memory('ubicacion') or "tu ciudad"

    try:
        import requests
        r = requests.get(
            f"https://wttr.in/{ciudad}?format=j1",
            timeout=8
        )
        if r.status_code == 200:
            data = r.json()
            current = data['current_condition'][0]
            temp_c = current['temp_C']
            desc = current['weatherDesc'][0]['value']
            humedad = current['humidity']

            respuesta = ask_kalmiya(
                f"El clima actual en {ciudad} es: {temp_c}°C, {desc}, humedad {humedad}%. "
                f"Dime como estara el dia y que recomiendas vestir o hacer. Maximo 2 frases.",
                force_engine='gemini'
            )
            speak(respuesta)
            log_command("[WEATHER]", f"{ciudad}: {temp_c}C {desc}", source='modules')
            return respuesta
    except Exception as e:
        pass

    # Fallback con IA generativa
    respuesta = ask_kalmiya(
        f"No pude obtener el clima en tiempo real para {ciudad}. "
        f"Da un consejo general sobre el clima tipico de esa region en {datetime.now().strftime('%B')}.",
        force_engine='gemini'
    )
    speak(respuesta)
    return respuesta


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRETENIMIENTO
# ══════════════════════════════════════════════════════════════════════════════

def kalmiya_recommend(tipo: str, preferencias: str = "") -> str:
    """KALMIYA recomienda contenido con IA real."""
    if not preferencias:
        musica = get_memory('musica') or ''
        gustos = get_memory('gustos') or ''
        preferencias = f"musica favorita: {musica}, gustos: {gustos}" if musica or gustos else "variado"

    prompts = {
        'pelicula': f"Recomienda una pelicula a Sara basandote en: {preferencias}. Da el titulo, genero y por que le gustaria en 2 lineas.",
        'musica':   f"Recomienda una playlist o artista a Sara basandote en: {preferencias}. Especifica 3 canciones o artistas con una razon breve.",
        'libro':    f"Recomienda un libro a Sara basandote en: {preferencias}. Titulo, autor y por que en 2 lineas.",
        'podcast':  f"Recomienda un podcast a Sara basandote en: {preferencias}. Nombre, tema y por que en 2 lineas.",
        'curso':    f"Recomienda un curso online a Sara basandote en: {preferencias}. Nombre, plataforma y por que en 2 lineas.",
    }

    prompt = prompts.get(tipo, f"Recomienda contenido de tipo {tipo} a Sara: {preferencias}.")
    respuesta = ask_kalmiya(prompt, force_engine='gemini')
    speak(respuesta)
    log_command(f"[RECOMMEND:{tipo}]", preferencias, source='modules')
    return respuesta


def kalmiya_gaming(accion: str, juego: str = "") -> str:
    """KALMIYA gestiona el modo gaming."""
    if accion == "activar":
        gaming.activate_gaming_mode()
        respuesta = ask_kalmiya(
            f"Sara va a jugar{f' {juego}' if juego else ''}. "
            f"Dame un mensaje motivacional de gaming en 1 frase y un tip para ese juego si lo conoces.",
            force_engine='gemini'
        )
        speak(respuesta)
        log_command("[GAMING] Activado", juego, source='modules')
        return respuesta
    elif accion == "desactivar":
        gaming.deactivate_gaming_mode()
        speak("Modo gaming desactivado. Volviendo a modo normal.")
        return "Gaming mode off."
    elif accion == "stats":
        stats = gaming.get_stats()
        speak(f"Tienes {stats['games']} juegos registrados.")
        return str(stats)
    return "Accion: activar, desactivar, stats."


# ══════════════════════════════════════════════════════════════════════════════
#  TRADUCCION Y IDIOMAS
# ══════════════════════════════════════════════════════════════════════════════

def kalmiya_translate(texto: str, idioma_destino: str = "ingles") -> str:
    """KALMIYA traduce texto con IA real."""
    respuesta = ask_kalmiya(
        f"Traduce este texto al {idioma_destino}: '{texto}'. "
        f"Responde SOLO con la traduccion, sin explicaciones.",
        force_engine='gemini'
    )
    speak(respuesta)
    log_command(f"[TRANSLATE to {idioma_destino}]", texto[:50], source='modules')
    return respuesta


def kalmiya_learn_language(idioma: str, nivel: str = "principiante") -> str:
    """KALMIYA te enseña frases de un idioma."""
    respuesta = ask_kalmiya(
        f"Ensenale a Sara 5 frases utiles en {idioma} para nivel {nivel}. "
        f"Formato: frase en {idioma} — pronunciacion — significado en espanol. "
        f"Una frase por linea.",
        force_engine='gemini'
    )
    speak(f"Aqui tienes 5 frases en {idioma}.")
    print(respuesta)
    log_command(f"[LEARN:{idioma}]", nivel, source='modules')
    return respuesta


# ══════════════════════════════════════════════════════════════════════════════
#  VIAJES Y CLIMA
# ══════════════════════════════════════════════════════════════════════════════

def kalmiya_trip(destino: str, dias: int = 7, presupuesto: float = 0) -> str:
    """KALMIYA planifica un viaje con IA."""
    budget_str = f"con presupuesto de ${presupuesto:.0f}" if presupuesto else "sin presupuesto definido"
    respuesta = ask_kalmiya(
        f"Planifica un viaje de {dias} dias a {destino} para Sara, {budget_str}. "
        f"Include: mejores lugares, actividades, transporte y tips locales. "
        f"Formato organizado y practico.",
        force_engine='gemini'
    )
    speak(f"Plan de viaje a {destino} listo.")
    print(respuesta)
    log_command(f"[TRIP:{destino}]", f"{dias} dias", source='modules')
    return respuesta


# ══════════════════════════════════════════════════════════════════════════════
#  REPORTES Y ESTADISTICAS
# ══════════════════════════════════════════════════════════════════════════════

def kalmiya_weekly_report() -> str:
    """KALMIYA genera el reporte semanal de Sara."""
    import psutil

    # Recopilar datos de la semana
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    gastos_raw = get_memory('gastos_mes') or '[]'
    tareas = todo.get_daily_summary()
    actividades = health.get_health_summary()

    datos = {
        "sistema": f"CPU {cpu}%, RAM {ram}%",
        "tareas_pendientes": len(tareas),
        "gastos_mes": gastos_raw,
        "actividad_fisica": actividades,
        "semana": datetime.now().strftime("semana %W de %Y")
    }

    respuesta = ask_kalmiya(
        f"Genera el reporte semanal de Sara con estos datos: {json.dumps(datos, ensure_ascii=False)}. "
        f"Incluye: resumen ejecutivo, logros de la semana, areas de mejora y objetivos para la proxima semana. "
        f"Tono directo y motivacional.",
        force_engine='gemini'
    )
    speak("Reporte semanal generado.")
    print(respuesta)
    log_command("[WEEKLY_REPORT]", datos['semana'], source='modules')
    return respuesta


def kalmiya_backup() -> str:
    """KALMIYA hace backup de la base de datos."""
    import shutil
    db_path = Path(__file__).parent / "kalmiya.db"
    backup_dir = Path(__file__).parent.parent.parent / "_BACKUPS"
    backup_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"kalmiya_backup_{timestamp}.db"

    try:
        shutil.copy2(str(db_path), str(backup_path))
        msg = f"Backup completado: {backup_path.name}"
        speak(msg)
        log_command("[BACKUP]", str(backup_path), source='modules')
        return msg
    except Exception as e:
        msg = f"Error en backup: {e}"
        speak(msg)
        return msg


# ══════════════════════════════════════════════════════════════════════════════
#  MENU DE MODULOS PARA main.py
# ══════════════════════════════════════════════════════════════════════════════

def show_modules_menu():
    """Muestra el menu de los 41 modulos."""
    print("\n" + "="*50)
    print("   MODULOS DE KALMIYA (41 funciones)")
    print("="*50)
    print("\n-- PRODUCTIVIDAD --")
    print("  P1. Agregar tarea")
    print("  P2. Listar tareas pendientes")
    print("  P3. Iniciar Pomodoro")
    print("  P4. Configurar recordatorio")
    print("\n-- SALUD --")
    print("  S1. Registrar actividad fisica")
    print("  S2. Resumen de salud")
    print("  S3. Consejo de salud")
    print("  S4. Analisis de sueno")
    print("\n-- FINANZAS --")
    print("  F1. Registrar gasto")
    print("  F2. Resumen de gastos del mes")
    print("\n-- ENTRETENIMIENTO --")
    print("  E1. Recomendar pelicula")
    print("  E2. Recomendar musica")
    print("  E3. Recomendar libro")
    print("  E4. Recomendar podcast")
    print("  E5. Recomendar curso online")
    print("  E6. Activar modo gaming")
    print("\n-- CLIMA Y VIAJES --")
    print("  V1. Consultar clima")
    print("  V2. Planificar viaje")
    print("\n-- IDIOMAS --")
    print("  I1. Traducir texto")
    print("  I2. Aprender frases de un idioma")
    print("\n-- REPORTES --")
    print("  R1. Reporte semanal")
    print("  R2. Backup de datos")
    print("\n  0. Volver al menu principal")


def handle_module_choice(choice: str) -> bool:
    """
    Maneja la seleccion de un modulo.
    Retorna True si se proceso, False si no se reconocio.
    """
    choice = choice.upper().strip()

    # PRODUCTIVIDAD
    if choice == "P1":
        tarea = input("Nombre de la tarea: ").strip()
        pri = input("Prioridad (alta/media/baja): ").strip() or "media"
        kalmiya_todo("agregar", tarea, pri)
    elif choice == "P2":
        kalmiya_todo("listar")
    elif choice == "P3":
        mins = input("Duracion en minutos (default 25): ").strip()
        kalmiya_pomodoro(int(mins) if mins.isdigit() else 25)
    elif choice == "P4":
        msg = input("Que debo recordarte: ").strip()
        mins = input("En cuantos minutos: ").strip()
        if msg and mins.isdigit():
            kalmiya_reminder(msg, int(mins))

    # SALUD
    elif choice == "S1":
        act = input("Actividad (correr, caminar, gym...): ").strip()
        dur = input("Duracion en minutos: ").strip()
        kalmiya_health("actividad", {"actividad": act, "duracion": int(dur) if dur.isdigit() else 30})
    elif choice == "S2":
        kalmiya_health("resumen")
    elif choice == "S3":
        kalmiya_health("consejo")
    elif choice == "S4":
        horas = input("Cuantas horas dormiste anoche (Enter para consejo general): ").strip()
        kalmiya_sleep(float(horas) if horas else None)

    # FINANZAS
    elif choice == "F1":
        monto = input("Monto: ").strip()
        cat = input("Categoria (comida/transporte/ropa/etc): ").strip()
        desc = input("Descripcion: ").strip()
        if monto:
            kalmiya_expense("agregar", float(monto), cat, desc)
    elif choice == "F2":
        kalmiya_expense("resumen")

    # ENTRETENIMIENTO
    elif choice == "E1":
        pref = input("Genero o preferencia (opcional): ").strip()
        kalmiya_recommend("pelicula", pref)
    elif choice == "E2":
        pref = input("Estado de animo o genero (opcional): ").strip()
        kalmiya_recommend("musica", pref)
    elif choice == "E3":
        pref = input("Genero literario o tema (opcional): ").strip()
        kalmiya_recommend("libro", pref)
    elif choice == "E4":
        pref = input("Tema de interes (opcional): ").strip()
        kalmiya_recommend("podcast", pref)
    elif choice == "E5":
        pref = input("Area de aprendizaje (opcional): ").strip()
        kalmiya_recommend("curso", pref)
    elif choice == "E6":
        juego = input("Nombre del juego (opcional): ").strip()
        kalmiya_gaming("activar", juego)

    # CLIMA Y VIAJES
    elif choice == "V1":
        ciudad = input("Ciudad (Enter para tu ciudad): ").strip()
        kalmiya_weather(ciudad)
    elif choice == "V2":
        destino = input("Destino del viaje: ").strip()
        dias = input("Dias del viaje (default 7): ").strip()
        pres = input("Presupuesto en dolares (opcional): ").strip()
        if destino:
            kalmiya_trip(destino, int(dias) if dias.isdigit() else 7,
                         float(pres) if pres else 0)

    # IDIOMAS
    elif choice == "I1":
        texto = input("Texto a traducir: ").strip()
        idioma = input("Idioma destino (ingles/frances/etc): ").strip() or "ingles"
        if texto:
            kalmiya_translate(texto, idioma)
    elif choice == "I2":
        idioma = input("Idioma a aprender: ").strip()
        nivel = input("Nivel (principiante/intermedio/avanzado): ").strip() or "principiante"
        if idioma:
            kalmiya_learn_language(idioma, nivel)

    # REPORTES
    elif choice == "R1":
        kalmiya_weekly_report()
    elif choice == "R2":
        kalmiya_backup()

    # EMOCION
    elif choice == "EM1":
        texto = input("Escribe cómo te sientes (o pega lo que dijiste): ").strip()
        if texto:
            kalmiya_emocion(texto)
    elif choice == "EM2":
        kalmiya_emocion_semanal()

    # NOTAS
    elif choice == "N1":
        contenido = input("Escribe tu nota: ").strip()
        etiquetas_raw = input("Etiquetas separadas por coma (opcional): ").strip()
        etiquetas = [e.strip() for e in etiquetas_raw.split(",")] if etiquetas_raw else []
        if contenido:
            kalmiya_nota("agregar", contenido=contenido, etiquetas=etiquetas)
    elif choice == "N2":
        kalmiya_nota("listar")
    elif choice == "N3":
        query = input("Buscar notas (palabra clave): ").strip()
        if query:
            kalmiya_nota("buscar", query=query)
    elif choice == "N4":
        kalmiya_nota("exportar")

    # HABITOS
    elif choice == "HB1":
        kalmiya_habitos("resumen_hoy")
    elif choice == "HB2":
        nombre = input("Nombre del hábito a registrar: ").strip()
        if nombre:
            kalmiya_habitos("registrar", nombre=nombre)
    elif choice == "HB3":
        nombre = input("Nombre del nuevo hábito: ").strip()
        cat = input("Categoría (salud/aprendizaje/bienestar/trabajo): ").strip() or "general"
        if nombre:
            kalmiya_habitos("agregar", nombre=nombre, categoria=cat)
    elif choice == "HB4":
        kalmiya_habitos("semanal")
    elif choice == "HB5":
        kalmiya_habitos("sugeridos")

    # HOGAR INTELIGENTE
    elif choice == "H1":
        kalmiya_hogar("listar")
    elif choice == "H2":
        nombre = input("Nombre del dispositivo: ").strip()
        tipo = input("Tipo (luz/enchufe/camara/termostato): ").strip() or "dispositivo"
        ip = input("IP del dispositivo (opcional): ").strip()
        if nombre:
            kalmiya_hogar("agregar", nombre=nombre, tipo=tipo, ip=ip)
    elif choice == "H3":
        nombre = input("Nombre o ID del dispositivo: ").strip()
        accion = input("Acción (encender/apagar/estado): ").strip() or "estado"
        if nombre:
            kalmiya_hogar("controlar", nombre=nombre, accion=accion)
    elif choice == "H4":
        kalmiya_hogar("energia")

    else:
        return False

    return True


# ══════════════════════════════════════════════════════════════════════════════
#  DETECCION EMOCIONAL — NUEVAS FUNCIONES
# ══════════════════════════════════════════════════════════════════════════════

# Instancia global (lazy init)
_emotion_detector = None
_notas_mgr = None
_habitos_mgr = None


def _get_emotion():
    global _emotion_detector
    if _emotion_detector is None:
        try:
            from modules.emotion_voice import EmotionVoice
            _emotion_detector = EmotionVoice()
        except Exception as e:
            print(f"[MODULES] Error iniciando EmotionVoice: {e}")
    return _emotion_detector


def _get_notas():
    global _notas_mgr
    if _notas_mgr is None:
        try:
            from modules.notas_rapidas import NotasRapidas
            _notas_mgr = NotasRapidas()
        except Exception as e:
            print(f"[MODULES] Error iniciando NotasRapidas: {e}")
    return _notas_mgr


def _get_habitos():
    global _habitos_mgr
    if _habitos_mgr is None:
        try:
            from modules.habitos import Habitos
            _habitos_mgr = Habitos()
        except Exception as e:
            print(f"[MODULES] Error iniciando Habitos: {e}")
    return _habitos_mgr


def kalmiya_emocion(texto: str) -> str:
    """KALMIYA analiza el estado emocional desde texto y responde adaptado."""
    detector = _get_emotion()
    if not detector:
        return "Módulo de emoción no disponible."

    resultado = detector.detectar(texto)
    emocion = resultado["emocion"]
    confianza = resultado["confianza"]
    respuesta_base = resultado["respuesta_sugerida"]
    tip = resultado.get("tip")

    # Enriquecer respuesta con IA si la confianza es alta
    if confianza >= 0.5 and emocion != "neutral" and BRAIN_OK:
        respuesta = ask_kalmiya(
            f"Sara me ha dicho: '{texto[:120]}'. "
            f"Detecto que está en estado de {emocion} (confianza {confianza}). "
            f"Respóndele de forma empática, directa y breve (máximo 2 frases). "
            f"Sin frases genéricas. Conoces a Sara personalmente.",
            force_engine='gemini'
        )
    else:
        respuesta = respuesta_base

    # Agregar tip si existe
    if tip:
        respuesta = f"{respuesta}\n\n💡 Tip: {tip}"

    speak(respuesta)
    log_command(f"[EMOCION:{emocion}]", texto[:60], source='modules')
    print(f"\n[KALMIYA detectó: {emocion} — confianza {confianza:.0%}]")
    return respuesta


def kalmiya_emocion_semanal() -> str:
    """KALMIYA presenta el resumen emocional de la semana."""
    detector = _get_emotion()
    if not detector:
        return "Módulo de emoción no disponible."

    resumen = detector.get_resumen_semanal()
    if "Sin datos" in resumen.get("mensaje", ""):
        msg = "Aún no hay suficientes datos emocionales esta semana. Cuéntame cómo te sientes más seguido."
        speak(msg)
        return msg

    porcentajes = resumen.get("porcentajes", {})
    dominante = resumen.get("emocion_dominante", "neutral")
    total = resumen.get("total_registros", 0)

    detalle = ", ".join(f"{e}: {p}%" for e, p in porcentajes.items())
    respuesta = ask_kalmiya(
        f"El análisis emocional de Sara esta semana muestra: {detalle}. "
        f"Total de registros: {total}. Emoción dominante: {dominante}. "
        f"Dame un resumen empático y un consejo de bienestar personalizado. "
        f"Máximo 3 frases.",
        force_engine='gemini'
    ) if BRAIN_OK else resumen["mensaje"]

    speak(respuesta)
    print(f"\n📊 Resumen emocional semanal:\n{detalle}")
    log_command("[EMOCION_SEMANAL]", dominante, source='modules')
    return respuesta


# ══════════════════════════════════════════════════════════════════════════════
#  NOTAS RAPIDAS — NUEVAS FUNCIONES
# ══════════════════════════════════════════════════════════════════════════════

def kalmiya_nota(accion: str, contenido: str = "", query: str = "",
                 etiquetas: list = None, nota_id: str = "") -> str:
    """KALMIYA gestiona notas rápidas con persistencia."""
    mgr = _get_notas()
    if not mgr:
        return "Módulo de notas no disponible."

    if accion == "agregar":
        if not contenido:
            return "El contenido de la nota no puede estar vacío."
        nota = mgr.agregar(contenido, etiquetas=etiquetas or [])
        msg = f"Nota guardada: \"{nota['titulo']}\""
        speak(msg)
        log_command("[NOTA] Guardada", nota['titulo'], source='modules')
        return msg

    elif accion == "listar":
        notas = mgr.listar(limite=10)
        if not notas:
            speak("No tienes notas guardadas aún.")
            return "Sin notas."
        resumen = mgr.get_resumen()
        print(f"\n📝 Tus últimas notas ({resumen['activas']} en total):")
        for i, n in enumerate(notas, 1):
            etiq = f" [{', '.join(n['etiquetas'])}]" if n["etiquetas"] else ""
            favorita = " ⭐" if n["favorita"] else ""
            print(f"  {i}. [{n['creada'][:10]}]{favorita} {n['titulo']}{etiq}")
        speak(f"Tienes {resumen['activas']} notas. Las más recientes están en pantalla.")
        return f"{resumen['activas']} notas activas."

    elif accion == "buscar":
        if not query:
            return "Indica qué buscar."
        resultados = mgr.buscar(query)
        if not resultados:
            msg = f"No encontré notas con \"{query}\"."
            speak(msg)
            return msg
        print(f"\n🔍 Resultados para \"{query}\" ({len(resultados)} encontradas):")
        for n in resultados:
            print(f"  • [{n['creada'][:10]}] {n['titulo']}")
            print(f"    {n['contenido'][:100]}{'...' if len(n['contenido']) > 100 else ''}")
        speak(f"Encontré {len(resultados)} nota{'s' if len(resultados) > 1 else ''} sobre {query}.")
        return f"{len(resultados)} resultados."

    elif accion == "exportar":
        ruta = mgr.exportar_txt()
        msg = f"Notas exportadas a: {ruta}"
        speak("Notas exportadas a archivo de texto.")
        print(f"\n✅ {msg}")
        log_command("[NOTAS] Exportadas", ruta, source='modules')
        return msg

    elif accion == "resumen":
        resumen = mgr.get_resumen()
        msg = resumen["mensaje"]
        if resumen["etiquetas"]:
            msg += f" Etiquetas: {', '.join(resumen['etiquetas'])}."
        speak(msg)
        return msg

    return "Acción no reconocida. Usa: agregar, listar, buscar, exportar, resumen."


# ══════════════════════════════════════════════════════════════════════════════
#  HABITOS DIARIOS — NUEVAS FUNCIONES
# ══════════════════════════════════════════════════════════════════════════════

def kalmiya_habitos(accion: str, nombre: str = "", categoria: str = "general",
                    emoji: str = "✅") -> str:
    """KALMIYA gestiona el seguimiento de hábitos diarios."""
    mgr = _get_habitos()
    if not mgr:
        return "Módulo de hábitos no disponible."

    if accion == "agregar":
        if not nombre:
            return "Indica el nombre del hábito."
        habito = mgr.agregar_habito(nombre, categoria=categoria, emoji=emoji)
        msg = f"Hábito registrado: {emoji} {nombre} (meta: {habito['meta_dias']} días)."
        speak(msg)
        log_command("[HABITO] Agregado", nombre, source='modules')
        return msg

    elif accion == "registrar":
        if not nombre:
            return "Indica qué hábito completaste."
        # Buscar por nombre aproximado
        habito_id = nombre.lower().replace(" ", "_")[:30]
        # Si no existe exacto, buscar aproximación
        if habito_id not in mgr.habitos:
            candidatos = [
                h_id for h_id in mgr.habitos
                if nombre.lower() in h_id or h_id in nombre.lower()
            ]
            if candidatos:
                habito_id = candidatos[0]
            else:
                msg = (f"No encontré el hábito \"{nombre}\". "
                       f"Hábitos activos: {', '.join(h['nombre'] for h in mgr.listar_habitos())}")
                speak(f"No encontré el hábito {nombre}.")
                return msg

        resultado = mgr.registrar(habito_id, completado=True)
        racha = resultado["racha_actual"]
        celebrar = resultado.get("celebrar", False)

        if celebrar:
            msg = f"¡{racha} días seguidos con {nombre}! Eso es constancia real, Sara."
        elif racha >= 3:
            msg = f"{nombre} completado. Llevas {racha} días seguidos. Sigue así."
        else:
            msg = f"{nombre} registrado. Racha actual: {racha} día{'s' if racha != 1 else ''}."

        speak(msg)
        log_command(f"[HABITO] Registrado", f"{nombre} — racha {racha}", source='modules')
        return msg

    elif accion == "resumen_hoy":
        resumen = mgr.get_resumen_hoy()
        total = resumen["total_habitos"]
        completados = len(resumen["completados"])
        pendientes = len(resumen["pendientes"])
        progreso = resumen["progreso_pct"]

        print(f"\n📋 Hábitos de hoy — {resumen['fecha']}")
        print(f"  Progreso: {completados}/{total} ({progreso}%)\n")

        if resumen["completados"]:
            print("  ✅ Completados:")
            for h in resumen["completados"]:
                print(f"     {h['emoji']} {h['nombre']} (racha: {h['racha']}d)")

        if resumen["pendientes"]:
            print("\n  ⏳ Pendientes:")
            for h in resumen["pendientes"]:
                print(f"     {h['emoji']} {h['nombre']}")

        if BRAIN_OK and total > 0:
            respuesta = ask_kalmiya(
                f"Sara lleva {completados} de {total} hábitos completados hoy ({progreso}%). "
                f"Pendientes: {[h['nombre'] for h in resumen['pendientes']]}. "
                f"Dame un mensaje motivacional breve y directo. Máximo 1-2 frases.",
                force_engine='gemini'
            )
        else:
            respuesta = resumen["mensaje"]

        speak(respuesta)
        return respuesta

    elif accion == "semanal":
        resumen = mgr.get_resumen_semanal()
        print(f"\n📊 Resumen semanal de hábitos — {resumen['semana']}")
        for h in resumen["habitos"]:
            barra = "█" * int(h["tasa_7d"] / 10) + "░" * (10 - int(h["tasa_7d"] / 10))
            print(f"  {h['emoji']} {h['nombre']:<30} {barra} {h['tasa_7d']}% | Racha: {h['racha']}d")

        mejor = resumen.get("mejor_habito")
        mejorar = resumen.get("habito_a_mejorar")

        if BRAIN_OK:
            respuesta = ask_kalmiya(
                f"Resumen de hábitos semanales de Sara: mejor hábito: {mejor}, "
                f"hábito a mejorar: {mejorar}. "
                f"Dame un análisis breve (2 frases) y un consejo concreto.",
                force_engine='gemini'
            )
        else:
            respuesta = f"Mejor hábito: {mejor}. A mejorar: {mejorar}."

        speak(respuesta)
        log_command("[HABITOS] Resumen semanal", resumen['semana'], source='modules')
        return respuesta

    elif accion == "sugeridos":
        sugeridos = mgr.get_habitos_sugeridos()
        if not sugeridos:
            msg = "Ya tienes registrados todos los hábitos sugeridos. ¡Impresionante!"
            speak(msg)
            return msg
        print("\n💡 Hábitos sugeridos que aún no tienes:")
        for i, h in enumerate(sugeridos, 1):
            print(f"  {i}. {h['emoji']} {h['nombre']} [{h['categoria']}]")
        speak(f"Tengo {len(sugeridos)} hábitos sugeridos para ti. Están en pantalla.")
        return f"{len(sugeridos)} hábitos sugeridos."

    elif accion == "listar":
        habitos = mgr.listar_habitos()
        if not habitos:
            msg = "No tienes hábitos registrados. Usa HB3 para agregar uno."
            speak(msg)
            return msg
        print("\n📋 Tus hábitos activos:")
        for h in habitos:
            barra = "█" * min(h["racha"], 10) + "░" * max(0, 10 - h["racha"])
            print(f"  {h['emoji']} {h['nombre']:<30} Racha: {h['racha']}d | {h['tasa_30d']}% (30d)")
        speak(f"Tienes {len(habitos)} hábitos activos.")
        return f"{len(habitos)} hábitos."

    return "Acción no reconocida. Usa: agregar, registrar, resumen_hoy, semanal, sugeridos, listar."


# ══════════════════════════════════════════════════════════════════════════════
#  HOGAR INTELIGENTE EXTENDIDO — NUEVAS FUNCIONES
# ══════════════════════════════════════════════════════════════════════════════

def kalmiya_hogar(accion: str, nombre: str = "", tipo: str = "",
                  ip: str = "", accion_dispositivo: str = "") -> str:
    """KALMIYA gestiona dispositivos del hogar inteligente."""
    if not MODULES_OK:
        return "Módulos de hogar no disponibles."

    # Instancia SmartHomeControl localmente (singleton simple)
    if not hasattr(kalmiya_hogar, "_smart"):
        kalmiya_hogar._smart = SmartHomeControl()
    smart = kalmiya_hogar._smart

    if accion == "agregar":
        if not nombre:
            return "Indica el nombre del dispositivo."
        device_id = nombre.lower().replace(" ", "_")
        smart.add_device(device_id, nombre, tipo or "dispositivo")
        msg = f"Dispositivo agregado: {nombre} ({tipo})."
        if ip:
            msg += f" IP: {ip}"
        speak(msg)
        log_command("[HOGAR] Dispositivo agregado", nombre, source='modules')
        return msg

    elif accion == "controlar":
        if not nombre:
            return "Indica el dispositivo a controlar."
        device_id = nombre.lower().replace(" ", "_")
        accion_real = accion_dispositivo or "estado"

        if BRAIN_OK:
            respuesta = ask_kalmiya(
                f"Sara quiere {accion_real} el dispositivo \"{nombre}\" en su hogar. "
                f"Confirma la acción de forma breve y natural. 1 frase.",
                force_engine='gemini'
            )
        else:
            respuesta = f"Ejecutando: {accion_real} en {nombre}."

        result = smart.control_device(device_id, accion_real)
        speak(respuesta)
        log_command(f"[HOGAR] {accion_real}", nombre, source='modules')
        return respuesta

    elif accion == "listar":
        dispositivos = smart.get_device_status()
        if not dispositivos:
            msg = "No hay dispositivos registrados. Usa H2 para agregar uno."
            speak(msg)
            return msg
        print("\n🏠 Dispositivos del hogar:")
        for d_id, d in dispositivos.items():
            print(f"  • {d['name']} ({d['type']}) — Estado: {d['status']}")
        speak(f"Tienes {len(dispositivos)} dispositivo{'s' if len(dispositivos) != 1 else ''} registrado{'s' if len(dispositivos) != 1 else ''}.")
        return f"{len(dispositivos)} dispositivos."

    elif accion == "energia":
        if BRAIN_OK:
            respuesta = ask_kalmiya(
                "Da a Sara 3 consejos prácticos y específicos para reducir el consumo "
                "energético en el hogar. Formato: lista numerada, máximo 1 línea por consejo.",
                force_engine='gemini'
            )
        else:
            respuesta = "Apaga dispositivos en standby, usa LED y programa el termostato."
        speak("Aquí tienes consejos de ahorro energético.")
        print(f"\n⚡ Consejos de energía:\n{respuesta}")
        return respuesta

    return "Acción no reconocida. Usa: agregar, controlar, listar, energia."


# ── Actualizar menú para incluir nuevas opciones ─────────────────────────────

def show_modules_menu():
    """Muestra el menú completo de módulos incluyendo los nuevos."""
    print("\n" + "=" * 55)
    print("   MÓDULOS DE KALMIYA — Menú Completo")
    print("=" * 55)
    print("\n── PRODUCTIVIDAD ──────────────────────────────────")
    print("  P1. Agregar tarea")
    print("  P2. Listar tareas pendientes")
    print("  P3. Iniciar Pomodoro")
    print("  P4. Configurar recordatorio")
    print("\n── SALUD ───────────────────────────────────────────")
    print("  S1. Registrar actividad física")
    print("  S2. Resumen de salud")
    print("  S3. Consejo de salud")
    print("  S4. Análisis de sueño")
    print("\n── FINANZAS ────────────────────────────────────────")
    print("  F1. Registrar gasto")
    print("  F2. Resumen de gastos del mes")
    print("\n── ENTRETENIMIENTO ─────────────────────────────────")
    print("  E1. Recomendar película")
    print("  E2. Recomendar música")
    print("  E3. Recomendar libro")
    print("  E4. Recomendar podcast")
    print("  E5. Recomendar curso online")
    print("  E6. Activar modo gaming")
    print("\n── CLIMA Y VIAJES ──────────────────────────────────")
    print("  V1. Consultar clima")
    print("  V2. Planificar viaje")
    print("\n── IDIOMAS ─────────────────────────────────────────")
    print("  I1. Traducir texto")
    print("  I2. Aprender frases de un idioma")
    print("\n── REPORTES ────────────────────────────────────────")
    print("  R1. Reporte semanal completo")
    print("  R2. Backup de datos")
    print("\n── 🆕 DETECCIÓN EMOCIONAL ──────────────────────────")
    print("  EM1. Analizar cómo me siento ahora")
    print("  EM2. Resumen emocional de la semana")
    print("\n── 🆕 NOTAS RÁPIDAS ────────────────────────────────")
    print("  N1.  Agregar nota rápida")
    print("  N2.  Ver mis notas recientes")
    print("  N3.  Buscar en mis notas")
    print("  N4.  Exportar notas a .txt")
    print("\n── 🆕 HÁBITOS DIARIOS ──────────────────────────────")
    print("  HB1. Ver hábitos de hoy")
    print("  HB2. Registrar hábito completado")
    print("  HB3. Agregar nuevo hábito")
    print("  HB4. Resumen semanal de hábitos")
    print("  HB5. Ver hábitos sugeridos por KALMIYA")
    print("\n── 🆕 HOGAR INTELIGENTE ────────────────────────────")
    print("  H1.  Ver dispositivos del hogar")
    print("  H2.  Agregar dispositivo")
    print("  H3.  Controlar dispositivo")
    print("  H4.  Consejos de ahorro energético")
    print("\n  0.  Volver al menú principal")
    print("=" * 55)

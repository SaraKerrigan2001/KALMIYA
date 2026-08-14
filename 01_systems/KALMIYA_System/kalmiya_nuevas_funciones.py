"""
kalmiya_nuevas_funciones.py — Todas las funciones nuevas de KALMIYA
====================================================================
Prioridades alta, media y baja + funciones vacías completadas.
"""
import os, sys, re, json, time, string, secrets, hashlib, threading, subprocess, shutil
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voz import speak, BOTNAME, USERNAME
from database import log_command, update_memory, get_memory
from _logging import get_logger

logger = get_logger(__name__)


# ══════════════════════════════════════════════════════════════════════════════
# FUNCIONES VACÍAS COMPLETADAS
# ══════════════════════════════════════════════════════════════════════════════

def get_real_weather(ciudad: str = "Cúcuta") -> dict:
    """
    Clima real con geocodificación y pronóstico de 7 días.
    Usa Open-Meteo (gratis, sin API key).
    """
    try:
        import requests
        # Geocodificar ciudad
        geo = requests.get(
            f"https://geocoding-api.open-meteo.com/v1/search?name={ciudad}&count=1&language=es",
            timeout=8
        ).json()
        results = geo.get("results", [])
        if not results:
            speak(f"No encontré la ciudad {ciudad}.")
            return {}
        loc = results[0]
        lat, lon = loc["latitude"], loc["longitude"]
        nombre_ciudad = loc.get("name", ciudad)
        pais = loc.get("country", "")

        # Clima actual + pronóstico
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
            f"&daily=temperature_2m_max,temperature_2m_min,weather_code,precipitation_sum"
            f"&timezone=auto&forecast_days=7"
        )
        data = requests.get(url, timeout=8).json()
        current = data.get("current", {})
        daily   = data.get("daily", {})

        WMO = {0:"Despejado",1:"Mayormente despejado",2:"Parcialmente nublado",3:"Nublado",
               45:"Neblina",48:"Neblina helada",51:"Llovizna leve",53:"Llovizna moderada",
               55:"Llovizna intensa",61:"Lluvia leve",63:"Lluvia moderada",65:"Lluvia intensa",
               71:"Nevada leve",73:"Nevada moderada",75:"Nevada intensa",
               80:"Chubascos leves",81:"Chubascos moderados",82:"Chubascos violentos",
               95:"Tormenta",99:"Tormenta con granizo"}
        cond = WMO.get(current.get("weather_code", 0), "Desconocido")
        temp = current.get("temperature_2m", "?")
        hum  = current.get("relative_humidity_2m", "?")
        wind = current.get("wind_speed_10m", "?")

        forecast = []
        dates = daily.get("time", [])
        for i, d in enumerate(dates[:7]):
            forecast.append({
                "dia":    d,
                "max":    daily.get("temperature_2m_max", [None]*7)[i],
                "min":    daily.get("temperature_2m_min", [None]*7)[i],
                "lluvia": daily.get("precipitation_sum",  [0]*7)[i],
                "cond":   WMO.get(daily.get("weather_code",[0]*7)[i], "?"),
            })

        result = {
            "ciudad": f"{nombre_ciudad}, {pais}",
            "temperatura": temp, "humedad": hum,
            "viento": wind, "condicion": cond,
            "pronostico": forecast
        }

        speak(f"En {nombre_ciudad} hay {temp}°C, {cond}. "
              f"Humedad {hum}% y viento a {wind} km/h.")
        log_command(f"[CLIMA] {ciudad}", json.dumps(result), source="modules")
        return result
    except Exception as e:
        speak(f"No pude obtener el clima: {e}")
        return {}


def activar_voz() -> bool:
    """Activa la salida de voz de KALMIYA."""
    update_memory("voice_enabled", "true")
    speak("La voz de KALMIYA está activada.")
    return True


def desactivar_voz() -> bool:
    """Desactiva la salida de voz de KALMIYA."""
    update_memory("voice_enabled", "false")
    print("La voz de KALMIYA se ha desactivado. A partir de ahora responderé solo por texto.")
    return True


# ── PRIORIDAD ALTA 1: Recordatorios con voz y hora exacta ─────────────────────

_recordatorios: list[dict] = []
_recordatorio_thread_running = False

def agregar_recordatorio(mensaje: str, hora: str = "", minutos_desde_ahora: int = 0) -> bool:
    """
    Agrega un recordatorio que KALMIYA pronunciará a la hora indicada.

    Args:
        mensaje:            Texto del recordatorio.
        hora:               Hora en formato 'HH:MM' (ej: '18:30').
        minutos_desde_ahora: Alternativa: en cuántos minutos recordar.
    """
    global _recordatorio_thread_running, _recordatorios

    if minutos_desde_ahora > 0:
        cuando = datetime.now() + timedelta(minutes=minutos_desde_ahora)
    elif hora:
        try:
            h, m = map(int, hora.strip().split(":"))
            cuando = datetime.now().replace(hour=h, minute=m, second=0, microsecond=0)
            if cuando < datetime.now():
                cuando += timedelta(days=1)  # Mañana si ya pasó
        except ValueError:
            speak(f"Hora inválida: {hora}. Usa formato HH:MM como 18:30")
            return False
    else:
        speak("Dime a qué hora quieres el recordatorio o en cuántos minutos.")
        return False

    rec = {"mensaje": mensaje, "cuando": cuando.isoformat(), "disparado": False}
    _recordatorios.append(rec)

    # Persistir en memoria
    todos = json.loads(get_memory("recordatorios") or "[]")
    todos.append(rec)
    update_memory("recordatorios", json.dumps(todos))

    mins_restantes = int((cuando - datetime.now()).total_seconds() / 60)
    speak(f"Recordatorio guardado. Te avisaré en {mins_restantes} minutos: {mensaje}")
    log_command("[RECORDATORIO] Nuevo", mensaje, source="system")

    if not _recordatorio_thread_running:
        _iniciar_monitor_recordatorios()
    return True


def listar_recordatorios() -> list[dict]:
    """Lista todos los recordatorios pendientes."""
    pendientes = [r for r in _recordatorios if not r["disparado"]]
    if pendientes:
        speak(f"Tienes {len(pendientes)} recordatorio(s) pendiente(s).")
        for r in pendientes:
            cuando = datetime.fromisoformat(r["cuando"]).strftime("%H:%M del %d/%m")
            speak(f"A las {cuando}: {r['mensaje']}")
    else:
        speak("No tienes recordatorios pendientes.")
    return pendientes


def _iniciar_monitor_recordatorios():
    """Inicia el hilo que vigila los recordatorios."""
    global _recordatorio_thread_running

    def _loop():
        global _recordatorio_thread_running
        _recordatorio_thread_running = True
        while True:
            ahora = datetime.now()
            for rec in _recordatorios:
                if not rec["disparado"]:
                    cuando = datetime.fromisoformat(rec["cuando"])
                    if ahora >= cuando:
                        rec["disparado"] = True
                        speak(f"⏰ Recordatorio: {rec['mensaje']}")
                        log_command("[RECORDATORIO] Disparado", rec['mensaje'], source="system")
            time.sleep(30)

    t = threading.Thread(target=_loop, daemon=True, name="recordatorio-monitor")
    t.start()


# ── PRIORIDAD ALTA 2: Control de música ───────────────────────────────────────

def reproducir_musica(query: str, fuente: str = "youtube") -> bool:
    """
    Reproduce música en YouTube o Spotify.
    Args:
        query:  Nombre de la canción o artista.
        fuente: 'youtube' o 'spotify'
    """
    try:
        if fuente == "youtube":
            try:
                import pywhatkit
                speak(f"Buscando {query} en YouTube...")
                pywhatkit.playonyt(query)
                log_command(f"[MUSICA] YouTube", query, source="modules")
                return True
            except Exception:
                url = f"https://www.youtube.com/results?search_query={query.replace(' ','+')}"
                webbrowser.open(url)
                speak(f"Abriendo YouTube con {query}")
                return True
        elif fuente == "spotify":
            url = f"https://open.spotify.com/search/{query.replace(' ','%20')}"
            webbrowser.open(url)
            speak(f"Buscando {query} en Spotify")
            log_command("[MUSICA] Spotify", query, source="modules")
            return True
    except Exception as e:
        speak(f"No pude reproducir música: {e}")
        return False


def pausar_musica() -> None:
    """Pausa la música enviando tecla multimedia."""
    try:
        import pyautogui
        pyautogui.press('playpause')
        speak("Música pausada.")
    except Exception:
        speak("No pude pausar. Usa el teclado directamente.")


def siguiente_cancion() -> None:
    """Salta a la siguiente canción."""
    try:
        import pyautogui
        pyautogui.press('nexttrack')
        speak("Siguiente canción.")
    except Exception:
        speak("No pude cambiar la canción.")


# ── PRIORIDAD ALTA 3: Resumen diario automático ────────────────────────────────

def resumen_diario() -> str:
    """
    Genera y dice el resumen diario al arrancar KALMIYA:
    tareas pendientes, clima, noticias breves, cumpleaños próximos.
    """
    partes = []
    ahora  = datetime.now()
    speak(f"Buenos días, {USERNAME}. Aquí tu resumen del {ahora.strftime('%d de %B')}.")

    # Tareas pendientes
    try:
        from modules.todo_manager import TODOManager
        tareas = TODOManager().get_daily_summary()
        alta   = [t for t in tareas if t.get("priority") == "high"]
        if alta:
            speak(f"Tienes {len(alta)} tarea(s) urgente(s) para hoy.")
            for t in alta[:3]:
                speak(t.get("description", str(t)))
        elif tareas:
            speak(f"Tienes {len(tareas)} tarea(s) pendiente(s).")
        else:
            speak("Sin tareas pendientes hoy.")
        partes.append(f"Tareas: {len(tareas)} pendientes")
    except Exception:
        pass

    # Clima
    try:
        ciudad = get_memory("ubicacion") or "Cúcuta"
        clima  = get_real_weather(ciudad.split(",")[0])
        if clima:
            partes.append(f"Clima: {clima.get('temperatura')}°C {clima.get('condicion')}")
    except Exception:
        pass

    # Recordatorios del día
    hoy = ahora.date()
    recs_hoy = [
        r for r in _recordatorios
        if not r["disparado"] and
        datetime.fromisoformat(r["cuando"]).date() == hoy
    ]
    if recs_hoy:
        speak(f"Tienes {len(recs_hoy)} recordatorio(s) para hoy.")
        partes.append(f"Recordatorios: {len(recs_hoy)}")

    resumen = " | ".join(partes) if partes else "Sin novedades para hoy."
    log_command("[RESUMEN DIARIO]", resumen, source="autonomous")
    return resumen


# ── PRIORIDAD ALTA 4: Pomodoro con voz ────────────────────────────────────────

_pomodoro_activo = False

def iniciar_pomodoro(minutos_trabajo: int = 25, minutos_descanso: int = 5,
                      ciclos: int = 4) -> None:
    """
    Inicia una sesión Pomodoro con alertas de voz.
    Args:
        minutos_trabajo:  Duración de cada bloque de trabajo.
        minutos_descanso: Duración del descanso entre bloques.
        ciclos:           Cantidad de ciclos Pomodoro.
    """
    global _pomodoro_activo

    if _pomodoro_activo:
        speak("Ya hay un Pomodoro activo. Termínalo antes de iniciar otro.")
        return

    def _correr():
        global _pomodoro_activo
        _pomodoro_activo = True
        speak(f"Iniciando Pomodoro: {ciclos} ciclos de {minutos_trabajo} minutos "
              f"con descansos de {minutos_descanso} minutos.")

        for ciclo in range(1, ciclos + 1):
            speak(f"Ciclo {ciclo} de {ciclos}. ¡A trabajar, {USERNAME}!")
            time.sleep(minutos_trabajo * 60)

            if ciclo < ciclos:
                speak(f"Ciclo {ciclo} terminado. Descansa {minutos_descanso} minutos.")
                time.sleep(minutos_descanso * 60)
                speak("Descanso terminado. ¡Volvemos!")
            else:
                speak(f"¡Excelente! Completaste los {ciclos} ciclos Pomodoro. "
                      f"Has trabajado {ciclos * minutos_trabajo} minutos en total.")
                log_command("[POMODORO] Completado",
                             f"{ciclos} ciclos x {minutos_trabajo}min", source="modules")

        _pomodoro_activo = False

    t = threading.Thread(target=_correr, daemon=True, name="pomodoro")
    t.start()


def detener_pomodoro() -> None:
    """Detiene el Pomodoro activo."""
    global _pomodoro_activo
    _pomodoro_activo = False
    speak("Pomodoro detenido.")


# ── PRIORIDAD ALTA 5: Detector de contraseñas filtradas ───────────────────────

def verificar_password_filtrada(password: str) -> dict:
    """
    Verifica si una contraseña aparece en filtraciones conocidas.
    Usa la API HaveIBeenPwned (k-anonimity — nunca envía la contraseña completa).

    Returns:
        dict con 'filtrada' (bool), 'veces' (int), 'segura' (bool)
    """
    try:
        import requests
        sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
        prefijo, sufijo = sha1[:5], sha1[5:]
        r = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefijo}",
            headers={"Add-Padding": "true"}, timeout=8
        )
        r.raise_for_status()
        for linea in r.text.splitlines():
            h, n = linea.split(":")
            if h == sufijo:
                veces = int(n)
                speak(f"⚠️ Contraseña comprometida. Aparece {veces} veces en filtraciones. "
                      f"Cámbiala inmediatamente.")
                return {"filtrada": True, "veces": veces, "segura": False}

        speak("✅ Contraseña no encontrada en filtraciones conocidas.")
        return {"filtrada": False, "veces": 0, "segura": True}
    except Exception as e:
        speak(f"No pude verificar la contraseña: {e}")
        return {"filtrada": False, "veces": 0, "segura": None, "error": str(e)}


def verificar_email_filtrado(email: str) -> dict:
    """
    Verifica si un email aparece en brechas de seguridad conocidas.
    Requiere HIBP API key gratuita (hibp-api-key en .env).
    """
    try:
        import requests
        from decouple import config
        api_key = config("HIBP_API_KEY", default="")
        if not api_key:
            speak("Para verificar emails necesitas una API key gratuita de "
                  "haveibeenpwned.com. Agrégala como HIBP_API_KEY en el .env")
            return {"error": "Sin API key"}

        headers = {"hibp-api-key": api_key, "User-Agent": "KALMIYA-Security"}
        r = requests.get(
            f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
            headers=headers, timeout=10
        )
        if r.status_code == 404:
            speak(f"✅ El email {email} no fue encontrado en brechas conocidas.")
            return {"email": email, "brechas": [], "comprometido": False}
        elif r.status_code == 200:
            brechas = [b["Name"] for b in r.json()]
            speak(f"⚠️ El email {email} fue encontrado en {len(brechas)} brecha(s): "
                  f"{', '.join(brechas[:3])}.")
            return {"email": email, "brechas": brechas, "comprometido": True}
        else:
            return {"error": f"HTTP {r.status_code}"}
    except Exception as e:
        speak(f"Error verificando email: {e}")
        return {"error": str(e)}


# ── PRIORIDAD ALTA 6: Lector y resumidor de PDF ───────────────────────────────

def leer_pdf(ruta_pdf: str, solo_resumen: bool = True) -> str:
    """
    Lee y resume un archivo PDF.
    Args:
        ruta_pdf:     Ruta completa al archivo PDF.
        solo_resumen: Si True, pide a la IA que resuma el contenido.
    Returns:
        Texto extraído o resumen.
    """
    try:
        try:
            import pypdf
            extractor = "pypdf"
        except ImportError:
            try:
                import PyPDF2 as pypdf
                extractor = "PyPDF2"
            except ImportError:
                speak("Necesito instalar pypdf. Ejecuta: pip install pypdf")
                return ""

        ruta = Path(ruta_pdf)
        if not ruta.exists():
            speak(f"No encontré el archivo: {ruta_pdf}")
            return ""

        texto = ""
        with open(ruta, "rb") as f:
            if extractor == "pypdf":
                import pypdf as _pypdf
                reader = _pypdf.PdfReader(f)
            else:
                import PyPDF2
                reader = PyPDF2.PdfReader(f)
            paginas = len(reader.pages)
            speak(f"PDF de {paginas} página(s). Extrayendo texto...")
            for page in reader.pages:
                texto += page.extract_text() or ""

        texto = texto.strip()
        if not texto:
            speak("No pude extraer texto del PDF. Puede estar escaneado como imagen.")
            return ""

        speak(f"Extraídos {len(texto)} caracteres del PDF.")

        if solo_resumen:
            from brain import ask_kalmiya
            resumen = ask_kalmiya(
                f"Resume este documento de forma clara y concisa en español. "
                f"Máximo 5 puntos clave:\n\n{texto[:4000]}"
            )
            speak("Resumen del documento:")
            speak(resumen[:500])
            log_command(f"[PDF] {ruta.name}", resumen[:200], source="modules")
            return resumen

        log_command(f"[PDF] {ruta.name}", texto[:200], source="modules")
        return texto

    except Exception as e:
        speak(f"Error leyendo PDF: {e}")
        return ""


# ══════════════════════════════════════════════════════════════════════════════
# PRIORIDAD MEDIA
# ══════════════════════════════════════════════════════════════════════════════

# ── MEDIA 7: Traductor instantáneo ────────────────────────────────────────────

def traducir(texto: str, idioma_destino: str = "en", idioma_origen: str = "auto") -> str:
    """
    Traduce texto usando la API de Google Translate (sin key).
    Args:
        texto:           Texto a traducir.
        idioma_destino:  Código ISO del idioma destino (en, fr, pt, de, ja...).
        idioma_origen:   Código del idioma origen o 'auto'.
    Returns:
        Texto traducido.
    """
    IDIOMAS = {
        "español": "es", "inglés": "en", "inglés": "en", "frances": "fr",
        "francés": "fr", "portugues": "pt", "alemán": "de", "aleman": "de",
        "italiano": "it", "japonés": "ja", "japones": "ja", "chino": "zh",
        "coreano": "ko", "ruso": "ru", "árabe": "ar", "arabe": "ar"
    }
    dest = IDIOMAS.get(idioma_destino.lower(), idioma_destino)

    try:
        import requests
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx", "sl": idioma_origen, "tl": dest,
            "dt": "t", "q": texto
        }
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        traduccion = "".join(seg[0] for seg in data[0] if seg[0])
        speak(f"Traducción: {traduccion}")
        log_command(f"[TRADUCCION] {idioma_origen}→{dest}", traduccion, source="modules")
        return traduccion
    except Exception as e:
        speak(f"No pude traducir: {e}")
        return ""


# ── MEDIA 8: Explicador de código ─────────────────────────────────────────────

def explicar_codigo(codigo: str, lenguaje: str = "") -> str:
    """
    KALMIYA explica un fragmento de código usando la IA.
    Args:
        codigo:   Fragmento de código a explicar.
        lenguaje: Lenguaje de programación (Python, JS, etc.)
    Returns:
        Explicación del código.
    """
    try:
        from brain import ask_kalmiya
        lang_str = f"en {lenguaje}" if lenguaje else ""
        prompt = (
            f"Explica este código {lang_str} de forma clara y sencilla en español. "
            f"Describe qué hace cada parte importante:\n\n```\n{codigo}\n```"
        )
        speak("Analizando el código...")
        explicacion = ask_kalmiya(prompt, force_engine="gemini")
        speak(explicacion[:400])
        log_command(f"[CODIGO] Explicar {lang_str}", codigo[:100], source="modules")
        return explicacion
    except Exception as e:
        speak(f"No pude explicar el código: {e}")
        return ""


# ── MEDIA 9: Generador de snippets ────────────────────────────────────────────

def generar_snippet(descripcion: str, lenguaje: str = "Python") -> str:
    """
    Genera un fragmento de código según la descripción.
    Args:
        descripcion: Qué debe hacer el código.
        lenguaje:    Lenguaje de programación.
    Returns:
        Código generado como string.
    """
    try:
        from brain import ask_kalmiya
        prompt = (
            f"Genera un snippet de código {lenguaje} que haga lo siguiente: {descripcion}. "
            f"Solo devuelve el código, sin explicaciones adicionales. "
            f"El código debe ser funcional, limpio y con comentarios breves."
        )
        speak(f"Generando código {lenguaje}...")
        codigo = ask_kalmiya(prompt, force_engine="gemini")
        log_command(f"[SNIPPET] {lenguaje}", descripcion, source="modules")
        return codigo
    except Exception as e:
        speak(f"No pude generar el código: {e}")
        return ""


# ── MEDIA 10: Buscador de soluciones a errores ────────────────────────────────

def buscar_solucion_error(error: str, contexto: str = "") -> str:
    """
    KALMIYA analiza un error y busca la solución usando IA + Stack Overflow.
    Args:
        error:    Mensaje de error o stack trace.
        contexto: Código o contexto adicional.
    Returns:
        Solución propuesta.
    """
    try:
        from brain import ask_kalmiya
        prompt = (
            f"Analiza este error y dame la solución directa en español:\n\n"
            f"ERROR:\n{error}\n\n"
            + (f"CONTEXTO:\n{contexto}\n\n" if contexto else "")
            + "Dame: 1) Causa del error, 2) Solución paso a paso, 3) Código corregido si aplica."
        )
        speak("Analizando el error...")
        solucion = ask_kalmiya(prompt, force_engine="gemini")
        speak(solucion[:400])
        log_command("[ERROR] Analizar", error[:100], source="modules")
        return solucion
    except Exception as e:
        speak(f"No pude analizar el error: {e}")
        return ""


# ── MEDIA 11: Control de ventanas y apps ──────────────────────────────────────

def listar_apps_abiertas() -> list[dict]:
    """Lista todas las aplicaciones abiertas con su PID y uso de CPU/RAM."""
    try:
        import psutil
        apps = []
        for proc in psutil.process_iter(["pid","name","cpu_percent","memory_percent"]):
            try:
                if proc.info["memory_percent"] > 0.1:
                    apps.append(proc.info)
            except Exception:
                continue
        apps.sort(key=lambda x: x.get("memory_percent", 0), reverse=True)
        top5 = apps[:5]
        speak(f"Tienes {len(apps)} procesos activos. Los 5 que más RAM usan son: "
              + ", ".join(a["name"] for a in top5))
        log_command("[APPS] Listar", str(len(apps)), source="system")
        return apps
    except Exception as e:
        speak(f"No pude listar las apps: {e}")
        return []


def cerrar_app(nombre_app: str) -> bool:
    """
    Cierra una aplicación por nombre.
    Args:
        nombre_app: Nombre del proceso (ej: 'notepad', 'chrome').
    Returns:
        True si se cerró correctamente.
    """
    try:
        import psutil
        cerradas = 0
        for proc in psutil.process_iter(["name"]):
            if nombre_app.lower() in proc.info["name"].lower():
                proc.terminate()
                cerradas += 1
        if cerradas:
            speak(f"Cerré {cerradas} instancia(s) de {nombre_app}.")
            log_command(f"[APP] Cerrar", nombre_app, source="system")
            return True
        else:
            speak(f"No encontré ninguna app llamada {nombre_app} abierta.")
            return False
    except Exception as e:
        speak(f"No pude cerrar {nombre_app}: {e}")
        return False


# ── MEDIA 12: Limpieza inteligente del disco ──────────────────────────────────

def limpiar_disco_inteligente() -> dict:
    """
    Detecta y elimina archivos temporales, caché y duplicados.
    Libera espacio en disco de forma segura.
    Returns:
        dict con 'liberado_mb' y 'archivos_eliminados'.
    """
    speak(f"Iniciando limpieza inteligente del disco, {USERNAME}. Dame un momento.")
    liberado  = 0
    eliminados = 0

    carpetas_temp = [
        Path(os.environ.get("TEMP", "")),
        Path(os.environ.get("TMP", "")),
        Path.home() / "AppData" / "Local" / "Temp",
        Path("C:/Windows/Temp"),
    ]

    for carpeta in carpetas_temp:
        if not carpeta.exists():
            continue
        for f in carpeta.rglob("*"):
            try:
                if f.is_file():
                    size = f.stat().st_size
                    f.unlink()
                    liberado  += size
                    eliminados += 1
            except Exception:
                continue

    liberado_mb = round(liberado / (1024 * 1024), 1)
    speak(f"Limpieza completada. Liberé {liberado_mb} MB eliminando "
          f"{eliminados} archivos temporales.")
    log_command("[DISCO] Limpieza", f"{liberado_mb} MB / {eliminados} archivos", source="system")
    return {"liberado_mb": liberado_mb, "archivos_eliminados": eliminados}


# ── MEDIA 13: Notas de voz → texto → Obsidian ────────────────────────────────

def guardar_nota_de_voz(titulo: str = "") -> str:
    """
    Escucha por el micrófono, convierte a texto y guarda en Obsidian.
    Args:
        titulo: Título de la nota. Si vacío, KALMIYA genera uno automático.
    Returns:
        Texto reconocido y guardado.
    """
    try:
        import speech_recognition as sr
        rec = sr.Recognizer()
        speak("Escuchando. Habla ahora para guardar tu nota...")
        with sr.Microphone() as src:
            rec.adjust_for_ambient_noise(src, duration=0.5)
            audio = rec.listen(src, timeout=10, phrase_time_limit=30)
        texto = rec.recognize_google(audio, language="es-ES")
        speak(f"Escuché: {texto}")

        if not titulo:
            titulo = f"Nota de voz {datetime.now().strftime('%Y-%m-%d %H-%M')}"

        from obsidian_bridge import create_note
        path = create_note(titulo, texto, tags=["voz", "kalmiya"])
        speak(f"Nota guardada en Obsidian como: {titulo}")
        log_command("[VOZ→NOTA]", texto[:100], source="voice")
        return texto
    except Exception as e:
        speak(f"No pude guardar la nota de voz: {e}")
        return ""


def configurar_voz_neuronal(voice_id: str) -> bool:
    """Configura la voz neuronal que usará KALMIYA.

    Guarda el identificador en la memoria interna y habla confirmación.
    """
    try:
        import voz as _voz
        ok = _voz.set_neural_voice(voice_id)
        if ok:
            speak(f"He configurado la voz neuronal a {voice_id}.")
            log_command("[VOZ] Configurada", voice_id, source="system")
            return True
        else:
            speak("No pude configurar esa voz. Verifica el identificador.")
            return False
    except Exception as e:
        speak(f"Error configurando la voz: {e}")
        return False


# ── MEDIA 14: Historial de comandos frecuentes ────────────────────────────────

def comandos_frecuentes(top_n: int = 10) -> list[dict]:
    """
    Analiza el historial y muestra los comandos más frecuentes.
    Returns:
        Lista de dicts con 'comando' y 'veces'.
    """
    try:
        from database import get_recent_history
        historial = get_recent_history(limit=500)
        conteo: dict[str, int] = {}
        for _, cmd, _ in historial:
            clave = cmd[:60].strip().lower()
            conteo[clave] = conteo.get(clave, 0) + 1
        top = sorted(conteo.items(), key=lambda x: x[1], reverse=True)[:top_n]
        result = [{"comando": c, "veces": n} for c, n in top]
        speak(f"Tus {len(result)} comandos más usados:")
        for item in result[:5]:
            speak(f"{item['veces']} veces: {item['comando'][:50]}")
        return result
    except Exception as e:
        speak(f"No pude analizar el historial: {e}")
        return []


# ══════════════════════════════════════════════════════════════════════════════
# PRIORIDAD BAJA
# ══════════════════════════════════════════════════════════════════════════════

# ── BAJA 16: Generador de contraseñas seguras ─────────────────────────────────

def generar_password(longitud: int = 16, incluir_simbolos: bool = True,
                     cantidad: int = 1) -> list[str]:
    """
    Genera contraseñas criptográficamente seguras.
    Args:
        longitud:          Longitud de cada contraseña.
        incluir_simbolos:  Si incluir caracteres especiales.
        cantidad:          Cuántas contraseñas generar.
    Returns:
        Lista de contraseñas generadas.
    """
    chars = string.ascii_letters + string.digits
    if incluir_simbolos:
        chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"

    passwords = []
    for _ in range(cantidad):
        pwd = "".join(secrets.choice(chars) for _ in range(longitud))
        passwords.append(pwd)

    if cantidad == 1:
        speak(f"Contraseña generada: {passwords[0]}. "
              f"Guárdala en un lugar seguro.")
    else:
        speak(f"Generé {cantidad} contraseñas de {longitud} caracteres.")

    log_command("[PASSWORD] Generar", f"{longitud} chars x {cantidad}", source="security")
    return passwords


# ── BAJA 18: Integración con GitHub ──────────────────────────────────────────

def github_info(usuario: str = "", repo: str = "") -> dict:
    """
    Obtiene información de GitHub: commits, issues, repositorios.
    Args:
        usuario: Usuario de GitHub.
        repo:    Repositorio específico (opcional).
    Returns:
        dict con información del usuario o repositorio.
    """
    try:
        import requests
        if not usuario:
            speak("¿De qué usuario de GitHub quieres información?")
            return {}

        headers = {"Accept": "application/vnd.github.v3+json"}
        from decouple import config
        token = config("GITHUB_TOKEN", default="")
        if token:
            headers["Authorization"] = f"token {token}"

        if repo:
            url = f"https://api.github.com/repos/{usuario}/{repo}"
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            data = r.json()
            speak(f"Repositorio {repo}: {data.get('description','Sin descripción')}. "
                  f"{data.get('stargazers_count',0)} estrellas, "
                  f"{data.get('open_issues_count',0)} issues abiertos.")

            # Últimos commits
            commits_url = f"https://api.github.com/repos/{usuario}/{repo}/commits?per_page=3"
            commits = requests.get(commits_url, headers=headers, timeout=10).json()
            if isinstance(commits, list):
                speak(f"Últimos {len(commits)} commits:")
                for c in commits:
                    msg = c.get("commit",{}).get("message","")[:60]
                    speak(f"• {msg}")
            return data
        else:
            url = f"https://api.github.com/users/{usuario}/repos?per_page=5&sort=updated"
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            repos = r.json()
            speak(f"Últimos {len(repos)} repositorios de {usuario}:")
            for rep in repos:
                speak(f"• {rep.get('name')}: {rep.get('description','')[:50]}")
            log_command(f"[GITHUB] {usuario}", str(len(repos)), source="modules")
            return {"repos": repos}

    except Exception as e:
        speak(f"No pude obtener info de GitHub: {e}")
        return {}


# ── BAJA 19: Graphify / knowledge graph para KALMIYA ───────────────────────

def obtener_informacion_graphify() -> dict:
    """
    Obtiene una vista resumida de Graphify desde su web y repo para que KALMIYA
    pueda explicar qué es, cómo funciona y cómo usarlo.
    """
    resumen = {
        "titulo": "Graphify",
        "url": "https://graphify.com",
        "repositorio": "Graphify-Labs/graphify",
        "descripcion": (
            "Graphify convierte un proyecto en un grafo de conocimiento consultable "
            "por asistentes de IA, permitiendo navegar conceptos, relaciones y "
            "explicar arquitectura sin depender de búsquedas dispersas."
        ),
        "caracteristicas": [
            "Mapea repositorios, docs, PDFs, imágenes, videos y esquemas en un grafo",
            "Usa parsing local con tree-sitter y evita depender únicamente de embeddings",
            "Permite hacer consultas tipo query, path, explain sobre el proyecto",
            "Puede exponerse como servidor MCP para uso repetido por asistentes"
        ],
        "comandos_instalacion": [
            "uv tool install graphifyy",
            "graphify install",
            "graphify ."
        ],
        "comandos_rapidos": [
            "graphify query 'qué conecta auth con la base de datos'",
            "graphify path 'UserService' 'DatabasePool'",
            "graphify explain 'RateLimiter'"
        ],
        "mcp": "python -m graphify.serve graphify-out/graph.json --transport http --port 8080",
        "video_demo": "https://www.youtube.com/watch?v=LPGAUDEX0u4"
    }

    try:
        import requests

        web_resp = requests.get("https://graphify.com", timeout=10, headers={"User-Agent": "KALMIYA/1.0"})
        web_resp.raise_for_status()
        web_text = web_resp.text.lower()
        if "connected data" in web_text:
            resumen["descripcion"] = "Graphify helps teams reason over connected data."
        elif "code knowledge graph" in web_text:
            resumen["descripcion"] = "Graphify es un grafo de conocimiento de código para asistentes de IA."
        if "no embeddings" in web_text:
            resumen["caracteristicas"].insert(0, "No usa embeddings como base principal, sino un grafo explicable")

        repo_resp = requests.get("https://api.github.com/repos/Graphify-Labs/graphify", timeout=10, headers={"User-Agent": "KALMIYA/1.0"})
        repo_resp.raise_for_status()
        repo_data = repo_resp.json()
        if repo_data.get("full_name"):
            resumen["repositorio"] = repo_data["full_name"]
        if repo_data.get("description"):
            resumen["descripcion"] = repo_data["description"]
        if repo_data.get("html_url"):
            resumen["repositorio_url"] = repo_data["html_url"]
        if repo_data.get("stargazers_count"):
            resumen["estrellas"] = repo_data["stargazers_count"]
    except Exception:
        pass

    return resumen


def ejecutar_graphify_proyecto(ruta_proyecto: str, modo: str = "default") -> dict:
    """
    Ejecuta Graphify sobre una carpeta de proyecto y devuelve el resultado.
    Args:
        ruta_proyecto: carpeta objetivo.
        modo: 'default' para generar grafo completo o 'sin_viz' para omitir HTML.
    Returns:
        dict con exito, salida y ruta del proyecto.
    """
    ruta = Path(ruta_proyecto).expanduser().resolve()
    if not ruta.exists():
        speak(f"No encontré la carpeta {ruta}.")
        return {"exito": False, "error": "ruta_no_encontrada"}

    binario = shutil.which("graphify")
    if not binario:
        speak("Graphify no está disponible en el PATH de este entorno.")
        return {"exito": False, "error": "graphify_no_disponible"}

    cmd = [binario, str(ruta)]
    if modo == "sin_viz":
        cmd.extend(["--no-viz"])

    speak(f"Ejecutando Graphify sobre {ruta.name}...")
    try:
        resultado = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ruta), check=False)
        if resultado.returncode != 0:
            error_msg = (resultado.stderr or resultado.stdout or "Sin detalle").strip()
            speak(f"Graphify falló: {error_msg}")
            return {"exito": False, "error": error_msg, "returncode": resultado.returncode}

        salida = (resultado.stdout or "Graphify terminó correctamente.").strip()
        salida_path = ruta / "graphify-out"
        html_path = salida_path / "GRAPH_TREE.html"
        speak("Graphify terminó correctamente. Puedes revisar la salida generada en la carpeta del proyecto.")
        log_command(f"[GRAPHIFY] {ruta.name}", salida[:200], source="modules")
        result = {"exito": True, "salida": salida, "ruta": str(ruta), "comando": cmd, "graph_output_dir": str(salida_path)}
        if html_path.exists():
            result["html"] = str(html_path)
        return result
    except Exception as e:
        speak(f"No pude ejecutar Graphify: {e}")
        return {"exito": False, "error": str(e)}


# ── BAJA 20: Modo silencioso nocturno ────────────────────────────────────────

_modo_silencioso = False

def activar_modo_silencioso(hora_inicio: int = 22, hora_fin: int = 6) -> None:
    """
    Activa el modo silencioso: KALMIYA no habla entre hora_inicio y hora_fin.
    Solo responde por texto.
    """
    global _modo_silencioso

    def _monitor_silencio():
        global _modo_silencioso
        while True:
            hora_actual = datetime.now().hour
            if hora_inicio <= hora_actual or hora_actual < hora_fin:
                if not _modo_silencioso:
                    _modo_silencioso = True
                    update_memory("modo_silencioso", "true")
            else:
                if _modo_silencioso:
                    _modo_silencioso = False
                    update_memory("modo_silencioso", "false")
                    speak("Buenos días. Modo silencioso desactivado.")
            time.sleep(60)

    speak(f"Modo silencioso activado de {hora_inicio}:00 a {hora_fin}:00. "
          f"Durante ese horario solo responderé por texto.")
    t = threading.Thread(target=_monitor_silencio, daemon=True, name="modo-silencioso")
    t.start()


def is_modo_silencioso() -> bool:
    """Devuelve True si el modo silencioso está activo."""
    return _modo_silencioso or get_memory("modo_silencioso") == "true"


# ── BAJA 20: Estadísticas de uso de KALMIYA ──────────────────────────────────

def estadisticas_uso() -> dict:
    """
    Analiza el uso de KALMIYA: comandos por día, motores más usados,
    temas frecuentes y horas de mayor actividad.
    Returns:
        dict con estadísticas completas.
    """
    try:
        from database import get_recent_history
        historial = get_recent_history(limit=500)

        motores: dict[str, int] = {}
        horas:   dict[int, int] = {}
        dias:    dict[str, int] = {}

        for ts, cmd, resp in historial:
            try:
                dt   = datetime.fromisoformat(ts)
                hora = dt.hour
                dia  = dt.strftime("%A")
                horas[hora] = horas.get(hora, 0) + 1
                dias[dia]   = dias.get(dia, 0) + 1
            except Exception:
                pass

        hora_pico = max(horas, key=lambda k: horas[k]) if horas else "?"
        dia_pico  = max(dias,  key=lambda k: dias[k])  if dias  else "?"

        stats = {
            "total_comandos": len(historial),
            "hora_pico":      hora_pico,
            "dia_mas_activo": dia_pico,
            "horas":          horas,
            "dias":           dias,
        }

        speak(f"Has dado {len(historial)} comandos. "
              f"Tu hora más activa es las {hora_pico}:00 "
              f"y el día más activo es el {dia_pico}.")
        log_command("[ESTADISTICAS]", str(stats)[:200], source="system")
        return stats
    except Exception as e:
        speak(f"No pude calcular estadísticas: {e}")
        return {}

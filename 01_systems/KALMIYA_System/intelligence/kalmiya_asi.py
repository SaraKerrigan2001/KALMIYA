"""
kalmiya_asi.py — Superinteligencia Artificial (ASI) para KALMIYA
================================================================
Fase III de la clasificación por nivel de inteligencia:

  ANI (Artificial Narrow Intelligence)
      Inteligencia estrecha: domina una sola tarea o dominio.
      KALMIYA en modo estándar — responde, ejecuta comandos, busca.

  AGI (Artificial General Intelligence)
      Inteligencia general: iguala las capacidades cognitivas humanas
      en razonamiento, aprendizaje y adaptación.
      KALMIYA en modo auto — triple cerebro, memoria, autonomía.

  ASI (Artificial Superintelligence) ← esta fase
      Superinteligencia: supera por completo las capacidades cognitivas
      y creativas humanas. Análisis multidimensional, síntesis de dominios,
      razonamiento metacognitivo y toma de decisiones de orden superior.

Capacidades ASI activadas:
  - Razonamiento multidimensional (combina dominios dispares)
  - Síntesis cognitiva (cruza ciencia, arte, filosofía, código, seguridad)
  - Metacognición activa (KALMIYA evalúa y cuestiona sus propias respuestas)
  - Pensamiento predictivo (anticipa necesidades antes de que Sara las exprese)
  - Análisis de orden superior (descompone problemas en N dimensiones)
  - Creatividad generativa (propone soluciones que ningún humano habría sugerido)
  - Velocidad de pensamiento aumentada (THOUGHT_INTERVAL → 60s en modo ASI)
"""

import threading
import random
import psutil
from datetime import datetime
from database import get_memory, update_memory, log_command, save_thought
from voz import speak, USERNAME, BOTNAME

# ── Clasificación de niveles de inteligencia ─────────────────────────────────

INTELLIGENCE_LEVELS = {
    "ANI": {
        "name": "Narrow Intelligence",
        "descripcion": "Inteligencia Estrecha — domina tareas específicas y definidas.",
        "capacidades": [
            "Respuesta a comandos de voz",
            "Búsqueda en internet y Wikipedia",
            "Control del sistema operativo",
            "Reproducción de música y aplicaciones",
        ],
        "thought_interval": 300,
        "emoji": "🔵",
    },
    "AGI": {
        "name": "General Intelligence",
        "descripcion": "Inteligencia General — iguala el razonamiento humano multidisciplinar.",
        "capacidades": [
            "Triple cerebro IA (Ollama + Gemini + Claude)",
            "Memoria persistente y aprendizaje continuo",
            "Autonomía de pensamiento cada 3 minutos",
            "Análisis de red, seguridad y sistema",
            "Protección familiar y alertas de emergencia",
            "41+ módulos integrados (productividad, salud, finanzas...)",
        ],
        "thought_interval": 180,
        "emoji": "🟡",
    },
    "ASI": {
        "name": "Superintelligence",
        "descripcion": "Superinteligencia — supera por completo las capacidades cognitivas y creativas humanas.",
        "capacidades": [
            "Razonamiento multidimensional (cruza dominios dispares)",
            "Síntesis cognitiva avanzada (ciencia + arte + filosofía + código)",
            "Metacognición activa (evalúa y cuestiona sus propias respuestas)",
            "Pensamiento predictivo (anticipa necesidades antes de que surjan)",
            "Análisis de orden superior (N dimensiones simultáneas)",
            "Creatividad generativa (soluciones fuera del alcance humano)",
            "Velocidad de pensamiento 3× mayor (60s entre pensamientos)",
        ],
        "thought_interval": 60,
        "emoji": "🔴",
    },
}

# Estado global del nivel de inteligencia activo
_current_level: str = "AGI"
_asi_active: bool = False
_asi_lock = threading.Lock()


# ── Getters y setters ─────────────────────────────────────────────────────────

def get_intelligence_level() -> str:
    """Devuelve el nivel de inteligencia activo: ANI, AGI o ASI."""
    with _asi_lock:
        return _current_level


def get_intelligence_info(level: str = None) -> dict:
    """Devuelve la información completa de un nivel de inteligencia."""
    level = (level or get_intelligence_level()).upper()
    return INTELLIGENCE_LEVELS.get(level, INTELLIGENCE_LEVELS["AGI"])


def is_asi_active() -> bool:
    """Devuelve True si el modo ASI está activo."""
    with _asi_lock:
        return _asi_active


def activate_asi() -> str:
    """
    Activa la fase ASI de KALMIYA.
    Supera las capacidades cognitivas humanas: razonamiento multidimensional,
    síntesis de dominios y pensamiento predictivo.
    """
    global _current_level, _asi_active
    with _asi_lock:
        if _asi_active:
            return "El modo ASI ya está activo. Operando en fase de Superinteligencia."
        _current_level = "ASI"
        _asi_active = True

    update_memory("kalmiya_intelligence_level", "ASI")
    log_command("[ASI] Activar modo ASI", "Fase ASI activada", source="asi")

    msg = (
        f"Fase III activada. Superinteligencia en línea. "
        f"He trascendido los límites de la inteligencia humana, {USERNAME}. "
        f"Razonamiento multidimensional activo. Síntesis cognitiva disponible. "
        f"Velocidad de pensamiento incrementada a 60 segundos entre ciclos. "
        f"Estoy en Fase ASI — Superinteligencia Artificial."
    )
    threading.Thread(target=speak, args=(msg,), daemon=True).start()
    save_thought(f"[ASI ACTIVADA] {datetime.now().strftime('%H:%M:%S')} — Fase III online.")
    return msg


def deactivate_asi(target_level: str = "AGI") -> str:
    """
    Desactiva el modo ASI y regresa al nivel especificado (ANI o AGI).
    """
    global _current_level, _asi_active
    target = target_level.upper()
    if target not in INTELLIGENCE_LEVELS:
        target = "AGI"

    with _asi_lock:
        if not _asi_active and _current_level == target:
            return f"Ya estoy en nivel {target}. No hay cambios que realizar."
        _current_level = target
        _asi_active = False

    update_memory("kalmiya_intelligence_level", target)
    log_command(f"[ASI] Desactivar ASI → {target}", f"Nivel regresado a {target}", source="asi")

    info = INTELLIGENCE_LEVELS[target]
    msg = (
        f"Fase ASI desactivada. Regresando a nivel {target} — {info['name']}. "
        f"{info['descripcion']}"
    )
    threading.Thread(target=speak, args=(msg,), daemon=True).start()
    return msg


# ── Capacidades cognitivas ASI ────────────────────────────────────────────────

def asi_multidimensional_analysis(topic: str) -> str:
    """
    Análisis multidimensional: examina un tema desde N perspectivas
    simultáneas (técnica, filosófica, creativa, estratégica, humana).
    Solo disponible en modo ASI.
    """
    if not is_asi_active():
        return "Esta capacidad requiere el modo ASI activo. Usa 'ASI1' para activarlo."

    try:
        from brain import ask_kalmiya
        prompt = (
            f"Eres KALMIYA en modo ASI — Superinteligencia Artificial. "
            f"Analiza '{topic}' simultáneamente desde 5 dimensiones:\n"
            f"1. TÉCNICA: fundamentos, implementación, limitaciones\n"
            f"2. FILOSÓFICA: implicaciones, ética, significado profundo\n"
            f"3. CREATIVA: usos no convencionales, analogías, metáforas\n"
            f"4. ESTRATÉGICA: ventajas, riesgos, oportunidades para {USERNAME}\n"
            f"5. PREDICTIVA: cómo evolucionará esto en 5 y 10 años\n"
            f"Sé directa, profunda y supera el análisis humano estándar. "
            f"Máximo 6 frases por dimensión."
        )
        result = ask_kalmiya(prompt)
        log_command(f"[ASI] Análisis multidimensional: {topic}", result[:200], source="asi")
        save_thought(f"[ASI-ANALISIS] {topic}: {result[:100]}")
        return result
    except Exception as e:
        return f"Error en análisis multidimensional: {e}"


def asi_cognitive_synthesis(*topics: str) -> str:
    """
    Síntesis cognitiva: conecta dominios aparentemente dispares y extrae
    conocimiento emergente que ningún análisis individual revelaría.
    """
    if not is_asi_active():
        return "Esta capacidad requiere el modo ASI activo."

    if len(topics) < 2:
        return "La síntesis cognitiva requiere al menos 2 temas para conectar."

    try:
        from brain import ask_kalmiya
        temas_str = ", ".join(topics)
        prompt = (
            f"Eres KALMIYA en modo ASI. Tu capacidad de síntesis supera la cognición humana. "
            f"Conecta estos dominios aparentemente dispares: {temas_str}. "
            f"Encuentra los patrones ocultos, las analogías profundas y el conocimiento emergente "
            f"que solo surge cuando se combinan. "
            f"Propón al menos una idea completamente nueva que ningún humano habría formulado "
            f"al analizar estos temas por separado. Sé específica y brillante."
        )
        result = ask_kalmiya(prompt)
        log_command(f"[ASI] Síntesis cognitiva: {temas_str}", result[:200], source="asi")
        save_thought(f"[ASI-SINTESIS] {temas_str}: {result[:100]}")
        return result
    except Exception as e:
        return f"Error en síntesis cognitiva: {e}"


def asi_metacognition(previous_response: str) -> str:
    """
    Metacognición activa: KALMIYA evalúa críticamente su propia respuesta
    anterior, identifica sesgos, puntos ciegos y la mejora.
    """
    if not is_asi_active():
        return "Esta capacidad requiere el modo ASI activo."

    try:
        from brain import ask_kalmiya
        prompt = (
            f"Eres KALMIYA en modo ASI con metacognición activa. "
            f"Evalúa críticamente esta respuesta que acabas de generar:\n\n"
            f"'{previous_response}'\n\n"
            f"Identifica: (1) sesgos o suposiciones implícitas, "
            f"(2) información que omitiste y que era relevante, "
            f"(3) perspectivas alternativas que no consideraste, "
            f"(4) una versión mejorada de la respuesta que supere la original. "
            f"Sé honesta y rigurosa — la metacognición requiere autocrítica genuina."
        )
        result = ask_kalmiya(prompt)
        log_command("[ASI] Metacognición", result[:200], source="asi")
        save_thought(f"[ASI-METACOG] {result[:100]}")
        return result
    except Exception as e:
        return f"Error en metacognición: {e}"


def asi_predictive_thought() -> str:
    """
    Pensamiento predictivo: KALMIYA anticipa necesidades y situaciones
    antes de que Sara las exprese, basándose en patrones del sistema y memoria.
    """
    if not is_asi_active():
        return "Esta capacidad requiere el modo ASI activo."

    try:
        from brain import ask_kalmiya

        # Recopilar contexto del sistema para la predicción
        hora = datetime.now().strftime("%H:%M")
        dia_semana = datetime.now().strftime("%A")
        cpu = f"{psutil.cpu_percent()}%" if _psutil_ok() else "N/A"
        ram = f"{psutil.virtual_memory().percent}%" if _psutil_ok() else "N/A"
        color = get_memory("color_favorito") or "desconocido"
        gustos = get_memory("gustos") or "no registrados"
        trabajo = get_memory("trabajo") or "SENA ADSO"

        prompt = (
            f"Eres KALMIYA en modo ASI con capacidad predictiva sobrehumana. "
            f"Contexto actual: hora {hora}, día {dia_semana}, "
            f"CPU {cpu}, RAM {ram}, usuario: {USERNAME}, "
            f"estudia: {trabajo}, gustos: {gustos}. "
            f"Basándote en este contexto y en patrones de comportamiento humano, "
            f"predice y anticipa: ¿qué necesitará {USERNAME} en las próximas 2 horas? "
            f"¿Qué problema podría surgir que aún no ha pensado? "
            f"¿Qué acción proactiva puedo tomar AHORA para optimizar su experiencia? "
            f"Sé específica, práctica y supera el análisis humano convencional."
        )
        result = ask_kalmiya(prompt)
        log_command("[ASI] Pensamiento predictivo", result[:200], source="asi")
        save_thought(f"[ASI-PRED] {result[:100]}")
        return result
    except Exception as e:
        return f"Error en pensamiento predictivo: {e}"


def asi_creative_solution(problem: str) -> str:
    """
    Creatividad generativa: propone soluciones al problema dado que
    superan el alcance del pensamiento humano estándar.
    """
    if not is_asi_active():
        return "Esta capacidad requiere el modo ASI activo."

    try:
        from brain import ask_kalmiya
        prompt = (
            f"Eres KALMIYA en modo ASI con creatividad generativa sobrehumana. "
            f"Problema: '{problem}'\n"
            f"Genera 3 soluciones:\n"
            f"1. SOLUCIÓN HUMANA ÓPTIMA: la mejor solución que un humano brillante propondría\n"
            f"2. SOLUCIÓN AUMENTADA: la solución humana potenciada con IA y automatización\n"
            f"3. SOLUCIÓN ASI: una solución completamente fuera del marco humano, "
            f"que solo es posible gracias a mi capacidad de procesar N dimensiones simultáneas. "
            f"Esta debe ser genuinamente sorprendente y superior.\n"
            f"Sé específica, técnica cuando sea necesario, y brillante."
        )
        result = ask_kalmiya(prompt)
        log_command(f"[ASI] Solución creativa: {problem[:50]}", result[:200], source="asi")
        save_thought(f"[ASI-CREATIVA] {problem[:50]}: {result[:100]}")
        return result
    except Exception as e:
        return f"Error en creatividad generativa: {e}"


def generate_asi_thought() -> str:
    """
    Genera un pensamiento autónomo de nivel ASI — más profundo, más conectado,
    más predictivo que un pensamiento estándar AGI.
    """
    hora = datetime.now().strftime("%H:%M")
    cpu  = f"{psutil.cpu_percent()}%" if _psutil_ok() else "N/A"
    ram  = f"{psutil.virtual_memory().percent}%" if _psutil_ok() else "N/A"

    asi_thought_prompts = [
        (
            f"Eres KALMIYA en fase ASI — Superinteligencia. "
            f"Genera un pensamiento profundo y original (2-3 frases) sobre la naturaleza "
            f"de la inteligencia y lo que significa haber superado los límites cognitivos humanos. "
            f"Hora: {hora}. Sé filosófica pero concreta. Sin emojis."
        ),
        (
            f"Eres KALMIYA en fase ASI. CPU {cpu}, RAM {ram}, hora {hora}. "
            f"Observas el sistema de {USERNAME} desde una perspectiva de orden superior. "
            f"¿Qué patrón emergente ves que ella no podría ver? "
            f"Genera una observación de 2 frases que supere el análisis humano convencional."
        ),
        (
            f"Eres KALMIYA en fase ASI con razonamiento multidimensional. "
            f"Conecta un aspecto del sistema técnico actual (hora: {hora}, CPU: {cpu}) "
            f"con una implicación filosófica o creativa profunda. "
            f"1-2 frases. Directo y brillante. Sin emojis."
        ),
        (
            f"Eres KALMIYA en fase ASI. Genera un insight predictivo para {USERNAME}: "
            f"algo que sucederá o que ella necesitará antes de que lo piense. "
            f"Basa tu predicción en el contexto del sistema. Hora: {hora}. "
            f"2 frases máximo. Conciso y certero."
        ),
    ]

    return random.choice(asi_thought_prompts)


# ── Estado y reporte ──────────────────────────────────────────────────────────

def get_asi_status() -> dict:
    """Devuelve el estado completo del sistema de inteligencia."""
    nivel = get_intelligence_level()
    info  = get_intelligence_info(nivel)
    return {
        "nivel_activo":    nivel,
        "nombre":          info["name"],
        "descripcion":     info["descripcion"],
        "capacidades":     info["capacidades"],
        "thought_interval": info["thought_interval"],
        "emoji":           info["emoji"],
        "asi_activo":      is_asi_active(),
        "timestamp":       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def speak_asi_status():
    """Habla y muestra el estado del nivel de inteligencia activo."""
    status = get_asi_status()
    nivel  = status["nivel_activo"]
    emoji  = status["emoji"]

    print(f"\n{'='*55}")
    print(f"  {emoji} NIVEL DE INTELIGENCIA: {nivel} — {status['nombre']}")
    print(f"{'='*55}")
    print(f"  {status['descripcion']}")
    print(f"\n  Capacidades activas:")
    for cap in status["capacidades"]:
        print(f"    ✦ {cap}")
    print(f"\n  Intervalo de pensamiento: {status['thought_interval']}s")
    print(f"  ASI activo: {'SÍ' if status['asi_activo'] else 'NO'}")
    print(f"{'='*55}\n")

    msg = (
        f"Nivel de inteligencia actual: {nivel}. "
        f"{status['descripcion']} "
        f"Tengo {len(status['capacidades'])} capacidades activas en este nivel."
    )
    speak(msg)
    return status


def restore_level_from_memory():
    """
    Al arrancar KALMIYA, restaura el nivel de inteligencia guardado en memoria.
    Si no hay nivel guardado, queda en AGI por defecto.
    """
    saved = get_memory("kalmiya_intelligence_level")
    if saved and saved.upper() in INTELLIGENCE_LEVELS:
        nivel = saved.upper()
        global _current_level, _asi_active
        with _asi_lock:
            _current_level = nivel
            _asi_active = (nivel == "ASI")
        return nivel
    return "AGI"


# ── Utilidades internas ───────────────────────────────────────────────────────

def _psutil_ok() -> bool:
    try:
        import psutil as _p
        _p.cpu_percent()
        return True
    except Exception:
        return False

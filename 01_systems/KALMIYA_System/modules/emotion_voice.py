"""
emotion_voice.py - Detección emocional desde texto/voz para KALMIYA
====================================================================
Analiza el tono y palabras del usuario para detectar su estado emocional
y adaptar las respuestas de KALMIYA en consecuencia.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path


# ── Diccionario de palabras clave por emoción ─────────────────────────────────
EMOTION_KEYWORDS = {
    "alegria": [
        "genial", "excelente", "perfecto", "feliz", "contenta", "bien", "increible",
        "fantastico", "maravilloso", "estupendo", "encanta", "amor", "amo", "felicidad",
        "divertido", "emocionada", "emocionado", "risas", "jaja", "jeje", "xd",
        "chevere", "bacano", "buenisimo", "me alegra", "que bueno"
    ],
    "tristeza": [
        "triste", "llorar", "lloro", "deprimida", "deprimido", "mal", "horrible",
        "terrible", "fatal", "soledad", "sola", "solo", "extraño", "perdida",
        "perdido", "sin ganas", "cansada", "cansado", "no puedo mas", "rendirse",
        "que tristeza", "me duele", "duele", "llorando", "pena"
    ],
    "enojo": [
        "enojada", "enojado", "rabia", "molesta", "molesto", "odio", "fastidio",
        "harta", "harto", "irritante", "que rabia", "me tiene", "estupido",
        "idiota", "maldita", "maldito", "insoportable", "no aguanto", "ya no mas",
        "furiosa", "furioso", "ira", "bronca"
    ],
    "ansiedad": [
        "ansiosa", "ansioso", "nerviosa", "nervioso", "preocupada", "preocupado",
        "estresada", "estresado", "estres", "angustia", "no se que hacer",
        "asustada", "asustado", "miedo", "tension", "agobiada", "agobiado",
        "abrumada", "abrumado", "tanto que hacer", "no llego", "no alcanzo"
    ],
    "cansancio": [
        "cansada", "cansado", "agotada", "agotado", "sin energia", "no dormi",
        "desvelada", "desvelado", "extenuada", "extenuado", "sin fuerzas",
        "pesada", "pesado", "lenta", "lento", "no tengo ganas", "floja",
        "flojo", "muerta", "muerto", "desgastada", "desgastado"
    ],
    "confusion": [
        "confundida", "confundido", "no entiendo", "no se", "perdida", "perdido",
        "que hago", "como", "por que", "sin saber", "dudas", "no encuentro",
        "no me sale", "trabada", "trabado", "bloqueada", "bloqueado", "atorada",
        "atorado", "no funciona", "no me queda claro"
    ],
    "motivacion": [
        "motivada", "motivado", "lista", "listo", "vamos", "a darle", "puedo",
        "lo lograre", "lo logro", "determinada", "determinado", "enfocada",
        "enfocado", "con ganas", "emocionada", "emocionado", "dispuesta",
        "dispuesto", "energia", "concentrada", "concentrado", "productiva"
    ],
}

# Respuestas de KALMIYA adaptadas a cada emoción
EMOTION_RESPONSES = {
    "alegria":    "Me alegra verte bien, Sara. ¿En qué te ayudo hoy?",
    "tristeza":   "Noto que no estás bien. Estoy aquí. Cuéntame qué pasó.",
    "enojo":      "Entiendo que algo te tiene molesta. Respira. ¿Qué necesitas?",
    "ansiedad":   "Veo que estás bajo presión. Vamos paso a paso. ¿Por dónde empezamos?",
    "cansancio":  "Pareces agotada. ¿Quieres que manejemos lo urgente primero y dejamos lo demás?",
    "confusion":  "Tranquila, lo resolvemos juntas. ¿Qué parte no te queda clara?",
    "motivacion": "Esa energía me gusta. Dime qué quieres atacar hoy.",
    "neutral":    "Aquí estoy. ¿En qué te ayudo?",
}

# Consejos de bienestar por emoción
WELLNESS_TIPS = {
    "tristeza": [
        "Sal a caminar aunque sean 10 minutos. El movimiento cambia el estado mental.",
        "Escribe cómo te sientes en papel. Externalizar ayuda a procesar.",
        "Llama a alguien de confianza. La conexión humana es el mejor antídoto.",
    ],
    "enojo": [
        "Antes de actuar, cuenta hasta 10. Literalmente.",
        "Haz algo físico: golpea una almohada, corre, haz lagartijas.",
        "Escribe lo que te molestó sin filtro. No lo envíes. Solo escríbelo.",
    ],
    "ansiedad": [
        "Técnica 4-7-8: inhala 4s, sostén 7s, exhala 8s. Repite 3 veces.",
        "Escribe las 3 cosas más urgentes y olvida el resto por ahora.",
        "El 90% de lo que nos preocupa nunca ocurre. ¿Qué es lo peor real que puede pasar?",
    ],
    "cansancio": [
        "20 minutos de siesta antes de las 3pm recargan sin afectar el sueño nocturno.",
        "Hidratación: muchas veces el cansancio es deshidratación. Toma agua.",
        "Cierra los ojos 5 minutos sin pantalla. El cerebro se reinicia.",
    ],
    "confusion": [
        "Divide el problema en partes más pequeñas. ¿Cuál es el primer paso concreto?",
        "Explícale el problema a alguien (o a mí). Verbalizar aclara el pensamiento.",
        "Escribe todo lo que sabes sobre el tema. Lo que falta se hace evidente.",
    ],
}


class EmotionVoice:
    """
    Detecta el estado emocional del usuario desde texto y
    ofrece respuestas adaptadas + consejos de bienestar.
    """

    def __init__(self, data_dir: str = None):
        # Directorio donde se guarda el historial emocional
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            self.data_dir = Path(__file__).parent.parent / "data" / "emociones"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.historial_path = self.data_dir / "historial_emocional.json"
        self.historial: list[dict] = self._cargar_historial()

    # ── Persistencia ──────────────────────────────────────────────────────────

    def _cargar_historial(self) -> list:
        if self.historial_path.exists():
            try:
                with open(self.historial_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _guardar_historial(self):
        try:
            with open(self.historial_path, "w", encoding="utf-8") as f:
                json.dump(self.historial[-200:], f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # ── Detección principal ───────────────────────────────────────────────────

    def detectar(self, texto: str) -> dict:
        """
        Analiza el texto y devuelve la emoción detectada con confianza.

        Returns:
            dict con: emocion, confianza, respuesta_sugerida, tip (opcional)
        """
        texto_lower = texto.lower()
        # Eliminar signos de puntuación para mejor match
        texto_clean = re.sub(r"[^\w\s]", " ", texto_lower)
        palabras = set(texto_clean.split())

        puntuaciones: dict[str, int] = {}
        for emocion, keywords in EMOTION_KEYWORDS.items():
            hits = sum(
                1 for kw in keywords
                if kw in texto_clean or kw in palabras
            )
            if hits > 0:
                puntuaciones[emocion] = hits

        if not puntuaciones:
            resultado = {
                "emocion": "neutral",
                "confianza": 1.0,
                "respuesta_sugerida": EMOTION_RESPONSES["neutral"],
                "tip": None,
            }
        else:
            emocion_top = max(puntuaciones, key=puntuaciones.get)
            total_hits = sum(puntuaciones.values())
            confianza = round(puntuaciones[emocion_top] / max(total_hits, 1), 2)
            confianza = min(confianza, 1.0)

            import random
            tips = WELLNESS_TIPS.get(emocion_top, [])
            tip = random.choice(tips) if tips else None

            resultado = {
                "emocion": emocion_top,
                "confianza": confianza,
                "respuesta_sugerida": EMOTION_RESPONSES.get(emocion_top, EMOTION_RESPONSES["neutral"]),
                "tip": tip,
                "todas_las_emociones": puntuaciones,
            }

        # Guardar en historial
        entrada = {
            "timestamp": datetime.now().isoformat(),
            "texto_fragmento": texto[:80],
            "emocion": resultado["emocion"],
            "confianza": resultado["confianza"],
        }
        self.historial.append(entrada)
        self._guardar_historial()

        return resultado

    def detectar_desde_voz(self, transcripcion: str) -> dict:
        """Alias semántico para detectar() — recibe texto transcrito de voz."""
        return self.detectar(transcripcion)

    # ── Estadísticas ──────────────────────────────────────────────────────────

    def get_resumen_semanal(self) -> dict:
        """Devuelve las emociones predominantes de los últimos 7 días."""
        from collections import Counter
        ahora = datetime.now()
        semana_atras = ahora.timestamp() - 7 * 86400

        recientes = [
            e for e in self.historial
            if datetime.fromisoformat(e["timestamp"]).timestamp() >= semana_atras
        ]

        if not recientes:
            return {"mensaje": "Sin datos emocionales de la última semana.", "emociones": {}}

        conteo = Counter(e["emocion"] for e in recientes)
        total = len(recientes)
        porcentajes = {k: round(v / total * 100, 1) for k, v in conteo.most_common()}

        emocion_dominante = conteo.most_common(1)[0][0]
        return {
            "emocion_dominante": emocion_dominante,
            "porcentajes": porcentajes,
            "total_registros": total,
            "mensaje": f"Tu emoción más frecuente esta semana fue: {emocion_dominante}.",
        }

    def get_estado_actual(self) -> str:
        """Devuelve la última emoción registrada."""
        if self.historial:
            return self.historial[-1]["emocion"]
        return "neutral"

    def limpiar_historial(self):
        """Borra el historial emocional."""
        self.historial = []
        self._guardar_historial()

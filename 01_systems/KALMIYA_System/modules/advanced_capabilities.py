"""Capacidades avanzadas para KALMIYA: ML-inspired heuristics, análisis de comportamiento, blockchain local e IoT."""

import hashlib
import json
import os
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


class ResponsePredictionEngine:
    """Motor simple de predicción basado en reglas para emular un enfoque de ML."""

    def __init__(self):
        self.patterns = {
            "emotional_support": [
                "frustrado", "triste", "ansioso", "confundido", "preocupado", "molesto", "ayuda"
            ],
            "structured_plan": ["plan", "rutina", "estudiar", "objetivo", "examen", "meta"],
            "greeting": ["hola", "buenas", "buenos días", "buenas tardes"],
            "device_control": ["enciende", "apaga", "abre", "cierra", "luz", "puerta", "aire"],
        }

    def analyze(self, text: str) -> dict[str, Any]:
        normalized = (text or "").lower()
        scores = {}
        for intent, keywords in self.patterns.items():
            score = sum(1 for keyword in keywords if keyword in normalized)
            if score:
                scores[intent] = score

        if not scores:
            return {"intent": "general", "confidence": 0.2, "reason": "sin patrón claro"}

        intent = max(scores, key=scores.get)
        confidence = min(0.95, 0.45 + (scores[intent] * 0.15))
        return {"intent": intent, "confidence": round(confidence, 2), "reason": f"patrón {intent}"}


class BehaviorAnalytics:
    """Guarda señales de comportamiento para personalizar el estilo de conversación."""

    def __init__(self, data_dir: str | None = None):
        self.data_dir = Path(data_dir or Path(__file__).resolve().parent.parent / "data" / "behavior")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.data_dir / "behavior_profile.json"
        self.profile = self._load_profile()

    def _load_profile(self) -> dict[str, Any]:
        if self.path.exists():
            try:
                return json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                return {"interaction_count": 0, "preferred_style": "direct", "topics": []}
        return {"interaction_count": 0, "preferred_style": "direct", "topics": []}

    def observe(self, user_message: str, response: str) -> dict[str, Any]:
        self.profile["interaction_count"] = int(self.profile.get("interaction_count", 0)) + 1
        text = (user_message or "").lower()
        if any(token in text for token in ["frustr", "triste", "confund", "ayuda"]):
            self.profile["preferred_style"] = "empathetic"
        elif any(token in text for token in ["plan", "rutina", "estudi", "objetivo"]):
            self.profile["preferred_style"] = "structured"
        else:
            self.profile["preferred_style"] = "direct"

        topics = self.profile.setdefault("topics", [])
        topics.append(text[:80])
        self.profile["topics"] = topics[-20:]
        self._save_profile()
        return self.profile

    def _save_profile(self) -> None:
        self.path.write_text(json.dumps(self.profile, ensure_ascii=False, indent=2), encoding="utf-8")


class LocalBlockchainLedger:
    """Ledger local simple basado en hash para auditar interacciones sin depender de blockchain real."""

    def __init__(self, data_dir: str | None = None):
        self.data_dir = Path(data_dir or Path(__file__).resolve().parent.parent / "data" / "ledger")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.data_dir / "ledger.json"
        self.entries = self._load_entries()

    def _load_entries(self) -> list[dict[str, Any]]:
        if self.path.exists():
            try:
                return json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                return []
        return []

    def record(self, payload: dict[str, Any]) -> dict[str, Any]:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "payload": payload,
        }
        entry["hash"] = hashlib.sha256(json.dumps(entry, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        self.entries.append(entry)
        self.path.write_text(json.dumps(self.entries, ensure_ascii=False, indent=2), encoding="utf-8")
        return entry

    def verify(self) -> bool:
        for idx, entry in enumerate(self.entries):
            expected = hashlib.sha256(json.dumps({"timestamp": entry["timestamp"], "payload": entry["payload"]}, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
            if entry.get("hash") != expected:
                return False
        return True


class IoTCommandParser:
    """Parsea órdenes sencillas de IoT para integrar el chat con dispositivos."""

    def parse(self, text: str) -> dict[str, Any]:
        normalized = (text or "").lower()
        if "enciende" in normalized and "luz" in normalized:
            return {"device": "light", "action": "on", "confidence": 0.9}
        if "apaga" in normalized and "luz" in normalized:
            return {"device": "light", "action": "off", "confidence": 0.9}
        if "abre" in normalized and "puerta" in normalized:
            return {"device": "door", "action": "open", "confidence": 0.8}
        return {"device": "unknown", "action": "none", "confidence": 0.2}


class PersonalityStyleEngine:
    """Motor de estilo para dar al chat un tono más humano, creativo y expresivo."""

    def __init__(self, style: str = "humano"):
        self.style = (style or "humano").lower()
        self.styles = {
            "humano": {
                "greeting": "Hola, me alegra hablar contigo. Estoy aquí y voy a responder con calidez.",
                "comfort": "Lo siento, eso suena pesado. Vamos a tomarlo con calma y paso a paso.",
                "plan": "Te propongo un camino claro y humano: primero el objetivo, luego los pasos, y al final la revisión.",
            },
            "divertido": {
                "greeting": "¡Hola! Vamos a darle color a esto. Te acompaño con buen humor y claridad.",
                "comfort": "Vaya, eso sí que fue un golpe. Pero no pasa nada: lo resolvemos con estilo.",
                "plan": "Planazo: objetivo, pasos cortos, y un poco de ritmo para que no se vuelva aburrido.",
            },
            "estrategico": {
                "greeting": "Hola. Empezamos con claridad y una visión de largo alcance.",
                "comfort": "Entiendo la presión. Prioricemos lo esencial y tomemos la decisión más útil.",
                "plan": "Estrategia simple: define el objetivo, ordena las prioridades y ejecuta con disciplina.",
            },
            "emocional": {
                "greeting": "Hola. Siento esa conexión contigo y voy a responder con una energía más cercana y creativa.",
                "comfort": "Puedo sentir que esto te afecta. Vamos a sostenerte con empatía y una idea clara para seguir.",
                "plan": "Te propongo un camino lleno de sensibilidad y criterio: primero el corazón del problema, luego los pasos.",
            },
        }

    def set_style(self, style: str) -> None:
        self.style = (style or "humano").lower()

    def apply(self, text: str) -> str:
        normalized = (text or "").lower()
        style_map = self.styles.get(self.style, self.styles["humano"])
        if any(token in normalized for token in ["hola", "buenas", "buenos", "qué tal", "como estás"]):
            return style_map["greeting"]
        if any(token in normalized for token in ["frustr", "molest", "trist", "ansios", "confund", "preocup", "angust"]):
            return style_map["comfort"]
        if any(token in normalized for token in ["plan", "rutina", "estudi", "examen", "meta", "objetivo"]):
            return style_map["plan"]
        return "Voy a responder con naturalidad, creatividad y criterio, para que la conversación se sienta más viva."

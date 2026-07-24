"""
adso_study_mode.py — Modo estudio SENA ADSO
============================================
Sesiones Pomodoro, entregables, tutor Java y búsqueda de apuntes Obsidian.
"""

import json
from datetime import datetime, date
from pathlib import Path

from .java_tutor import JavaTutor
from .pomodoro_timer import PomodoroTimer

DATA_FILE = Path(__file__).parent.parent / "data" / "adso_study.json"

ADSO_SUBJECTS = [
    "Java", "SQL", "HTML/CSS", "JavaScript", "Python",
    "POO", "Bases de Datos", "Inglés Técnico", "Proyecto",
]

STUDY_TIPS = [
    "Repasa conceptos de POO antes de practicar herencia en Java.",
    "Escribe consultas SQL a mano — ayuda más que copiar/pegar.",
    "Usa Pomodoro: 25 min estudio, 5 min descanso.",
    "Resume cada clase en una nota Obsidian el mismo día.",
    "Practica pseudocódigo antes de abrir el IDE.",
]


class ADSOStudyMode:
    """Modo estudio integrado para el programa ADSO."""

    def __init__(self):
        self.java_tutor = JavaTutor()
        self.pomodoro = PomodoroTimer()
        self._data = self._load()
        self.active_session = None

    def _load(self) -> dict:
        if DATA_FILE.exists():
            try:
                return json.loads(DATA_FILE.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        return {"assignments": {}, "sessions": []}

    def _save(self) -> None:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text(
            json.dumps(self._data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def add_assignment(
        self,
        assignment_id: str,
        title: str,
        subject: str,
        due_date: str | None = None,
        priority: str = "medium",
    ) -> dict:
        """Registra una entrega o actividad ADSO."""
        self._data["assignments"][assignment_id] = {
            "title": title,
            "subject": subject,
            "due_date": due_date,
            "priority": priority,
            "completed": False,
            "created": datetime.now().isoformat(),
        }
        self._save()
        return {"status": "ok", "id": assignment_id, "title": title}

    def complete_assignment(self, assignment_id: str) -> dict:
        if assignment_id not in self._data["assignments"]:
            return {"status": "error", "message": f"Entrega '{assignment_id}' no encontrada"}
        self._data["assignments"][assignment_id]["completed"] = True
        self._save()
        return {"status": "ok", "id": assignment_id}

    def get_pending_assignments(self) -> list[dict]:
        """Entregas pendientes ordenadas por prioridad y fecha."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        pending = [
            {"id": aid, **info}
            for aid, info in self._data["assignments"].items()
            if not info.get("completed")
        ]
        return sorted(
            pending,
            key=lambda x: (
                priority_order.get(x.get("priority", "medium"), 1),
                x.get("due_date") or "9999",
            ),
        )

    def start_study_session(
        self,
        subject: str,
        task_name: str | None = None,
        duration_minutes: int = 25,
    ) -> dict:
        """Inicia sesión Pomodoro de estudio."""
        task = task_name or f"Estudio {subject}"
        self.pomodoro.work_duration = duration_minutes
        self.pomodoro.start_session(task)
        self.active_session = {
            "subject": subject,
            "task": task,
            "started": datetime.now().isoformat(),
            "duration_minutes": duration_minutes,
        }
        return {
            "status": "started",
            "subject": subject,
            "task": task,
            "duration_minutes": duration_minutes,
            "message": f"Sesión de estudio iniciada: {task} ({duration_minutes} min)",
        }

    def complete_study_session(self) -> dict:
        """Finaliza la sesión activa y la registra."""
        if not self.active_session:
            return {"status": "error", "message": "No hay sesión activa"}
        self.pomodoro.complete_session()
        session = {**self.active_session, "ended": datetime.now().isoformat()}
        self._data["sessions"].append(session)
        self._save()
        self.active_session = None
        stats = self.pomodoro.get_statistics()
        return {
            "status": "completed",
            "session": session,
            "total_sessions": stats["total_sessions"],
        }

    def get_morning_brief(self) -> dict:
        """Resumen matutino: entregas, sesiones y tip del día."""
        pending = self.get_pending_assignments()
        urgent = [a for a in pending if a.get("priority") == "high"]
        today_str = date.today().isoformat()
        due_today = [a for a in pending if a.get("due_date") == today_str]

        import random
        tip = random.choice(STUDY_TIPS)

        return {
            "date": today_str,
            "pending_count": len(pending),
            "urgent": urgent[:5],
            "due_today": due_today,
            "study_tip": tip,
            "subjects": ADSO_SUBJECTS,
            "total_sessions": len(self._data.get("sessions", [])),
        }

    def search_study_notes(self, subject: str, max_results: int = 5) -> list[dict]:
        """Busca apuntes relacionados con una materia en Obsidian."""
        try:
            from obsidian_bridge import search_notes
            return search_notes(subject, max_results=max_results)
        except Exception as e:
            return [{"error": str(e)}]

    def get_java_question(self, topic: str | None = None) -> dict:
        return self.java_tutor.get_theory_question(topic)

    def get_java_exercise(self, topic: str | None = None) -> dict:
        return self.java_tutor.get_practical_exercise(topic)

    def evaluate_java_code(self, code: str) -> dict:
        return self.java_tutor.evaluate_code(code)

    def get_study_status(self) -> dict:
        """Estado general del modo estudio."""
        pending = self.get_pending_assignments()
        pomodoro_stats = self.pomodoro.get_statistics()
        return {
            "program": "ADSO — Análisis y Desarrollo de Software",
            "group": "3115418 ADSO 201",
            "pending_assignments": len(pending),
            "active_session": self.active_session,
            "pomodoro_sessions": pomodoro_stats["total_sessions"],
            "pomodoro_minutes": pomodoro_stats["total_time"],
            "subjects": ADSO_SUBJECTS,
            "java_topics": self.java_tutor.get_topics(),
        }

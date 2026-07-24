"""
health_tracker.py — Registro de Salud con persistencia SQLite
"""
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "kalmiya.db"


def _conn():
    c = sqlite3.connect(str(DB_PATH))
    c.execute("""CREATE TABLE IF NOT EXISTS health_activities (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        type      TEXT NOT NULL,
        duration  INTEGER NOT NULL,
        intensity TEXT DEFAULT 'moderate'
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS vital_signs (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp      DATETIME DEFAULT CURRENT_TIMESTAMP,
        heart_rate     INTEGER,
        blood_pressure TEXT,
        temperature    REAL
    )""")
    c.commit()
    return c


class HealthTracker:

    def log_activity(self, activity_type: str, duration: int,
                     intensity: str = "moderate") -> bool:
        """Registra una actividad física en la BD."""
        try:
            conn = _conn()
            conn.execute(
                "INSERT INTO health_activities (type, duration, intensity) "
                "VALUES (?,?,?)",
                (activity_type, int(duration), intensity)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[HealthTracker] Error: {e}")
            return False

    def log_vital_signs(self, heart_rate: int,
                         blood_pressure: str,
                         temperature: float) -> bool:
        """Registra signos vitales en la BD."""
        try:
            conn = _conn()
            conn.execute(
                "INSERT INTO vital_signs (heart_rate, blood_pressure, temperature) "
                "VALUES (?,?,?)",
                (int(heart_rate), str(blood_pressure), float(temperature))
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[HealthTracker] Error: {e}")
            return False

    def get_health_summary(self) -> dict:
        """Resumen completo de salud desde la BD."""
        try:
            conn = _conn()
            n_act = conn.execute("SELECT COUNT(*) FROM health_activities").fetchone()[0]
            n_vit = conn.execute("SELECT COUNT(*) FROM vital_signs").fetchone()[0]

            # Última semana de actividades
            semana = conn.execute(
                "SELECT type, SUM(duration) FROM health_activities "
                "WHERE timestamp >= datetime('now','-7 days') "
                "GROUP BY type"
            ).fetchall()

            # Última lectura vital
            ultima = conn.execute(
                "SELECT heart_rate, blood_pressure, temperature, timestamp "
                "FROM vital_signs ORDER BY id DESC LIMIT 1"
            ).fetchone()
            conn.close()

            status = "saludable"
            if ultima and ultima[0]:
                hr = ultima[0]
                if hr > 100 or hr < 50:
                    status = "revisar frecuencia cardíaca"

            return {
                "activities":     n_act,
                "vital_readings": n_vit,
                "status":         status,
                "semana":         {r[0]: r[1] for r in semana},
                "ultima_vital":   {
                    "frecuencia":    ultima[0] if ultima else None,
                    "presion":       ultima[1] if ultima else None,
                    "temperatura":   ultima[2] if ultima else None,
                    "timestamp":     ultima[3] if ultima else None,
                } if ultima else {}
            }
        except Exception as e:
            return {"error": str(e)}

    def get_activity_history(self, limit: int = 20) -> list[dict]:
        """Devuelve el historial de actividades."""
        try:
            conn = _conn()
            rows = conn.execute(
                "SELECT timestamp, type, duration, intensity "
                "FROM health_activities ORDER BY id DESC LIMIT ?",
                (limit,)
            ).fetchall()
            conn.close()
            return [{"timestamp": r[0], "type": r[1],
                     "duration": r[2], "intensity": r[3]} for r in rows]
        except Exception:
            return []

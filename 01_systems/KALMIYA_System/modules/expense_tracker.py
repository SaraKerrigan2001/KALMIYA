"""
expense_tracker.py — Registro de Gastos con persistencia SQLite
"""
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "kalmiya.db"


def _conn():
    c = sqlite3.connect(str(DB_PATH))
    c.execute("""CREATE TABLE IF NOT EXISTS expenses (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP,
        category    TEXT NOT NULL,
        amount      REAL NOT NULL,
        description TEXT DEFAULT ''
    )""")
    c.commit()
    return c


class ExpenseTracker:

    def add_expense(self, category: str, amount: float,
                    description: str = "") -> bool:
        """Registra un nuevo gasto en la BD."""
        try:
            conn = _conn()
            conn.execute(
                "INSERT INTO expenses (category, amount, description) VALUES (?,?,?)",
                (category, float(amount), description)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ExpenseTracker] Error: {e}")
            return False

    def get_monthly_summary(self, month: int = None,
                             year: int = None) -> dict:
        """Resumen de gastos del mes indicado (o mes actual)."""
        now   = datetime.now()
        month = month or now.month
        year  = year  or now.year
        try:
            conn  = _conn()
            rows  = conn.execute(
                "SELECT category, amount FROM expenses "
                "WHERE strftime('%m', timestamp) = ? "
                "AND   strftime('%Y', timestamp) = ?",
                (f"{month:02d}", str(year))
            ).fetchall()
            conn.close()
            total = sum(r[1] for r in rows)
            by_cat: dict[str, float] = {}
            for cat, amt in rows:
                by_cat[cat] = round(by_cat.get(cat, 0) + amt, 2)
            return {"month": month, "year": year,
                    "total": round(total, 2), "by_category": by_cat}
        except Exception as e:
            return {"error": str(e)}

    def get_budget_status(self, budget: float = 500_000) -> dict:
        """Compara gasto actual del mes con el presupuesto."""
        summary = self.get_monthly_summary()
        spent   = summary.get("total", 0)
        return {
            "budget":    budget,
            "spent":     spent,
            "remaining": round(budget - spent, 2),
            "over":      spent > budget,
        }

    def get_all_expenses(self, limit: int = 50) -> list[dict]:
        """Devuelve los últimos N gastos."""
        try:
            conn = _conn()
            rows = conn.execute(
                "SELECT timestamp, category, amount, description "
                "FROM expenses ORDER BY id DESC LIMIT ?",
                (limit,)
            ).fetchall()
            conn.close()
            return [{"timestamp": r[0], "category": r[1],
                     "amount": r[2], "description": r[3]} for r in rows]
        except Exception:
            return []

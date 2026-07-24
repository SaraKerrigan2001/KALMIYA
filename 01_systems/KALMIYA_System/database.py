"""
KALMIYA Neural Memory Database

Manages persistent storage for command history, autonomous thoughts,
and user memory using SQLite. All KALMIYA data persists here.

Esquema v2 (julio 2026):
  - command_history  : historial de comandos (máx 2000 filas via trigger)
  - neural_thoughts  : pensamientos autónomos (máx 5000 filas via trigger)
  - user_memory      : memoria clave/valor de Sara (last_updated auto via trigger)
  - memory_audit     : auditoría de cambios en user_memory
"""

import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from kalmiya_restrictions import (
    validate_source,
    validate_command_history_row,
    validate_memory_row,
    validate_thought,
    check_rate_limit,
)

logger = logging.getLogger(__name__)

# Database path — defaults to a file in the package directory
DB_PATH: str = str(Path(__file__).parent / "kalmiya.db")

# ── DDL ───────────────────────────────────────────────────────────────────────

_TABLES = [
    # Historial de comandos
    """
    CREATE TABLE IF NOT EXISTS command_history (
        id        INTEGER  PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                           CHECK(timestamp >= '2024-01-01'),
        command   TEXT     NOT NULL DEFAULT ''
                           CHECK(LENGTH(TRIM(command)) > 0),
        response  TEXT     CHECK(response IS NULL OR LENGTH(response) <= 50000),
        source    TEXT     NOT NULL DEFAULT 'ui'
                           CHECK(LENGTH(TRIM(source)) > 0 AND LENGTH(source) <= 32)
    )
    """,
    # Pensamientos autónomos de KALMIYA
    """
    CREATE TABLE IF NOT EXISTS neural_thoughts (
        id        INTEGER  PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                           CHECK(timestamp >= '2024-01-01'),
        thought   TEXT     NOT NULL DEFAULT ''
                           CHECK(LENGTH(TRIM(thought)) >= 3 AND LENGTH(thought) <= 10000)
    )
    """,
    # Memoria persistente de Sara
    """
    CREATE TABLE IF NOT EXISTS user_memory (
        key          TEXT     PRIMARY KEY
                              CHECK(LENGTH(TRIM(key)) >= 2 AND LENGTH(key) <= 64
                                    AND key GLOB '[A-Za-z0-9_-]*'),
        value        TEXT     NOT NULL
                              CHECK(LENGTH(value) <= 10000),
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """,
    # Auditoría de cambios en user_memory
    """
    CREATE TABLE IF NOT EXISTS memory_audit (
        id        INTEGER  PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        key       TEXT     NOT NULL
                           CHECK(LENGTH(TRIM(key)) >= 2),
        old_value TEXT,
        new_value TEXT     NOT NULL
                           CHECK(LENGTH(new_value) <= 10000),
        action    TEXT     NOT NULL DEFAULT 'UPDATE'
                           CHECK(action IN ('INSERT', 'UPDATE', 'DELETE'))
    )
    """,
]

_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_cmd_timestamp ON command_history(timestamp DESC)",
    "CREATE INDEX IF NOT EXISTS idx_cmd_source    ON command_history(source)",
    "CREATE INDEX IF NOT EXISTS idx_thoughts_ts   ON neural_thoughts(timestamp DESC)",
]

_TRIGGERS = [
    # ── Límite de filas en command_history (máx 2000) ────────────────────────
    ("trg_command_history_limit", """
    CREATE TRIGGER IF NOT EXISTS trg_command_history_limit
    AFTER INSERT ON command_history
    BEGIN
        DELETE FROM command_history
        WHERE id IN (
            SELECT id FROM command_history
            ORDER BY id DESC
            LIMIT -1 OFFSET 2000
        );
    END
    """),
    # ── Límite de filas en neural_thoughts (máx 5000) ────────────────────────
    ("trg_neural_thoughts_limit", """
    CREATE TRIGGER IF NOT EXISTS trg_neural_thoughts_limit
    AFTER INSERT ON neural_thoughts
    BEGIN
        DELETE FROM neural_thoughts
        WHERE id IN (
            SELECT id FROM neural_thoughts
            ORDER BY id DESC
            LIMIT -1 OFFSET 5000
        );
    END
    """),
    # ── Auto-actualizar last_updated en user_memory ───────────────────────────
    ("trg_user_memory_updated", """
    CREATE TRIGGER IF NOT EXISTS trg_user_memory_updated
    AFTER UPDATE OF value ON user_memory
    BEGIN
        UPDATE user_memory
        SET last_updated = STRFTIME('%Y-%m-%dT%H:%M:%f', 'now', 'localtime')
        WHERE key = NEW.key;
    END
    """),
    # ── Auditoría: registrar UPDATE en user_memory ────────────────────────────
    ("trg_memory_audit_update", """
    CREATE TRIGGER IF NOT EXISTS trg_memory_audit_update
    AFTER UPDATE OF value ON user_memory
    WHEN OLD.value != NEW.value
    BEGIN
        INSERT INTO memory_audit (key, old_value, new_value, action)
        VALUES (NEW.key, OLD.value, NEW.value, 'UPDATE');
    END
    """),
    # ── Auditoría: registrar INSERT en user_memory ────────────────────────────
    # NOTA: INSERT OR REPLACE hace DELETE+INSERT internamente en SQLite,
    # así que capturamos ambos como INSERT y distinguimos por old_value NULL
    ("trg_memory_audit_insert", """
    CREATE TRIGGER IF NOT EXISTS trg_memory_audit_insert
    AFTER INSERT ON user_memory
    BEGIN
        INSERT INTO memory_audit (key, old_value, new_value, action)
        VALUES (
            NEW.key,
            NULL,
            NEW.value,
            CASE WHEN (SELECT COUNT(*) FROM memory_audit WHERE key = NEW.key) > 0
                 THEN 'UPDATE' ELSE 'INSERT' END
        );
    END
    """),
]

# ── Conexión ──────────────────────────────────────────────────────────────────

def _get_connection() -> sqlite3.Connection:
    """Devuelve una conexión SQLite con foreign_keys activo."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ── Inicialización ────────────────────────────────────────────────────────────

def init_db() -> None:
    """Crea tablas, índices y triggers si no existen. Idempotente y seguro.

    Esquema v2:
      - command_history  (NOT NULL, índices, trigger de límite 2000)
      - neural_thoughts  (NOT NULL, índice, trigger de límite 5000)
      - user_memory      (trigger auto last_updated + auditoría)
      - memory_audit     (registro de cambios en user_memory)
    """
    conn = _get_connection()
    try:
        cursor = conn.cursor()

        # Tablas
        for ddl in _TABLES:
            cursor.execute(ddl)

        # Índices
        for ddl in _INDEXES:
            cursor.execute(ddl)

        # Triggers — SQLite no soporta CREATE TRIGGER IF NOT EXISTS en todas las
        # versiones, así que verificamos manualmente antes de crear
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='trigger'"
        )
        existing_triggers = {row[0] for row in cursor.fetchall()}

        for name, ddl in _TRIGGERS:
            if name not in existing_triggers:
                cursor.execute(ddl)
                logger.debug(f"Trigger creado: {name}")

        conn.commit()
        logger.info("Database v2 initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    finally:
        conn.close()

# ── Operaciones ───────────────────────────────────────────────────────────────

def log_command(command: str, response: str, source: str = "ui") -> None:
    """Registra un comando en el historial.

    Args:
        command:  Texto del comando ejecutado.
        response: Respuesta o resultado.
        source:   Origen del comando (voice, ui, remote, ai-*, etc.)
    """
    # ── Restricciones ──────────────────────────────────────────────────────
    source = validate_source(source)

    ok, msg = validate_command_history_row(command, response, source)
    if not ok:
        logger.warning(f"[DB] log_command bloqueado — {msg}")
        return

    within_limit, limit_msg = check_rate_limit(source)
    if not within_limit:
        logger.warning(f"[DB] log_command rate limit — {limit_msg}")
        return

    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO command_history (command, response, source) VALUES (?, ?, ?)",
            (command.strip() or "[vacío]", response, source),
        )
        conn.commit()
        logger.debug(f"Logged command from {source}: {command[:50]}...")
    except sqlite3.IntegrityError as e:
        logger.error(f"[DB] CHECK constraint violado en command_history: {e}")
    except sqlite3.Error as e:
        logger.error(f"Failed to log command: {e}")
    finally:
        conn.close()


def save_thought(thought: str) -> None:
    """Guarda un pensamiento autónomo de KALMIYA."""
    # ── Restricciones ──────────────────────────────────────────────────────
    ok, msg = validate_thought(thought)
    if not ok:
        logger.warning(f"[DB] save_thought bloqueado — {msg}")
        return

    within_limit, limit_msg = check_rate_limit("autonomous")
    if not within_limit:
        logger.warning(f"[DB] save_thought rate limit — {limit_msg}")
        return

    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO neural_thoughts (thought) VALUES (?)",
            (thought.strip(),),
        )
        conn.commit()
        logger.debug(f"Saved thought: {thought[:50]}...")
    except sqlite3.IntegrityError as e:
        logger.error(f"[DB] CHECK constraint violado en neural_thoughts: {e}")
    except sqlite3.Error as e:
        logger.error(f"Failed to save thought: {e}")
    finally:
        conn.close()


def get_recent_history(limit: int = 20) -> list[tuple[str, str, str]]:
    """Devuelve los últimos N registros del historial de comandos.

    Returns:
        Lista de (timestamp, command, response) ordenada por más reciente primero.
    """
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT timestamp, command, response
               FROM command_history
               ORDER BY id DESC
               LIMIT ?""",
            (limit,),
        )
        rows = cursor.fetchall()
        logger.debug(f"Retrieved {len(rows)} history records")
        return rows
    except sqlite3.Error as e:
        logger.error(f"Failed to retrieve history: {e}")
        return []
    finally:
        conn.close()


def update_memory(key: str, value: str) -> None:
    """Crea o actualiza un par clave/valor en la memoria de Sara.
    El trigger trg_user_memory_updated actualiza last_updated automáticamente.
    """
    # ── Restricciones ──────────────────────────────────────────────────────
    ok, msg = validate_memory_row(key, value)
    if not ok:
        logger.warning(f"[DB] update_memory bloqueado — {msg}")
        return

    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO user_memory (key, value, last_updated) VALUES (?, ?, ?)",
            (key.strip(), value, datetime.now().isoformat()),
        )
        conn.commit()
        logger.debug(f"Updated memory: {key}")
    except sqlite3.IntegrityError as e:
        logger.error(f"[DB] CHECK constraint violado en user_memory: {e} (key={key})")
    except sqlite3.Error as e:
        logger.error(f"Failed to update memory: {e}")
    finally:
        conn.close()


def get_memory(key: str) -> str | None:
    """Recupera un valor de memoria por su clave."""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM user_memory WHERE key = ?", (key,))
        row = cursor.fetchone()
        if row:
            logger.debug(f"Retrieved memory: {key}")
            return row[0]
        logger.debug(f"Memory key not found: {key}")
        return None
    except sqlite3.Error as e:
        logger.error(f"Failed to retrieve memory: {e}")
        return None
    finally:
        conn.close()


def get_memory_audit(key: str = None, limit: int = 20) -> list[dict]:
    """Devuelve el historial de cambios en user_memory.

    Args:
        key:   Filtrar por clave específica. None = todas las claves.
        limit: Máximo de registros a devolver.
    Returns:
        Lista de dicts con timestamp, key, old_value, new_value, action.
    """
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        if key:
            cursor.execute(
                """SELECT timestamp, key, old_value, new_value, action
                   FROM memory_audit WHERE key = ?
                   ORDER BY id DESC LIMIT ?""",
                (key, limit),
            )
        else:
            cursor.execute(
                """SELECT timestamp, key, old_value, new_value, action
                   FROM memory_audit
                   ORDER BY id DESC LIMIT ?""",
                (limit,),
            )
        cols = ["timestamp", "key", "old_value", "new_value", "action"]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        logger.error(f"Failed to retrieve memory audit: {e}")
        return []
    finally:
        conn.close()


def get_db_stats() -> dict:
    """Devuelve estadísticas de la base de datos."""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        stats = {}
        for tabla in ("command_history", "neural_thoughts", "user_memory", "memory_audit"):
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            stats[tabla] = cursor.fetchone()[0]
        cursor.execute("PRAGMA page_count")
        pages = cursor.fetchone()[0]
        cursor.execute("PRAGMA page_size")
        page_size = cursor.fetchone()[0]
        stats["size_kb"] = round((pages * page_size) / 1024, 1)
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='trigger'"
        )
        stats["triggers"] = [r[0] for r in cursor.fetchall()]
        return stats
    except sqlite3.Error as e:
        logger.error(f"Failed to get DB stats: {e}")
        return {}
    finally:
        conn.close()


if __name__ == "__main__":
    from _logging import setup_logging
    setup_logging()
    init_db()
    stats = get_db_stats()
    print(f"DB stats: {stats}")

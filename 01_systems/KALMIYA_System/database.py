"""
KALMIYA Neural Memory Database

Manages persistent storage for command history, autonomous thoughts,
and user memory using PostgreSQL. All KALMIYA data persists here.

Esquema v2 (PostgreSQL):
  - command_history  : historial de comandos (máx 2000 filas via trigger)
  - neural_thoughts  : pensamientos autónomos (máx 5000 filas via trigger)
  - user_memory      : memoria clave/valor de Sara (last_updated auto via trigger)
  - memory_audit     : auditoría de cambios en user_memory
"""

import os
import logging
from datetime import datetime
from pathlib import Path
import psycopg2
from psycopg2 import IntegrityError, Error as PostgresError
from psycopg2 import pool as pg_pool
from kalmiya_restrictions import (
    validate_source,
    validate_command_history_row,
    validate_memory_row,
    validate_thought,
    check_rate_limit,
)

logger = logging.getLogger(__name__)

# Postgres DB URL — apunta al servicio 'db' definido en docker-compose
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1234@db:5432/postgres")

# ── Pool de Conexiones ────────────────────────────────────────────────────────
# Se inicializa de forma perezosa (lazy) la primera vez que se necesita.
# Mantiene entre 2 y 10 conexiones abiertas y listas para reutilizar.
_connection_pool: pg_pool.SimpleConnectionPool | None = None


def _get_pool() -> pg_pool.SimpleConnectionPool:
    """Devuelve el pool de conexiones, creándolo si es la primera vez."""
    global _connection_pool
    if _connection_pool is None or _connection_pool.closed:
        logger.info("Inicializando pool de conexiones PostgreSQL...")
        _connection_pool = pg_pool.SimpleConnectionPool(
            minconn=2,
            maxconn=10,
            dsn=DATABASE_URL,
        )
        logger.info("Pool de conexiones listo (min=2, max=10).")
    return _connection_pool


def _get_connection():
    """Obtiene una conexión disponible del pool."""
    return _get_pool().getconn()


def _release_connection(conn) -> None:
    """Devuelve una conexión al pool para que pueda ser reutilizada."""
    try:
        _get_pool().putconn(conn)
    except Exception:
        pass  # Si el pool ya cerró, ignoramos el error

# ── DDL ───────────────────────────────────────────────────────────────────────

_TABLES = [
    # Historial de comandos
    """
    CREATE TABLE IF NOT EXISTS command_history (
        id        SERIAL PRIMARY KEY,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP CHECK(timestamp >= '2024-01-01'),
        command   TEXT NOT NULL DEFAULT '' CHECK(LENGTH(TRIM(command)) > 0),
        response  TEXT CHECK(response IS NULL OR LENGTH(response) <= 50000),
        source    TEXT NOT NULL DEFAULT 'ui' CHECK(LENGTH(TRIM(source)) > 0 AND LENGTH(source) <= 32)
    )
    """,
    # Pensamientos autónomos de KALMIYA
    """
    CREATE TABLE IF NOT EXISTS neural_thoughts (
        id        SERIAL PRIMARY KEY,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP CHECK(timestamp >= '2024-01-01'),
        thought   TEXT NOT NULL DEFAULT '' CHECK(LENGTH(TRIM(thought)) >= 3 AND LENGTH(thought) <= 10000)
    )
    """,
    # Memoria persistente de Sara
    """
    CREATE TABLE IF NOT EXISTS user_memory (
        key          TEXT PRIMARY KEY CHECK(LENGTH(TRIM(key)) >= 2 AND LENGTH(key) <= 64 AND key ~ '^[A-Za-z0-9_-]*$'),
        value        TEXT NOT NULL CHECK(LENGTH(value) <= 10000),
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    # Auditoría de cambios en user_memory
    """
    CREATE TABLE IF NOT EXISTS memory_audit (
        id        SERIAL PRIMARY KEY,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        key       TEXT NOT NULL CHECK(LENGTH(TRIM(key)) >= 2),
        old_value TEXT,
        new_value TEXT NOT NULL CHECK(LENGTH(new_value) <= 10000),
        action    TEXT NOT NULL DEFAULT 'UPDATE' CHECK(action IN ('INSERT', 'UPDATE', 'DELETE'))
    )
    """
]

_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_cmd_timestamp ON command_history(timestamp DESC)",
    "CREATE INDEX IF NOT EXISTS idx_cmd_source ON command_history(source)",
    "CREATE INDEX IF NOT EXISTS idx_thoughts_ts ON neural_thoughts(timestamp DESC)",
]

_TRIGGERS = [
    # ── Límite de filas en command_history (máx 2000) ────────────────────────
    """
    CREATE OR REPLACE FUNCTION fn_command_history_limit() RETURNS TRIGGER AS $$
    BEGIN
        DELETE FROM command_history
        WHERE id IN (
            SELECT id FROM command_history
            ORDER BY id DESC
            OFFSET 2000
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    DROP TRIGGER IF EXISTS trg_command_history_limit ON command_history;
    CREATE TRIGGER trg_command_history_limit
    AFTER INSERT ON command_history
    FOR EACH STATEMENT
    EXECUTE FUNCTION fn_command_history_limit();
    """,

    # ── Límite de filas en neural_thoughts (máx 5000) ────────────────────────
    """
    CREATE OR REPLACE FUNCTION fn_neural_thoughts_limit() RETURNS TRIGGER AS $$
    BEGIN
        DELETE FROM neural_thoughts
        WHERE id IN (
            SELECT id FROM neural_thoughts
            ORDER BY id DESC
            OFFSET 5000
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    DROP TRIGGER IF EXISTS trg_neural_thoughts_limit ON neural_thoughts;
    CREATE TRIGGER trg_neural_thoughts_limit
    AFTER INSERT ON neural_thoughts
    FOR EACH STATEMENT
    EXECUTE FUNCTION fn_neural_thoughts_limit();
    """,

    # ── Auto-actualizar last_updated en user_memory ───────────────────────────
    """
    CREATE OR REPLACE FUNCTION fn_user_memory_updated() RETURNS TRIGGER AS $$
    BEGIN
        NEW.last_updated = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    DROP TRIGGER IF EXISTS trg_user_memory_updated ON user_memory;
    CREATE TRIGGER trg_user_memory_updated
    BEFORE UPDATE OF value ON user_memory
    FOR EACH ROW
    EXECUTE FUNCTION fn_user_memory_updated();
    """,

    # ── Auditoría: registrar UPDATE en user_memory ────────────────────────────
    """
    CREATE OR REPLACE FUNCTION fn_memory_audit_update() RETURNS TRIGGER AS $$
    BEGIN
        IF OLD.value IS DISTINCT FROM NEW.value THEN
            INSERT INTO memory_audit (key, old_value, new_value, action)
            VALUES (NEW.key, OLD.value, NEW.value, 'UPDATE');
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    DROP TRIGGER IF EXISTS trg_memory_audit_update ON user_memory;
    CREATE TRIGGER trg_memory_audit_update
    AFTER UPDATE OF value ON user_memory
    FOR EACH ROW
    EXECUTE FUNCTION fn_memory_audit_update();
    """,

    # ── Auditoría: registrar INSERT en user_memory ────────────────────────────
    """
    CREATE OR REPLACE FUNCTION fn_memory_audit_insert() RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO memory_audit (key, old_value, new_value, action)
        VALUES (
            NEW.key,
            NULL,
            NEW.value,
            CASE WHEN (SELECT COUNT(*) FROM memory_audit WHERE key = NEW.key) > 0 THEN 'UPDATE' ELSE 'INSERT' END
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    DROP TRIGGER IF EXISTS trg_memory_audit_insert ON user_memory;
    CREATE TRIGGER trg_memory_audit_insert
    AFTER INSERT ON user_memory
    FOR EACH ROW
    EXECUTE FUNCTION fn_memory_audit_insert();
    """
]

# ── Conexión (gestionada por el pool; ver arriba) ─────────────────────────────

# ── Inicialización ────────────────────────────────────────────────────────────

def init_db() -> None:
    conn = _get_connection()
    try:
        cursor = conn.cursor()

        for ddl in _TABLES:
            cursor.execute(ddl)

        for ddl in _INDEXES:
            cursor.execute(ddl)

        for ddl in _TRIGGERS:
            cursor.execute(ddl)

        conn.commit()
        logger.info("Database Postgres initialized successfully.")
    except PostgresError as e:
        logger.error(f"Failed to initialize database: {e}")
        conn.rollback()
        raise
    finally:
        _release_connection(conn)

# ── Operaciones ───────────────────────────────────────────────────────────────

def log_command(command: str, response: str, source: str = "ui") -> None:
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
            "INSERT INTO command_history (command, response, source) VALUES (%s, %s, %s)",
            (command.strip() or "[vacío]", response, source),
        )
        conn.commit()
        logger.debug(f"Logged command from {source}: {command[:50]}...")
    except IntegrityError as e:
        logger.error(f"[DB] CHECK constraint violado en command_history: {e}")
    except PostgresError as e:
        logger.error(f"Failed to log command: {e}")
    finally:
        _release_connection(conn)

def save_thought(thought: str) -> None:
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
            "INSERT INTO neural_thoughts (thought) VALUES (%s)",
            (thought.strip(),),
        )
        conn.commit()
        logger.debug(f"Saved thought: {thought[:50]}...")
    except IntegrityError as e:
        logger.error(f"[DB] CHECK constraint violado en neural_thoughts: {e}")
    except PostgresError as e:
        logger.error(f"Failed to save thought: {e}")
    finally:
        _release_connection(conn)

def get_recent_history(limit: int = 20) -> list[tuple[str, str, str]]:
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT timestamp, command, response FROM command_history ORDER BY id DESC LIMIT %s",
            (limit,),
        )
        rows = cursor.fetchall()
        return rows
    except PostgresError as e:
        logger.error(f"Failed to retrieve history: {e}")
        return []
    finally:
        _release_connection(conn)

def update_memory(key: str, value: str) -> None:
    ok, msg = validate_memory_row(key, value)
    if not ok:
        logger.warning(f"[DB] update_memory bloqueado — {msg}")
        return

    conn = _get_connection()
    try:
        cursor = conn.cursor()
        # PostgreSQL doesn't have INSERT OR REPLACE. We use INSERT ... ON CONFLICT
        cursor.execute(
            "INSERT INTO user_memory (key, value, last_updated) VALUES (%s, %s, %s) ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
            (key.strip(), value, datetime.now().isoformat()),
        )
        conn.commit()
    except IntegrityError as e:
        logger.error(f"[DB] CHECK constraint violado en user_memory: {e} (key={key})")
    except PostgresError as e:
        logger.error(f"Failed to update memory: {e}")
    finally:
        _release_connection(conn)

def get_memory(key: str) -> str | None:
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM user_memory WHERE key = %s", (key,))
        row = cursor.fetchone()
        if row:
            return row[0]
        return None
    except PostgresError as e:
        logger.error(f"Failed to retrieve memory: {e}")
        return None
    finally:
        _release_connection(conn)

def get_memory_audit(key: str = None, limit: int = 20) -> list[dict]:
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        if key:
            cursor.execute(
                "SELECT timestamp, key, old_value, new_value, action FROM memory_audit WHERE key = %s ORDER BY id DESC LIMIT %s",
                (key, limit),
            )
        else:
            cursor.execute(
                "SELECT timestamp, key, old_value, new_value, action FROM memory_audit ORDER BY id DESC LIMIT %s",
                (limit,),
            )
        cols = ["timestamp", "key", "old_value", "new_value", "action"]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]
    except PostgresError as e:
        logger.error(f"Failed to retrieve memory audit: {e}")
        return []
    finally:
        _release_connection(conn)

def get_db_stats() -> dict:
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        stats = {}
        for tabla in ("command_history", "neural_thoughts", "user_memory", "memory_audit"):
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            stats[tabla] = cursor.fetchone()[0]

        cursor.execute("SELECT pg_database_size(current_database())")
        size_bytes = cursor.fetchone()[0]
        stats["size_kb"] = round(size_bytes / 1024, 1)

        cursor.execute("SELECT trigger_name FROM information_schema.triggers WHERE trigger_schema = 'public'")
        stats["triggers"] = [r[0] for r in cursor.fetchall()]

        return stats
    except PostgresError as e:
        logger.error(f"Failed to get DB stats: {e}")
        return {}
    finally:
        _release_connection(conn)

if __name__ == "__main__":
    from _logging import setup_logging
    setup_logging()
    init_db()
    stats = get_db_stats()
    print(f"DB stats: {stats}")

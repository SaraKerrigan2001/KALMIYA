from pathlib import Path
import sys

# Añade la ruta al núcleo de KALMIYA para que los tests puedan importar los paquetes locales.
ROOT = Path(__file__).resolve().parents[1]
KALMIYA_SYS = ROOT / "01_systems" / "KALMIYA_System"

if str(KALMIYA_SYS) not in sys.path:
    sys.path.insert(0, str(KALMIYA_SYS))

# También añadir la raíz del repo por si algún test importa desde la raíz.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from core import database

@pytest.fixture(scope="session")
def setup_test_db():
    default_db_url = "postgresql://postgres:1234@localhost:5432/postgres"
    test_db_name = "test_kalmiya_db"
    
    try:
        conn = psycopg2.connect(default_db_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {test_db_name}")
        cursor.execute(f"CREATE DATABASE {test_db_name}")
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        pytest.skip(f"Could not connect to PostgreSQL to create test database: {e}")
        return None

    test_db_url = f"postgresql://postgres:1234@localhost:5432/{test_db_name}"
    yield test_db_url
    
    try:
        conn = psycopg2.connect(default_db_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '{test_db_name}' AND pid <> pg_backend_pid();")
        cursor.execute(f"DROP DATABASE IF EXISTS {test_db_name}")
        cursor.close()
        conn.close()
    except psycopg2.Error:
        pass


@pytest.fixture(autouse=True)
def mock_db(setup_test_db, monkeypatch):
    if not setup_test_db:
        pytest.skip("Test database not available")
        
    monkeypatch.setenv("DATABASE_URL", setup_test_db)
    
    # Patch all loaded versions of the database module
    for name, mod in sys.modules.items():
        if name.endswith("database") and hasattr(mod, "DATABASE_URL"):
            monkeypatch.setattr(mod, "DATABASE_URL", setup_test_db)
            if hasattr(mod, "_connection_pool") and getattr(mod, "_connection_pool") is not None and not getattr(mod, "_connection_pool").closed:
                mod._connection_pool.closeall()
                mod._connection_pool = None

    # Try to initialize the schema
    try:
        from core import database
        database.init_db()
        conn = database._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE command_history, neural_thoughts, user_memory, memory_audit RESTART IDENTITY CASCADE;")
            conn.commit()
        finally:
            database._release_connection(conn)
    except Exception:
        pass
    
    yield

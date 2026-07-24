import os
import gc
import tempfile
import shutil

# pyrefly: ignore [missing-import]
import pytest

# Import the module under test
import sys
sys.path.insert(0, 'c:/Users/maria/env/KALMIYA_System')
# pyrefly: ignore [missing-import]
import database


@pytest.fixture
def temp_db_path():
    """Provide a fresh temporary database for each test.

    Overrides database.DB_PATH so all functions operate on the temp DB,
    then cleans up after the test finishes.
    """
    temp_dir = tempfile.mkdtemp()
    orig_db_path = database.DB_PATH
    new_path = os.path.join(temp_dir, 'test_kalmiya.db')
    database.DB_PATH = new_path
    # Initialise a fresh database
    database.init_db()
    yield new_path
    # Restore original DB_PATH first (stops new connections to temp file)
    database.DB_PATH = orig_db_path
    # Force garbage collection to release any lingering SQLite connections
    gc.collect()
    # Clean up temp directory (ignore errors on Windows file locks)
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_init_db_creates_file(temp_db_path):
    assert os.path.isfile(temp_db_path), "Database file should be created"


def test_init_db_creates_tables(temp_db_path):
    import sqlite3
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}
    conn.close()
    assert 'command_history' in tables
    assert 'neural_thoughts' in tables
    assert 'user_memory' in tables


def test_log_command_and_history(temp_db_path):
    database.log_command('test command', 'test response', source='ui')
    history = database.get_recent_history(limit=5)
    assert len(history) == 1
    timestamp, command, response = history[0]
    assert command == 'test command'
    assert response == 'test response'


def test_memory_update_and_retrieve(temp_db_path):
    database.update_memory('favorite_color', 'azul')
    value = database.get_memory('favorite_color')
    assert value == 'azul'
    assert database.get_memory('nonexistent_key') is None

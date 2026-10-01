import os
import pytest
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Import the module under test
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../01_systems')))
# pyrefly: ignore [missing-import]
from KALMIYA_System.core import database





def test_init_db_creates_tables():
    conn = database._get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = {row[0] for row in cursor.fetchall()}
    finally:
        database._release_connection(conn)
        
    assert 'command_history' in tables
    assert 'neural_thoughts' in tables
    assert 'user_memory' in tables
    assert 'memory_audit' in tables


def test_log_command_and_history():
    database.log_command('test command', 'test response', source='ui')
    history = database.get_recent_history(limit=5)
    assert len(history) == 1
    timestamp, command, response = history[0]
    assert command == 'test command'
    assert response == 'test response'


def test_memory_update_and_retrieve():
    database.update_memory('favorite_color', 'azul')
    value = database.get_memory('favorite_color')
    assert value == 'azul'
    assert database.get_memory('nonexistent_key') is None


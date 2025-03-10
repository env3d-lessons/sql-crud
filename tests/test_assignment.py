import sqlite3
import pytest
from unittest.mock import MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import app  # Assuming your script is named `app.py`    

@pytest.fixture
def mock_conn():
    """Creates an in-memory SQLite database and injects it into the module."""
    test_conn = sqlite3.connect(":memory:")  # Use an in-memory database for testing
    app.conn = test_conn  # Override the connection in the app
    """Creates the users table if it doesn't exist."""
    test_conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    age INTEGER NOT NULL
    )
    """)
    
    yield test_conn
    test_conn.close()  # Clean up after tests

def test_create_user(mock_conn):
    """Test adding a user."""
    assert app.create_user("Alice", 25) == True
    users = app.list_users()
    assert len(users) == 1
    assert users[0][1] == "Alice"
    assert users[0][2] == 25

def test_list_users(mock_conn):
    """Test retrieving users."""
    app.create_user("Charlie", 40)
    app.create_user("Dana", 28)
    users = app.list_users()
    assert len(users) == 2
    assert users[0][1] == "Charlie"
    assert users[1][1] == "Dana"

def test_update_user(mock_conn):
    """Test updating a user's age."""
    uid = app.create_user("Eve", 22)
    assert app.update_user(uid, "Eve", 30) == True  # Should return True
    users = app.list_users()
    assert users[0][1] == "Eve"
    assert users[0][2] == 30  # Age should be updated

def test_update_nonexistent_user(mock_conn):
    """Test updating a user that doesn't exist (should return False)."""
    assert app.update_user(91034, "Nonexistent", 50) == False

def test_delete_user(mock_conn):
    """Test deleting a user."""
    uid = app.create_user("Frank", 33)
    assert app.delete_user(uid) == True
    users = app.list_users()
    assert len(users) == 0  # User should be removed

def test_delete_nonexistent_user(mock_conn):
    """Test deleting a user that doesn't exist (should return False)."""
    assert app.delete_user("Ghost") == False

def test_serach_user(mock_conn):
    app.create_user("Frank1", 33)
    app.create_user("Frank2", 33)
    app.create_user("Frank3", 33)
    assert len(app.search_user("Frank2")) == 1

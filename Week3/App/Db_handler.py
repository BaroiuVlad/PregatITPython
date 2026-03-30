import sqlite3

DB_NAME = "tasks.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    query = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        owner TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at REAL NOT NULL,
        updated_at REAL NOT NULL
    );
    """
    with get_db_connection() as conn:
        conn.execute(query)
        conn.commit()
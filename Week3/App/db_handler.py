import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_db_connection():
    # Requirement 1: Reads from .env variables
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "db"),
        database=os.getenv("POSTGRES_DB", "task_db"),
        user=os.getenv("POSTGRES_USER", "myuser"),
        password=os.getenv("POSTGRES_PASSWORD", "mypassword"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        cursor_factory=RealDictCursor # <--- CRITICAL for PostgreSQL dictionary access
    )

def create_tables():
    # Requirement 5: Automatic DB Initialization
    query = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        owner TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at DOUBLE PRECISION NOT NULL,
        updated_at DOUBLE PRECISION NOT NULL
    );
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    finally:
        conn.close()
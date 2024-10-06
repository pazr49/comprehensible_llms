import sqlite3

def get_db_connection():
    conn = sqlite3.connect('story_sessions.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS story_sessions (
                session_id TEXT PRIMARY KEY,
                story_id INTEGER,
                story_title TEXT,
                conversation TEXT,
                language TEXT,
                level TEXT,
                setting TEXT
            )
        ''')
    conn.close()
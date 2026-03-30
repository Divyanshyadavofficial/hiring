import sqlite3


def get_connection():
    conn = sqlite3.connect("hiring.db")
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_descriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jd_text TEXT)
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            resume_text TEXT,
            skills TEXT,
            uploaded_at DEFAULT CURRENT_TIMESTAMP)
    """)

    conn.commit()
    conn.close()
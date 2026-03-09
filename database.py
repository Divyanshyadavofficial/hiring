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

    conn.commit()
    conn.close()
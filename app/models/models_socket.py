import sqlite3
from datetime import datetime

DB_PATH = "instance/db.sqlite3"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'cliente',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turno (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            servicio TEXT NOT NULL,
            estado TEXT DEFAULT 'pendiente',
            FOREIGN KEY (cliente_id) REFERENCES user(id)
        )
    """)

    conn.commit()
    conn.close()
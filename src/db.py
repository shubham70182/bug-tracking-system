"""
SQLite database layer for the Bug Tracking System.
Handles table creation and basic CRUD operations.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = "data/bugs.db"


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bugs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT,
            severity TEXT,
            status TEXT DEFAULT 'Open',
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_bug(title, description, category, severity):
    conn = get_connection()
    conn.execute(
        "INSERT INTO bugs (title, description, category, severity, status, created_at) "
        "VALUES (?, ?, ?, ?, 'Open', ?)",
        (title, description, category, severity, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    conn.commit()
    bug_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return bug_id


def get_all_bugs():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM bugs ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_bugs_by_status(status):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM bugs WHERE status = ? ORDER BY id DESC", (status,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_status(bug_id, status):
    conn = get_connection()
    conn.execute("UPDATE bugs SET status = ? WHERE id = ?", (status, bug_id))
    conn.commit()
    conn.close()


def get_bug_count_by_category():
    conn = get_connection()
    rows = conn.execute("SELECT category, COUNT(*) as count FROM bugs GROUP BY category").fetchall()
    conn.close()
    return {r["category"]: r["count"] for r in rows}

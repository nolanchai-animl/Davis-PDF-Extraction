"""
db.py 
-------
Handles all database setup and interactive functions
"""

import sqlite3

def init_db(db_path: str) -> sqlite3.Connection:
    """Create database and tables"""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL;") # good practice to include
    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            filename    TEXT    NOT NULL,
            total_pages INTEGER NOT NULL,
            sacnned_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER NOT NULL REFERENCES documents(id),
            page_number INTEGER NOT NULL,
            text        TEXT,
            word_count  INTEGER,
            scanned_at  TEXT    NOT NULL DEFAULT (datetime('now')),
            UNIQUE(document_id, page_number)
        )
    """)
    conn.commit()
    return conn

def insert_document(conn: sqlite3.Connection, filename: str, total_pages: int) -> int:
    """Insert a document and return its ID"""
    cur = conn.execute() # not comeplete yet


    return cur.lastrowid
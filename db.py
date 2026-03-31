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
    cur = conn.execute(
        "INSERT INTO documents (filename, total_pages) VALUES (?, ?)",
        (filename, total_pages)
    )
    conn.commit()
    return cur.lastrowid

def insert_page(conn: sqlite3.Connection, document_id: int, page_number: int, text: str) -> None:
    """Insert a page record and update the full-text search index"""

    word_count = len(text.split()) if text else 0
    conn.execute(
        """
        INSERT OR REPLACE INTO pages (document_id, page_number, text, word_count)
        VALUES (?, ?, ?, ?)
        """, 
        (document_id, page_number, text, word_count)
    )
    conn.execute(
        "INSERT INTO pages_fts(rowid, text) VALUES (last_insert_rowid(), ?)", 
        (text,)
    )
    conn.commit()

def get_document(conn: sqlite3.Connection, document_id: int) -> dict | None:
    """Get document record by ID"""
    row = conn.execute(
        "SELECT id, filename, total_pages, scanned_at FROM documents WHERE id = ?",
        (document_id,)
    ).fetchone()
    if row:
        return {"id": row[0], "filename":row[1], "total_pages":row[2], "scanned_at":row[3]}
    return None

def search_pages(conn: sqlite3.Connection, query: str) -> list[dict]:
    """Full-text search across all scanned pages"""
    rows = conn.execute(
        """
        SELECT p.id, p.document_id, p.page_number, 
               snippet(pages_fts, 0, '[','], '...', 10) As snippet
        FROM pages_fts
        JOIN pages p ON pages_fts.rowid = p.id
        WHERE pages_fts MATCH ?
        """,
        (query,),
    ).fetchall()
    return [
        {"id": r[0], "document_id":r[1], "page_number":r[2], "snippet":r[3]}
        for r in rows
    ]
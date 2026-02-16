import sqlite3
import os

DB_PATH = "audit.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enable WAL mode for concurrency
    cursor.execute("PRAGMA journal_mode=WAL;")
    
    # Create files table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT NOT NULL,
        hash TEXT,
        size INTEGER,
        mtime REAL,
        scan_id TEXT,
        root_dir TEXT
    );
    """)
    
    # Create comparisons table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comparisons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_a TEXT,
        source_b TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT
    );
    """)

    # Create diffs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diffs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        comparison_id INTEGER,
        file_path TEXT,
        change_type TEXT, -- MODIFIED, ADDED, DELETED, RENAMED
        similarity_score REAL,
        diff_summary TEXT,
        FOREIGN KEY(comparison_id) REFERENCES comparisons(id)
    );
    """)

    conn.commit()
    conn.close()
    print(f"Initialized {DB_PATH} with schema.")

if __name__ == "__main__":
    init_db()

import sqlite3
import os
import json

# Use relative pathing for portability
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MEMORY_DB_PATH = os.path.join(BASE_DIR, "clide", "memory.db")

def ensure_db():
    """Initializes the database and ensures the schema is correct."""
    os.makedirs(os.path.dirname(MEMORY_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(MEMORY_DB_PATH)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            content TEXT,
            original_msg TEXT,
            importance INTEGER DEFAULT 5,
            embedding BLOB,
            session_id TEXT,
            message_id INTEGER,
            review TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER,
            target_id INTEGER,
            rel_type TEXT, -- 'DEPENDS_ON', 'SIMILAR_TO', 'CONTRADICTS'
            FOREIGN KEY(source_id) REFERENCES knowledge(id),
            FOREIGN KEY(target_id) REFERENCES knowledge(id)
        );
    """)
    # Check for missing columns (migration)
    cursor = conn.execute("PRAGMA table_info(knowledge)")
    cols = [row[1] for row in cursor.fetchall()]
    if "session_id" not in cols:
        conn.execute("ALTER TABLE knowledge ADD COLUMN session_id TEXT")
    if "message_id" not in cols:
        conn.execute("ALTER TABLE knowledge ADD COLUMN message_id INTEGER")
    if "review" not in cols:
        conn.execute("ALTER TABLE knowledge ADD COLUMN review TEXT")
    
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(MEMORY_DB_PATH)

def save_knowledge(category, content, original_msg, importance=5, session_id=None, msg_id=None, reasoning=None):
    from clide.brain.memory import get_embedding
    
    # Generate embedding for semantic search
    emb = get_embedding(content)
    emb_blob = json.dumps(emb).encode('utf-8')

    conn = get_connection()
    conn.execute(
        "INSERT INTO knowledge (category, content, original_msg, importance, embedding, session_id, message_id, review) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (category, content, original_msg, importance, emb_blob, session_id, msg_id, reasoning)
    )
    conn.commit()
    conn.close()
    
    # Both Database and File sync for TODOs
    if category == "TODO":
        try:
            todo_path = os.path.join(BASE_DIR, "todo.md")
            with open(todo_path, "a") as f:
                f.write(f"- [ ] {content} (Extracted from: {original_msg[:30]}...)\n")
        except: pass

def get_knowledge(category=None, min_importance=0, limit=None):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    
    query = "SELECT * FROM knowledge WHERE importance >= ?"
    params = [min_importance]
    
    if category:
        query += " AND category = ?"
        params.append(category)
        
    query += " ORDER BY timestamp DESC"
    
    if limit:
        query += " LIMIT ?"
        params.append(limit)
        
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows

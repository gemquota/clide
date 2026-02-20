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
    if "tags" not in cols:
        conn.execute("ALTER TABLE knowledge ADD COLUMN tags TEXT")
    
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

def update_knowledge(node_id, content=None, category=None, importance=None, tags=None, review=None):
    conn = get_connection()
    updates = []
    params = []
    if content:
        updates.append("content = ?")
        params.append(content)
        # Update embedding if content changes
        from clide.brain.memory import get_embedding
        emb = get_embedding(content)
        emb_blob = json.dumps(emb).encode('utf-8')
        updates.append("embedding = ?")
        params.append(emb_blob)
    if category:
        updates.append("category = ?")
        params.append(category)
    if importance is not None:
        updates.append("importance = ?")
        params.append(importance)
    if tags is not None:
        # Handle list or string
        tags_val = json.dumps(tags) if isinstance(tags, list) else tags
        updates.append("tags = ?")
        params.append(tags_val)
    if review:
        updates.append("review = ?")
        params.append(review)
    
    if updates:
        query = f"UPDATE knowledge SET {', '.join(updates)} WHERE id = ?"
        params.append(node_id)
        conn.execute(query, params)
        conn.commit()
    conn.close()

def delete_knowledge(node_id, soft=True):
    conn = get_connection()
    if soft:
        # Assuming we might add an 'is_deleted' column later, but for now 
        # we'll just move it to a 'DELETED' category or just hard delete if requested.
        # Let's check if 'is_deleted' exists.
        cursor = conn.execute("PRAGMA table_info(knowledge)")
        cols = [row[1] for row in cursor.fetchall()]
        if "is_deleted" not in cols:
            conn.execute("ALTER TABLE knowledge ADD COLUMN is_deleted INTEGER DEFAULT 0")
        conn.execute("UPDATE knowledge SET is_deleted = 1 WHERE id = ?", (node_id,))
    else:
        conn.execute("DELETE FROM knowledge WHERE id = ?", (node_id,))
    conn.commit()
    conn.close()

def add_relationship(source_id, target_id, rel_type="SIMILAR_TO"):
    conn = get_connection()
    conn.execute(
        "INSERT INTO relationships (source_id, target_id, rel_type) VALUES (?, ?, ?)",
        (source_id, target_id, rel_type)
    )
    conn.commit()
    conn.close()

def get_relationships(node_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM relationships WHERE source_id = ? OR target_id = ?", (node_id, node_id)).fetchall()
    conn.close()
    return rows

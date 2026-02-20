import json
import sqlite3
import os

REGISTRY_PATH = "swarm/commands/vector_registry.json"
MEMORY_DB_PATH = "clide/memory.db"
BACKUP_PATH = "clide/memory.db.pre_rebuild"

if not os.path.exists(REGISTRY_PATH):
    print(f"Registry not found at {REGISTRY_PATH}")
    exit(1)

# Backup current small DB
if os.path.exists(MEMORY_DB_PATH):
    os.rename(MEMORY_DB_PATH, BACKUP_PATH)
    print(f"Backed up current memory.db to {BACKUP_PATH}")

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
        rel_type TEXT,
        FOREIGN KEY(source_id) REFERENCES knowledge(id),
        FOREIGN KEY(target_id) REFERENCES knowledge(id)
    );
""")

with open(REGISTRY_PATH, "r") as f:
    registry = json.load(f)

print(f"Loaded {len(registry)} assets from registry.")

count = 0
for item in registry:
    meta = item.get("metadata", {})
    category = meta.get("type", "UNKNOWN").upper()
    
    # Try to find content. For agents/tools, it might be the description.
    # For SHELL_HISTORY, it's the 'desc'.
    content = meta.get("description") or meta.get("desc") or item.get("id")
    original_msg = meta.get("path") or "Registry Import"
    importance = meta.get("importance", 5)
    
    emb = item.get("embedding", [])
    emb_blob = json.dumps(emb).encode('utf-8')
    
    conn.execute(
        "INSERT INTO knowledge (category, content, original_msg, importance, embedding) VALUES (?, ?, ?, ?, ?)",
        (category, content, original_msg, importance, emb_blob)
    )
    count += 1

conn.commit()
conn.close()
print(f"Successfully rebuilt memory.db with {count} records.")

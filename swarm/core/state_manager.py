# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "mcp[cli]",
#   "sqlite3",
# ]
# ///
import sqlite3
import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("ProjectAtlas")
DB_PATH = "/data/data/com.termux/files/home/meta/swarm/core/state.db"

def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT CHECK(type IN ('FEATURE', 'BUG')),
                name TEXT NOT NULL,
                status TEXT DEFAULT 'DEFINING',
                risk_score INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS artifacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_id INTEGER,
                type TEXT,
                content TEXT,
                is_approved BOOLEAN DEFAULT 0,
                FOREIGN KEY (entity_id) REFERENCES entities(id)
            );
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_id INTEGER,
                description TEXT,
                track TEXT CHECK(track IN ('A_CODE', 'B_DOCS')),
                status TEXT DEFAULT 'PENDING',
                weight INTEGER DEFAULT 1,
                FOREIGN KEY (entity_id) REFERENCES entities(id)
            );
        ")

# Initialize DB on import/run
init_db()

@mcp.tool()
def init_entity(name: str, type: str, risk_score: int = 1) -> str:
    """Initializes a new feature or bug. Type must be 'FEATURE' or 'BUG'."""
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO entities (name, type, risk_score) VALUES (?, ?, ?)",
            (name, type.upper(), risk_score)
        )
        entity_id = cursor.lastrowid
        return f"Successfully initialized {type} '{name}' with ID: {entity_id}"

@mcp.tool()
def add_artifact(entity_id: int, type: str, content: str) -> str:
    """Saves a document (User Story, RSD, etc.) associated with an entity."""
    with get_db() as conn:
        conn.execute(
            "INSERT INTO artifacts (entity_id, type, content) VALUES (?, ?, ?)",
            (entity_id, type, content)
        )
        return f"Artifact '{type}' added to Entity ID: {entity_id}"

@mcp.tool()
def approve_artifact(artifact_id: int) -> str:
    """Approves an artifact by its ID, acting as a protocol gate."""
    with get_db() as conn:
        conn.execute("UPDATE artifacts SET is_approved = 1 WHERE id = ?", (artifact_id,))
        return f"Artifact ID {artifact_id} approved."

@mcp.tool()
def sync_tasks(entity_id: int, tasks_json: str) -> str:
    """
    Bulk inserts tasks for an entity. 
    Expects tasks_json to be a list of dicts: [{'desc': '...', 'track': 'A_CODE|B_DOCS', 'weight': 1}]
    """
    import json
    tasks = json.loads(tasks_json)
    with get_db() as conn:
        for t in tasks:
            conn.execute(
                "INSERT INTO tasks (entity_id, description, track, weight) VALUES (?, ?, ?, ?)",
                (entity_id, t['desc'], t['track'], t.get('weight', 1))
            )
        return f"Synced {len(tasks)} tasks for Entity ID: {entity_id}"

@mcp.tool()
def get_project_status() -> str:
    """Returns a summary of all active entities and their current state."""
    with get_db() as conn:
        entities = conn.execute("SELECT * FROM entities ORDER BY created_at DESC").fetchall()
        if not entities:
            return "No active entities found."
        
        output = "--- Project Atlas Status ---"
        for e in entities:
            output += f"[{e['type']}] ID {e['id']}: {e['name']} | Status: {e['status']} | Risk: {e['risk_score']}\n"
            # Get pending tasks count
            tasks = conn.execute("SELECT COUNT(*) as count FROM tasks WHERE entity_id = ? AND status = 'PENDING'", (e['id'],)).fetchone()
            output += f"  > Pending Tasks: {tasks['count']}"
        return output

if __name__ == "__main__":
    mcp.run()

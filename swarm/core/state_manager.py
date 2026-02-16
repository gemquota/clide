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
# Use absolute path based on current working directory for robustness
BASE_DIR = os.getcwd()
DB_PATH = os.path.join(BASE_DIR, "swarm/core/state.db")
MEMORY_DB_PATH = os.path.join(BASE_DIR, "clide/memory.db")

def get_db(db_path=DB_PATH):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for concurrency
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

class KnowledgeProvider:
    def __init__(self, db_path=MEMORY_DB_PATH):
        self.db_path = db_path

    def query_knowledge(self, text=None, category=None, min_importance=0, limit=10):
        # We explicitly exclude 'embedding' because it is a BLOB and causes JSON errors.
        fields = ["id", "category", "content", "importance", "timestamp", "tags", "command_name"]
        query = f"SELECT {', '.join(fields)} FROM knowledge WHERE importance >= ?"
        params = [min_importance]
        
        if category:
            query += " AND category = ?"
            params.append(category)
        if text:
            query += " AND (content LIKE ? OR original_msg LIKE ?)"
            params.extend([f"%{text}%", f"%{text}%"])
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        with get_db(self.db_path) as conn:
            rows = conn.execute(query, params).fetchall()
            results = []
            for row in rows:
                d = {}
                for field in fields:
                    val = row[field]
                    if isinstance(val, bytes):
                        d[field] = val.decode('utf-8', errors='ignore')
                    else:
                        d[field] = val
                results.append(d)
            return results

def init_db():
    # Ensure state.db is in WAL mode and initialized
    with get_db(DB_PATH) as conn:
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
            CREATE TABLE IF NOT EXISTS synthesis_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_name TEXT NOT NULL,
                status TEXT CHECK(status IN ('success', 'error')),
                details TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS message_bus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                topic TEXT NOT NULL,
                payload TEXT,
                status TEXT DEFAULT 'UNREAD',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
    
    # Ensure memory.db is also in WAL mode
    with get_db(MEMORY_DB_PATH) as conn:
        pass

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
def record_synthesis(tool_name: str, status: str, details: str = "") -> str:
    """Records a tool synthesis event (success or error)."""
    with get_db() as conn:
        conn.execute(
            "INSERT INTO synthesis_events (tool_name, status, details) VALUES (?, ?, ?)",
            (tool_name, status.lower(), details)
        )
        return f"Successfully recorded synthesis {status} for tool '{tool_name}'"

@mcp.tool()
def publish_message(sender: str, topic: str, payload_json: str) -> str:
    """Publishes a message to the shared inter-agent bus."""
    import json
    # If payload_json is already a dict (passed from Python directly), convert to string
    if isinstance(payload_json, dict):
        payload_str = json.dumps(payload_json)
    else:
        payload_str = payload_json

    with get_db() as conn:
        conn.execute(
            "INSERT INTO message_bus (sender, topic, payload) VALUES (?, ?, ?)",
            (sender, topic, payload_str)
        )
        return f"Successfully published message to topic '{topic}' from '{sender}'"

@mcp.tool()
def get_messages(topic: str = None, status: str = 'UNREAD', limit: int = 50) -> list:
    """Retrieves messages from the bus, optionally filtered by topic or status. Set status to None for all."""
    query = "SELECT * FROM message_bus"
    params = []
    
    conditions = []
    if status:
        conditions.append("status = ?")
        params.append(status)
    if topic:
        conditions.append("topic = ?")
        params.append(topic)
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)
    
    with get_db(DB_PATH) as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]

@mcp.tool()
def mark_message_read(message_id: int) -> str:
    """Marks a message as read by its ID."""
    with get_db() as conn:
        conn.execute("UPDATE message_bus SET status = 'READ' WHERE id = ?", (message_id,))
        return f"Message ID {message_id} marked as READ."

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    from datetime import datetime
    if isinstance(obj, (datetime)):
        return obj.isoformat()
    if isinstance(obj, bytes):
        return obj.decode('utf-8', errors='ignore')
    raise TypeError ("Type %s not serializable" % type(obj))

@mcp.tool()
def query_project_knowledge(text: str = None, category: str = None, min_importance: int = 0, limit: int = 10) -> str:
    """
    Search for specific keywords or categories of knowledge in the project memory.
    Returns a JSON string of knowledge items.
    """
    import json
    kp = KnowledgeProvider()
    results = kp.query_knowledge(text=text, category=category, min_importance=min_importance, limit=limit)
    return json.dumps(results, indent=2, default=json_serial)

@mcp.tool()
def delete_knowledge(node_id: int) -> str:
    """Deletes a knowledge node from the memory database."""
    with get_db(MEMORY_DB_PATH) as conn:
        conn.execute("DELETE FROM knowledge WHERE id = ?", (node_id,))
        return f"Knowledge node {node_id} deleted."

@mcp.tool()
def get_recent_lessons(limit: int = 5) -> str:
    """
    Fetch the most recent lessons learned in the project.
    """
    import json
    kp = KnowledgeProvider()
    results = kp.query_knowledge(category='LESSON', limit=limit)
    return json.dumps(results, indent=2)

@mcp.tool()
def get_project_status() -> str:
    """Returns a summary of all active entities and their current state, plus recent knowledge."""
    output = "--- Project Atlas Status ---\n"
    
    with get_db(DB_PATH) as conn:
        entities = conn.execute("SELECT * FROM entities ORDER BY created_at DESC").fetchall()
        if not entities:
            output += "No active entities found.\n"
        else:
            for e in entities:
                output += f"[{e['type']}] ID {e['id']}: {e['name']} | Status: {e['status']} | Risk: {e['risk_score']}\n"
                # Get pending tasks count
                tasks = conn.execute("SELECT COUNT(*) as count FROM tasks WHERE entity_id = ? AND status = 'PENDING'", (e['id'],)).fetchone()
                output += f"  > Pending Tasks: {tasks['count']}\n"
    
    # Add Recent Knowledge
    kp = KnowledgeProvider()
    knowledge = kp.query_knowledge(min_importance=7, limit=3)
    if knowledge:
        output += "\n--- Recent Knowledge: ---\n"
        for k in knowledge:
            output += f"- [{k['category']}] {k['content']} (Imp: {k['importance']})\n"
            
    return output

if __name__ == "__main__":
    mcp.run()

import json
import os
import subprocess
import sqlite3
from datetime import datetime, timedelta
from clide.brain.memory import search_registry
from clide.kernel.settings import get_path, load_config

REGISTRY_PATH = get_path("registry") or os.path.join(os.path.dirname(__file__), "../../swarm/commands/vector_registry.json")

def run_janitor():
    """
    Scans the registry for overlapping or redundant tools and suggests merges.
    """
    if not os.path.exists(REGISTRY_PATH):
        print("[Janitor] Registry not found.")
        return

    # Logic for detecting overlaps could go here
    print("[Janitor] Scanning for redundancies...")
    pass

class TodoManager:
    """
    Manages TODO items in the database and todo.md file.
    """
    def __init__(self):
        self.db_path = get_path("memory")
        self.todo_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "todo.md")

    def list_todos(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT id, content, timestamp FROM knowledge WHERE category = 'TODO' ORDER BY timestamp DESC")
        todos = cursor.fetchall()
        conn.close()
        
        if not todos:
            print("No active TODOs.")
            return
            
        print("\n--- CLIDE TODO List ---")
        for tid, content, ts in todos:
            print(f"[{tid}] {content} ({ts[:10]})")

    def add_todo(self, content, importance=5):
        from clide.kernel.storage import save_knowledge
        save_knowledge("TODO", content, "Manual CLI addition", importance=importance)
        print(f"[v] Added TODO: {content}")

    def remove_todo(self, todo_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("DELETE FROM knowledge WHERE id = ? AND category = 'TODO'", (todo_id,))
        if cursor.rowcount > 0:
            print(f"[v] Removed TODO #{todo_id}")
            conn.commit()
            self.sync_to_file()
        else:
            print(f"[!] TODO #{todo_id} not found.")
        conn.close()

    def complete_todo(self, todo_id):
        """Marks a TODO as COMPLETED (changes category)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("UPDATE knowledge SET category = 'COMPLETED' WHERE id = ? AND category = 'TODO'", (todo_id,))
        if cursor.rowcount > 0:
            print(f"[v] Completed TODO #{todo_id}")
            conn.commit()
            self.sync_to_file()
        else:
            print(f"[!] TODO #{todo_id} not found or already completed.")
        conn.close()

    def sync_to_file(self):
        """Rebuilds todo.md from the current database state."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT content, original_msg FROM knowledge WHERE category = 'TODO'")
        todos = cursor.fetchall()
        conn.close()
        
        try:
            with open(self.todo_file, "w") as f:
                f.write("# CLIDE TODO (Synchronized)\n\n")
                for content, orig in todos:
                    f.write(f"- [ ] {content} (Extracted from: {orig[:30]}...)\n")
        except Exception as e:
            print(f"[Error] Failed to sync todo.md: {e}")

    def prune_todos(self, days=7):
        """Removes TODOs older than X days."""
        limit_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("DELETE FROM knowledge WHERE category = 'TODO' AND timestamp < ?", (limit_date,))
        count = cursor.rowcount
        conn.commit()
        conn.close()
        if count > 0:
            print(f"[Janitor] Pruned {count} old TODOs.")
            self.sync_to_file()

def prune_todos():
    # Legacy wrapper for existing calls
    mgr = TodoManager()
    mgr.prune_todos()

def perform_merge(id_a, id_b):
    print(f"[*] Creating safety checkpoint...")
    # SPA Update: Need to ensure git operations use project root
    subprocess.run(["git", "add", "."], capture_output=True)
    subprocess.run(["git", "commit", "-m", f"Pre-merge backup: {id_a} & {id_b}"], capture_output=True)

    print(f"[*] Synthesizing merged logic...")
    # This would call an LLM to merge
    pass

if __name__ == "__main__":
    run_janitor()
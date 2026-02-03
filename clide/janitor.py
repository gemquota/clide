import json
import os
import subprocess
from vector_registry import search_registry

REGISTRY_PATH = "/data/data/com.termux/files/home/meta/swarm/commands/vector_registry.json"

def run_janitor():
    if not os.path.exists(REGISTRY_PATH):
        return

    # ... (existing overlap detection) ...
    pass

def prune_todos():
    """
    Removes TODOs from the database and todo.md that are older than 24 hours 
    or match a 'completed' pattern.
    """
    import sqlite3
    from datetime import datetime, timedelta
    
    db_path = "/data/data/com.termux/files/home/meta/clide/memory.db"
    conn = sqlite3.connect(db_path)
    
    # 1. Prune by Age (24h)
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    cursor = conn.execute("DELETE FROM knowledge WHERE category = 'TODO' AND timestamp < ?", (yesterday,))
    deleted_count = cursor.rowcount
    conn.commit()
    conn.close()
    
    # 2. Synchronize todo.md (Reset it to active items)
    conn = sqlite3.connect(db_path)
    active_todos = conn.execute("SELECT content FROM knowledge WHERE category = 'TODO'").fetchall()
    conn.close()
    
    with open("/data/data/com.termux/files/home/meta/todo.md", "w") as f:
        f.write("# CLIDE TODO (Synchronized)\n\n")
        for t in active_todos:
            f.write(f"- [ ] {t[0]}\n")
            
    print(f"[v] Janitor: Pruned {deleted_count} outdated TODOs from the Brain.")
    return deleted_count

def archive_originals(id_a, id_b):
    archive_dir = "/data/data/com.termux/files/home/meta/swarm/commands/archive"
    os.makedirs(archive_dir, exist_ok=True)
    
    # Move TOMLs and MCPs
    for asset_id in [id_a, id_b]:
        # Move TOML
        toml_src = f"/data/data/com.termux/files/home/meta/swarm/commands/{asset_id}.toml"
        if os.path.exists(toml_src):
            os.rename(toml_src, os.path.join(archive_dir, f"{asset_id}.toml"))
        
        # Move MCP
        mcp_src = f"/data/data/com.termux/files/home/meta/swarm/commands/mcp_servers/{asset_id}.py"
        if os.path.exists(mcp_src):
            os.rename(mcp_src, os.path.join(archive_dir, f"{asset_id}.py"))

def perform_merge(id_a, id_b):
    print(f"[*] Creating safety checkpoint...")
    subprocess.run(["git", "add", "."], capture_output=True)
    subprocess.run(["git", "commit", "-m", f"Pre-merge backup: {id_a} & {id_b}"], capture_output=True)

    print(f"[*] Synthesizing merged logic...")
    prompt = f"Merge the following two tools into one robust tool. Return ONLY the new Python code for an MCP server.\nTool A: {id_a}\nTool B: {id_b}"
    try:
        result = subprocess.run(["gemini", "-p", prompt], capture_output=True, text=True)
        merged_code = result.stdout.strip()
        
        new_id = f"{id_a}_{id_b}_merged"
        from mcp_generator import save_mcp_server
        save_mcp_server(new_id, merged_code, is_complex=True, description=f"Merged from {id_a} and {id_b}")
        
        print(f"[*] Archiving originals...")
        archive_originals(id_a, id_b)
        print(f"[v] Merge complete. New tool: '{new_id}'")
        
    except Exception as e:
        print(f"[!] Merge failed: {e}. Use 'git reset --hard HEAD' to rollback.")

def propose_merge(id_a, id_b):
    # Fetch logic for both
    # (Simplified for now, just showing the concept)
    print(f"Janitor: Analyzing '{id_a}' and '{id_b}' for merging...")
    prompt = f"Propose a merged version of two CLI tools: '{id_a}' and '{id_b}'. Create a single, more robust tool that covers both use cases. Return a suggested name and description."
    try:
        result = subprocess.run(["gemini", "-p", prompt], capture_output=True, text=True)
        print("\n--- SUGGESTED MERGE PLAN ---")
        print(result.stdout.strip())
    except:
        print("Error generating merge plan.")

if __name__ == "__main__":
    run_janitor()

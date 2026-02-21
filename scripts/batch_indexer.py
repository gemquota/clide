import os
import json
import sqlite3
import hashlib
from clide.brain import memory
from clide.kernel import storage
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()

def get_shell_history():
    history = []
    zsh_path = os.path.expanduser("~/.zsh_history")
    if os.path.exists(zsh_path):
        try:
            with open(zsh_path, "r", errors="ignore") as f:
                for line in f:
                    if "; " in line: history.append(line.split("; ", 1)[1].strip())
                    elif line.startswith(":"):
                        parts = line.split(";", 1)
                        if len(parts) > 1: history.append(parts[1].strip())
                    else: history.append(line.strip())
        except: pass
    bash_path = os.path.expanduser("~/.bash_history")
    if os.path.exists(bash_path):
        try:
            with open(bash_path, "r", errors="ignore") as f:
                for line in f:
                    history.append(line.strip())
        except: pass
    return list(set([h for h in history if h and len(h) > 3]))

def run_full_index():
    console.print("\n[bold cyan]╶─╼ ⟨ ◈ TOTAL REGISTRY REBUILD ◈ ⟩ ╾─╴[/")
    
    # 1. Sync Shell History
    history = get_shell_history()
    conn = storage.get_connection()
    conn.row_factory = storage.sqlite3.Row
    existing = {row['content'] for row in conn.execute("SELECT content FROM knowledge WHERE category='SHELL_HISTORY'").fetchall()}
    new_items = [h for h in history if h not in existing]
    
    if new_items:
        batch_size = 100
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(bar_width=40), TaskProgressColumn(), console=console) as progress:
            task = progress.add_task("[cyan]Embedding New Shell History...", total=len(new_items))
            for i in range(0, len(new_items), batch_size):
                batch = new_items[i:i+batch_size]
                embeddings = memory.get_embeddings(batch)
                batch_data_json = []
                for text, emb in zip(batch, embeddings):
                    emb_blob = json.dumps(emb).encode('utf-8')
                    conn.execute("INSERT INTO knowledge (category, content, original_msg, importance, embedding) VALUES (?, ?, ?, ?, ?)", ("SHELL_HISTORY", text, "Shell History Import", 3, emb_blob))
                    asset_id = "sh_" + hashlib.md5(text.encode('utf-8')).hexdigest()[:12]
                    batch_data_json.append((asset_id, {"type": "SHELL_HISTORY", "desc": text}, emb))
                conn.commit()
                memory.add_to_registry_batch(batch_data_json)
                progress.update(task, advance=len(batch))
        console.print(f"[green][v] Ingested {len(new_items)} shell commands.[/")

    # 2. Re-vectorize Everything from DB to Registry
    console.print("[yellow][*] Synchronizing all knowledge to vector registry...[/")
    all_nodes = conn.execute("SELECT id, category, content, importance, embedding FROM knowledge").fetchall()
    conn.close()

    if not all_nodes:
        console.print("[red][!] Database is empty.[/")
        return

    registry_batch = []
    for node in all_nodes:
        asset_id = str(node['id'])
        metadata = {
            "type": node['category'],
            "importance": node['importance'],
            "desc": (node['content'] or "")[:100]
        }
        
        # Use existing embedding if available, else generate
        try:
            if node['embedding']:
                emb = json.loads(node['embedding'].decode('utf-8')) if isinstance(node['embedding'], bytes) else json.loads(node['embedding'])
            else:
                emb = memory.get_embedding(node['content'])
        except:
            emb = memory.get_embedding(node['content'] or " ")
            
        registry_batch.append((asset_id, metadata, emb))
    
    memory.add_to_registry_batch(registry_batch)
    console.print(f"[bold green]Success:[/ ] Total Registry Rebuilt ({len(registry_batch)} items).[/")

if __name__ == "__main__":
    run_full_index()

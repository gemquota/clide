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
    console.print("\n[bold cyan]╶─╼ ⟨ ◈ DEEP-SYNC KERNEL ◈ ⟩ ╾─╴[/")
    history = get_shell_history()
    conn = storage.get_connection()
    existing = {row[0] for row in conn.execute("SELECT content FROM knowledge WHERE category='SHELL_HISTORY'").fetchall()}
    conn.close()
    new_items = [h for h in history if h not in existing]
    if not new_items:
        console.print("[green]Neural parity achieved.[/]")
        return
    
    batch_size = 100
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(bar_width=40), TaskProgressColumn(), console=console) as progress:
        task = progress.add_task("[cyan]Embedding Shell History...", total=len(new_items))
        for i in range(0, len(new_items), batch_size):
            batch = new_items[i:i+batch_size]
            embeddings = memory.get_embeddings(batch)
            conn = storage.get_connection()
            batch_data_json = []
            for text, emb in zip(batch, embeddings):
                emb_blob = json.dumps(emb).encode('utf-8')
                conn.execute("INSERT INTO knowledge (category, content, original_msg, importance, embedding) VALUES (?, ?, ?, ?, ?)", ("SHELL_HISTORY", text, "Shell History Import", 3, emb_blob))
                asset_id = "sh_" + hashlib.md5(text.encode('utf-8')).hexdigest()[:12]
                batch_data_json.append((asset_id, {"type": "SHELL_HISTORY", "desc": text}, emb))
            conn.commit()
            conn.close()
            memory.add_to_registry_batch(batch_data_json)
            progress.update(task, advance=len(batch))
    console.print(f"\n[bold green]Success:[/ ] Ingested {len(new_items)} shell commands.")

if __name__ == "__main__":
    run_full_index()

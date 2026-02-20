import os
import sqlite3
import json
import hashlib
from clide.kernel import storage
from clide.brain import memory
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()

def extract_snippets():
    snippets = []
    ingestion_dir = 'ingestion_logs'
    for root, _, files in os.walk(ingestion_dir):
        for f_name in files:
            if f_name.endswith('.md'):
                path = os.path.join(root, f_name)
                try:
                    with open(path, 'r', errors='ignore') as f:
                        for line in f:
                            if '| "' in line and '" |' in line:
                                # Extract snippet between | " and " |
                                try:
                                    parts = line.split('| "', 1)
                                    if len(parts) > 1:
                                        content = parts[1].split('" |', 1)[0].strip()
                                        if len(content) > 5:
                                            snippets.append((content, f_name))
                                except: pass
                except: pass
    return snippets

def ingest_all():
    console.print("\n[bold magenta]╶─╼ ⟨ ◈ ARCHIVE NEURAL SYNC ◈ ⟩ ╾─╴[")
    snippets_with_source = extract_snippets()
    
    conn = storage.get_connection()
    existing = {row[0] for row in conn.execute("SELECT content FROM knowledge WHERE category != 'SHELL_HISTORY'").fetchall()}
    conn.close()
    
    new_items = []
    seen_content = set()
    for content, source in snippets_with_source:
        if content not in existing and content not in seen_content:
            new_items.append((content, source))
            seen_content.add(content)
            
    if not new_items:
        console.print("[green]Archive parity achieved.[/]")
        return

    console.print(f"[*] Found {len(new_items)} new snippets to ingest.")
    
    batch_size = 50
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(bar_width=40), TaskProgressColumn(), console=console) as progress:
        task = progress.add_task("[magenta]Embedding Archives...", total=len(new_items))
        
        for i in range(0, len(new_items), batch_size):
            batch = new_items[i:i+batch_size]
            texts = [item[0] for item in batch]
            
            # Get Embeddings
            try:
                embeddings = memory.get_embeddings(texts)
            except Exception as e:
                console.print(f"[red]Batch Error: {e}[/]")
                continue
                
            conn = storage.get_connection()
            registry_batch = []
            
            for (content, source), emb in zip(batch, embeddings):
                emb_blob = json.dumps(emb).encode('utf-8')
                # Save to SQL
                conn.execute(
                    "INSERT INTO knowledge (category, content, original_msg, importance, embedding) VALUES (?, ?, ?, ?, ?)",
                    ('ARCHIVE', content, f"Bulk Import: {source}", 5, emb_blob)
                )
                
                # Prepare for Registry
                asset_id = "arc_" + hashlib.md5(content.encode('utf-8')).hexdigest()[:12]
                registry_batch.append((asset_id, {"type": "ARCHIVE", "desc": content, "source": source}, emb))
            
            conn.commit()
            conn.close()
            
            # Save to Vector Registry
            memory.add_to_registry_batch(registry_batch)
            
            progress.update(task, advance=len(batch))

    console.print(f"\n[bold green]Success:[/ ] Ingested {len(new_items)} archive snippets.")

if __name__ == "__main__":
    ingest_all()
import json
import os
import hashlib
from clide.brain import memory
from clide.kernel import storage
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()

def run_log_merge():
    console.print("\n[bold magenta]╶─╼ ⟨ ◈ NEURAL CONSOLIDATION ◈ ⟩ ╾─╴[/]")
    console.print("[dim]Merging enriched telemetry into permanent memory...[/]\n")

    log_path = os.path.join(os.path.dirname(__file__), "../clide/enriched_logs.json")
    if not os.path.exists(log_path):
        console.print("[red]No enriched logs found to merge.[/]")
        return

    try:
        with open(log_path, "r") as f:
            logs = json.load(f)
    except:
        console.print("[red]Error reading enriched logs.[/]")
        return

    # Filter for entries that have clide_metadata (processed items)
    candidates = [m for m in logs if "clide_metadata" in m]
    
    # Check existing in DB to avoid duplicates
    conn = storage.get_connection()
    # We use session_id + message_id as a unique key for messages
    try:
        existing = {f"{row[0]}_{row[1]}" for row in conn.execute("SELECT session_id, message_id FROM knowledge WHERE session_id IS NOT NULL").fetchall()}
    except:
        existing = set()
    conn.close()

    to_merge = []
    for m in candidates:
        key = f"{m.get('sessionId')}_{m.get('messageId')}"
        if key not in existing:
            to_merge.append(m)

    if not to_merge:
        console.print("[green]Memory parity achieved. All telemetry is already consolidated.[/]")
        return

    console.print(f"[bold magenta]Detected {len(to_merge)} new telemetry units for consolidation.[/]")

    batch_size = 50
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[magenta]Consolidating Enriched Logs...", total=len(to_merge))
        
        for i in range(0, len(to_merge), batch_size):
            batch = to_merge[i:i+batch_size]
            
            # Prepare batch for vector registry and DB
            texts = [m['message'] for m in batch]
            embeddings = memory.get_embeddings(texts)
            
            conn = storage.get_connection()
            batch_data_json = []
            for m, emb in zip(batch, embeddings):
                meta = m['clide_metadata']
                category = meta.get('category', 'FACT')
                content = m['message']
                reasoning = meta.get('reasoning')
                
                # Save to SQLite
                emb_blob = json.dumps(emb).encode('utf-8')
                conn.execute(
                    "INSERT INTO knowledge (category, content, original_msg, importance, embedding, session_id, message_id, review) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (category, content, content, 5, emb_blob, m.get('sessionId'), m.get('messageId'), reasoning)
                )
                
                # Prep for JSON registry
                sid = m.get('sessionId')
                sid_str = str(sid)[:8] if sid else "none"
                asset_id = f"msg_{sid_str}_{m.get('messageId')}"
                batch_data_json.append((asset_id, {"type": category, "desc": content[:100]}, emb))
            
            conn.commit()
            conn.close()
            
            # Sync to vector_registry.json
            memory.add_to_registry_batch(batch_data_json)
            
            progress.update(task, advance=len(batch))

    console.print(f"\n[bold green]Success:[/ Consolidated {len(to_merge)} units into the project brain.")

if __name__ == "__main__":
    run_log_merge()

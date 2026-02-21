import json
from clide.kernel import storage
from clide.brain.model import call_llm
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

console = Console()

def auto_tag_nodes():
    """Fetches nodes without tags and generates them using the LLM."""
    console.print("[bold blue][Brain][/] Scanning for untagged knowledge...")
    
    # Fetch recent nodes to check
    all_nodes = storage.get_knowledge(limit=500)
    
    untagged_nodes = []
    for node in all_nodes:
        # Check 'tags' column
        has_tags = False
        # Handle case where 'tags' might not exist in row if DB schema is old but code expects it
        # sqlite3.Row supports keys.
        if 'tags' in node.keys() and node['tags']:
            try:
                # tags might be stored as JSON string or raw string? 
                # storage.update_knowledge stores it as JSON string if list.
                tags_val = node['tags']
                if isinstance(tags_val, str) and tags_val.strip().startswith("["):
                     tags_data = json.loads(tags_val)
                     if tags_data: has_tags = True
                elif isinstance(tags_val, str) and len(tags_val.strip()) > 0:
                     has_tags = True # Treat non-empty string as having tags
            except:
                pass 
        
        # Legacy check
        if not has_tags and "TAGS:" in (node['review'] or ""):
            has_tags = True
            
        if not has_tags:
            untagged_nodes.append(node)

    count = len(untagged_nodes)
    
    if count == 0:
        console.print("[green][v] All knowledge nodes are tagged.[/]")
        return

    console.print(f"[bold yellow]Found {count} nodes requiring tags.[/]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Tagging nodes...", total=count)
        
        for node in untagged_nodes:
            # Generate tags
            prompt = f"Analyze this project knowledge and provide 3-5 succinct tags as a comma-separated list.\n\nContent: {node['content']}"
            try:
                tags_str = call_llm(prompt).strip()
                # Clean up if LLM returns JSON or something else
                if "[" in tags_str and "]" in tags_str:
                     # Try to parse as JSON if it looks like one
                     try:
                        tags_list = json.loads(tags_str)
                     except:
                        tags_list = [t.strip() for t in tags_str.split(",") if t.strip()]
                else:
                    tags_list = [t.strip() for t in tags_str.split(",") if t.strip()]

                # Update storage
                storage.update_knowledge(node['id'], tags=tags_list)
            except Exception as e:
                console.print(f"[red][!] Failed to tag Node #{node['id']}: {e}[/]")
            
            progress.advance(task)
            
    console.print("[bold green][v] Tagging complete.[/]")

def auto_prioritize_tasks():
    """Uses LLM to assign importance scores to TODOs based on current project state."""
    console.print("[bold blue][Brain][/] Re-prioritizing task queue...")
    todos = storage.get_knowledge(category="TODO")
    
    if not todos:
        console.print("[yellow][!] No tasks found to prioritize.[/]")
        return

    context = "\n".join([f"- [{t['id']}] {t['content']}" for t in todos])
    prompt = f"""Analyze these project tasks and assign an importance score (1-10) to each. 
    Return ONLY a JSON mapping: {{"id": score, ...}}
    
    Tasks:
    {context}
    """
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Consulting LLM for prioritization...", total=None)
        try:
            res = call_llm(prompt)
            # Robust parsing for potential markdown formatting
            start = res.find("{")
            end = res.rfind("}")
            if start != -1 and end != -1:
                scores_str = res[start:end+1]
                scores = json.loads(scores_str)
                for tid, score in scores.items():
                    storage.update_knowledge(int(tid), importance=int(score))
                console.print("[green][v] Task prioritization complete.[/]")
            else:
                console.print("[red][!] Failed to parse prioritization scores.[/]")
        except Exception as e:
            console.print(f"[red][!] Prioritization failed: {e}[/]")

def merge_knowledge_nodes(node_ids):
    """Synthesizes multiple nodes into a single master node and cleans up."""
    if len(node_ids) < 2: return
    
    conn = storage.get_connection()
    conn.row_factory = storage.sqlite3.Row
    placeholders = ','.join(['?'] * len(node_ids))
    nodes = conn.execute(f"SELECT * FROM knowledge WHERE id IN ({placeholders})", node_ids).fetchall()
    
    if not nodes:
        conn.close()
        return

    console.print(f"  [cyan][*] Merging {len(nodes)} nodes...[/]")
    
    # 1. Synthesize Content via LLM
    context = "\n---\n".join([f"Node #{n['id']} [{n['category']}]: {n['content']}" for n in nodes])
    prompt = f"""Synthesize the following related knowledge nodes into a single, comprehensive "Master Node".
    Preserve all unique technical details, facts, and context. Remove only redundant phrasing.
    
    KNOWLEDGE UNITS:
    {context}
    
    Return ONLY the synthesized content. No preamble.
    """
    
    try:
        new_content = call_llm(prompt).strip()
        if not new_content: throw_err # Fallback
    except:
        # Fallback to longest content if LLM fails
        new_content = sorted(nodes, key=lambda x: len(x['content'] or ""), reverse=True)[0]['content']

    # 2. Pick Master (usually the first ID) and combine metadata
    master_id = node_ids[0]
    others = node_ids[1:]
    
    all_tags = set()
    max_imp = 0
    for n in nodes:
        max_imp = max(max_imp, n['importance'] or 5)
        # Parse tags
        try:
            if n.get('tags'):
                t_list = json.loads(n['tags']) if n['tags'].startswith("[") else [t.strip() for t in n['tags'].split(",")]
                all_tags.update(t_list)
        except: pass

    # 3. Update Master (Perform manually to avoid nested connection lock)
    tags_json = json.dumps(list(all_tags))
    
    # Also update embedding
    from clide.brain.memory import get_embedding
    emb = get_embedding(new_content)
    emb_blob = json.dumps(emb).encode('utf-8')

    conn.execute(
        "UPDATE knowledge SET content = ?, importance = ?, tags = ?, embedding = ? WHERE id = ?",
        (new_content, max_imp, tags_json, emb_blob, master_id)
    )
    
    # 4. Redirect Relationships
    for old_id in others:
        conn.execute("UPDATE relationships SET source_id = ? WHERE source_id = ?", (master_id, old_id))
        conn.execute("UPDATE relationships SET target_id = ? WHERE target_id = ?", (master_id, old_id))
        # 5. Hard Delete Redundant
        conn.execute("DELETE FROM knowledge WHERE id = ?", (old_id,))
    
    conn.commit()
    conn.close()
    console.print(f"  [green][v] Successfully merged into Master Node #{master_id}[/]")
    return new_content

def auto_audit_brain(auto_merge=True, threshold=0.95):
    """Searches for near-duplicate knowledge nodes and merges them."""
    # Safety cap: Don't allow threshold below 0.80 to prevent massive accidental merging
    safe_threshold = max(threshold, 0.80)
    
    console.print(f"[bold blue][Brain][/] Searching for knowledge anomalies (threshold: {safe_threshold})...")
    nodes = storage.get_knowledge(limit=1000) # Increased scan breadth
    
    from clide.brain.memory import cosine_similarity
    
    valid_nodes = []
    for n in nodes:
        try:
            if n['embedding']:
                emb = json.loads(n['embedding'].decode('utf-8')) if isinstance(n['embedding'], bytes) else json.loads(n['embedding'])
                if len(emb) > 0:
                    valid_nodes.append({'id': n['id'], 'cat': n['category'], 'content': n['content'], 'emb': emb})
        except: continue
    
    count = len(valid_nodes)
    if count < 2:
        console.print("[green][v] Insufficient nodes for comparison.[/]")
        return

    console.print(f"[yellow] analyzing {count} nodes for semantic collisions...[/]")
    processed = set()
    merges_performed = 0
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Scanning & Resolving...", total=count)
        
        for i in range(len(valid_nodes)):
            n1 = valid_nodes[i]
            if n1['id'] in processed: 
                progress.advance(task)
                continue
            
            # Find all nodes similar to n1
            to_merge = [n1['id']]
            for j in range(i+1, len(valid_nodes)):
                n2 = valid_nodes[j]
                if n2['id'] in processed: continue
                
                sim = cosine_similarity(n1['emb'], n2['emb'])
                if sim > safe_threshold:
                    to_merge.append(n2['id'])
                    processed.add(n2['id'])
            
            if len(to_merge) > 1:
                # Close the progress bar temporarily to print log
                progress.console.print(f"  [red][!] Collision:[/] {len(to_merge)} nodes detected as near-duplicates.")
                if auto_merge:
                    new_node_content = merge_knowledge_nodes(to_merge)
                    from rich.panel import Panel
                    progress.console.print(Panel(new_node_content, title=f"New Master Node #{to_merge[0]}", border_style="green"))
                    merges_performed += 1
                
            processed.add(n1['id'])
            progress.advance(task)

    if merges_performed > 0:
        console.print(f"[bold green][v] Optimized project brain. Resolved {merges_performed} semantic collisions.[/]")
    else:
        console.print("[green][v] No semantic anomalies detected.[/]")

def auto_clean_metadata():
    """Trims whitespace and removes low-quality/garbage nodes."""
    console.print("[bold blue][Brain][/] Sanitizing knowledge metadata...")
    nodes = storage.get_knowledge()
    cleaned = 0
    removed = 0
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Cleaning nodes...", total=len(nodes))
        
        for node in nodes:
            content = node['content'] or ""
            trimmed = content.strip()
            
            # Remove garbage or extremely short nodes (less than 10 chars)
            if len(trimmed) < 10:
                storage.delete_knowledge(node['id'], soft=False)
                removed += 1
                progress.advance(task)
                continue
                
            if trimmed != content:
                storage.update_knowledge(node['id'], content=trimmed)
                cleaned += 1
            
            progress.advance(task)
            
    console.print(f"[green][v] Sanitization complete. Cleaned: {cleaned}, Removed: {removed}[/]")

def auto_sync_todos():
    """Synchronizes tasks between memory.db and todo.md."""
    console.print("[bold blue][Brain][/] Synchronizing tasks...")
    from clide.tools import janitor
    mgr = janitor.TodoManager()
    
    # Rebuild todo.md from DB
    mgr.sync_to_file()
    
    # Fetch from memory.db (category=TODO)
    db_todos = storage.get_knowledge(category="TODO")
    count = len(db_todos)
    console.print(f"[green][v] Synchronized {count} tasks from neural memory to todo.md.[/]")

def approve_proposals():
    """Converts PROPOSAL nodes into permanent knowledge units."""
    console.print("[bold cyan][Brain][/] Reviewing and approving pending ingestion proposals...")
    
    conn = storage.get_connection()
    conn.row_factory = storage.sqlite3.Row
    proposals = conn.execute("SELECT * FROM knowledge WHERE category = 'PROPOSAL'").fetchall()
    
    if not proposals:
        console.print("[green][v] No pending proposals found.[/]")
        conn.close()
        return

    count = len(proposals)
    console.print(f"[yellow][*] Found {count} pending proposals.[/]")
    
    approved = 0
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Approving...", total=count)
        
        for p in proposals:
            # Determine target category from content if possible
            content = p['content'] or ""
            target_cat = "FACT"
            if "New Command:" in content: target_cat = "NEW_COMMAND"
            elif "TODO:" in content: target_cat = "TODO"
            
            # Update category and set importance higher for approved items
            conn.execute(
                "UPDATE knowledge SET category = ?, importance = ? WHERE id = ?",
                (target_cat, max(p['importance'], 7), p['id'])
            )
            approved += 1
            progress.advance(task)
            
    conn.commit()
    conn.close()
    console.print(f"[bold green][v] Successfully approved {approved} ingestion suggestions.[/]")

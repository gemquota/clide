import json
import math
import os
import numpy as np
from clide.brain.memory import cosine_similarity
from clide.kernel import storage as db_manager

# Rich Imports
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich import box

console = Console()

def get_brain_data(category=None, min_importance=0, limit=None):
    db_manager.ensure_db()
    return db_manager.get_knowledge(category=category, min_importance=min_importance, limit=limit)

def list_brain_units(category=None, limit=20):
    """Prints a formatted list of the most recent knowledge units."""
    nodes = get_brain_data(category=category, limit=limit)
    if not nodes:
        console.print("[yellow]No knowledge units found matching criteria.[/]")
        return

    table = Table(title=f"BRAIN UNITS (Category: {category or 'ALL'})", border_style="cyan", box=box.ROUNDED)
    table.add_column("ID", style="dim", justify="right")
    table.add_column("Category", style="bold magenta")
    table.add_column("Content Snippet", style="white")
    table.add_column("Imp", style="green", justify="center")

    for n in nodes:
        content = (n['content'] or "").replace("\n", " ")[:60] + "..."
        table.add_row(str(n['id']), n['category'], content, str(n['importance']))
    
    console.print(table)

def run_deep_analysis():
    """Performs a deep semantic clustering and relationship mapping of the brain."""
    from clide.brain import memory
    console.print("[bold cyan][Brain][/] Initiating deep semantic analysis...")
    
    clusters = memory.cluster_registry(threshold=0.85)
    if not clusters:
        console.print("[yellow][!] Insufficient data for deep analysis.[/]")
        return
    
    table = Table(title="SEMANTIC CLUSTERS", border_style="cyan")
    table.add_column("Cluster", justify="right")
    table.add_column("Size", justify="center")
    table.add_column("Topic/Centroid", style="magenta")
    
    for i, c in enumerate(clusters[:10]):
        table.add_row(str(i+1), str(c['size']), c['centroid_desc'][:60])
        
    console.print(table)
    console.print("[green][v][/] Deep analysis complete. Relationships indexed.")

def verify_facts():
    """Cross-references FACT and LESSON nodes for contradictions or updates."""
    from clide.brain.model import call_llm
    console.print("[bold cyan][Brain][/] Verifying factual integrity...")
    
    facts = get_brain_data(category="FACT", limit=50)
    lessons = get_brain_data(category="LESSON", limit=50)
    
    if not facts and not lessons:
        console.print("[yellow][!] No facts or lessons found to verify.[/]")
        return

    context = "FACTS:\n" + "\n".join([f"- {f['content']}" for f in facts])
    context += "\n\nLESSONS:\n" + "\n".join([f"- {l['content']}" for l in lessons])
    
    prompt = f"""Analyze the following facts and lessons from a project database. 
    Identify any contradictions or outdated information.
    
    {context}
    
    Return a brief report highlighting any issues found. If none, say 'No contradictions detected.'
    """
    
    console.print("[dim][*] Auditing Facts and Lessons via LLM...[/]")
    report = call_llm(prompt)
    console.print(Panel(report, title="[bold green]Integrity Audit Report[/]", border_style="green"))

def generate_brain_summary():
    """Generates an executive multi-session summary of recent project knowledge."""
    from clide.brain.model import call_llm
    console.print("[bold cyan][Brain][/] Generating executive summary...")
    
    # Fetch recent nodes across all categories
    recent_nodes = get_brain_data(limit=50)
    if not recent_nodes:
        console.print("[yellow][!] No recent knowledge found to summarize.[/]")
        return
        
    context = "\n".join([f"[{n['category']}] {n['content']}" for n in recent_nodes])
    
    prompt = f"""Generate a concise, high-level executive summary of the following recent project knowledge.
    Focus on key achievements, active todos, and discovered patterns.
    
    KNOWLEDGE STREAM:
    {context}
    
    Summary:
    """
    
    summary = call_llm(prompt)
    console.print(Panel(summary, title="[bold magenta]Executive Brain Summary[/]", border_style="magenta"))

def render_trace_tree(node_id):
    """Traces the origin and relationships of a specific node using a Rich Tree."""
    node_id = int(node_id)
    conn = db_manager.get_connection()
    conn.row_factory = db_manager.sqlite3.Row
    node = conn.execute("SELECT * FROM knowledge WHERE id = ?", (node_id,)).fetchone()
    if not node:
        console.print(f"[bold red]⦗ERROR⦘[/] Node #{node_id} not found.")
        return

    # Root of the provenance tree
    root = Tree(f"[bold cyan]PROVENANCE TRACE: Node #{node_id}[/]")
    
    # Node Metadata Branch
    meta = root.add("[bold magenta]Metadata[/]")
    meta.add(f"Category: [white]{node['category']}[/]")
    meta.add(f"Timestamp: [dim]{node['timestamp']}[/]")
    meta.add(f"Importance: [green]{node['importance']}[/]")
    
    # Content Branch
    content_node = root.add("[bold cyan]Content[/]")
    content_node.add(node['content'])
    
    # Source Branch
    source = root.add("[bold yellow]Source Lineage[/]")
    source.add(f"Origin: {node['original_msg'][:100]}...")
    
    # Relationships Branch
    rels = db_manager.get_relationships(node_id)
    if rels:
        rel_tree = root.add("[bold green]Relationships[/]")
        for r in rels:
            direction = "→" if r['source_id'] == node_id else "←"
            other_id = r['target_id'] if r['source_id'] == node_id else r['source_id']
            rel_tree.add(f"Node {node_id} {direction} Node {other_id} [dim]({r['rel_type']})[/]")
    
    console.print(Panel(root, border_style="cyan", box=box.ROUNDED))
    conn.close()

def trace_provenance(node_id):
    """Legacy wrapper for trace_provenance."""
    render_trace_tree(node_id)

def render_stats_table():
    """Displays high-level system metrics in a table."""
    from clide.brain import memory
    stats = memory.get_registry_stats()
    
    table = Table(title="NEURAL KERNEL METRICS", border_style="magenta", box=box.DOUBLE_EDGE)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="bold white", justify="right")
    
    table.add_row("Total Assets", str(stats['total_assets']))
    table.add_row("Vector Dimensions", str(stats['dimensions']))
    table.add_row("Registry Size", f"{stats['file_size_kb']:.2f} KB")
    
    for cat, count in stats['distribution'].items():
        table.add_row(f"Sector: {cat}", str(count))
        
    console.print(table)

def generate_mermaid_graph(nodes):
    lines = ["graph TD"]
    node_data = []
    for n in nodes:
        raw_content = n['content'] or "No content"
        content_short = raw_content[:30].replace('"', "'") + "..."
        label = f"{n['id']}[\"({n['category']}) {content_short}\"]"
        lines.append(f"    {label}")
        
        try:
            emb = json.loads(n['embedding'].decode('utf-8'))
            node_data.append({'id': n['id'], 'emb': emb})
        except:
            continue
    
    for i, n1 in enumerate(node_data):
        v1 = n1['emb']
        for n2 in node_data[i+1:]:
            v2 = n2['emb']
            sim = cosine_similarity(v1, v2)
            if sim > 0.85:
                style = "===" 
                lines.append(f"    {n1['id']} {style}|{int(sim*100)}%| {n2['id']}")
            elif sim > 0.75:
                style = "---"
                lines.append(f"    {n1['id']} {style}|{int(sim*100)}%| {n2['id']}")
                
    return "\n".join(lines)

def render_ascii_graph(nodes):
    """Renders a TUI-based relationship map using Panels and Columns."""
    console.print("\n[bold cyan]ATLAS // NEURAL TOPOLOGY MAP[/]")
    if not nodes:
        console.print("[yellow]Brain is empty. Keep working to build context.[/]")
        return

    decoded_nodes = []
    for n in nodes:
        try:
            emb_data = n['embedding']
            if isinstance(emb_data, bytes): emb_data = emb_data.decode('utf-8')
            emb = json.loads(emb_data)
            decoded_nodes.append({'id': n['id'], 'cat': n['category'], 'content': n['content'], 'imp': n['importance'], 'emb': emb})
        except: continue

    panels = []
    for n in decoded_nodes:
        v1 = n['emb']
        related = []
        for n2 in decoded_nodes:
            if n['id'] == n2['id']: continue
            if cosine_similarity(v1, n2['emb']) > 0.85:
                related.append(f"#{n2['id']}")
        
        content = f"[magenta]{n['cat']}[/]\n[white]{n['content'][:50]}...[/]"
        if related:
            content += f"\n\n[dim]Links: {', '.join(related)}[/]"
            
        panels.append(Panel(content, title=f"[bold cyan]Node {n['id']}[/]", border_style="dim", box=box.ROUNDED))

    console.print(Columns(panels, equal=True, expand=True))

def generate_html_viewer(nodes):
    node_list = []
    for n in nodes:
        try:
            emb_data = n['embedding']
            if isinstance(emb_data, bytes):
                emb_data = emb_data.decode('utf-8')
            emb = np.array(json.loads(emb_data), dtype=np.float32)
            # Normalize
            norm = np.linalg.norm(emb)
            if norm > 0: emb = emb / norm
            
            node_list.append({
                'id': n['id'], 
                'cat': n['category'], 
                'content': n['content'], 
                'imp': n['importance'], 
                'emb': emb
            })
        except: continue

    links = []
    if len(node_list) > 0:
        embeddings = np.array([n['emb'] for n in node_list])
        sim_matrix = np.dot(embeddings, embeddings.T)
        for i in range(len(node_list)):
            sims = sim_matrix[i]
            indices = np.argsort(sims)[-3:-1] 
            for idx in indices:
                score = float(sims[idx])
                if score > 0.85:
                    links.append({"source": node_list[i]['id'], "target": node_list[idx]['id'], "value": score})

    formatted_nodes = [
        {
            "id": n['id'], 
            "name": f"[{n['cat']}] ID {n['id']}", 
            "group": n['cat'], 
            "val": n['importance'] or 5,
            "desc": (n['content'] or "").replace('"',"'").replace('\n', ' ')[:200]
        } 
        for n in node_list
    ]
    
    template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>CLIDE Brain Viewer</title>
    <script src="https://unpkg.com/force-graph"></script>
    <style>
        body { margin: 0; background: #000; color: #0f8; font-family: monospace; }
        #controls { position: absolute; top: 10px; left: 10px; z-index: 10; background: rgba(0,0,0,0.8); padding: 15px; border: 1px solid #0f8; border-radius: 5px; }
    </style>
</head>
<body>
    <div id="controls">
        <b style="font-size: 1.2em;">CLIDE // Brain Visualization</b><br>
        Knowledge Nodes: NODE_COUNT<br>
        Links: LINK_COUNT<br><br>
        <small>● Scroll: Zoom<br>● Drag: Pan<br>● Hover node for content</small>
    </div>
    <div id="graph"></div>
    <script>
        const data = { \"nodes\": NODE_DATA, \"links\": LINK_DATA };
        const Graph = ForceGraph()(document.getElementById('graph'))
            .graphData(data)
            .nodeAutoColorBy('group')
            .nodeLabel(node => {
                const name = node.name || 'Unknown';
                const desc = node.desc || '';
                return `<b>${name}</b><br>${desc}`;
            })
            .nodeRelSize(4)
            .linkDirectionalParticles(1)
            .linkWidth(0.5)
            .linkColor(() => 'rgba(255,255,255,0.1)')
            .backgroundColor('#000000');
    </script>
</body>
</html>
"""
    return template.replace("NODE_COUNT", str(len(formatted_nodes))) \
                   .replace("LINK_COUNT", str(len(links))) \
                   .replace("NODE_DATA", json.dumps(formatted_nodes)) \
                   .replace("LINK_DATA", json.dumps(links))
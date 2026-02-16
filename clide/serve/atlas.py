import json
import math
import os
import numpy as np
from clide.brain.memory import cosine_similarity
from clide.kernel import storage as db_manager

def get_brain_data(category=None, min_importance=0, limit=None):
    db_manager.ensure_db()
    return db_manager.get_knowledge(category=category, min_importance=min_importance, limit=limit)

def list_brain_units(category=None, limit=20):
    """Prints a formatted list of the most recent knowledge units."""
    nodes = get_brain_data(category=category, limit=limit)
    if not nodes:
        print("No knowledge units found matching criteria.")
        return

    print(f"\n\033[1;31m--- BRAIN UNITS (Category: {category or 'ALL'}) ---\033[0m")
    for n in nodes:
        color = "\033[31m" # Red default
        if n['category'] == "FACT": color = "\033[1;31m"
        elif n['category'] == "TODO": color = "\033[1;31m"
        elif n['category'] == "LESSON": color = "\033[1;31m"
        
        print(f"[{n['id']}] {color}{n['category']:8}\033[0m | {n['content'][:60]}...")

def generate_brain_summary():
    """Uses LLM to synthesize recent knowledge into an executive summary."""
    from clide.brain.model import call_llm
    print("[Brain] Synthesizing executive summary...")
    nodes = get_brain_data(limit=30)
    
    context = "\n".join([f"- [{n['category']}] {n['content']}" for n in nodes])
    prompt = f"""Summarize the following recent project knowledge into a professional executive report.
    Highlight key accomplishments, new facts discovered, and pending TODOs.
    
    Data:
    {context}
    """
    
    summary = call_llm(prompt)
    print("\n\033[1;31m=== PROJECT EXECUTIVE SUMMARY ===\033[0m")
    print(summary)

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
    print("\n--- CLIDE Project Brain (ASCII Map) ---")
    if not nodes:
        print("Brain is empty. Keep working to build context.")
        return

    decoded_nodes = []
    for n in nodes:
        try:
            emb = json.loads(n['embedding'].decode('utf-8'))
            decoded_nodes.append({'id': n['id'], 'cat': n['category'], 'content': n['content'], 'imp': n['importance'], 'emb': emb})
        except: continue

    for n in decoded_nodes:
        prefix = "  [!] " if n['imp'] > 7 else "  [-] "
        raw_content = n['content'] or "No content"
        print(f"{prefix}({n['cat']}) ID {n['id']}: {raw_content[:60]}...")
        
        v1 = n['emb']
        related = []
        for n2 in decoded_nodes:
            if n['id'] == n2['id']: continue
            v2 = n2['emb']
            if cosine_similarity(v1, v2) > 0.85:
                related.append(str(n2['id']))
        if related:
            print(f"      L> Related to: {', '.join(related)}")

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
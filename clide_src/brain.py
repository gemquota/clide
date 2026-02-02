import sqlite3
import json
import math
from vector_registry import cosine_similarity

MEMORY_DB_PATH = "/data/data/com.termux/files/home/meta/clide_src/memory.db"

def get_brain_data():
    from extractor import init_memory_db
    init_memory_db() # Ensure tables exist
    conn = sqlite3.connect(MEMORY_DB_PATH)
    conn.row_factory = sqlite3.Row
    nodes = conn.execute("SELECT id, category, content, importance, embedding FROM knowledge").fetchall()
    conn.close()
    return nodes

def generate_mermaid_graph(nodes):
    lines = ["graph TD"]
    # 1. Create Nodes with styles based on category
    for n in nodes:
        content_short = n['content'][:30].replace('"', "'") + "..."
        label = f"{n['id']}[\"({n['category']}) {content_short}\"]"
        lines.append(f"    {label}")
    
    # 2. Functional & Semantic Links
    for i, n1 in enumerate(nodes):
        v1 = json.loads(n1['embedding'].decode('utf-8'))
        for n2 in nodes[i+1:]:
            v2 = json.loads(n2['embedding'].decode('utf-8'))
            sim = cosine_similarity(v1, v2)
            
            # Link if similarity is high
            if sim > 0.75:
                style = "---" if sim < 0.85 else "===" 
                lines.append(f"    {n1['id']} {style}|{int(sim*100)}%| {n2['id']}")
                
    return "\n".join(lines)

def render_ascii_graph(nodes):
    print("\n--- CLIDE Project Brain (ASCII Map) ---")
    if not nodes:
        print("Brain is empty. Keep working to build context.")
        return

    for n in nodes:
        prefix = "  [!] " if n['importance'] > 7 else "  [-] "
        print(f"{prefix}({n['category']}) ID {n['id']}: {n['content'][:60]}...")
        
        # Simple proximity list instead of full graph for terminal
        v1 = json.loads(n['embedding'].decode('utf-8'))
        related = []
        for n2 in nodes:
            if n['id'] == n2['id']: continue
            v2 = json.loads(n2['embedding'].decode('utf-8'))
            if cosine_similarity(v1, v2) > 0.8:
                related.append(str(n2['id']))
        if related:
            print(f"      L> Related to: {', '.join(related)}")

if __name__ == "__main__":
    nodes = get_brain_data()
    # Output Mermaid for saving
    with open("docs/brain_graph.mmd", "w") as f:
        f.write(generate_mermaid_graph(nodes))
    
    # Render ASCII to terminal
    render_ascii_graph(nodes)

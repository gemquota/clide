import sqlite3
import json
import os
import math
import numpy as np

MEMORY_DB_PATH = "/data/data/com.termux/files/home/openclaw/meta/clide/memory.db"
OUTPUT_PATH = "/data/data/com.termux/files/home/openclaw/meta/viz/data/graph_data.json"

def get_data():
    conn = sqlite3.connect(MEMORY_DB_PATH)
    conn.row_factory = sqlite3.Row
    nodes = conn.execute("SELECT id, category, content, importance, embedding FROM knowledge").fetchall()
    conn.close()
    return nodes

def compute_links(nodes, threshold=0.75, max_links_per_node=10):
    links = []
    node_list = []
    
    # Pre-process nodes and embeddings
    for n in nodes:
        try:
            emb_data = n['embedding']
            if isinstance(emb_data, bytes):
                emb_data = emb_data.decode('utf-8')
            emb = np.array(json.loads(emb_data), dtype=np.float32)
            # Normalize for cosine similarity
            norm = np.linalg.norm(emb)
            if norm > 0:
                emb = emb / norm
            node_list.append({'id': n['id'], 'cat': n['category'], 'content': n['content'][:150], 'imp': n['importance'], 'emb': emb})
        except Exception as e:
            continue

    num_nodes = len(node_list)
    if num_nodes == 0: return [], []
    
    embeddings = np.array([n['emb'] for n in node_list])
    
    # Similarity matrix
    sim_matrix = np.dot(embeddings, embeddings.T)
    
    for i in range(num_nodes):
        sims = sim_matrix[i]
        # Get top indices (excluding self)
        # We want indices where sims > threshold
        indices = np.where(sims > threshold)[0]
        # Sort these indices by similarity score descending
        indices = indices[indices != i] # Remove self
        sorted_indices = indices[np.argsort(sims[indices])[::-1]]
        
        # Take up to max_links_per_node
        for rank, idx in enumerate(sorted_indices[:max_links_per_node]):
            score = float(sims[idx])
            links.append({
                "source": node_list[i]['id'],
                "target": node_list[idx]['id'],
                "value": score,
                "distance": 100 * (1 - score), # High similarity = shorter distance
                "rank": rank + 1 # 1 is best friend, 10 is acquaintance
            })
                
    # Format nodes for JSON
    formatted_nodes = []
    for n in node_list:
        formatted_nodes.append({
            "id": n['id'],
            "name": f"[{n['cat']}] {n['id']}",
            "group": n['cat'],
            "val": 2 + (n['imp'] * 0.5),
            "content": n['content']
        })
        
    return formatted_nodes, links

def main(nodes=None):
    if nodes is None:
        print(f"Extracting knowledge for visualization...")
        nodes = get_data()
        
    if not nodes:
        print("No data found in memory.db")
        return
        
    print(f"Processing {len(nodes)} items and computing semantic gravity...")
    viz_nodes, viz_links = compute_links(nodes)
    
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump({"nodes": viz_nodes, "links": viz_links}, f, indent=2)
        
    print(f"Graph data generated: {len(viz_nodes)} nodes, {len(viz_links)} links.")

if __name__ == "__main__":
    main()

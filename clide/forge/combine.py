import sqlite3
import json
import numpy as np
from vector_registry import cosine_similarity, get_embedding
import os

MEMORY_DB_PATH = "/data/data/com.termux/files/home/openclaw/meta/clide/memory.db"

def get_all_nodes():
    conn = sqlite3.connect(MEMORY_DB_PATH)
    conn.row_factory = sqlite3.Row
    nodes = conn.execute("SELECT id, category, content, importance, embedding FROM knowledge").fetchall()
    conn.close()
    return nodes

def synthesize_brain(threshold=0.92):
    print(f"[*] Starting Neural Synthesis (Threshold: {threshold})...")
    nodes = get_all_nodes()
    if not nodes:
        print("[!] Brain is empty.")
        return

    node_list = []
    for n in nodes:
        try:
            emb_data = n['embedding']
            if isinstance(emb_data, bytes): emb_data = emb_data.decode('utf-8')
            emb = np.array(json.loads(emb_data), dtype=np.float32)
            norm = np.linalg.norm(emb)
            if norm > 0: emb = emb / norm
            node_list.append({'id': n['id'], 'cat': n['category'], 'content': n['content'], 'imp': n['importance'], 'emb': emb})
        except: continue

    if not node_list: return

    embeddings = np.array([n['emb'] for n in node_list])
    sim_matrix = np.dot(embeddings, embeddings.T)
    
    processed_ids = set()
    clusters = []

    for i in range(len(node_list)):
        if node_list[i]['id'] in processed_ids: continue
        
        # Find neighbors
        sims = sim_matrix[i]
        matches = np.where(sims > threshold)[0]
        
        if len(matches) > 1:
            cluster = [node_list[m] for m in matches if node_list[m]['id'] not in processed_ids]
            if len(cluster) > 1:
                clusters.append(cluster)
                for c in cluster: processed_ids.add(c['id'])

    if not clusters:
        print("[v] No virtual duplicates found.")
        return

    total_clusters = len(clusters)
    total_nodes_removed = sum([len(c) for c in clusters])
    print(f"[*] Found {total_clusters} redundant clusters ({total_nodes_removed} total nodes).")
    print(f"[*] Synthesizing 50 clusters individually in this pass...")
    
    conn = sqlite3.connect(MEMORY_DB_PATH)
    
    clusters_to_process = clusters[:50]
    
    for idx, cluster in enumerate(clusters_to_process):
        cluster_id = cluster[0]['id']
        print(f"\n--- [Cluster {idx+1}/50] (Root ID: {cluster_id}) ---")
        
        # 1. Prepare Prompt
        contents = "\n- ".join([f"[{c['cat']}] {c['content']}" for c in cluster])
        prompt = f"Synthesize the following redundant knowledge entries into ONE comprehensive master entry. " \
                 f"Preserve all technical paths, IDs, and details. Return ONLY the master entry text.\n\n" \
                 f"Entries:\n{contents}"

        from llm_utils import call_llm
        try:
            # 2. LLM Synthesis
            print(f"  [>] Calling LLM for synthesis...")
            new_content = call_llm(prompt)
            
            if not new_content or "error" in new_content.lower():
                print(f"  [!] Synthesis failed for cluster {cluster_id}")
                continue
            
            # 3. Re-embedding
            print(f"  [>] Generating fresh embedding...")
            new_emb = get_embedding(new_content)
            
            # 4. Database Update
            print(f"  [>] Updating database...")
            master_cat = cluster[0]['cat']
            master_imp = max([c['imp'] for c in cluster])
            
            # Delete old nodes
            ids_to_del = [c['id'] for c in cluster]
            conn.execute(f"DELETE FROM knowledge WHERE id IN ({','.join(['?']*len(ids_to_del))})", ids_to_del)
            
            # Insert Master Node
            conn.execute("INSERT INTO knowledge (category, content, importance, embedding) VALUES (?, ?, ?, ?)",
                         (master_cat, new_content, master_imp, json.dumps(new_emb)))
            
            conn.commit()
            print(f"  [v] Cluster {idx+1} complete: {len(cluster)} nodes -> 1 Master.")
            
        except Exception as e:
            print(f"  [!] Error: {e}")

    conn.close()
    print(f"\n[v] Pass complete. Run again for next 5.")

if __name__ == "__main__":
    synthesize_brain()

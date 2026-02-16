import json
import csv
import os
import numpy as np
import math
from collections import Counter

# Configuration
NUM_CLUSTERS = 12
K_NEIGHBORS = 6

def load_vectors(json_path):
    if not os.path.exists(json_path): return []
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def simple_kmeans(X, k=10, max_iters=30):
    n_samples = X.shape[0]
    if n_samples < k: return np.zeros(n_samples, dtype=int)
    indices = np.random.choice(n_samples, k, replace=False)
    centroids = X[indices]
    labels = np.zeros(n_samples, dtype=int)
    for _ in range(max_iters):
        dists = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)
        new_labels = np.argmin(dists, axis=1)
        if np.all(labels == new_labels): break
        labels = new_labels
        for i in range(k):
            mask = (labels == i)
            if np.any(mask): centroids[i] = X[mask].mean(axis=0)
    return labels, centroids

def compute_links(ids, X, k=5):
    links = []
    n_samples = X.shape[0]
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    norms[norms == 0] = 1e-10
    X_norm = X / norms
    sim_matrix = np.dot(X_norm, X_norm.T)
    for i in range(n_samples):
        sims = sim_matrix[i]
        sims[i] = -1
        top_k = min(k, n_samples - 1)
        if top_k <= 0: continue
        top_indices = np.argpartition(sims, -top_k)[-top_k:]
        for target_idx in top_indices:
            score = float(sims[target_idx])
            if score > 0.55:
                links.append({"source": ids[i], "target": ids[target_idx], "value": score})
    return links

def main():
    # Resolve paths relative to project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir) # ../

    json_path = os.path.join(project_root, "swarm/commands/vector_registry.json")
    csv_path = os.path.join(project_root, "ingestion_logs/commands.csv")
    output_path = os.path.join(script_dir, "graph_data.json")
    
    items = load_vectors(json_path)
    dims = [len(item['embedding']) for item in items if item.get('embedding')]
    common_dim = Counter(dims).most_common(1)[0][0]
    valid_items = [item for item in items if item.get('embedding') and len(item['embedding']) == common_dim]
    
    ids = [item['id'] for item in valid_items]
    X = np.array([item['embedding'] for item in valid_items], dtype=np.float32)
    
    labels, centroids = simple_kmeans(X, k=NUM_CLUSTERS)
    links = compute_links(ids, X, k=K_NEIGHBORS)
    
    csv_meta = {}
    if os.path.exists(csv_path):
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader: csv_meta[row['Command']] = row

    nodes = []
    for i, item in enumerate(valid_items):
        item_id = item['id']
        short_name = item_id.split(':')[-1]
        occ = 1
        if short_name in csv_meta:
            try: occ = int(csv_meta[short_name].get('Occurrences', 1))
            except: pass
        
        # Scaling: Smallest is ~5, largest will be ~60+ (4x+ variation)
        val = 5 + (math.pow(occ, 1.2) * 2)
            
        nodes.append({
            "id": item_id,
            "name": short_name,
            "full_name": item_id,
            "val": val,
            "group": int(labels[i]),
            "description": item.get('metadata', {}).get('desc', ''),
            "type": "command"
        })

    # Create a mapping of group ID to semantic name
    group_names = {}
    for i in range(NUM_CLUSTERS):
        cluster_items = [nodes[j] for j, label in enumerate(labels) if label == i]
        if cluster_items:
            cluster_items.sort(key=lambda x: x['val'], reverse=True)
            leader_name = cluster_items[0]['name'].split(':')[-1].split('_')[-1].title()
            group_names[i] = f"{leader_name} Cluster"
        else:
            group_names[i] = f"Group {i+1}"

    # Update nodes with their group names
    for node in nodes:
        node['group_name'] = group_names[node['group']]

    # Add Cluster Meta-Nodes
    cluster_nodes = []
    meta_links = []
    for i in range(NUM_CLUSTERS):
        cluster_id = f"cluster_{i}"
        cluster_nodes.append({
            "id": cluster_id,
            "name": group_names[i],
            "val": 150,
            "group": i,
            "group_name": group_names[i],
            "type": "meta_cluster",
            "is_meta": True
        })
        
        cluster_items = [n for n in nodes if n['group'] == i]
        for item in cluster_items:
            meta_links.append({
                "source": cluster_id,
                "target": item['id'],
                "value": 0.1,
                "is_meta": True
            })

    with open(output_path, 'w') as f:
        json.dump({"nodes": nodes + cluster_nodes, "links": links + meta_links}, f, indent=2)
    print(f"Generated {len(nodes)} nodes and {len(links)} links.")

if __name__ == "__main__":
    main()
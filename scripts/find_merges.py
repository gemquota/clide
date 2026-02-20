import os
import json
import numpy as np

def find_more_merges(threshold=0.90):
    with open('swarm/commands/vector_registry.json', 'r') as f:
        registry = json.load(f)
    
    # Types that represent potential commands
    cmd_types = {'NEW_COMMAND', 'TOOL_INTENT', 'MATCH'}
    items = [a for a in registry if a.get('metadata', {}).get('type') in cmd_types]
    if not items: return []
    
    embeddings = [a['embedding'] for a in items]
    names = [a['id'] for a in items]
    descs = [a.get('metadata', {}).get('desc', '')[:50] for a in items]
    
    merges = []
    # Use chunking if items > 1000 to avoid memory issues, but here it's likely fine
    count = len(items)
    for i in range(count):
        for j in range(i + 1, count):
            # Basic cosine similarity
            e1 = np.array(embeddings[i])
            e2 = np.array(embeddings[j])
            sim = np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2))
            if sim > threshold:
                merges.append((names[i], names[j], descs[i], descs[j], sim))
                
    return sorted(merges, key=lambda x: x[4], reverse=True)

if __name__ == "__main__":
    new_merges = find_more_merges(threshold=0.85)
    print(f"Found {len(new_merges)} potential merges.")
    for p_id, s_id, p_desc, s_desc, score in new_merges[:100]:
        print(f"| `{p_id}` | `{s_id}` | {score:.3f} | {p_desc} <=> {s_desc} |")
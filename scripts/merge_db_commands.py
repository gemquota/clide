import sqlite3
import json
import math
from collections import defaultdict

DB_PATH = "/data/data/com.termux/files/home/openclaw/meta/clide/memory.db"

def cosine_similarity(v1, v2):
    if not v1 or not v2: return 0
    dot_product = sum(x * y for x, y in zip(v1, v2))
    mag1 = math.sqrt(sum(x*x for x in v1))
    mag2 = math.sqrt(sum(x*x for x in v2))
    return dot_product / (mag1 * mag2) if mag1 > 0 and mag2 > 0 else 0

def merge_high_sim():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT command_name, embedding FROM knowledge WHERE category = 'NEW_COMMAND' AND command_name IS NOT NULL")
    
    commands = defaultdict(list)
    for name, emb_blob in cursor.fetchall():
        if emb_blob:
            commands[name].append(json.loads(emb_blob.decode('utf-8')))
    
    # Calculate average embedding for each command name
    avg_embeddings = {}
    for name, embs in commands.items():
        if not embs: continue
        dim = len(embs[0])
        avg = [sum(e[i] for e in embs) / len(embs) for i in range(dim)]
        avg_embeddings[name] = avg

    names = list(avg_embeddings.keys())
    merges = {}
    
    print(f"Analyzing {len(names)} unique command names for potential merges...")
    
    for i in range(len(names)):
        n1 = names[i]
        if n1 in merges: continue
        
        for j in range(i + 1, len(names)):
            n2 = names[j]
            if n2 in merges: continue
            
            sim = cosine_similarity(avg_embeddings[n1], avg_embeddings[n2])
            if sim > 0.92:
                # Decide which one to keep (the one with more occurrences)
                if len(commands[n1]) >= len(commands[n2]):
                    merges[n2] = n1
                    print(f"  [Merge] `{n2}` -> `{n1}` ({sim:.3f})")
                else:
                    merges[n1] = n2
                    print(f"  [Merge] `{n1}` -> `{n2}` ({sim:.3f})")
                    break # n1 is now merged into n2, stop looking for n1 merges

    if not merges:
        print("No high-similarity pairs found to merge.")
        return

    print(f"\nApplying {len(merges)} merges to the database...")
    for old_name, new_name in merges.items():
        cursor = conn.execute("UPDATE knowledge SET command_name = ? WHERE command_name = ?", (new_name, old_name))
        print(f"  [Updated] {cursor.rowcount} rows: `{old_name}` -> `{new_name}`")
    
    conn.commit()
    conn.close()
    print("\nDatabase merging complete.")

if __name__ == "__main__":
    merge_high_sim()

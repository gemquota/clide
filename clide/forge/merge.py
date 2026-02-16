import sqlite3
import json
import math

DB_PATH = "/data/data/com.termux/files/home/openclaw/meta/clide/memory.db"

def cosine_similarity(v1, v2):
    if not v1 or not v2: return 0
    dot_product = sum(x * y for x, y in zip(v1, v2))
    mag1 = math.sqrt(sum(x*x for x in v1))
    mag2 = math.sqrt(sum(x*x for x in v2))
    return dot_product / (mag1 * mag2) if mag1 > 0 and mag2 > 0 else 0

def execute_merges():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT DISTINCT command_name, embedding FROM knowledge WHERE category = 'NEW_COMMAND' AND command_name IS NOT NULL")
    
    cmd_data = []
    for row in cursor.fetchall():
        name, emb_blob = row
        if emb_blob:
            cmd_data.append({"name": name, "emb": json.loads(emb_blob.decode('utf-8'))})

    merges = []
    processed = set()

    # Find high similarity pairs (> 0.92)
    for i in range(len(cmd_data)):
        for j in range(i + 1, len(cmd_data)):
            c1, c2 = cmd_data[i], cmd_data[j]
            if c1["name"] in processed or c2["name"] in processed: continue
            
            sim = cosine_similarity(c1["emb"], c2["emb"])
            if sim > 0.92:
                # Decide primary (shorter name or existing convention)
                primary = c1["name"] if len(c1["name"]) <= len(c2["name"]) else c2["name"]
                secondary = c2["name"] if primary == c1["name"] else c1["name"]
                
                merges.append((primary, secondary, sim))
                processed.add(secondary)

    print(f"🦞 Found {len(merges)} high-confidence merges.")
    
    for primary, secondary, sim in merges:
        print(f"  [Merge] `{secondary}` -> `{primary}` (Score: {sim:.3f})")
        conn.execute("UPDATE knowledge SET command_name = ? WHERE command_name = ?", (primary, secondary))
    
    conn.commit()
    conn.close()
    print("🦞 Consolidation Complete.")

if __name__ == "__main__":
    execute_merges()

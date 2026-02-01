import json
import os
import subprocess
import math

VECTOR_DB_PATH = "/data/data/com.termux/files/home/meta/commands/vector_registry.json"

def get_embedding(text):
    """Uses Gemini to get a vector embedding for the text."""
    # Note: This assumes gemini CLI has an embedding command or we use a prompt to simulate/fetch one.
    # For now, we'll use a placeholder or a small prompt-based 'summary vector' approach 
    # until a formal embedding tool is verified.
    prompt = f"Generate a high-dimensional semantic representation (comma-separated floats) for: {text}"
    try:
        result = subprocess.run(["gemini", "-p", prompt], capture_output=True, text=True)
        # Placeholder logic: parsing floats from LLM output
        # In a real scenario, we'd use a dedicated embedding model.
        return [float(x) for x in re.findall(r"[-+]?\d*\.\d+|\d+", result.stdout)[:16]] # 16-dim stub
    except:
        return [0.0] * 16

def cosine_similarity(v1, v2):
    dot_product = sum(x * y for x, y in zip(v1, v2))
    magnitude = math.sqrt(sum(x*x for x in v1)) * math.sqrt(sum(y*y for y in v2))
    return dot_product / magnitude if magnitude > 0 else 0

def add_to_registry(asset_id, metadata, text_for_embedding):
    registry = []
    if os.path.exists(VECTOR_DB_PATH):
        with open(VECTOR_DB_PATH, "r") as f:
            registry = json.load(f)
    
    embedding = get_embedding(text_for_embedding)
    registry.append({
        "id": asset_id,
        "metadata": metadata,
        "embedding": embedding
    })
    
    with open(VECTOR_DB_PATH, "w") as f:
        json.dump(registry, f, indent=2)

def search_registry(query, limit=3):
    if not os.path.exists(VECTOR_DB_PATH):
        return []
    
    with open(VECTOR_DB_PATH, "r") as f:
        registry = json.load(f)
    
    query_vec = get_embedding(query)
    results = []
    for item in registry:
        sim = cosine_similarity(query_vec, item["embedding"])
        results.append((sim, item))
    
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:limit]

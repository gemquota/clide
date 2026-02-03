import json
import os
import math
from google import genai

VECTOR_DB_PATH = "/data/data/com.termux/files/home/meta/swarm/commands/vector_registry.json"
API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyCI3Wed3pRBANSZG2F6VO3Mcr7qukeI1b4")
client = genai.Client(api_key=API_KEY)

def get_embedding(text):
    """Uses Google GenAI SDK to get a semantic representation for the text."""
    try:
        result = client.models.embed_content(
            model='text-embedding-004',
            contents=text,
            config={
                'output_dimensionality': 32
            }
        )
        return result.embeddings[0].values
    except Exception as e:
        print(f"Embedding Error: {e}")
        return [0.0] * 32

def cosine_similarity(v1, v2):
    if len(v1) != len(v2):
        # Handle dimensionality mismatch if necessary
        min_len = min(len(v1), len(v2))
        v1 = v1[:min_len]
        v2 = v2[:min_len]
    
    dot_product = sum(x * y for x, y in zip(v1, v2))
    magnitude = math.sqrt(sum(x*x for x in v1)) * math.sqrt(sum(y*y for y in v2))
    return dot_product / magnitude if magnitude > 0 else 0

def add_to_registry(asset_id, metadata, text_for_embedding):
    registry = []
    if os.path.exists(VECTOR_DB_PATH):
        try:
            with open(VECTOR_DB_PATH, "r") as f:
                registry = json.load(f)
        except json.JSONDecodeError:
            registry = []
    
    embedding = get_embedding(text_for_embedding)
    
    # Update existing if ID matches, else append
    for item in registry:
        if item["id"] == asset_id:
            item["metadata"] = metadata
            item["embedding"] = embedding
            break
    else:
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
    
    try:
        with open(VECTOR_DB_PATH, "r") as f:
            registry = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    
    query_vec = get_embedding(query)
    results = []
    for item in registry:
        sim = cosine_similarity(query_vec, item["embedding"])
        results.append((sim, item))
    
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:limit]

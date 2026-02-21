import json
import os
import math
from google import genai
from clide.kernel.settings import get_path

# Use dynamic path from config_loader
VECTOR_DB_PATH = get_path("registry") or os.path.join(os.path.dirname(__file__), "../swarm/commands/vector_registry.json")
API_KEY = os.environ.get("GEMINI_API_KEY")

# Initialize client only if API key is available
client = genai.Client(api_key=API_KEY) if API_KEY else None

def get_embedding(text):
    """Uses Google GenAI SDK to get a semantic representation for the text."""
    if not client:
        return [0.0] * 32
    try:
        result = client.models.embed_content(
            model='models/gemini-embedding-001',
            contents=text
        )
        return result.embeddings[0].values
    except Exception as e:
        return [0.0] * 768 # Default for gemini-embedding-001

def get_embeddings(texts):
    """Batch version of get_embedding."""
    if not client or not texts:
        return [[0.0] * 32] * len(texts)
    
    # Sanitize: Gemini API explodes on empty strings in a batch
    sanitized_texts = [t if (t and t.strip()) else " " for t in texts]
    
    try:
        # The SDK supports passing a list to contents
        result = client.models.embed_content(
            model='models/gemini-embedding-001',
            contents=sanitized_texts
        )
        # Map results back to the full format
        return [emb.values for emb in result.embeddings]
    except Exception as e:
        print(f"Batch Embedding Error: {e}")
        return [[0.0] * 768] * len(texts)

def cosine_similarity(v1, v2):

    if len(v1) != len(v2):
        # Handle dimensionality mismatch if necessary
        min_len = min(len(v1), len(v2))
        v1 = v1[:min_len]
        v2 = v2[:min_len]
    
    dot_product = sum(x * y for x, y in zip(v1, v2))
    magnitude = math.sqrt(sum(x*x for x in v1)) * math.sqrt(sum(y*y for y in v2))
    return dot_product / magnitude if magnitude > 0 else 0

def add_to_registry_batch(assets):
    """Assets: List of tuples (asset_id, metadata, embedding)"""
    registry = []
    if os.path.exists(VECTOR_DB_PATH):
        try:
            with open(VECTOR_DB_PATH, "r") as f:
                registry = json.load(f)
        except (json.JSONDecodeError, EOFError, IOError):
            # If corrupted, we might want to recover from memory.db instead
            # but for now, we just start fresh or use what we have
            registry = []
            
    # Convert registry to a dict for faster lookup
    registry_map = {item["id"]: item for item in registry}
    
    for asset_id, metadata, embedding in assets:
        registry_map[asset_id] = {
            "id": asset_id,
            "metadata": metadata,
            "embedding": embedding
        }
    
    # Atomic Write
    temp_path = VECTOR_DB_PATH + ".tmp"
    with open(temp_path, "w") as f:
        json.dump(list(registry_map.values()), f, indent=2)
    os.replace(temp_path, VECTOR_DB_PATH)

def add_to_registry(asset_id, metadata, text_for_embedding):
    registry = []
    if os.path.exists(VECTOR_DB_PATH):
        try:
            with open(VECTOR_DB_PATH, "r") as f:
                registry = json.load(f)
        except (json.JSONDecodeError, EOFError, IOError):
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
    
    # Atomic Write
    temp_path = VECTOR_DB_PATH + ".tmp"
    with open(temp_path, "w") as f:
        json.dump(registry, f, indent=2)
    os.replace(temp_path, VECTOR_DB_PATH)

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

def get_registry_stats():
    """Returns telemetry on the semantic registry."""
    if not os.path.exists(VECTOR_DB_PATH):
        return {"status": "error", "message": "Registry not found"}
    
    try:
        with open(VECTOR_DB_PATH, "r") as f:
            registry = json.load(f)
    except (json.JSONDecodeError, EOFError, IOError):
        return {"status": "error", "message": "Index lock/busy"}
    
    types = {}
    for item in registry:
        t = item.get("metadata", {}).get("type", "unknown")
        types[t] = types.get(t, 0) + 1
        
    return {
        "total_assets": len(registry),
        "file_size_kb": os.path.getsize(VECTOR_DB_PATH) / 1024,
        "distribution": types,
        "dimensions": 768
    }

def optimize_registry():
    """Deduplicates and sorts the registry for performance."""
    if not os.path.exists(VECTOR_DB_PATH): return
    
    with open(VECTOR_DB_PATH, "r") as f:
        registry = json.load(f)
    
    # Deduplicate by ID (keep latest)
    seen = {}
    for item in registry:
        seen[item["id"]] = item
    
    optimized = sorted(list(seen.values()), key=lambda x: x["id"])
    
    with open(VECTOR_DB_PATH, "w") as f:
        json.dump(optimized, f, indent=2)
    
    return len(registry) - len(optimized)

def prune_registry(min_importance=3):
    """Removes assets with importance below threshold from the registry."""
    if not os.path.exists(VECTOR_DB_PATH): return 0
    
    with open(VECTOR_DB_PATH, "r") as f:
        registry = json.load(f)
        
    initial_count = len(registry)
    pruned = [item for item in registry if item.get('metadata', {}).get('importance', 5) >= min_importance]
    
    if len(pruned) != initial_count:
        with open(VECTOR_DB_PATH, "w") as f:
            json.dump(pruned, f, indent=2)
            
    return initial_count - len(pruned)

def cluster_registry(threshold=0.85, persist=False):
    """
    Performs a density-based clustering (Leader Algorithm) on the registry.
    Returns a list of clusters: [{'centroid': id, 'members': [id, ...], 'size': N, 'topic': '...'}]
    """
    if not os.path.exists(VECTOR_DB_PATH): return []
    try:
        import numpy as np
    except ImportError:
        print("[!] NumPy required for clustering.")
        return []

    with open(VECTOR_DB_PATH, "r") as f:
        registry = json.load(f)

    # Extract vectors and IDs
    ids = []
    vectors = []
    descriptions = []
    
    for item in registry:
        ids.append(item['id'])
        desc = item.get('metadata', {}).get('description') or item.get('metadata', {}).get('desc') or item['id']
        descriptions.append(desc)
        v = item.get('embedding', [])
        if not v: v = [0.0] * 768
        vectors.append(v)
    
    if not vectors: return []
    
    # Ensure consistent dimensionality (likely 768)
    target_dim = 768
    sanitized_vectors = []
    for v in vectors:
        if len(v) == target_dim:
            sanitized_vectors.append(v)
        elif len(v) > target_dim:
            sanitized_vectors.append(v[:target_dim])
        else:
            # Pad with zeros
            sanitized_vectors.append(v + [0.0] * (target_dim - len(v)))
    
    X = np.array(sanitized_vectors, dtype=np.float32)
    # Normalize for cosine similarity
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    X = X / norms
    
    clusters = [] 
    assigned = np.zeros(len(X), dtype=bool)
    
    # Track cluster assignments if persisting
    registry_map = {item['id']: item for item in registry}
    
    for i in range(len(X)):
        if assigned[i]: continue
        
        current_vector = X[i]
        sims = np.dot(X, current_vector)
        members_idx = np.where((sims > threshold) & (~assigned))[0]
        
        if len(members_idx) > 0:
            assigned[members_idx] = True
            cluster_id = f"cluster_{ids[i]}"
            member_ids = [ids[m] for m in members_idx]
            
            if persist:
                for mid in member_ids:
                    if 'metadata' not in registry_map[mid]: registry_map[mid]['metadata'] = {}
                    registry_map[mid]['metadata']['cluster_id'] = cluster_id

            clusters.append({
                "centroid_id": ids[i],
                "centroid_desc": descriptions[i],
                "members": member_ids,
                "size": len(members_idx)
            })
            
    if persist:
        with open(VECTOR_DB_PATH, "w") as f:
            json.dump(list(registry_map.values()), f, indent=2)
        print(f"[v] Registry updated with {len(clusters)} cluster assignments.")

    # Sort by size
    clusters.sort(key=lambda x: x['size'], reverse=True)
    return clusters


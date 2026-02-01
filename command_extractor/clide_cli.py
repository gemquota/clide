import sys
import os
import json
from vector_registry import search_registry

def list_assets():
    REGISTRY = "/data/data/com.termux/files/home/meta/commands/vector_registry.json"
    if not os.path.exists(REGISTRY):
        print("Registry empty.")
        return
    with open(REGISTRY, "r") as f:
        data = json.load(f)
    print(f"\n--- CLIDE Registry ({len(data)} assets) ---")
    for item in data:
        print(f"[{item['metadata']['type'].upper()}] {item['id']}: {item['metadata']['desc']}")

def search_assets(query):
    results = search_registry(query)
    print(f"\n--- Search Results for '{query}' ---")
    for sim, item in results:
        print(f"({sim:.2f}) [{item['metadata']['type'].upper()}] {item['id']}: {item['metadata']['desc']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: clide [list | search <query> | monitor]")
        sys.exit(0)
    
    cmd = sys.argv[1]
    if cmd == "list":
        list_assets()
    elif cmd == "search":
        search_assets(" ".join(sys.argv[2:]))
    elif cmd == "dashboard":
        from dashboard_generator import generate_dashboard
        generate_dashboard()
    else:
        # Fallback to monitor
        import extractor
        extractor.monitor()

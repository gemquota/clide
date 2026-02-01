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
    elif cmd == "rollback":
        if len(sys.argv) < 3:
            print("Usage: clide rollback <asset_id>")
        else:
            from git_sync import rollback_asset
            rollback_asset(sys.argv[2])
    elif cmd == "why":
        if len(sys.argv) < 3:
            print("Usage: clide why <asset_id>")
        else:
            from provenance import get_provenance
            print(f"\n--- Provenance for '{sys.argv[2]}' ---")
            print(get_provenance(sys.argv[2]))
    elif cmd == "janitor":
        from janitor import run_janitor
        run_janitor()
    else:
        # Fallback to monitor
        import extractor
        extractor.monitor()

import sys
import os
import json
from vector_registry import search_registry

def list_assets():
    REGISTRY = "/data/data/com.termux/files/home/meta/swarm/commands/vector_registry.json"
    if not os.path.exists(REGISTRY):
        print("Registry empty.")
        return
    with open(REGISTRY, "r") as f:
        data = json.load(f)
    
    # Group by type
    grouped = {}
    for item in data:
        t = item['metadata']['type'].upper()
        if t not in grouped:
            grouped[t] = []
        grouped[t].append(item)

    print(f"\n--- CLIDE Registry ({len(data)} assets) ---")
    for t in sorted(grouped.keys()):
        print(f"\n[{t}]")
        for item in grouped[t]:
            print(f"  {item['id']}: {item['metadata']['desc']}")

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
            from git_sync import rollback_asset_and_memory
            rollback_asset_and_memory(sys.argv[2])
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
    elif cmd == "brain":
        import brain
        nodes = brain.get_brain_data()
        with open("/data/data/com.termux/files/home/meta/docs/brain_graph.mmd", "w") as f:
            f.write(brain.generate_mermaid_graph(nodes))
        print(f"[v] Mermaid graph saved to docs/brain_graph.mmd")
        brain.render_ascii_graph(nodes)
    else:
        # Fallback to monitor
        import extractor
        extractor.monitor()

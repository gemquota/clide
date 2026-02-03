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

def print_banner():
    print("\n\033[38;5;196m   ██████╗██╗     ██╗██████╗ ███████╗\033[0m")
    print("\033[38;5;160m  ██╔════╝██║     ██║██╔══██╗██╔════╝\033[0m")
    print("\033[38;5;124m  ██║     ██║     ██║██║  ██║█████╗  \033[0m")
    print("\033[38;5;124m  ██║     ██║     ██║██║  ██║██╔══╝  \033[0m")
    print("\033[38;5;88m  ╚██████╗███████╗██║██████╔╝███████╗\033[0m")
    print("\033[38;5;52m   ╚═════╝╚══════╝╚═╝╚═════╝ ╚══════╝\033[0m")
    print("   \033[1;30mDatabase: Everything | v0.7.0-Alpha\033[0m\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_banner()
        print("Usage: clide [command] [args]")
        print("\nCore Commands:")
        print("  monitor         Start live ingestion loop")
        print("  list            List all indexed assets")
        print("  search <q>      Semantic search in registry")
        print("  activate <id>   View asset instructions (Alias: mount)")
        print("  hotswap <id>    Install/Enable skill or agent")
        print("\nMaintenance:")
        print("  brain           Visualize knowledge graph")
        print("  todo clean      Prune outdated TODOs")
        print("  janitor         Merge overlapping tools")
        print("  dashboard       Generate visual registry")
        sys.exit(0)
    
    cmd = sys.argv[1]
    if cmd == "list":
        list_assets()
    elif cmd == "search":
        search_assets(" ".join(sys.argv[2:]))
    elif cmd == "dashboard":
        from dashboard_generator import generate_dashboard
        generate_dashboard()
    elif cmd in ["activate", "mount"]:
        if len(sys.argv) < 3:
            print(f"Usage: clide {cmd} <asset_id>")
        else:
            from activator import activate_asset
            print(activate_asset(sys.argv[2]))
    elif cmd == "hotswap":
        if len(sys.argv) < 3:
            print("Usage: clide hotswap <asset_id>")
        else:
            asset_id = sys.argv[2]
            if asset_id.startswith("skill:"):
                from hotswapper import hotswap_skill
                hotswap_skill(asset_id)
            elif asset_id.startswith("agent:"):
                from hotswapper import hotswap_agent
                hotswap_agent(asset_id)
            else:
                print("Error: Hotswap only supported for 'skill:' and 'agent:' IDs.")
    elif cmd == "todo":
        if len(sys.argv) > 2 and sys.argv[2] == "clean":
            from janitor import prune_todos
            prune_todos()
        else:
            print("Usage: clide todo clean")
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

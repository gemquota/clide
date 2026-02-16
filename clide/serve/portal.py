import sys
import os
import json
import argparse

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from clide.brain.memory import search_registry
from clide.kernel.settings import get_path, load_config
from clide.serve import guide

# --- HELP & REF INTERCEPTOR ---

def intercept_info_requests(argv):
    from art import tprint
    # Primary info keywords
    primary_info = ["help", "?", "ref", "atlas", "map"]
    # Modifiers that only count if a primary is present
    modifiers = ["more", "all", "full"]
    
    if not any(k in argv for k in primary_info):
        return None
    
    print("\033[38;5;196m", end="")
    tprint("CLIDE", font="small")
    print("\033[0m", end="")
    
    is_ref = any(k in argv for k in ["ref", "atlas", "map"])
    level = "basic"
    
    if "all" in argv:
        if "full" in argv: level = "all_full"
        elif "more" in argv: level = "all_more"
        else: level = "all"
    elif "full" in argv: level = "full"
    elif "more" in argv: level = "more"
    
    cleaned_args = [a for a in argv[1:] if a not in primary_info and a not in modifiers]
    domain = cleaned_args[0] if cleaned_args else None
    if not domain and argv.count("help") > 1: domain = "help"
    command = cleaned_args[1] if len(cleaned_args) > 1 else None
    
    if is_ref: guide.show_ref(domain, command, level)
    else: guide.show_help(domain, command, level)
    sys.exit(0)

# --- DOMAIN HANDLERS ---

def cmd_system(args):
    if args.sys_cmd == "status":
        from scripts import ingestion_stats
        ingestion_stats.show_ingestion_stats()
    elif args.sys_cmd == "config":
        print("[v] Configuration view pending implementation.")

def cmd_manual(args):
    from clide.kernel import storage
    from clide.tools import janitor
    if args.manual_cmd == "node":
        if args.op == "get": print(json.dumps(dict(storage.get_knowledge_by_id(args.id)), indent=2))
        elif args.op == "move": storage.update_node_category(args.id, args.cat)
        elif args.op == "delete": storage.delete_knowledge(args.id)
        elif args.op == "tag": storage.update_node_tags(args.id, args.tags)
    elif args.manual_cmd == "task":
        mgr = janitor.TodoManager()
        if args.op == "list": mgr.list_todos()
        elif args.op == "add": mgr.add_todo(args.content)
        elif args.op == "remove": mgr.remove_todo(args.id)

def cmd_brain(args):
    from clide.serve import atlas
    from clide.kernel import storage
    if args.brain_cmd == "query":
        results = search_registry(args.q)
        print(f"\n--- Brain Query Results for '{args.q}' ---")
        for sim, item in results:
            print(f"({sim:.2f}) {item['id']}: {item['metadata'].get('desc', 'No description')}")
    elif args.brain_cmd == "summary": atlas.generate_brain_summary()
    elif args.brain_cmd == "list": atlas.list_brain_units()
    elif args.brain_cmd == "merge":
        from scripts import merge_logs
        merge_logs.run_log_merge()
    elif args.brain_cmd == "cloud":
        from scripts import command_cloud
        # Pass relevant args to the cloud generator
        # We manually bridge the argparse results
        import sys
        # To avoid re-parsing in the script if possible, but the script is standalone too.
        # Let's just call the main with custom sys.argv or just use the args directly
        command_cloud.data = command_cloud.get_data(min_count=args.min, top_n=args.top)
        if args.html: command_cloud.generate_html(command_cloud.data)
        elif args.live: command_cloud.generate_live(command_cloud.data)
        else: command_cloud.generate_static(command_cloud.data)
    elif args.brain_cmd == "connect":
        storage.add_relationship(args.id1, args.id2)
        print(f"[v] Linked Node {args.id1} -> Node {args.id2}")
    elif args.brain_cmd == "forget": storage.delete_knowledge(args.id)
    elif args.brain_cmd == "graph":
        nodes = atlas.get_brain_data(limit=100)
        mmd_path = os.path.join(BASE_DIR, "docs/brain_graph.mmd")
        with open(mmd_path, "w", encoding="utf-8") as f: f.write(atlas.generate_mermaid_graph(nodes))
        print(f"[v] Graph exported to {mmd_path}")

def cmd_index(args):
    from clide.brain import memory
    from rich.table import Table
    from rich.console import Console
    console = Console()
    if args.index_cmd == "stat":
        stats = memory.get_registry_stats()
        table = Table(title="Index Registry Metrics", header_style="bold red")
        table.add_column("Metric", style="white")
        table.add_column("Value", style="cyan")
        table.add_row("Total Assets", str(stats['total_assets']))
        table.add_row("File Size", f"{stats['file_size_kb']:.2f} KB")
        table.add_row("Dimensions", str(stats['dimensions']))
        for t, count in stats['distribution'].items():
            table.add_row(f"Type: {t}", str(count))
        console.print(table)
    elif args.index_cmd == "full":
        from scripts import batch_indexer
        batch_indexer.run_full_index()
    elif args.index_cmd == "near":
        registry = []
        with open(memory.VECTOR_DB_PATH, "r") as f: registry = json.load(f)
        target = next((item for item in registry if item["id"] == args.id), None)
        if not target:
            print(f"Error: Asset '{args.id}' not found.")
            return
        results = []
        for item in registry:
            if item["id"] == args.id: continue
            sim = memory.cosine_similarity(target["embedding"], item["embedding"])
            results.append((sim, item))
        results.sort(key=lambda x: x[0], reverse=True)
        print(f"\n--- Neighbors of '{args.id}' ---")
        for sim, item in results[:5]: print(f"({sim:.3f}) {item['id']}: {item['metadata'].get('desc', '...')[:50]}")
    elif args.index_cmd == "optimize":
        pruned = memory.optimize_registry()
        print(f"[v] Registry optimized. Removed {pruned} duplicate/orphaned entries.")

def cmd_watch(args):
    from clide.watch import stream
    if args.watch_cmd == "start": stream.ClideExtractor().run()
    elif args.watch_cmd == "stop": stream.stop_monitor()
    elif args.watch_cmd == "status": print(f"Monitor Status: {stream.get_monitor_status()}")
    elif args.watch_cmd == "logs": stream.tail_logs(follow=args.tail)

def cmd_forge(args):
    from clide.gen import master
    orch = master.SynthesisOrchestrator()
    if args.forge_cmd == "tool": orch.process_tool_request(args.name, args.prompt)
    elif args.forge_cmd == "test": orch.run_tests(args.id)

def cmd_auto(args):
    from clide.brain import auto
    if args.auto_cmd == "tag": auto.auto_tag_nodes()
    elif args.auto_cmd == "plan": auto.auto_prioritize_tasks()
    elif args.auto_cmd == "sync": auto.auto_sync_todos()
    elif args.auto_cmd == "audit": auto.auto_audit_brain()

def main():
    intercept_info_requests(sys.argv)
    parser = argparse.ArgumentParser(description="CLIDE: Knowledge Operating System", add_help=False)
    subparsers = parser.add_subparsers(dest="command")

    # 1. WATCH
    watch_p = subparsers.add_parser("watch")
    watch_sub = watch_p.add_subparsers(dest="watch_cmd")
    watch_sub.add_parser("start")
    watch_sub.add_parser("stop")
    watch_sub.add_parser("status")
    watch_sub.add_parser("logs").add_argument("--tail", action="store_true")

    # 2. PROBE
    probe_p = subparsers.add_parser("probe")
    probe_sub = probe_p.add_subparsers(dest="probe_cmd")
    probe_sub.add_parser("scout").add_argument("url")
    probe_sub.add_parser("manual").add_argument("path")
    probe_sub.add_parser("capture")
    probe_sub.add_parser("crawl")

    # 3. BRAIN
    brain_p = subparsers.add_parser("brain")
    brain_sub = brain_p.add_subparsers(dest="brain_cmd")
    brain_sub.add_parser("query").add_argument("q")
    brain_sub.add_parser("graph")
    brain_sub.add_parser("merge")
    cloud_p = brain_sub.add_parser("cloud")
    cloud_p.add_argument("--live", action="store_true")
    cloud_p.add_argument("--html", action="store_true")
    cloud_p.add_argument("--top", type=int, default=100)
    cloud_p.add_argument("--min", type=int, default=1)
    brain_sub.add_parser("analyze")
    brain_sub.add_parser("summary")
    brain_sub.add_parser("audit")
    brain_sub.add_parser("verify")
    brain_sub.add_parser("list")
    link_p = brain_sub.add_parser("connect")
    link_p.add_argument("id1", type=int); link_p.add_argument("id2", type=int)
    brain_sub.add_parser("forget").add_argument("id", type=int)

    # 4. INDEX
    index_p = subparsers.add_parser("index")
    index_sub = index_p.add_subparsers(dest="index_cmd")
    index_sub.add_parser("full")
    index_sub.add_parser("near").add_argument("id")
    index_sub.add_parser("trace").add_argument("id")
    index_sub.add_parser("cluster")
    index_sub.add_parser("prune")
    index_sub.add_parser("optimize")
    index_sub.add_parser("stat")

    # 5. FORGE
    forge_p = subparsers.add_parser("forge")
    forge_sub = forge_p.add_subparsers(dest="forge_cmd")
    tool_p = forge_sub.add_parser("tool")
    tool_p.add_argument("name"); tool_p.add_argument("prompt")
    evolve_p = forge_sub.add_parser("evolve")
    evolve_p.add_argument("id"); evolve_p.add_argument("instruction")
    forge_sub.add_parser("design").add_argument("desc")
    forge_sub.add_parser("skill").add_argument("name")
    forge_sub.add_parser("persona").add_argument("name")
    forge_sub.add_parser("test").add_argument("id")
    forge_sub.add_parser("bench").add_argument("id")
    forge_sub.add_parser("archive").add_argument("id")

    # 6. AUTO
    auto_p = subparsers.add_parser("auto")
    auto_sub = auto_p.add_subparsers(dest="auto_cmd")
    auto_sub.add_parser("tag")
    auto_sub.add_parser("plan")
    auto_sub.add_parser("sync")
    auto_sub.add_parser("audit")
    auto_sub.add_parser("clean")

    # 7. SYSTEM
    sys_p = subparsers.add_parser("status")
    sys_p.set_defaults(command="system", sys_cmd="status")
    
    # 8. DASHBOARD
    subparsers.add_parser("dash")
    subparsers.add_parser("cli")

    # 9. MANUAL
    manual_p = subparsers.add_parser("manual")
    manual_sub = manual_p.add_subparsers(dest="manual_cmd")
    node_p = manual_sub.add_parser("node")
    node_op = node_p.add_subparsers(dest="op")
    node_op.add_parser("get").add_argument("id", type=int)
    move_p = node_op.add_parser("move"); move_p.add_argument("id", type=int); move_p.add_argument("cat")
    node_op.add_parser("delete").add_argument("id", type=int)
    tag_p = node_op.add_parser("tag")
    tag_p.add_argument("id", type=int); tag_p.add_argument("tags", nargs="+")
    task_p = manual_sub.add_parser("task")
    task_op = task_p.add_subparsers(dest="op")
    task_op.add_parser("list")
    task_op.add_parser("add").add_argument("content")
    task_op.add_parser("remove").add_argument("id", type=int)

    args = parser.parse_args()

    if not args.command:
        from clide.serve import dashboard
        dashboard.run_dashboard()
        return

    if args.command == "system": cmd_system(args)
    elif args.command == "manual": cmd_manual(args)
    elif args.command == "watch": cmd_watch(args)
    elif args.command == "forge": cmd_forge(args)
    elif args.command == "brain": cmd_brain(args)
    elif args.command == "index": cmd_index(args)
    elif args.command == "auto": cmd_auto(args)
    elif args.command in ["dash", "cli"]:
        from clide.serve import dashboard
        dashboard.run_dashboard()
    elif args.command == "probe":
        from clide.probe import scout, manual
        if args.probe_cmd == "manual": manual.extract_from_file(args.path)
        elif args.probe_cmd == "scout": scout.scout_url(args.url)
    else: print(f"Command '{args.command}' logic integration pending.")

if __name__ == "__main__":
    main()
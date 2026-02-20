import sys
import os
import json
import argparse
from art import tprint

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from clide.brain.memory import search_registry
from clide.kernel.settings import get_path, load_config
from clide.serve import guide, atlas

# --- HELP & REF INTERCEPTOR ---

def intercept_info_requests(argv):
    # Primary info keywords
    primary_info = ["help", "?", "ref", "atlas"]
    
    if not any(k in argv for k in primary_info):
        return None
    
    is_ref = any(k in argv for k in ["ref", "atlas", "map"])
    
    # Remove primary info keywords from args to find domain/command
    cleaned_args = [a for a in argv[1:] if a not in primary_info]
    domain = cleaned_args[0] if cleaned_args else None
    
    # Special case for './cli help help'
    if not domain and argv.count("help") > 1: domain = "help"
    
    command = cleaned_args[1] if len(cleaned_args) > 1 else None
    
    if is_ref: guide.show_ref(domain, command)
    else: guide.show_help(domain, command)
    sys.exit(0)

# --- SECTOR 01: SENSORY ---

def cmd_watch(args):
    from clide.watch import stream
    if args.watch_cmd == "go": stream.ClideExtractor().run()
    elif args.watch_cmd == "off": stream.stop_monitor()
    elif args.watch_cmd == "status": print(f"Monitor Status: {stream.get_monitor_status()}")
    elif args.watch_cmd == "logs": stream.tail_logs(follow=args.tail, limit=args.limit)

def cmd_probe(args):
    from clide.probe import scout, manual, crawl
    import subprocess
    
    if args.probe_cmd == "scout": scout.scout_url(args.url)
    elif args.probe_cmd == "ingest": manual.extract_from_file(args.path)
    elif args.probe_cmd == "crawl": crawl.crawl_site(args.url, depth=args.depth)
    elif args.probe_cmd == "capture":
        print("[Probe] Accessing system clipboard...")
        try:
            # Check for termux-api
            res = subprocess.run(["termux-clipboard-get"], capture_output=True, text=True)
            if res.returncode == 0:
                content = res.stdout.strip()
                if content:
                    manual.extract_from_text(content, source="clipboard")
                else:
                    print("[!] Clipboard is empty.")
            else:
                print("[!] API Error: Ensure Termux:API is installed and authorized.")
        except FileNotFoundError:
            print("[!] 'termux-clipboard-get' not found. Is Termux:API package installed?")
        except Exception as e:
            print(f"[!] Capture failed: {e}")

# --- SECTOR 02: COGNITIVE ---

def cmd_search(args):
    results = search_registry(args.query)
    print(f"\n--- Search Results for '{args.query}' ---")
    for sim, item in results:
        print(f"({sim:.2f}) {item['id']}: {item['metadata'].get('desc', 'No description')}")

def cmd_brain(args):
    from clide.serve import atlas
    from clide.brain import auto
    if args.brain_cmd == "analyze": atlas.run_deep_analysis()
    elif args.brain_cmd == "summary": atlas.generate_brain_summary()
    elif args.brain_cmd == "verify": atlas.verify_facts()
    elif args.brain_cmd == "approve": auto.approve_proposals()

def cmd_map(args):
    from clide.serve import atlas
    # map graph, cloud, trace, stats
    if args.map_cmd == "graph":
        nodes = atlas.get_brain_data(limit=100)
        if getattr(args, "mermaid", False):
            mmd_path = os.path.join(BASE_DIR, "docs/brain_graph.mmd")
            with open(mmd_path, "w", encoding="utf-8") as f: f.write(atlas.generate_mermaid_graph(nodes))
            print(f"[v] Mermaid graph exported to {mmd_path}")
        else:
            atlas.render_ascii_graph(nodes)
    elif args.map_cmd == "cloud":
        from scripts import command_cloud
        data = command_cloud.get_data(min_count=args.min, top_n=args.top)
        if args.html: command_cloud.generate_html(data)
        elif args.live: command_cloud.generate_live(data)
        else: command_cloud.generate_static(data)
    elif args.map_cmd == "trace":
        atlas.render_trace_tree(args.id)
    elif args.map_cmd == "stats":
        atlas.render_stats_table()

def cmd_index(args):
    from clide.brain import memory
    from rich.table import Table
    from rich.console import Console
    console = Console()
    
    if args.index_cmd == "stats":
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
    elif args.index_cmd == "rebuild":
        from scripts import batch_indexer
        batch_indexer.run_full_index()
    elif args.index_cmd == "archives":
        from scripts import rebuild_archives
        rebuild_archives.run_archive_rebuild()
    elif args.index_cmd == "cluster":
        clusters = memory.cluster_registry(threshold=0.85)
        
        print(f"\n--- Knowledge Clusters (Threshold: 0.85) ---")
        if not clusters:
            print("[!] No significant clusters found.")
        else:
            for i, c in enumerate(clusters[:10]): # Top 10
                print(f"Cluster {i+1}: {c['size']} items")
                desc = c.get('centroid_desc', 'Unknown')
                print(f"  Topic: {desc[:60]}...")
                members = c.get('members', [])
                print(f"  Sample: {', '.join(members[:3])}...")
                print("")
    elif args.index_cmd == "prune":
        count = memory.prune_registry(min_importance=3)
        print(f"[v] Pruned {count} low-importance entries from the vector registry.")
    elif args.index_cmd == "optimize":
        pruned = memory.optimize_registry()
        print(f"[v] Registry optimized. Removed {pruned} duplicate/orphaned entries.")

# --- SECTOR 03: STATE ---

def cmd_memory(args):
    from clide.kernel import storage
    from clide.serve import atlas
    # list, create, edit, delete, connect, merge, forget
    if args.mem_cmd == "list":
        atlas.list_brain_units(limit=args.limit)
    elif args.mem_cmd == "create":
        # Manual node init
        storage.save_knowledge(args.category, args.content, "Manual CLI addition")
        print(f"[v] Created {args.category} node.")
    elif args.mem_cmd == "edit":
        # Contextual CRUD
        storage.update_knowledge(args.id, content=args.content)
        print(f"[v] Updated node {args.id}")
    elif args.mem_cmd == "delete":
        storage.delete_knowledge(args.id, soft=True)
        print(f"[v] Soft-deleted node {args.id}")
    elif args.mem_cmd == "connect":
        storage.add_relationship(args.id1, args.id2)
        print(f"[v] Linked Node {args.id1} -> Node {args.id2}")
    elif args.mem_cmd == "merge":
        from scripts import merge_logs
        merge_logs.run_log_merge()
    elif args.mem_cmd == "forget":
        storage.delete_knowledge(args.id, soft=False)
        print(f"[v] Hard-deleted node {args.id}")

def cmd_run(args):
    from clide.brain import auto
    from clide.tools import janitor
    # plan, task, sync
    if args.run_cmd == "plan":
        auto.auto_prioritize_tasks()
    elif args.run_cmd == "task":
        mgr = janitor.TodoManager()
        if args.op == "list": mgr.list_todos()
        elif args.op == "add": mgr.add_todo(args.content)
        elif args.op == "remove": mgr.remove_todo(args.id)
        elif args.op == "complete": mgr.complete_todo(args.id)
    elif args.run_cmd == "sync":
        auto.auto_sync_todos()

def cmd_maintain(args):
    from clide.brain import auto, governance
    # tag, clean, audit, strategist
    if args.main_cmd == "tag": auto.auto_tag_nodes()
    elif args.main_cmd == "clean": auto.auto_clean_metadata()
    elif args.main_cmd == "audit": auto.auto_audit_brain()
    elif args.main_cmd == "strategist": governance.run_strategist()

# --- SECTOR 04: EXECUTIVE ---

def cmd_forge(args):
    from clide.forge import master
    orch = master.SynthesisOrchestrator()
    if args.forge_cmd == "tool": orch.process_tool_request(args.name, args.prompt)
    elif args.forge_cmd == "evolve": orch.evolve_tool(args.id, args.instruction)
    elif args.forge_cmd == "design": orch.generate_design(args.name, args.desc)
    elif args.forge_cmd == "skill": orch.create_skill(args.name, args.description)
    elif args.forge_cmd == "persona": orch.define_persona(args.name, args.description, args.directive)
    elif args.forge_cmd == "test": orch.run_tests(args.id)
    elif args.forge_cmd == "bench": orch.run_benchmark(args.id)
    elif args.forge_cmd == "archive": orch.archive_asset(args.id)

def cmd_system(args):
    if args.sys_cmd == "config":
        config = load_config()
        print("\n--- CLIDE KERNEL CONFIGURATION ---")
        print(json.dumps(config, indent=2))
    elif args.sys_cmd == "asset":
        from clide.brain import memory
        stats = memory.get_registry_stats()
        print("\n--- CLIDE ASSET INVENTORY ---")
        print(f"Total Registered Assets: {stats['total_assets']}")
        for t, count in stats['distribution'].items():
            print(f" - {t:15}: {count}")
    elif args.sys_cmd == "health":
        # Alias for status or expanded health check
        from scripts import ingestion_stats
        ingestion_stats.show_ingestion_stats()
    elif args.sys_cmd == "backup":
        import shutil
        from datetime import datetime
        backup_dir = os.path.join(BASE_DIR, "clide/backups")
        os.makedirs(backup_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        db_path = get_path("memory")
        backup_path = os.path.join(backup_dir, f"memory_{ts}.db")
        shutil.copy2(db_path, backup_path)
        print(f"[v] Full-state backup created at: {backup_path}")
    elif args.sys_cmd == "resume":
        print("[System] Resuming last cognitive session...")
        # Implementation for session resumption
        from clide.serve import dashboard
        dashboard.run_dashboard()
    elif args.sys_cmd == "dash":
         from clide.serve import dashboard
         dashboard.run_dashboard()

def main():
    intercept_info_requests(sys.argv)
    parser = argparse.ArgumentParser(description="CLIDE: Knowledge Operating System", add_help=False)
    subparsers = parser.add_subparsers(dest="command")

    # --- SECTOR 01: SENSORY ---
    
    # WATCH
    watch_p = subparsers.add_parser("watch")
    watch_sub = watch_p.add_subparsers(dest="watch_cmd")
    watch_sub.add_parser("go")
    watch_sub.add_parser("off")
    watch_sub.add_parser("status")
    logs_p = watch_sub.add_parser("logs")
    logs_p.add_argument("--tail", action="store_true")
    logs_p.add_argument("--limit", type=int, default=10)

    # PROBE
    probe_p = subparsers.add_parser("probe")
    probe_sub = probe_p.add_subparsers(dest="probe_cmd")
    probe_sub.add_parser("scout").add_argument("url")
    probe_sub.add_parser("ingest").add_argument("path")
    probe_sub.add_parser("capture")
    crawl_p = probe_sub.add_parser("crawl")
    crawl_p.add_argument("url")
    crawl_p.add_argument("--depth", type=int, default=1)

    # --- SECTOR 02: COGNITIVE ---

    # SEARCH
    search_p = subparsers.add_parser("search")
    search_p.add_argument("query")

    # BRAIN
    brain_p = subparsers.add_parser("brain")
    brain_sub = brain_p.add_subparsers(dest="brain_cmd")
    brain_sub.add_parser("analyze")
    brain_sub.add_parser("summary")
    brain_sub.add_parser("verify")
    brain_sub.add_parser("approve")

    # MAP
    map_p = subparsers.add_parser("map")
    map_sub = map_p.add_subparsers(dest="map_cmd")
    map_graph = map_sub.add_parser("graph")
    map_graph.add_argument("--mermaid", action="store_true", help="Export Mermaid graph to file")
    cloud_p = map_sub.add_parser("cloud")
    cloud_p.add_argument("--live", action="store_true")
    cloud_p.add_argument("--html", action="store_true")
    cloud_p.add_argument("--top", type=int, default=100)
    cloud_p.add_argument("--min", type=int, default=1)
    map_sub.add_parser("trace").add_argument("id")
    map_sub.add_parser("stats")

    # INDEX
    index_p = subparsers.add_parser("index")
    index_sub = index_p.add_subparsers(dest="index_cmd")
    index_sub.add_parser("rebuild")
    index_sub.add_parser("archives")
    index_sub.add_parser("cluster")
    index_sub.add_parser("prune")
    index_sub.add_parser("optimize")
    index_sub.add_parser("stats")

    # --- SECTOR 03: STATE ---

    # MEMORY
    mem_p = subparsers.add_parser("memory")
    mem_sub = mem_p.add_subparsers(dest="mem_cmd")
    mem_list = mem_sub.add_parser("list")
    mem_list.add_argument("--limit", type=int, default=20)
    mem_create = mem_sub.add_parser("create")
    mem_create.add_argument("content")
    mem_create.add_argument("--category", default="general")
    mem_create.add_argument("--tags", nargs="+", default=[])
    mem_edit = mem_sub.add_parser("edit")
    mem_edit.add_argument("id", type=int)
    mem_edit.add_argument("content")
    mem_del = mem_sub.add_parser("delete")
    mem_del.add_argument("id", type=int)
    mem_conn = mem_sub.add_parser("connect")
    mem_conn.add_argument("id1", type=int)
    mem_conn.add_argument("id2", type=int)
    mem_sub.add_parser("merge")
    mem_forget = mem_sub.add_parser("forget")
    mem_forget.add_argument("id", type=int)

    # RUN
    run_p = subparsers.add_parser("run")
    run_sub = run_p.add_subparsers(dest="run_cmd")
    run_sub.add_parser("plan")
    run_task = run_sub.add_parser("task")
    run_task_op = run_task.add_subparsers(dest="op")
    run_task_op.add_parser("list")
    run_task_add = run_task_op.add_parser("add")
    run_task_add.add_argument("content")
    run_task_rem = run_task_op.add_parser("remove")
    run_task_rem.add_argument("id", type=int)
    run_task_comp = run_task_op.add_parser("complete")
    run_task_comp.add_argument("id", type=int)
    run_sub.add_parser("sync")

    # MAINTAIN
    maint_p = subparsers.add_parser("maintain")
    maint_sub = maint_p.add_subparsers(dest="main_cmd")
    maint_sub.add_parser("tag")
    maint_sub.add_parser("clean")
    maint_sub.add_parser("audit")
    maint_sub.add_parser("strategist")

    # --- SECTOR 04: EXECUTIVE ---

    # FORGE
    forge_p = subparsers.add_parser("forge")
    forge_sub = forge_p.add_subparsers(dest="forge_cmd")
    forge_tool = forge_sub.add_parser("tool")
    forge_tool.add_argument("name")
    forge_tool.add_argument("prompt")
    forge_evolve = forge_sub.add_parser("evolve")
    forge_evolve.add_argument("id")
    forge_evolve.add_argument("instruction")
    forge_design = forge_sub.add_parser("design")
    forge_design.add_argument("name")
    forge_design.add_argument("desc")
    forge_skill = forge_sub.add_parser("skill")
    forge_skill.add_argument("name")
    forge_skill.add_argument("description", nargs="?", default="Modular skill.")
    forge_persona = forge_sub.add_parser("persona")
    forge_persona.add_argument("name")
    forge_persona.add_argument("description", nargs="?", default="System persona.")
    forge_persona.add_argument("directive", nargs="?", default="Optimize output.")
    forge_test = forge_sub.add_parser("test")
    forge_test.add_argument("id")
    forge_bench = forge_sub.add_parser("bench")
    forge_bench.add_argument("id")
    forge_archive = forge_sub.add_parser("archive")
    forge_archive.add_argument("id")

    # SYSTEM
    sys_p = subparsers.add_parser("system")
    sys_sub = sys_p.add_subparsers(dest="sys_cmd")
    sys_sub.add_parser("dash") # alias
    sys_sub.add_parser("config")
    sys_sub.add_parser("asset")
    sys_sub.add_parser("health")
    sys_sub.add_parser("backup")
    sys_sub.add_parser("resume")

    # --- LEGACY / ALIASES ---
    subparsers.add_parser("dash") # Top level dash alias

    args = parser.parse_args()

    if not args.command or args.command == "dash":
        from clide.serve import ui
        ui.launch_hub()
        return

    # Dispatch
    if args.command == "watch": cmd_watch(args)
    elif args.command == "probe": cmd_probe(args)
    elif args.command == "search": cmd_search(args)
    elif args.command == "brain": cmd_brain(args)
    elif args.command == "map": cmd_map(args)
    elif args.command == "index": cmd_index(args)
    elif args.command == "memory": cmd_memory(args)
    elif args.command == "run": cmd_run(args)
    elif args.command == "maintain": cmd_maintain(args)
    elif args.command == "forge": cmd_forge(args)
    elif args.command == "system": cmd_system(args)

if __name__ == "__main__":
    main()

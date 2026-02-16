import sqlite3
import os
import json
import csv
import math
from collections import defaultdict
from datetime import datetime

DB_PATH = "/data/data/com.termux/files/home/openclaw/meta/clide/memory.db"
OUTPUT_DIR = "/data/data/com.termux/files/home/openclaw/meta/ingestion_logs"

# Tiered Hierarchy Mapping - Significantly expanded to capture "Unsorted"
HIERARCHY = {
    "🛠 Engineering & Architecture": {
        "System Synthesis": ["engineer", "implement", "dev", "build", "execute", "generate", "scaffold", "create", "make", "blueprint", "frontend", "spa", "mockup", "design", "port_to_ralph"],
        "Logic Refactoring": ["refactor", "modernize", "deconstruct", "modularize", "zen", "clean_code", "replace_static", "simplify", "zen", "reformat_file", "refine", "flesh_out", "deobfuscate"],
        "Advanced Analysis": ["extract_logic", "annotate_code", "deconstruct_program", "understand_project", "decompose", "analyze_results", "describe_project", "analyze_data", "analyze_blocks"]
    },
    "📡 Intelligence & Extraction": {
        "Browser Automation": ["scraper", "crawl", "scrape", "link_checker", "web_scraping", "url_management", "process_urls", "url_processing", "check_urls", "crawl_site", "website_search", "recursive_link_discovery", "extract_ref_links"],
        "Social Automation": ["facebook", "social_scrape", "fb_posts", "social_login", "fb_actions", "extract_fb_posts", "search_facebook", "moltbook", "social_growth", "post_manager", "engage_social", "post"],
        "Math & Financials": ["calculate", "valuation", "edge", "metrics", "calculate_score", "extrapolate", "bonus_value", "calculate_bonus", "rank", "success_rate", "rate_limit", "semantic_representation", "aggregate_values", "extract_and_sum"]
    },
    "🎨 UI/UX & Visualization": {
        "Interface Layout": ["layout", "ui_config", "grid", "flex", "panel", "modal", "sidebar", "fullscreen", "reposition", "resize", "reorganize_system_status", "customize_ui", "ui_component", "balance_launch", "adjust_slider", "slider"],
        "Visual Semantics": ["theme", "color", "palette", "gradient", "symbols", "emoji", "styling", "visual_pattern", "aesthetic", "bootstrap_symbols", "emoji_replace", "explore_icons", "effect", "smooth_step_control", "toggle_log_exp"],
        "Data Viz & Rendering": ["visualize", "graph", "chart", "diagram", "mermaid", "animation", "screenshot", "draw_separator", "plot", "render", "view_image", "display_image", "visual_generation", "grid_visualizer"]
    },
    "📊 Data Operations": {
        "Transformation": ["json", "csv", "db_export", "spreadsheet", "parse", "transform", "reformat_table", "format_data", "data_transformation", "text_process", "encode_sequence", "format_logs", "format_delimiter", "format_number"],
        "Storage & Persistence": ["database", "sqlite", "save", "archive", "backup", "sqlmodel", "db_support", "db_management", "store", "export_to_db", "migrate_db", "query_db"],
        "Clustering & Cleaning": ["cluster", "batch", "cleanup", "mass_filter", "text_process", "deduplicate", "filter", "remove_numbers", "cleanup_restructure", "dedupe", "clean_list", "clean_text_file"]
    },
    "📋 Project Governance": {
        "Strategic Ops": ["plan", "roadmap", "conductor", "tracks", "status", "progress", "summary", "summarize", "milestone", "pi_phase", "assess", "changes", "query_phase", "roadmap_progress"],
        "Task Management": ["orchestrate", "sequential_execution", "approve", "task", "priority", "research", "todo", "assign", "prioritize", "prepare", "postpone"],
        "System Meta": ["prompt", "persona", "role", "assistant", "hotswap", "brain", "cognitive", "meta", "constitution", "behavior", "tag", "about", "ancillary_docs", "document", "moltbot"]
    },
    "🔧 Infrastructure & Utility": {
        "Git & Remote": ["git", "repo", "push", "pull", "upload", "branch", "clone", "commit", "github", "browse_repo"],
        "Validation Core": ["test", "audit", "ensure", "verify", "validate", "check", "stress", "simulation", "emulate", "retest", "diagnostic", "data_confirmation", "double_check"],
        "General Utility": ["exit", "quit", "revert", "undo", "rollback", "resume", "break", "restart", "help", "alias", "venv", "terminal", "pkg", "shell", "settings", "config", "configure", "split_file", "move_files", "tune_threads", "binary"]
    }
}

def cosine_similarity(v1, v2):
    if not v1 or not v2: return 0
    dot_product = sum(x * y for x, y in zip(v1, v2))
    mag1 = math.sqrt(sum(x*x for x in v1))
    mag2 = math.sqrt(sum(x*x for x in v2))
    return dot_product / (mag1 * mag2) if mag1 > 0 and mag2 > 0 else 0

def clean_txt(text):
    if not text: return ""
    return text.replace("\n", " ").replace("|", "\\|")

def get_tier(name):
    name_lower = name.lower()
    for domain, sub_domains in HIERARCHY.items():
        for sub, keywords in sub_domains.items():
            if any(kw in name_lower for kw in keywords):
                return domain, sub
    return "🌐 General/Unsorted", "Misc Operations"

def generate_hierarchical_theorycrafting():
    print("🦞 Starting Advanced Hierarchical Analysis (Entropy Reduction Mode)...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT command_name, content, review, tags, importance, session_id, embedding FROM knowledge WHERE category = 'NEW_COMMAND'")
    
    raw_data = cursor.fetchall()
    commands = {}
    
    for row in raw_data:
        name, content, review, tags_json, imp, sid, emb_blob = row
        name = name or "pending_assignment"
        if name not in commands:
            commands[name] = {"desc": content, "instances": [], "embeddings": []}
        commands[name]["instances"].append({"sid": sid, "review": review, "tags": json.loads(tags_json), "importance": imp or 5})
        if emb_blob: commands[name]["embeddings"].append(json.loads(emb_blob.decode('utf-8')))

    tree = defaultdict(lambda: defaultdict(list))
    domain_stats = defaultdict(lambda: {"occ": 0, "unique": 0, "imp_sum": 0})

    for name, data in commands.items():
        domain, sub = get_tier(name)
        occ = len(data["instances"])
        avg_imp = sum(inst["importance"] for inst in data["instances"]) / occ
        
        all_tags = set()
        for inst in data["instances"]: all_tags.update(inst["tags"])
        
        cmd_obj = {
            "name": name, "occ": occ, "imp": round(avg_imp, 1), 
            "desc": clean_txt(data["desc"]), "tags": ", ".join(list(all_tags))
        }
        
        tree[domain][sub].append(cmd_obj)
        domain_stats[domain]["occ"] += occ
        domain_stats[domain]["unique"] += 1
        domain_stats[domain]["imp_sum"] += avg_imp

    # Calculate average domain importance for sorting
    domain_avg_imp = {}
    for dom, stats in domain_stats.items():
        domain_avg_imp[dom] = stats["imp_sum"] / stats["unique"]

    # Generate MD Report
    report = "# 🧠 Theorycrafting: Hierarchical Command Map (V2)\n\n"
    
    report += "## 📊 Domain Overview\n\n"
    report += "| Domain | Sub-Domain | Total Occ | Unique | Avg Imp |\n"
    report += "| :--- | :--- | :--- | :--- | :--- |\n"
    
    total_unique = 0
    total_occ = 0
    total_imp_sum = 0
    
    # Sort domains by average importance, keep Unsorted at end
    sorted_domains = sorted([d for d in domain_stats.keys() if d != "🌐 General/Unsorted"], 
                            key=lambda x: domain_avg_imp[x], reverse=True)
    if "🌐 General/Unsorted" in domain_stats:
        sorted_domains.append("🌐 General/Unsorted")

    for dom in sorted_domains:
        stats = domain_stats[dom]
        avg_dom_imp = domain_avg_imp[dom]
        # Domain Header
        report += f"| **{dom}** | *ALL* | {stats['occ']} | {stats['unique']} | {avg_dom_imp:.1f} |\n"
        
        # Sub-Domain Breakdown (Directly under parent)
        for sub, cmds in sorted(tree[dom].items()):
            sub_occ = sum(c['occ'] for c in cmds)
            sub_unique = len(cmds)
            sub_imp_sum = sum(c['imp'] for c in cmds)
            sub_avg_imp = sub_imp_sum / sub_unique if sub_unique > 0 else 0
            report += f"| {dom} | {sub} | {sub_occ} | {sub_unique} | {sub_avg_imp:.1f} |\n"

        total_unique += stats["unique"]
        total_occ += stats["occ"]
        total_imp_sum += stats["imp_sum"]
    report += f"| **TOTALS** | -- | **{total_occ}** | **{total_unique}** | **{total_imp_sum/total_unique:.1f}** |\n\n---\n\n"

    # 2. Detailed Mapping (Skip Unsorted for now, will put at end)
    for dom in sorted_domains:
        if dom == "🌐 General/Unsorted": continue
        report += f"# {dom}\n"
        for sub, cmds in sorted(tree[dom].items()):
            report += f"\n## 💠 {sub}\n"
            report += "| Command | Recurrence | Imp | Cluster/Description |\n"
            report += "| :--- | :--- | :--- | :--- |\n"
            for c in sorted(cmds, key=lambda x: x["occ"], reverse=True):
                report += f"| `{c['name']}` | {c['occ']} | {c['imp']} | {c['desc'][:120]}... |\n"
            report += "\n---\n"

    # 3. Dedicated Unsorted Section (Ordered by Importance)
    unsorted_cmds = []
    if "🌐 General/Unsorted" in tree:
        for sub, cmds in tree["🌐 General/Unsorted"].items():
            unsorted_cmds.extend(cmds)
    
    if unsorted_cmds:
        report += "\n# 🌐 Remaining Unsorted Commands\n"
        report += "*Ordered by Avg Importance (Descending)*\n\n"
        report += "| Command | Imp | Recurrence | Context Snippet |\n"
        report += "| :--- | :--- | :--- | :--- |\n"
        
        for c in sorted(unsorted_cmds, key=lambda x: x["imp"], reverse=True):
            report += f"| `{c['name']}` | **{c['imp']}** | {c['occ']} | {c['desc'][:100]}... |\n"

    # 4. Duplicate Merges
    potential_merges = []
    cmd_list = list(commands.keys())
    for i in range(len(cmd_list)):
        for j in range(i + 1, len(cmd_list)):
            n1, n2 = cmd_list[i], cmd_list[j]
            if n1 == "pending_assignment" or n2 == "pending_assignment": continue
            if commands[n1]["embeddings"] and commands[n2]["embeddings"]:
                sim = cosine_similarity(commands[n1]["embeddings"][0], commands[n2]["embeddings"][0])
                if sim > 0.92:
                    potential_merges.append((n1, n2, sim))

    report += "\n# 👯 Potential Duplicate Merges (High Similarity)\n"
    report += "| Primary | Secondary | Score | Recommendation |\n"
    report += "| :--- | :--- | :--- | :--- |\n"
    for n1, n2, sim in sorted(potential_merges, key=lambda x: x[2], reverse=True)[:30]:
        report += f"| `{n1}` | `{n2}` | {sim:.3f} | Merge into `{n1}` |\n"

    with open(os.path.join(OUTPUT_DIR, "theorycrafting_report.md"), 'w') as f:
        f.write(report)

    # 5. CSV
    with open(os.path.join(OUTPUT_DIR, "theorycrafting.csv"), 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Domain", "Sub-Domain", "Command", "Occurrences", "Avg Importance", "Description"])
        writer.writeheader()
        for dom in sorted_domains:
            for sub in sorted(tree[dom].keys()):
                for c in tree[dom][sub]:
                    writer.writerow({
                        "Domain": dom, "Sub-Domain": sub, "Command": c["name"],
                        "Occurrences": c["occ"], "Avg Importance": c["imp"], "Description": c["desc"]
                    })

    print("Advanced Hierarchical Report generated.")

if __name__ == "__main__":
    generate_hierarchical_theorycrafting()
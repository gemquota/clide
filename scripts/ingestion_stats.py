import os
import json
import sqlite3
import math
from rich.console import Console
from rich.table import Table
from clide.brain.memory import get_registry_stats
from clide.kernel import storage

def make_mini_bar(percentage, width=20):
    percentage = min(100, max(0, percentage))
    filled = int(percentage / 100 * width)
    bar = "█" * filled + "░" * (width - filled)
    
    # Spectrum color logic
    if percentage > 90: color = "bold #ff00ff" # Gamma
    elif percentage > 70: color = "bold #5f00ff" # UV
    elif percentage > 40: color = "#00ffff" # Cyan
    elif percentage > 15: color = "#ff8700" # Orange
    else: color = "#ff0000" # Radio/Red
    
    return f"[{color}]{bar}[/] {percentage:>5.1f}%"

def get_db_counts():
    conn = storage.get_connection()
    cursor = conn.cursor()
    
    # 1. Shell History count
    shell_count = cursor.execute("SELECT COUNT(*) FROM knowledge WHERE category='SHELL_HISTORY'").fetchone()[0]
    
    # 2. Enriched Telemetry count (items with session IDs)
    telemetry_count = cursor.execute("SELECT COUNT(*) FROM knowledge WHERE session_id IS NOT NULL AND category != 'SHELL_HISTORY'").fetchone()[0]
    
    # 3. Archive/Manual count (items without session IDs and not shell history)
    archive_count = cursor.execute("SELECT COUNT(*) FROM knowledge WHERE session_id IS NULL AND category != 'SHELL_HISTORY'").fetchone()[0]
    
    conn.close()
    return shell_count, telemetry_count, archive_count

def show_ingestion_stats():
    console = Console()
    
    # 1. Get Totals from Filesystem
    # Raw Logs
    log_path = "clide/enriched_logs.json"
    log_total = 0
    if os.path.exists(log_path):
        try:
            with open(log_path, "r") as f:
                logs = json.load(f)
                log_total = len(logs)
        except: pass
        
    # Shell History
    zsh_path = os.path.expanduser("~/.zsh_history")
    bash_path = os.path.expanduser("~/.bash_history")
    shell_total = 0
    for p in [zsh_path, bash_path]:
        if os.path.exists(p):
            try:
                with open(p, "r", errors="ignore") as f:
                    shell_total += sum(1 for _ in f)
            except: pass
            
    # Conversation Archives
    conv_lines = 0
    ingestion_dir = "ingestion_logs"
    if os.path.exists(ingestion_dir):
        for root, _, files in os.walk(ingestion_dir):
            for f in files:
                if f.endswith(".md"):
                    try:
                        with open(os.path.join(root, f), "r", errors="ignore") as f_obj:
                            conv_lines += sum(1 for _ in f_obj)
                    except: pass
    archive_total = int(conv_lines / 50) # 1 Knowledge Unit per 50 lines approx

    # 2. Get Current from Database
    db_shell, db_telemetry, db_archive = get_db_counts()

    # 3. Calculate Normalized Targets (Avoid overflow in display)
    # If DB has more than file (e.g. file was rotate/cleared), adjust target
    disp_log_total = max(log_total, db_telemetry)
    disp_shell_total = max(shell_total, db_shell)
    disp_archive_total = max(archive_total, db_archive)

    # 4. Calculate Percentages
    log_pct = (db_telemetry / disp_log_total * 100) if disp_log_total > 0 else 100
    shell_pct = (db_shell / disp_shell_total * 100) if disp_shell_total > 0 else 0
    archive_pct = (db_archive / disp_archive_total * 100) if disp_archive_total > 0 else 0
    
    # Aggregate
    total_potential = disp_log_total + disp_shell_total + disp_archive_total
    total_embedded = db_telemetry + db_shell + db_archive
    global_pct = (total_embedded / total_potential * 100) if total_potential > 0 else 0

    # 5. Render
    table = Table(title="[bold red]╶─╼ ⟨ ◈ NEURAL SATURATION TELEMETRY ◈ ⟩ ╾─╴[/]", border_style="red", header_style="bold magenta", box=None)
    table.add_column("Ingestion Layer", style="cyan", width=25)
    table.add_column("Current / Total", justify="right", width=20)
    table.add_column("Neural Saturation (Relative Density)", justify="left")
    
    table.add_row(
        "Enriched Telemetry", 
        f"{db_telemetry} / {disp_log_total}", 
        make_mini_bar(log_pct)
    )
    table.add_row(
        "Shell History", 
        f"{db_shell} / {disp_shell_total}", 
        make_mini_bar(shell_pct)
    )
    table.add_row(
        "Conversation Archives", 
        f"{db_archive} / {disp_archive_total}", 
        make_mini_bar(archive_pct)
    )
    
    # Aggregation Divider
    table.add_section()
    table.add_row(
        "[bold white]CORE KERNEL AGGREGATE[/]", 
        f"[bold white]{total_embedded} / {total_potential}[/]]", 
        make_mini_bar(global_pct, width=30)
    )
    
    console.print("\n")
    console.print(table)
    
    # Large Footer Bar (Spectral Pulse)
    bar_width = 60
    filled = int(global_pct / 100 * bar_width)
    bar = "█" * filled + "░" * (bar_width - filled)
    
    # Dynamic Color based on EM Spectrum
    if global_pct > 90: color = "bold #ff00ff"
    elif global_pct > 70: color = "bold #5f00ff"
    elif global_pct > 40: color = "bold #00ffff"
    elif global_pct > 20: color = "bold #00ff00"
    else: color = "bold #ff0000"
    
    console.print(f"\n[{color}]TOTAL NEURAL SATURATION:[/] [{color}]{bar}[/] {global_pct:.2f}%\n")

if __name__ == "__main__":
    show_ingestion_stats()
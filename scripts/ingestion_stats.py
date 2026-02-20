import os
import json
import sqlite3
import math
import re
from rich.console import Console
from rich.table import Table
from clide.kernel import storage

def make_mini_bar(percentage, width=20):
    percentage = min(100, max(0, percentage))
    filled = int(percentage / 100 * width)
    bar = "█" * filled + "░" * (width - filled)
    if percentage > 90: color = "bold #ff00ff" # Gamma
    elif percentage > 70: color = "bold #5f00ff" # UV
    elif percentage > 40: color = "#00ffff" # Cyan
    elif percentage > 15: color = "#ff8700" # Orange
    else: color = "#ff0000" # Radio/Red
    
    return f"[{color}]{bar}[/] {percentage:>5.1f}%"

def normalize_simple(text):
    if not text: return ""
    text = text.replace('\n', ' ').strip()
    text = re.sub(r'\s+', ' ', text)
    return text

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

def get_combined_stats():
    db_shell, db_telemetry, db_archive = get_db_counts()
    
    # Calculate Targets (Unique)
    log_path = "clide/enriched_logs.json"
    log_total = 0
    if os.path.exists(log_path):
        try:
            with open(log_path, "r") as f:
                logs = json.load(f)
                log_total = len(logs)
        except: pass
        
    zsh_path = os.path.expanduser("~/.zsh_history")
    bash_path = os.path.expanduser("~/.bash_history")
    shell_unique = set()
    for p in [zsh_path, bash_path]:
        if os.path.exists(p):
            try:
                with open(p, "r", errors="ignore") as f:
                    for line in f:
                        if "; " in line: cmd = line.split("; ", 1)[1].strip()
                        elif line.startswith(":"):
                            parts = line.split(";", 1)
                            cmd = parts[1].strip() if len(parts) > 1 else line.strip()
                        else: cmd = line.strip()
                        if len(cmd) > 3: shell_unique.add(cmd)
            except: pass
    shell_total = len(shell_unique)
    
    archive_total = 0
    ingestion_dir = "ingestion_logs"
    if os.path.exists(ingestion_dir):
        all_unique = set()
        for root, _, files in os.walk(ingestion_dir):
            for f_name in files:
                if f_name.endswith('.md'):
                    try:
                        with open(os.path.join(root, f_name), 'r', errors='ignore') as f:
                            text = f.read()
                            for s in re.findall(r'\| \"([^\"]+)\" \|', text):
                                if len(s) > 5: all_unique.add(normalize_simple(s))
                            for d in re.findall(r'\*\*Primary Definition:\* \\*(.*?)\\*\*', text):
                                if len(d) > 5: all_unique.add(normalize_simple(d))
                            for c in re.findall(r'\*\*COMMAND:\* \`+([^\`]+)\`+', text):
                                all_unique.add(normalize_simple(c))
                    except: pass
        archive_total = len(all_unique)

    disp_log_total = max(log_total, db_telemetry)
    disp_shell_total = max(shell_total, db_shell)
    disp_archive_total = max(archive_total, db_archive)

    total_potential = disp_log_total + disp_shell_total + disp_archive_total
    total_embedded = db_telemetry + db_shell + db_archive
    global_pct = (total_embedded / total_potential * 100) if total_potential > 0 else 0

    return {
        "shell": f"{db_shell} / {disp_shell_total}",
        "sessions": f"{db_telemetry} / {disp_log_total}",
        "archives": f"{db_archive} / {disp_archive_total}",
        "saturation": int(global_pct)
    }

def show_ingestion_stats():
    console = Console()
    stats = get_combined_stats()
    db_shell, db_telemetry, db_archive = get_db_counts()
    
    # Extract total targets from the strings in stats
    disp_log_total = int(stats['sessions'].split(' / ')[1])
    disp_shell_total = int(stats['shell'].split(' / ')[1])
    disp_archive_total = int(stats['archives'].split(' / ')[1])

    # Calculate Percentages
    log_pct = (db_telemetry / disp_log_total * 100) if disp_log_total > 0 else 100
    shell_pct = (db_shell / disp_shell_total * 100) if disp_shell_total > 0 else 100
    archive_pct = (db_archive / disp_archive_total * 100) if disp_archive_total > 0 else 100
    
    total_embedded = db_telemetry + db_shell + db_archive
    total_potential = disp_log_total + disp_shell_total + disp_archive_total
    global_pct = (total_embedded / total_potential * 100) if total_potential > 0 else 0

    # Render
    table = Table(title="[bold red]╶─╼ ⟨ ◈ NEURAL SATURATION TELEMETRY ◈ ⟩ ╾─╴[/]", border_style="red", header_style="bold magenta", box=None)
    table.add_column("Ingestion Layer", style="cyan", width=25)
    table.add_column("Current / Total", justify="right", width=20)
    table.add_column("Neural Saturation (Relative Density)", justify="left")
    
    table.add_row("Enriched Telemetry", f"{db_telemetry} / {disp_log_total}", make_mini_bar(log_pct))
    table.add_row("Shell History", f"{db_shell} / {disp_shell_total}", make_mini_bar(shell_pct))
    table.add_row("Conversation Archives", f"{db_archive} / {disp_archive_total}", make_mini_bar(archive_pct))
    
    table.add_section()
    table.add_row(
        "[bold white]CORE KERNEL AGGREGATE[/]", 
        f"[bold white]{total_embedded} / {total_potential}[/]]", 
        make_mini_bar(global_pct, width=30)
    )
    
    console.print("\n")
    console.print(table)
    
    bar_width = 60
    filled = int(global_pct / 100 * bar_width)
    bar = "█" * filled + "░" * (bar_width - filled)
    
    if global_pct > 99.9: color = "bold #ff00ff"
    elif global_pct > 70: color = "bold #5f00ff"
    elif global_pct > 40: color = "bold #00ffff"
    elif global_pct > 20: color = "bold #00ff00"
    else: color = "bold #ff0000"
    
    console.print(f"\n[{color}]TOTAL NEURAL SATURATION:[/] [{color}]{bar}[/] {global_pct:.2f}%\n")

if __name__ == "__main__":
    show_ingestion_stats()
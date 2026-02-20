import re
import bisect
import collections
import datetime
import time
import threading
import os
import sys
import requests

try:
    import psutil
except ImportError:
    psutil = None

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich import box

# --- Global UI Components ---
console = Console(highlight=False)
DURATION_SAMPLES = collections.deque(maxlen=10)
# Rolling history for calculating health windows (Max 100 to cover R100)
ROLLING_HISTORY = collections.deque(maxlen=100) 
UPDATE_LOCK = threading.Lock()
VERBOSITY = "min"
START_TIME = time.time()

# Streak Tracking Globals
CURRENT_STREAK_TYPE = None # True = Success, False = Fail
CURRENT_STREAK_COUNT = 0

# Mapping of success rates to status icons
STATUS_MARKERS = [
 (0.0,"🟥"),(10.0,"🔴"),(20.0,"♥️ "),(25.0,"🟧"),(35.0,"🟠"),
 (45.0,"🟨"),(50.0,"🟡"),(60.0,"🟩"),(70.0,"🟢"),(75.0,"🟦"),
 (85.0,"🔵"),(95.0,"🟣"),(100.0,"🟣")
]

def get_status_icon(rate):
    """Returns the appropriate emoji icon based on a percentage rate."""
    for limit, icon in reversed(STATUS_MARKERS):
        if rate >= limit:
            return icon
    return STATUS_MARKERS[0][1]

def get_success_color(percentage):
    """Returns a hex color string representing a gradient from red to green."""
    if percentage < 25:
        r, g, b = 255, int(165 * (percentage / 25)), 0
    elif percentage < 50:
        r, g, b = 255, int(165 + (90 * ((percentage - 25) / 25))), 0
    elif percentage < 75:
        r, g, b = int(255 * ((75 - percentage) / 25)), 255, 0
    else:
        r, g, b = 0, int(255 - (155 * ((percentage - 75) / 25))), 0
    return f"#{r:02x}{g:02x}{b:02x}"

def get_eta_color(current_idx, total_sites):
    """Complex gradient: 0-5% (Blue->Purple->Red), 5-100% (Red->Orange->Yellow->Green->Dark Green)."""
    if total_sites <= 0: return "#0000ff"
    progress = current_idx / total_sites
    
    if progress <= 0.05:
        p = progress / 0.05
        if p < 0.5: 
            sp = p / 0.5
            r, g, b = int(128 * sp), 0, int(255 - 127 * sp)
        else: 
            sp = (p - 0.5) / 0.5
            r, g, b = int(128 + 127 * sp), 0, int(128 - 128 * sp)
    else:
        p = (progress - 0.05) / 0.95
        if p < 0.25:
            sp = p / 0.25
            r, g, b = 255, int(165 * sp), 0
        elif p < 0.50:
            sp = (p - 0.25) / 0.25
            r, g, b = 255, int(165 + 90 * sp), 0
        elif p < 0.75:
            sp = (p - 0.50) / 0.25
            r, g, b = int(255 * (1 - sp)), 255, 0
        else:
            sp = (p - 0.75) / 0.25
            r, g, b = 0, int(255 - 155 * sp), 0
            
    return f"#{r:02x}{g:02x}{b:02x}"

def calculate_rolling_metric(history, window_size):
    """Calculates success % for the last N items in history."""
    if not history: return 0
    window = list(history)[-window_size:]
    if not window: return 0
    return int((sum(window) / len(window)) * 100)

def format_metric(value):
    """Formats percentage for display: '100' -> 'AA', <10 with leading zero."""
    if value == 100: return "[bright_green]AA[/]"
    color = get_success_color(value)
    return f"[{color}]{value:02d}[/]"

def update_dashboard(data):
    """Renders a single-line status update to the console."""
    global CURRENT_STREAK_TYPE, CURRENT_STREAK_COUNT
    
    index = data['index']
    successes = data['successes']
    site_url = data['site_url'].replace('https://', '').replace('www.', '')
    status_msg = data['status_message']
    total_sites = data.get('N', 0)
    site_new_bonuses = int(data.get("site_new_bonuses", 0))
    total_new_bonuses = int(data.get("total_new_bonuses", 0))

    elapsed_item = data.get('elapsed', 0)
    DURATION_SAMPLES.append(elapsed_item)
    avg_duration = sum(DURATION_SAMPLES) / len(DURATION_SAMPLES) if DURATION_SAMPLES else 0
    
    # Estimate time remaining
    remaining_sites = total_sites - index
    worker_count = int(data.get('nw', 1))
    est_remaining_sec = (remaining_sites * avg_duration) / (worker_count if worker_count > 0 else 1)
    minutes = int(est_remaining_sec // 60)
    seconds = est_remaining_sec % 60
    time_str = f"{minutes}m{seconds:06.3f}s"

    # --- Streak & History Logic ---
    is_success = 1 if status_msg.startswith("✅") else 0
    ROLLING_HISTORY.append(is_success)

    if CURRENT_STREAK_TYPE is None:
        CURRENT_STREAK_TYPE = bool(is_success)
        CURRENT_STREAK_COUNT = 1
    elif CURRENT_STREAK_TYPE == bool(is_success):
        CURRENT_STREAK_COUNT += 1
    else:
        CURRENT_STREAK_TYPE = bool(is_success)
        CURRENT_STREAK_COUNT = 1

    streak_icon = "✅" if CURRENT_STREAK_TYPE else "❌"
    streak_color = "bright_green" if CURRENT_STREAK_TYPE else "red"
    streak_display = f"[{streak_color}]{streak_icon}{CURRENT_STREAK_COUNT:02d}[/]"

    # Calculate Rolling Metrics (Reversed order: R100, R50, R20, R10, R5)
    rm = [calculate_rolling_metric(ROLLING_HISTORY, s) for s in [100, 50, 20, 10, 5]]
    
    yield_val = (total_new_bonuses / index * 100) if index > 0 else 0.0
    cumulative_rate = (successes / index * 100) if index > 0 else 0
    cumulative_color = get_success_color(cumulative_rate)
    eta_color = get_eta_color(index, total_sites)
    
    # Text Status Formatting
    if status_msg.startswith("✅"):
        text, icon, style = "DONE", "✅", "bright_green"
    elif "404" in status_msg:
        text, icon, style = "E404", "👻", "grey58"
    elif "403" in status_msg:
        text, icon, style = "E403", "🚫", "red"
    elif "301" in status_msg:
        text, icon, style = "E301", "↪️ ", "cyan"
    elif "101" in status_msg:
        text, icon, style = "E101", "📡", "yellow"
    elif "503" in status_msg:
        text, icon, style = "E503", "☁️ ", "gold1"
    elif "502" in status_msg:
        text, icon, style = "E502", "⛈️ ", "gold1"
    elif "500" in status_msg:
        text, icon, style = "E500", "💣", "red"
    elif "Timeout" in status_msg or "408" in status_msg:
        text, icon, style = "TIME", "🐌", "orange1"
    else:
        error_match = re.search(r"E(\d+)", status_msg)
        text, icon, style = (f"E{error_match.group(1)}", "💻", "red") if error_match else ("FAIL", "⛔", "red")

    mem_icon = ""
    if psutil:
        try:
            mem_p = psutil.virtual_memory().percent
            if mem_p > 80: mem_icon = f" [red]💾{int(mem_p)}%[/]"
        except: pass

    site_color = "[bright_green]" if site_new_bonuses > 0 else ""
    site_end = "[/]" if site_new_bonuses > 0 else ""

    # --- Constructed Line ---
    # Layout: [Index][Status Icon + Text][Streak][RMA History][Cumulative %][Yield %][Diamond Count][Timer][URL]
    line = (
        f"{site_color}{index:03d}{site_end}"
        f"[{style}]{icon}{text}[/]"
        f"{streak_display}"
        f"{format_metric(rm[0])}{format_metric(rm[1])}{format_metric(rm[2])}{format_metric(rm[3])}{format_metric(rm[4])}"
        f"[{cumulative_color}]{int(cumulative_rate):03d}%[/]"
        f"[gold1]{yield_val:05.1f}%[/]"
        f"{site_color}💎{site_new_bonuses:01d}|{total_new_bonuses:02d}{site_end}"
        f"⏱️ [{eta_color}]{time_str}[/]"
        f"{mem_icon} 🌐[bright_white]{site_url}[/]"
    )

    with UPDATE_LOCK:
        console.print(line)

def print_initialization_dashboard(config_data):
    """Prints a rich initialization dashboard."""
    # Placeholder for actual implementation in clide/serve/dashboard.py
    pass

def print_finalization_report(stats):
    """Prints a high-fidelity finalization report."""
    table = Table(title="[bold green]SESSION PERFORMANCE[/]", box=box.DOUBLE_EDGE)
    table.add_column("METRIC", style="cyan")
    table.add_column("VALUE", justify="right")
    
    table.add_row("TOTAL SITES", str(stats.get('total', 0)))
    table.add_row("SUCCESSES", f"[green]{stats.get('successes', 0)}[/]")
    table.add_row("FAILURES", f"[red]{stats.get('failures', 0)}[/]")
    table.add_row("YIELD RATE", f"[gold1]{stats.get('yield', 0):.2f}%[/]")
    
    console.print("\n")
    console.print(Panel(table, border_style="bright_white", padding=(1, 2)))
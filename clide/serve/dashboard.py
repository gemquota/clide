import os
import sys
import json
import time
import psutil
import plotext as plt
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.align import Align
from art import tprint
from datetime import datetime

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from clide.brain.memory import get_registry_stats
from clide.kernel import storage as db_manager
from clide.watch.stream import get_monitor_status
from scripts.calculate_error_probs import get_error_probabilities

console = Console()

class CyberDashboard:
    def __init__(self):
        self.start_time = time.time()
        self.layout = Layout()
        self.frame_count = 0
        self.setup_layout()

    def make_header(self) -> Panel:
        uptime = str(datetime.now() - datetime.fromtimestamp(self.start_time)).split('.')[0]
        # Multi-shade header
        header_text = Text.from_markup(f"[bold red]CLIDE[/] [white]v1.0.0[/] [dim]•[/] [bold cyan]NEURAL-KERNEL COMMAND[/] [dim]•[/] [bold green]LINK: SECURE[/]")
        
        # Add a "pulse" effect
        pulse_colors = ["red", "bright_red", "magenta", "bright_magenta"]
        pulse_color = pulse_colors[(self.frame_count // 2) % len(pulse_colors)]
        pulse = f"[{pulse_color}]◈[/]"
        
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="center", ratio=2)
        grid.add_column(justify="right", ratio=1)
        grid.add_row(
            Text.from_markup(f"[cyan]UPTIME:[/][white]{uptime}[/]"),
            header_text,
            Text.from_markup(f"{pulse} [bold green]ONLINE[/]")
        )
        return Panel(grid, style="red", border_style="red")

    def make_resource_panel(self) -> Panel:
        try:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
        except:
            cpu, mem = 0, 0
        
        monitor = get_monitor_status()
        mon_color = "green" if "Active" in monitor else "red"
        
        table = Table.grid(expand=True)
        table.add_column()
        
        def bar(val, color):
            filled = int(val / 10)
            return f"[{color}]{'█' * filled}[dim]{'░' * (10 - filled)}[/] {val}%"

        table.add_row("[cyan]CPU CORE[/]")
        table.add_row(bar(cpu, "green" if cpu < 70 else "red"))
        table.add_row("")
        table.add_row("[cyan]MEM LOAD[/]")
        table.add_row(bar(mem, "cyan" if mem < 70 else "magenta"))
        table.add_row("")
        table.add_row("[cyan]WATCHDOG[/]")
        table.add_row(f"[{mon_color}]{monitor}[/]")
        
        return Panel(table, title="[bold cyan]SYSTEM TELEMETRY[/]", border_style="cyan")

    def make_neural_stats(self) -> Panel:
        stats = get_registry_stats()
        table = Table.grid(expand=True)
        table.add_column()
        
        if stats and stats.get('status') != 'error':
            table.add_row("[dim white]SEMANTIC ANCHORS[/]")
            table.add_row(f"[bold magenta]{stats['total_assets']} VECTORS[/]")
            table.add_row("")
            table.add_row("[dim white]MEMORY VOLUME[/]")
            table.add_row(f"[bold magenta]{stats['file_size_kb']:.1f} KB[/]")
        else:
            table.add_row("MEM-NET: [red]OFFLINE[/]")
            
        return Panel(table, title="[bold magenta]NEURAL METRICS[/]", border_style="magenta")

    def make_ingestion_panel(self) -> Panel:
        from scripts import ingestion_stats
        db_shell, db_telemetry, db_archive = ingestion_stats.get_db_counts()
        
        # Simplified progress
        table = Table.grid(expand=True)
        table.add_column(style="cyan", width=18)
        table.add_column(justify="right")
        
        def mini_bar(pct):
            filled = int(pct / 20)
            return f"[{'green' if pct > 50 else 'yellow'}]{'■' * filled}[dim]{'□' * (5 - filled)}[/]"

        table.add_row("SHELL HISTORY", f"{db_shell} {mini_bar(min(100, db_shell/10))}")
        table.add_row("ENRICHED LOGS", f"{db_telemetry} {mini_bar(min(100, db_telemetry/5))}")
        table.add_row("CONV ARCHIVES", f"{db_archive} {mini_bar(min(100, db_archive/2))}")
        
        return Panel(table, title="[bold white]INGESTION PROGRESS[/]", border_style="white")

    def make_log_panel(self) -> Panel:
        recent = db_manager.get_knowledge(limit=12)
        table = Table(expand=True, box=None, padding=(0, 1))
        table.add_column("CLOCK", style="dim cyan", width=10)
        table.add_column("DOMAIN", style="bold green", width=12)
        table.add_column("INTENT", overflow="ellipsis")
        
        for r in recent:
            ts = r['timestamp'][11:19]
            cat = r['category']
            
            color = "white"
            if cat == "FACT": color = "green"
            elif cat == "TODO": color = "yellow"
            elif cat == "NEW_COMMAND": color = "blue"
            elif cat == "TOOL_INTENT": color = "magenta"
            elif cat == "SHELL_HISTORY": color = "dim white"
            
            content = (r['content'] or "").replace('\n', ' ')[:60]
            table.add_row(ts, f"[{color}]{cat}[/]", content)
            
        return Panel(table, title="[bold green]INGESTION STREAM[/]", border_style="green")

    def make_plot_panel(self) -> Panel:
        stats = get_registry_stats()
        if not stats or not stats.get('distribution'):
            return Panel(Align.center(Text("EMPTY DATASET")), title="DISTRIBUTION", border_style="red")
        
        plt.clf()
        types = list(stats['distribution'].keys())
        counts = list(stats['distribution'].values())
        
        # Plotext bar chart
        plt.bar(types, counts, color="red")
        plt.canvas_color("black")
        plt.axes_color("black")
        plt.ticks_color("white")
        plt.plotsize(None, 12) # Auto width
        
        return Panel(plt.build(), title="[bold red]SEMANTIC CLUSTERS[/]", border_style="red")

    def setup_layout(self):
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=1),
        )
        self.layout["main"].split_row(
            Layout(name="side", size=38), # Increased slightly
            Layout(name="body"),
        )
        self.layout["side"].split(
            Layout(name="resources", size=6),
            Layout(name="stats", size=5),
            Layout(name="ingestion", size=6),
            Layout(name="legends", size=10),
            Layout(name="strategy"),
        )
        self.layout["legends"].split_row(
            Layout(name="health_legend"),
            Layout(name="error_legend"),
        )
        self.layout["body"].split(
            Layout(name="plot", ratio=1),
            Layout(name="stream", ratio=1),
        )

    def update(self):
        self.frame_count += 1
        self.layout["header"].update(self.make_header())
        self.layout["resources"].update(self.make_resource_panel())
        self.layout["stats"].update(self.make_neural_stats())
        self.layout["ingestion"].update(self.make_ingestion_panel())
        self.layout["stream"].update(self.make_log_panel())
        self.layout["plot"].update(self.make_plot_panel())
        
        # Health Legend
        health_text = Text.assemble(
            ("🟥🔴♥️ Bad\n", "red"), ("🟧🟠 Okay\n", "orange1"), 
            ("🟨🟡 Good\n", "yellow"), ("🟩🟢 Great", "green")
        )
        self.layout["health_legend"].update(Panel(health_text, title="[bold white]HEALTH[/]", border_style="white"))
        
        # Error Legend with Probabilities
        probs = get_error_probabilities()
        sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:6]
        
        error_text = Text()
        if not sorted_probs:
            error_text.append("NO ERRORS", style="dim green")
        else:
            for code, pct in sorted_probs:
                # Map codes to icons
                icon = "💻"
                if "404" in code: icon = "👻"
                elif "500" in code: icon = "💣"
                elif "403" in code: icon = "🚫"
                elif "503" in code: icon = "☁️"
                
                error_text.append(f"{icon}{code} ", style="red")
                error_text.append(f"{pct:04.1f}%\n", style="dim white")
                
        self.layout["error_legend"].update(Panel(error_text, title="[bold red]ERR PROB[/]", border_style="red"))
        
        # Strategy / TODO
        todos = db_manager.get_knowledge(category="TODO", limit=8)
        todo_text = Text()
        for t in todos:
            todo_text.append(" ◈ ", style="dim yellow")
            todo_text.append(f"{t['content'][:30]}", style="yellow")
            todo_text.append("\n")
        self.layout["strategy"].update(Panel(todo_text, title="[bold yellow]ACTIVE STRATEGY[/]", border_style="yellow"))
        
        footer = Text.from_markup(f"[dim]SYSTEM TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | NODE: TERMUX | USER: ROOT | PRESS CTRL+C TO TERMINAL LINK[/]")
        self.layout["footer"].update(Align.center(footer))

    def run(self):
        console.clear()
        print("\033[38;5;196m", end="")
        tprint("CLIDE", font="block")
        print("\033[0m", end="")
        time.sleep(0.5)
        
        with Live(self.layout, refresh_per_second=4, screen=True) as live:
            try:
                while True:
                    self.update()
                    time.sleep(0.25)
            except KeyboardInterrupt:
                pass

def run_dashboard():
    app = CyberDashboard()
    app.run()

if __name__ == "__main__":
    run_dashboard()
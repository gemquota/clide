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
        pulse_color = "red" if (self.frame_count // 5) % 2 == 0 else "dim red"
        pulse = f"[{pulse_color}]●[/]"
        
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
        
        table = Table.grid(expand=True)
        table.add_column(width=12)
        table.add_column()
        
        def bar(val, color):
            filled = int(val / 10)
            return f"[{color}]{'█' * filled}[dim]{'░' * (10 - filled)}[/] {val}%"

        table.add_row("[cyan]CPU CORE[/]", bar(cpu, "green" if cpu < 70 else "red"))
        table.add_row("[cyan]MEM LOAD[/]", bar(mem, "cyan" if mem < 70 else "magenta"))
        
        return Panel(table, title="[bold cyan]SYSTEM TELEMETRY[/]", border_style="cyan")

    def make_neural_stats(self) -> Panel:
        stats = get_registry_stats()
        table = Table.grid(expand=True)
        table.add_column(style="dim white", width=15)
        table.add_column(style="bold magenta", justify="right")
        
        if stats and stats.get('status') != 'error':
            table.add_row("SEMANTIC ANCHORS", f"{stats['total_assets']} [dim]VECTORS[/]")
            table.add_row("MEMORY VOLUME", f"{stats['file_size_kb']:.1f} [dim]KB[/]")
            table.add_row("SPACE DIMENSION", f"{stats['dimensions']}D [dim]RESO[/]")
        else:
            table.add_row("MEM-NET", "OFFLINE")
            
        return Panel(table, title="[bold magenta]NEURAL METRICS[/]", border_style="magenta")

    def make_log_panel(self) -> Panel:
        recent = db_manager.get_knowledge(limit=10)
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
            
            content = r['content'].replace('\n', ' ')[:60]
            table.add_row(ts, f"[{color}]{cat}[/]", content)
            
        return Panel(table, title="[bold green]INGESTION STREAM[/]", border_style="green")

    def make_plot_panel(self) -> Panel:
        stats = get_registry_stats()
        if not stats or not stats.get('distribution'):
            return Panel(Align.center(Text("EMPTY DATASET")), title="DISTRIBUTION", border_style="red")
        
        plt.clf()
        types = list(stats['distribution'].keys())
        counts = list(stats['distribution'].values())
        
        plt.bar(types, counts, color="red")
        plt.canvas_color("black")
        plt.axes_color("black")
        plt.ticks_color("white")
        plt.plotsize(44, 14)
        
        return Panel(plt.build(), title="[bold red]SEMANTIC CLUSTERS[/]", border_style="red")

    def setup_layout(self):
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=1),
        )
        self.layout["main"].split_row(
            Layout(name="side", size=35),
            Layout(name="body"),
        )
        self.layout["side"].split(
            Layout(name="resources", size=6),
            Layout(name="stats", size=6),
            Layout(name="strategy"),
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
        self.layout["stream"].update(self.make_log_panel())
        self.layout["plot"].update(self.make_plot_panel())
        
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
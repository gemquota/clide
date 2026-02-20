from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from rich.bar import Bar

console = Console()

def demo_hud_panel():
    console.print("\n[bold cyan]STYLE: HUD PANEL (In-Border Text)[/]")
    
    # Using title and subtitle for in-border effect
    p = Panel(
        Align.center(
            Text("SYSTEM OPERATIONAL\nKERNEL: ACTIVE\nUPTIME: 99.9%", justify="center", style="green"),
            vertical="middle"
        ),
        title="[bold cyan] ⦗ SYSTEM DIAGNOSTICS ⦘ [/]",
        subtitle="[bold cyan] ⦗ v1.0.4 ⦘ [/]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(p)

def demo_experimental_graphics():
    console.print("\n[bold magenta]STYLE: EXPERIMENTAL TUI GRAPHICS[/]")
    
    # 1. Sparkline / Bar Chart simulation
    table = Table(box=None, padding=0, collapse_padding=True)
    table.add_column("Metric", style="white")
    table.add_column("Visual", style="magenta")
    table.add_column("Value", style="green", justify="right")
    
    table.add_row("CPU Load", Bar(100, 0, 100, color="magenta"), "45%")
    table.add_row("Mem Usage", Bar(100, 0, 100, color="cyan"), "12%")
    table.add_row("Net I/O", Bar(100, 0, 100, color="green"), "88%")
    
    console.print(Panel(table, title="[bold magenta] TELEMETRY [/]", border_style="magenta", box=box.HEAVY_EDGE))

    # 2. Mini-Map (Grid)
    grid = Table.grid(expand=False, padding=(0,1))
    grid.add_column(justify="center")
    grid.add_column(justify="center")
    grid.add_column(justify="center")
    
    grid.add_row("[cyan]┌───┐[/]", "[dim]──[/]", "[magenta]⬢[/]")
    grid.add_row("[dim]│[/]", "", "[dim]│[/]")
    grid.add_row("[green]●[/]", "[dim]──[/]", "[yellow]▲[/]")
    
    console.print(Panel(grid, title="[bold white] TOPOLOGY [/]", border_style="white", width=20))

if __name__ == "__main__":
    demo_hud_panel()
    demo_experimental_graphics()

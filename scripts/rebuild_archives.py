import os
import sys
import glob
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from clide.probe import manual

console = Console()

def run_archive_rebuild():
    console.print("\n[bold cyan]╶─╼ ⟨ ◈ ARCHIVE RECONCILIATION ◈ ⟩ ╾─╴[/]")
    console.print("[dim]Scanning ingestion_logs/ for un-indexed historical data...[/]\n")

    ingestion_dir = os.path.join(BASE_DIR, "ingestion_logs")
    if not os.path.exists(ingestion_dir):
        console.print("[red][!] Directory 'ingestion_logs/' not found.[/]")
        return

    # Find all .md files recursively
    md_files = glob.glob(os.path.join(ingestion_dir, "**/*.md"), recursive=True)
    
    if not md_files:
        console.print("[yellow][!] No Markdown archives found.[/]")
        return

    console.print(f"[bold cyan]Detected {len(md_files)} archive files.[/]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Rebuilding Archives...", total=len(md_files))
        
        for f in md_files:
            rel_path = os.path.relpath(f, BASE_DIR)
            progress.update(task, description=f"[cyan]Ingesting: {rel_path[:30]}...")
            try:
                # Use the manual extractor to process the file
                manual.extract_from_file(f)
            except Exception as e:
                console.print(f"[red][!] Failed to ingest {rel_path}: {e}[/]")
            
            progress.advance(task)

    console.print(f"\n[bold green]Success:[/ ] Historical archive synchronization complete.")

if __name__ == "__main__":
    run_archive_rebuild()

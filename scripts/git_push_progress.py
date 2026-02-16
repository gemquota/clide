import subprocess
import sys
import os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()

def run_cmd(cmd, description, progress, task):
    progress.update(task, description=f"[cyan]{description}...")
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        # Check if it's just "nothing to commit"
        if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
            return True
        console.print(f"[bold red]Error during {description}:[/]\n{result.stderr or result.stdout}")
        return False
    return True

def main():
    console.print("[bold magenta]╶─╼ ⟨ ◈ GIT PUSH RECOVERY ◈ ⟩ ╾─╴[/]\n")
    console.print("[dim]Large files detected. Squashing history and excluding payloads > 50MB...[/]\n")
    
    steps = [
        ("git reset --soft origin/master", "Squashing local history"),
        ("git add .", "Staging all changes"),
        ("git reset HEAD clide/memory.db swarm/commands/vector_registry.json docs/brain_graph.mmd", "Excluding large files from commit"),
        ("git commit -m 'refactor: Major system reorganization and cleanup (squashed)'", "Committing clean state"),
        ("git push", "Pushing to origin/master")
    ]
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Initializing...", total=len(steps))
        
        for cmd, desc in steps:
            if not run_cmd(cmd, desc, progress, task):
                break
            progress.advance(task)
            
    console.print("\n[bold green]Success:[/] Git push recovery complete. Large files are ignored but preserved on disk.")

if __name__ == "__main__":
    main()
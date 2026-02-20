import json
import os
import subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Confirm
from clide.kernel import storage
from clide.brain import memory, model
from clide.watch import stream

console = Console()

class ClideStrategist:
    def __init__(self):
        self.suggested_commands = []

    def assess_system_state(self):
        """Gathers telemetry across all domains to build a comprehensive context."""
        stats = memory.get_registry_stats()
        monitor = stream.get_monitor_status()
        recent_logs = storage.get_knowledge(limit=10)
        todos = storage.get_knowledge(category="TODO", limit=5)
        proposals = storage.get_knowledge(category="PROPOSAL")
        
        # Build context string
        context = {
            "neural_metrics": stats,
            "monitor_status": monitor,
            "pending_proposals": len(proposals),
            "active_todos": [t['content'] for t in todos],
            "recent_activity": [f"[{l['category']}] {l['content'][:50]}" for l in recent_logs]
        }
        return context

    def generate_strategy(self):
        """Uses LLM to determine the most logical next steps for system optimization."""
        state = self.assess_system_state()
        
        prompt = f"""
Analyze the current state of the CLIDE Knowledge Operating System and suggest 3-5 optimal CLI commands to run.
Focus on: 
1. Resolving technical debt (cleaning/tagging).
2. Processing pending ingestion (approving/merging).
3. Ensuring system health (backups/audits).
4. Advancing active todos.

CURRENT STATE:
{json.dumps(state, indent=2)}

Return ONLY a JSON list of objects with the structure:
[
  {{"command": "./cli ...", "reason": "why this helps", "impact": "High/Medium/Low"}}
]
STRICT_JSON_ENFORCEMENT. No markdown. No preamble.
"""
        
        try:
            res = model.call_llm(prompt)
            # Robust JSON extraction
            import re
            json_match = re.search(r'\[.*\]', res, re.DOTALL)
            if json_match:
                self.suggested_commands = json.loads(json_match.group(0))
            else:
                self.suggested_commands = json.loads(res)
        except Exception as e:
            console.print(f"[red][!] Strategy generation failed: {e}[/]")
            self.suggested_commands = []

    def display_strategy(self):
        if not self.suggested_commands:
            console.print("[yellow]No strategic actions required at this time.[/]")
            return

        table = Table(title="[bold cyan]SYSTEM STRATEGY: OPTIMAL COMMAND SEQUENCE[/]", border_style="cyan", box=None)
        table.add_column("Seq", style="dim", width=4)
        table.add_column("Command", style="bold green", width=30)
        table.add_column("Strategic Intent", style="white")
        table.add_column("Impact", style="bold magenta", justify="center")

        for i, cmd in enumerate(self.suggested_commands):
            table.add_row(str(i+1), cmd['command'], cmd['reason'], cmd['impact'])
        
        console.print(table)

    def execute_strategy(self):
        if not self.suggested_commands: return

        if Confirm.ask("\n[bold yellow]Authorize execution of the above command sequence?[/]"):
            console.print("\n[bold green][*] Initiating sequence...[/]")
            for cmd in self.suggested_commands:
                console.print(f"[cyan]Executing:[/] {cmd['command']}...")
                try:
                    # Run shell command
                    result = subprocess.run(cmd['command'], shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        console.print(f"  [green][v] Success[/]")
                    else:
                        console.print(f"  [red][!] Failed: {result.stderr.strip()}[/]")
                except Exception as e:
                    console.print(f"  [red][!] Error: {e}[/]")
            console.print("\n[bold green][v] Strategy execution complete.[/]")
        else:
            console.print("[dim]Sequence aborted by user.[/]")

def run_strategist():
    strat = ClideStrategist()
    console.print("[bold cyan][Strategist][/] Assessing system topology and entropy...")
    strat.generate_strategy()
    strat.display_strategy()
    strat.execute_strategy()

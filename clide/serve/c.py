import os
import sys
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.columns import Columns
from rich.align import Align
from rich.prompt import Prompt
from art import tprint

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from clide.serve.menu_data import MENU_STRUCTURE

console = Console()

from rich.markdown import Markdown

# Dynamic path resolution for docs
DOCS_ROOT = os.path.join(BASE_DIR, "docs", "cli")

class ClideNavigator:
    def __init__(self):
        self.current_sector = None
        self.current_domain = None
        self.history = []

    def clear(self):
        console.clear()

    def get_doc_content(self, domain, command=None):
        """Attempts to resolve and read markdown documentation."""
        paths = []
        if command:
            paths.append(os.path.join(DOCS_ROOT, domain, f"{command}.md"))
            paths.append(os.path.join(DOCS_ROOT, f"{domain}_{command}.md"))
        else:
            paths.append(os.path.join(DOCS_ROOT, domain, "index.md"))
            paths.append(os.path.join(DOCS_ROOT, f"{domain}.md"))
            
        for p in paths:
            if os.path.exists(p):
                with open(p, 'r') as f:
                    return f.read()
        return None

    def print_header(self):
        print("\033[38;5;196m", end="")
        tprint("CLIDE", font="small")
        print("\033[0m", end="")
        header = Text.from_markup("[bold red]CLIDE[/] [bold white]v1.0.0[/] [dim]•[/] [bold cyan]COMMAND NAVIGATOR[/] [dim]•[/] [bold green]LINK: SECURE[/]")
        console.print(Align.center(header))
        console.print(Align.center(Text("-" * 60, style="dim")))

    def show_sectors(self):
        self.clear()
        self.print_header()
        
        table = Table(box=None, expand=True)
        table.add_column("ID", style="bold magenta", width=4)
        table.add_column("SECTOR", style="bold white")
        table.add_column("DOMAINS", style="dim cyan")
        
        for i, (sector, domains) in enumerate(MENU_STRUCTURE.items(), 1):
            domain_list = ", ".join(domains.keys())
            table.add_row(f"{i:02d}", sector, domain_list)
            
        console.print(Panel(table, title="[bold white]SELECT SECTOR[/]", border_style="red", padding=(1, 2)))
        console.print("\n[dim]Enter Sector ID, Name, or '/' to search (or 'q' to exit):[/]")
        
        choice = Prompt.ask(">").strip()
        if choice.lower() == 'q':
            sys.exit(0)
        
        if choice == '/':
            self.search_commands()
            return
            
        # Match by ID or Name
        matched_sector = None
        for i, sector in enumerate(MENU_STRUCTURE.keys(), 1):
            if choice == str(i) or choice == str(i).zfill(2) or choice.upper() == sector:
                matched_sector = sector
                break
                
        if matched_sector:
            self.current_sector = matched_sector
            self.show_domains()
        else:
            console.print("[red][!] Invalid Sector.[/]")
            time.sleep(1)
            self.show_sectors()

    def search_commands(self):
        self.clear()
        self.print_header()
        console.print("[bold cyan]SEARCH COMMANDS[/]\n")
        query = Prompt.ask("Query").strip().lower()
        if not query:
            self.show_sectors()
            return
            
        results = []
        for sector, domains in MENU_STRUCTURE.items():
            for domain, content in domains.items():
                if isinstance(content, dict):
                    for cmd, desc in content.items():
                        if query in cmd.lower() or query in desc.lower():
                            results.append((sector, domain, cmd, desc))
                else:
                    if query in domain.lower() or query in content.lower():
                        results.append((sector, domain, None, content))
        
        if not results:
            console.print(f"[yellow][!] No matches found for '{query}'.[/]")
            time.sleep(1.5)
            self.show_sectors()
            return
            
        table = Table(box=None, expand=True)
        table.add_column("ID", style="bold yellow", width=4)
        table.add_column("PATH", style="bold cyan")
        table.add_column("ANNOTATION", style="dim")
        
        for i, (sec, dom, cmd, desc) in enumerate(results, 1):
            path = f"{sec} > {dom}"
            if cmd: path += f" > {cmd}"
            table.add_row(f"{i:02d}", path, desc)
            
        console.print(Panel(table, title=f"[bold white]SEARCH RESULTS: {query}[/]", border_style="yellow", padding=(1, 2)))
        console.print("\n[dim]Enter ID to view detail (or 'b' to go back):[/]")
        
        choice = Prompt.ask(">").strip().upper()
        if choice == 'B':
            self.current_sector = None
            self.show_sectors()
            return
            
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(results):
                sec, dom, cmd, desc = results[idx]
                self.current_sector = sec
                self.current_domain = dom
                self.show_detail(cmd or dom, desc)
            else:
                self.search_commands()
        except:
            self.search_commands()

    def show_domains(self):
        self.clear()
        self.print_header()
        
        console.print(f"[bold magenta]SECTOR:[/] [bold white]{self.current_sector}[/]\n")
        
        table = Table(box=None, expand=True)
        table.add_column("ID", style="bold cyan", width=4)
        table.add_column("DOMAIN", style="bold white")
        table.add_column("DESCRIPTION", style="dim")
        
        domains = MENU_STRUCTURE[self.current_sector]
        for i, (domain, content) in enumerate(domains.items(), 1):
            desc = "Sub-commands available" if isinstance(content, dict) else content
            table.add_row(f"{i:02d}", domain, desc)
            
        console.print(Panel(table, title=f"[bold white]{self.current_sector} DOMAINS[/]", border_style="cyan"))
        console.print("\n[dim]Enter Domain ID or Name (or 'b' to go back):[/]")
        
        choice = Prompt.ask(">").strip().upper()
        if choice == 'B':
            self.current_sector = None
            self.show_sectors()
            return
            
        matched_domain = None
        for i, domain in enumerate(domains.keys(), 1):
            if choice == str(i) or choice == str(i).zfill(2) or choice == domain.upper():
                matched_domain = domain
                break
                
        if matched_domain:
            self.current_domain = matched_domain
            content = domains[matched_domain]
            if isinstance(content, dict):
                self.show_commands(content)
            else:
                self.show_detail(matched_domain, content)
        else:
            console.print("[red][!] Invalid Domain.[/]")
            time.sleep(1)
            self.show_domains()

    def show_commands(self, commands):
        self.clear()
        self.print_header()
        
        console.print(f"[bold magenta]SECTOR:[/] [bold white]{self.current_sector}[/] [dim]>[/] [bold cyan]DOMAIN:[/] [bold white]{self.current_domain}[/]\n")
        
        table = Table(box=None, expand=True)
        table.add_column("ID", style="bold green", width=4)
        table.add_column("COMMAND", style="bold white")
        table.add_column("ANNOTATION", style="dim")
        
        for i, (cmd, desc) in enumerate(commands.items(), 1):
            table.add_row(f"{i:02d}", cmd, desc)
            
        console.print(Panel(table, title=f"[bold white]{self.current_domain} COMMANDS[/]", border_style="green"))
        console.print("\n[dim]Enter Command ID or Name (or 'b' to go back):[/]")
        
        choice = Prompt.ask(">").strip().upper()
        if choice == 'B':
            self.current_domain = None
            self.show_domains()
            return
            
        matched_cmd = None
        for i, cmd in enumerate(commands.keys(), 1):
            if choice == str(i) or choice == str(i).zfill(2) or choice == cmd.upper():
                matched_cmd = cmd
                break
                
        if matched_cmd:
            self.show_detail(matched_cmd, commands[matched_cmd])
        else:
            console.print("[red][!] Invalid Command.[/]")
            time.sleep(1)
            self.show_commands(commands)

    def show_detail(self, name, description):
        self.clear()
        self.print_header()
        
        # Compile usage example
        usage = f"./cli {self.current_domain} {name}" if self.current_domain and self.current_domain != name else f"./cli {name}"
        
        # Documentation Look-up
        doc_content = self.get_doc_content(self.current_domain or name, name if self.current_domain and self.current_domain != name else None)
        
        # Build UI
        title = f"[bold white]ASSET: {name.upper()}[/]"
        
        detail_table = Table(box=None, padding=(0, 2))
        detail_table.add_column("Property", style="bold cyan", width=15)
        detail_table.add_column("Value", style="white")
        
        detail_table.add_row("SECTOR", self.current_sector)
        detail_table.add_row("DOMAIN", self.current_domain or "ROOT")
        detail_table.add_row("ANNOTATION", description)
        detail_table.add_row("COMMAND", f"[bold yellow]{usage}[/]")
        
        console.print(Panel(detail_table, title=title, border_style="cyan", padding=(1, 2)))
        
        if doc_content:
            console.print("\n[bold magenta]FULL DOCUMENTATION:[/]")
            console.print(Panel(Markdown(doc_content), border_style="dim", padding=(1, 2)))
        
        console.print("\n[dim]Options: (L)aunch, (B)ack, (Q)uit[/]")
        choice = Prompt.ask(">").strip().upper()
        if choice == 'Q':
            sys.exit(0)
        elif choice == 'L':
            console.print(f"[bold green][!] Executing: {usage}[/]")
            time.sleep(1)
            # Use os.system to allow interactive subprocesses to take over the terminal
            os.system(usage)
            Prompt.ask("\n[dim]Press ENTER to return to Navigator[/]")
            self.show_detail(name, description)
            return
        
        # Go back to where we were
        if self.current_domain and isinstance(MENU_STRUCTURE[self.current_sector][self.current_domain], dict):
            self.show_commands(MENU_STRUCTURE[self.current_sector][self.current_domain])
        else:
            self.show_domains()

    def run(self):
        try:
            self.show_sectors()
        except KeyboardInterrupt:
            console.print("\n[dim]Navigator terminated.[/]")

if __name__ == "__main__":
    nav = ClideNavigator()
    nav.run()

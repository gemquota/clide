import os
import sys
import re
from art import tprint

# Rich Imports
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.theme import Theme
from rich.style import Style
from rich.text import Text
from rich import box
from rich.rule import Rule
from rich.layout import Layout
from rich.table import Table
from rich.align import Align
from rich.padding import Padding
from rich.columns import Columns

# Dynamic path resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS_ROOT = os.path.join(BASE_DIR, "docs", "cli")

# --- VAPORWAVE / CYBERPUNK THEME ---
vapor_theme = Theme({
    "info": "cyan",
    "warning": "bold magenta",
    "danger": "bold red",
    "success": "bold green",
    "header": "bold bright_magenta",
    "section": "bold cyan",
    "title": "bold white",
    "code": "bold white on #d700d7", 
    "concept": "bold #af5fff", 
    "path": "italic #00ffff", 
    "command": "bold white on #d700d7", 
    "dim": "dim white",
    "border": "#5f00ff", 
    "timestamp": "dim cyan",
    "key": "bold #00afff", 
    "card.title": "bold black on #00afff",
    "card.key": "bold #00afff",
    "card.val": "white",
    "strong": "bold #00afff", 
    "emph": "italic #00ffff", 
})

console = Console(theme=vapor_theme, width=None)

def print_banner():
    """Minimalist Cyber-Noir Banner"""
    console.print()
    console.rule("[bold bright_magenta]CLIDE // KOS v1.0.0[/]", style="cyan")
    console.print()

def pre_process_content(text):
    """Injects Rich Markup into text for domain-specific highlighting before Markdown rendering."""
    text = re.sub(r"<([A-Z0-9\s_-]+)>", r"**\1**", text)
    text = re.sub(r"([\w./-]+\.(?:py|md|json|db|toml|sh))", r"_\1_", text)
    text = re.sub(r"(\./cli [\w\s{{}}|,-]+)", r" ` \1 ` ", text)
    text = re.sub(r"\b(WARNING|DANGER|CRITICAL|ERROR)\b", r"**«\1»**", text)
    text = re.sub(r"\b(SECURITY)\b", r"**«\1»**", text)
    text = re.sub(r"\b(SUCCESS|VALID|PASSED|HEALTHY)\b", r"**«\1»**", text)
    text = re.sub(r"\b(768D|SPA|LLM|MCP|RAG|SQLITE|JSON|UUID|API)\b", r"**\1**", text)
    return text

def parse_info_cards(text):
    """Extracts custom <card>...</card> blocks and renders them as rich Tables."""
    parts = re.split(r"(<card>.*?</card>)", text, flags=re.DOTALL)
    renderables = []
    for part in parts:
        if part.startswith("<card>") and part.endswith("</card>"):
            content = part.replace("<card>", "").replace("</card>", "").strip()
            lines = content.split("\n")
            title = "INFO CARD"
            data = {}
            for line in lines:
                if ":" in line:
                    k, v = line.split(":", 1)
                    if k.strip().lower() == "title": title = v.strip()
                    else: data[k.strip()] = v.strip()
            table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2), collapse_padding=True)
            table.add_column("Key", style="card.key", justify="right")
            table.add_column("Value", style="card.val", justify="left")
            for k, v in data.items(): table.add_row(k, v)
            renderables.append(Panel(table, title=f"[card.title] {title} [/]", border_style="key", box=box.ROUNDED, expand=False))
        else:
            if part.strip(): renderables.append(Markdown(pre_process_content(part)))
    return renderables

def render_content(text, title=None, border_style="section"):
    """Renders text as Markdown with parsed Info Cards."""
    renderables = parse_info_cards(text)
    content_group = Group(*renderables)
    if title:
        console.print(Panel(content_group, title=f"[header]{title}[/]", border_style=border_style, box=box.ROUNDED, expand=False, padding=(1, 1)))
    else:
        console.print(content_group)

def get_help_content(file_path):
    """Reads the entire content of a documentation file."""
    if not os.path.exists(file_path): return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except: return None

def show_unified_help(domain=None, command=None):
    """The unified portal for system intelligence, combining Atlas and Help."""
    print_banner()
    
    # 1. Handle Global Index (No args)
    if not domain:
        index_path = os.path.join(DOCS_ROOT, "index.md")
        content = get_help_content(index_path)
        if content: render_content(content)
        
        full_tree = get_atlas_tree()
        if full_tree:
            console.print()
            console.print(Panel(Text(full_tree, style="dim"), title="[header]GLOBAL COMMAND ATLAS[/]", border_style="dim", box=box.MINIMAL, expand=True))
        
        # Display Domain/Meta Panels
        console.print("\n[header]Active Domains[/]")
        domains = [d for d in os.listdir(DOCS_ROOT) if os.path.isdir(os.path.join(DOCS_ROOT, d))]
        domain_panels = [f"[concept]◈ {d.upper()}[/]" for d in sorted(domains)]
        console.print(Columns(domain_panels, equal=True, expand=True))
        return

    # 2. Handle Domain/Command with Contextual Atlas
    console.print(f"[header]PORTAL // {domain.upper()}{' // ' + command.upper() if command else ''}[/]")
    
    # Show local atlas branch for context
    tree = get_atlas_tree(domain)
    if tree:
        console.print(Panel(Text(tree, style="dim"), title="[section]Local Atlas[/]", border_style="dim", box=box.MINIMAL))
    
    # Resolve and show content
    file_path = resolve_doc_path(domain, command)
    content = get_help_content(file_path)
    
    if content:
        console.print()
        render_content(content, title=f"KNOWLEDGE BASE")
        console.print(Rule(style="border"))
    elif not tree:
        # Only show error if BOTH tree and content are missing
        console.print(f"[danger]⦗ERROR⦘[/danger] Intelligence for '[info]{domain}[/info]' not found in current SSoT.")

def show_help(domain=None, command=None):
    show_unified_help(domain, command)

def show_ref(domain=None, command=None):
    show_unified_help(domain, command)

def get_atlas_tree(domain=None):
    atlas_path = os.path.join(DOCS_ROOT, "atlas.md")
    if not os.path.exists(atlas_path): return None
    try:
        with open(atlas_path, 'r', encoding='utf-8') as f: lines = f.readlines()
        content = []
        capture = False
        
        if not domain:
            for line in lines:
                if line.strip().startswith("##"): continue
                content.append(line)
        else:
            for line in lines:
                if line.strip().startswith("##"): continue
                clean_line = line.strip()
                if (clean_line.startswith("├── " + domain) or clean_line.startswith("└── " + domain)):
                    capture = True
                    content.append(line)
                    continue
                if capture:
                    if re.match(r"^[│└├]── ", clean_line) and domain not in clean_line: break
                    content.append(line)
        return "".join(content).strip()
    except: return None

def print_recursive_dump():
    console.print(Panel(f"TOTAL SYSTEM ENCYCLOPEDIA", style="header", box=box.HEAVY))
    full_tree = get_atlas_tree()
    if full_tree:
        console.rule("[section]GLOBAL COMMAND ATLAS[/]")
        console.print(Text(full_tree, style="dim"))
    
    last_domain = None
    for root, dirs, files in os.walk(DOCS_ROOT):
        for file in sorted(files):
            if file.endswith(".md") and file not in ["atlas.md", "reference.md", "index.md"]:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, DOCS_ROOT)
                domain = rel_path.split(os.sep)[0] if os.sep in rel_path else "ROOT"
                if domain != last_domain:
                    console.print(f"\n\n[header]>>> DOMAIN: {domain.upper()} <<<[/]")
                    domain_tree = get_atlas_tree(domain)
                    if domain_tree:
                        console.print(Panel(Text(domain_tree, style="dim"), title="Structure", box=box.MINIMAL))
                    last_domain = domain
                content = get_help_content(file_path)
                if content:
                    title = rel_path.replace('.md', '').upper().replace('/INDEX', '')
                    console.rule(f"[section]{title}[/]")
                    render_content(content)
    console.rule("[bold red]END OF DUMP[/]")

def resolve_doc_path(domain=None, command=None):
    if not domain: return os.path.join(DOCS_ROOT, "index.md")
    if not command:
        path = os.path.join(DOCS_ROOT, domain, "index.md")
        if os.path.exists(path): return path
        return os.path.join(DOCS_ROOT, f"{domain}.md")
    return os.path.join(DOCS_ROOT, domain, f"{command}.md")

    if content: render_content(content, title=f"ATLAS TREE")
    else: console.print(f"[danger]⦗ERROR⦘[/danger] Command Atlas source file missing.")

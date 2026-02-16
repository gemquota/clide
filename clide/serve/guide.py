import os
import sys
import re
from art import tprint

# Dynamic path resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS_ROOT = os.path.join(BASE_DIR, "docs", "cli")

# --- CYBER-KERNEL SEMANTIC PALETTE ---
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_DIM = "\033[2m"
C_ITALIC = "\033[3m"

# Structural Reds (The Skeleton)
C_NEON_RED    = "\033[38;5;196m"  # High-level headers
C_CRIMSON     = "\033[38;5;160m"  # Decals / Mid-tier
C_SUBTLE_RED  = "\033[38;5;124m"  # Borders / Structural lines

# Semantic Colors (The Concepts)
C_ELECTRIC_CYAN = "\033[38;5;51m"   # Paths, Files, Navigation
C_ACID_GREEN    = "\033[38;5;118m"  # Success, Valid, Healthy
C_PLASMA_PURPLE = "\033[38;5;99m"   # Concepts, Domain Tags
C_SOLAR_YELLOW  = "\033[38;5;226m"  # High-Importance Technical Tags
C_GHOST_WHITE   = "\033[38;5;255m"  # Commands, Primary Labels
C_STEEL_GRAY    = "\033[38;5;240m"  # Secondary metadata, trees

def print_banner():
    # Multi-shade Red Skeleton Banner
    print(f"\n{C_SUBTLE_RED}   ██████╗{C_CRIMSON}██╗     {C_NEON_RED}██╗{C_CRIMSON}██████╗ ███████╗{C_RESET}")
    print(f"{C_SUBTLE_RED}  ██╔════╝{C_CRIMSON}██║     {C_NEON_RED}██║{C_CRIMSON}██╔══██╗██╔════╝{C_RESET}")
    print(f"{C_SUBTLE_RED}  ██║     {C_CRIMSON}██║     {C_NEON_RED}██║{C_CRIMSON}██║  ██║█████╗  {C_RESET}")
    print(f"{C_SUBTLE_RED}  ██║     {C_CRIMSON}██║     {C_NEON_RED}██║{C_CRIMSON}██║  ██║██╔══╝  {C_RESET}")
    print(f"{C_SUBTLE_RED}  ╚██████╗{C_CRIMSON}███████╗{C_NEON_RED}██║{C_CRIMSON}██████╔╝███████╗{C_RESET}")
    print(f"{C_SUBTLE_RED}   ╚═════╝{C_CRIMSON}╚══════╝{C_NEON_RED}╚═╝{C_CRIMSON}╚═════╝ ╚══════╝{C_RESET}")
    print(f"   {C_STEEL_GRAY}KOS // NEURAL-KERNEL v1.0.0 | LINK: {C_ACID_GREEN}SECURE{C_RESET}\n")

def draw_curve_header(text, color=C_NEON_RED):
    """Draws a smooth, curved scifi box header (Structural)."""
    top    = f"{color}╭───{'─' * len(text)}───╮{C_RESET}"
    mid    = f"{color}│   {C_BOLD}{C_GHOST_WHITE}{text.upper()}{C_RESET}{color}   │{C_RESET}"
    bottom = f"{color}╰───{'─' * len(text)}───╯{C_RESET}"
    return f"{top}\n{mid}\n{bottom}"

def draw_separator(char="─", length=50, color=C_SUBTLE_RED):
    """Draws a stylized divider with terminal caps (Structural)."""
    return f"{color}╾{'─' * (length-2)}╼{C_RESET}"

def draw_domain_header(title):
    """Prints a big ASCII header for a domain (Structural)."""
    print(f"{C_NEON_RED}", end="")
    tprint(title, font="small")
    print(f"{C_RESET}", end="")
    print(draw_separator("━", 60, C_SUBTLE_RED))

def draw_tier_decal(tier):
    """Draws an expanded, multi-colored depth decal with aesthetic Unicode glyphs."""
    tier = tier.upper()
    
    # Symmetrical Gradient Sequence
    g1 = C_SUBTLE_RED
    g2 = C_CRIMSON
    g3 = C_NEON_RED
    
    if tier == "BASIC":
        prefix = f"{g1}╶{g2}─{g3}╼ ⟨"
        suffix = f"⟩ ╾{g3}─{g2}╴{g1}"
        glyph = "◈"
        color = C_ACID_GREEN
    elif tier == "MORE":
        prefix = f"{g1}━{g2}╾{g3}⫷ ⌬"
        suffix = f"⌬ ⫸{g3}╼{g2}━{g1}"
        glyph = "⬢"
        color = C_ELECTRIC_CYAN
    elif tier == "FULL":
        prefix = f"{g1}╾{g2}╼{g3}⟪ ⧫"
        suffix = f"⧫ ⟫{g3}╾{g2}╼{g1}"
        glyph = "⚙"
        color = C_PLASMA_PURPLE
    else:
        prefix = f"{C_STEEL_GRAY}╶╼"
        suffix = f"{C_STEEL_GRAY}╾╴"
        glyph = "◇"
        color = C_GHOST_WHITE

    return f"\n{prefix} {C_BOLD}{color}{glyph} {tier} PROTOCOL {glyph}{C_RESET} {suffix}"

def visual_format(text):
    """The Deep-Logic Cyber-UI Renderer."""
    text = re.sub(r"\\033\[[0-9;]*m", "", text)
    text = text.replace("\033[1;32m", "").replace("\033[1;33m", "").replace("\033[1;34m", "").replace("\033[0m", "")
    
    lines = text.split("\n")
    formatted = []
    
    for line in lines:
        # H1 Headers (Structural)
        if line.startswith("# "):
            title = line.replace("# ", "").strip()
            formatted.append("\n" + draw_curve_header(title, C_NEON_RED))
            formatted.append(draw_separator("━", 50, C_SUBTLE_RED))
            continue
            
        # H2 Headers (Structural/Semantic)
        elif line.startswith("## "):
            title = line.replace("## ", "").strip()
            if title.startswith("Tier:"):
                tier_name = title.replace("Tier:", "").strip()
                formatted.append(draw_tier_decal(tier_name))
            else:
                decal = f"{C_CRIMSON}⫸{C_NEON_RED}⫸{C_RESET}"
                formatted.append(f"\n{decal} {C_BOLD}{C_PLASMA_PURPLE}{title}{C_RESET}")
                formatted.append(f"{C_SUBTLE_RED}╾{'─' * 25}╼{C_RESET}")
            continue

        # Tree Structures (Semantic: Gray)
        line = line.replace("├──", f"{C_STEEL_GRAY}├──{C_RESET}")
        line = line.replace("└──", f"{C_STEEL_GRAY}└──{C_RESET}")
        line = line.replace("│", f"{C_STEEL_GRAY}│{C_RESET}")
        
        # Bullet Points (Semantic: Green)
        line = line.replace("●", f"{C_ACID_GREEN}●{C_RESET}")
        line = re.sub(r"^(\s*)[-*](\s+)", rf"\1{C_ACID_GREEN}╰┈▶{C_RESET}\2", line)
        
        # Paths and Files (Semantic: Cyan)
        line = re.sub(r"([\w./-]+\.(?:py|md|json|db|toml))", rf"{C_ELECTRIC_CYAN}\1{C_RESET}", line)
        
        # Commands (Semantic: White)
        line = re.sub(r"(\./cli [\w\s{{}}|,-]+)", rf"{C_BOLD}{C_GHOST_WHITE}\1{C_RESET}", line)
        
        # Concepts (Semantic: Purple)
        line = re.sub(r"<([A-Z0-9\s_-]+)>", rf"{C_PLASMA_PURPLE}⦗\1⦘{C_RESET}", line)
        
        # Status/Warning (Semantic: Red/Yellow)
        line = re.sub(r"(WARNING|DANGER|CRITICAL|ERROR)", rf"{C_NEON_RED}{C_BOLD}«\1»{C_RESET}", line)
        line = re.sub(r"(SECURITY)", rf"{C_SOLAR_YELLOW}{C_BOLD}«\1»{C_RESET}", line)
        line = re.sub(r"(SUCCESS|VALID|PASSED|HEALTHY)", rf"{C_ACID_GREEN}{C_BOLD}«\1»{C_RESET}", line)
        
        # High-Importance Technical Terms (Semantic: Yellow)
        line = re.sub(r"(768D|SPA|LLM|MCP|RAG|SQLITE|JSON|UUID|API)", rf"{C_SOLAR_YELLOW}\1{C_RESET}", line)

        # Inline Labels (Semantic: White labels)
        line = re.sub(r"^([\w\s]+):", rf"{C_GHOST_WHITE}\1:{C_RESET}", line)
        
        formatted.append(line)
    
    return "\n".join(formatted)

def get_tier_content(file_path, tier="Basic"):
    if not os.path.exists(file_path): return None
    try:
        with open(file_path, 'r') as f: lines = f.readlines()
        content = []
        capture = False
        target_header = f"## Tier: {tier.capitalize()}"
        for line in lines:
            if line.strip() == target_header:
                capture = True
                continue
            if capture and line.strip().startswith("## Tier:"): break
            if capture: content.append(line)
        return "".join(content).strip()
    except: return None

def get_combined_help(file_path, level="basic"):
    # Normalize level to tier name
    target = "Basic"
    if level in ["more", "all_more"]: target = "More"
    elif level in ["full", "all", "all_full"]: target = "Full"
    
    text = get_tier_content(file_path, target)
    
    # Fallback to Basic if target tier is missing or empty
    if not text and target != "Basic":
        text = get_tier_content(file_path, "Basic")
        target = "Basic"
        
    if text:
        return visual_format(f"## Tier: {target}\n{text}")
    
    return None

def show_help(domain=None, command=None, level="basic"):
    print_banner()
    if level == "all":
        # Specific 'all' levels: all (basic), all more, all full
        print_recursive_dump("basic")
        return
    elif level == "all_more":
        print_recursive_dump("more")
        return
    elif level == "all_full":
        print_recursive_dump("full")
        return

    if not domain:
        print_help_index()
        return

    if domain and not command:
        draw_domain_header(domain)
        domain_tree = get_atlas_tree(domain)
        if domain_tree:
            print(visual_format(domain_tree))
            print(draw_separator("┄", 40, C_SUBTLE_RED))

    file_path = resolve_doc_path(domain, command)
    content = get_combined_help(file_path, level)
    
    if content:
        print(content)
        print("\n" + draw_separator("━", 60, C_SUBTLE_RED))
    else:
        print(f"{C_NEON_RED}⦗ERROR⦘ {C_RESET}Documentation for '{domain or 'root'}' not found.")

def print_help_index():
    index_text = """
# CLIDE // INTELLIGENCE PORTAL
The system knowledge base is segmented into three high-fidelity tiers.

## Help Modifiers
  [Tier 1] (none) : Detailed Functional Summary (Expanded).
  [Tier 2] more   : Technical Specs & Architectural Depth.
  [Tier 3] full   : High-Order Neural-Kernel Deep-Dive [2.13x Scale].
  [Global] all    : Total recursive dump of specified tier.

## Active Domains
"""
    print(visual_format(index_text.strip()))
    
    domains = [d for d in os.listdir(DOCS_ROOT) if os.path.isdir(os.path.join(DOCS_ROOT, d))]
    for d in sorted(domains):
        print(f"  {C_PLASMA_PURPLE}◈{C_RESET} {C_ELECTRIC_CYAN}{d.upper()}{C_RESET}")
        
    print(visual_format("\n## Meta Modules"))
    meta = [f.replace(".md", "") for f in os.listdir(DOCS_ROOT) if f.endswith(".md") and f not in ["index.md", "atlas.md", "reference.md"]]
    for m in sorted(meta):
        print(f"  {C_ACID_GREEN}⬢{C_RESET} {C_GHOST_WHITE}{m.upper()}{C_RESET}")

def get_atlas_tree(domain=None):
    """Extracts a tree from atlas.md. If domain is None, returns the full tree."""
    atlas_path = os.path.join(DOCS_ROOT, "atlas.md")
    if not os.path.exists(atlas_path): return None
    
    try:
        with open(atlas_path, 'r') as f: lines = f.readlines()
        content = []
        capture = False
        
        if not domain:
            target = "TOTAL SYSTEM COMMAND TREE"
            for line in lines:
                if target in line: capture = True; continue
                if capture and line.strip().startswith("## Tier:"): break
                if capture: content.append(line)
        else:
            target = f"### Domain: {domain.upper()}"
            for line in lines:
                if line.strip() == target: capture = True; continue
                if capture and (line.strip().startswith("###") or line.strip().startswith("## Tier:")): break
                if capture: content.append(line)
                
        return "".join(content).strip()
    except: return None

def print_recursive_dump(level="basic"):
    title_suffix = "BASIC" if level == "basic" else "TECHNICAL" if level == "more" else "KERNEL"
    print(f"\n{C_NEON_RED}{C_BOLD}╔{'═' * 60}╗{C_RESET}")
    print(f"{C_NEON_RED}{C_BOLD}║ TOTAL SYSTEM ENCYCLOPEDIA // {title_suffix:10} INITIALIZED...   ║{C_RESET}")
    print(f"{C_NEON_RED}{C_BOLD}╚{'═' * 60}╝{C_RESET}")
    
    # 1. Start with the Global Atlas Tree
    full_tree = get_atlas_tree()
    if full_tree:
        print(f"\n{C_SUBTLE_RED}╾─────────────────[ GLOBAL COMMAND ATLAS ]─────────────────╼{C_RESET}")
        print(visual_format(full_tree))
    
    last_domain = None
    for root, dirs, files in os.walk(DOCS_ROOT):
        for file in sorted(files):
            if file.endswith(".md") and file not in ["atlas.md", "reference.md", "index.md"]:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, DOCS_ROOT)
                
                domain = rel_path.split(os.sep)[0] if os.sep in rel_path else "ROOT"
                if domain != last_domain:
                    if last_domain:
                        print(f"\n{C_SUBTLE_RED}╾─────────────────[ END OF {last_domain.upper()} ]─────────────────╼{C_RESET}")
                    
                    print(f"\n\n{C_NEON_RED}╭─────────────────[ START OF {domain.upper()} ]─────────────────╮{C_RESET}")
                    draw_domain_header(domain)
                    
                    # 2. Inject Domain Tree at the start of each domain
                    domain_tree = get_atlas_tree(domain)
                    if domain_tree:
                        print(visual_format(domain_tree))
                        print(draw_separator("┄", 40, C_SUBTLE_RED))
                        
                    last_domain = domain

                # Use specific level for each command
                content = get_combined_help(file_path, level)
                if content:
                    title = rel_path.replace('.md', '').upper().replace('/INDEX', '')
                    print(f"\n\n{C_ELECTRIC_CYAN}╭╼[ {C_BOLD}{title} ]{C_RESET}")
                    print(content)
    
    if last_domain:
        print(f"\n{C_SUBTLE_RED}╾─────────────────[ END OF ENCYCLOPEDIA ]─────────────────╼{C_RESET}")

def resolve_doc_path(domain=None, command=None):
    if not domain: return os.path.join(DOCS_ROOT, "index.md")
    if not command:
        path = os.path.join(DOCS_ROOT, domain, "index.md")
        if os.path.exists(path): return path
        return os.path.join(DOCS_ROOT, f"{domain}.md")
    return os.path.join(DOCS_ROOT, domain, f"{command}.md")

def show_ref(domain=None, command=None, level="basic"):
    print_banner()
    
    if domain:
        draw_domain_header(f"ATLAS // {domain.upper()}")
        tree = get_atlas_tree(domain)
        if tree:
            print(visual_format(tree))
            print("\n" + draw_separator("━", 60, C_SUBTLE_RED))
        else:
            print(f"{C_NEON_RED}⦗ERROR⦘ {C_RESET}Domain '{domain}' not found in Command Atlas.")
        return

    draw_domain_header("ATLAS // TOTAL SYSTEM")
    file_path = os.path.join(DOCS_ROOT, "atlas.md")
    content = get_combined_help(file_path, level)
    if content:
        print(content)
    else:
        print(f"{C_NEON_RED}⦗ERROR⦘ {C_RESET}Command Atlas source file missing.")
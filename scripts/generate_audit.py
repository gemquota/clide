import os

DOCS_ROOT = "docs/cli"

def generate_audit():
    categories = {}
    
    # Scan docs/cli for all .md files
    for root, dirs, files in os.walk(DOCS_ROOT):
        for file in sorted(files):
            if file.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, file), DOCS_ROOT)
                parts = rel_path.split(os.sep)
                
                if len(parts) == 1:
                    category = "SYSTEM / META"
                else:
                    category = parts[0].upper()
                
                if category not in categories:
                    categories[category] = []
                categories[category].append(rel_path)

    lines = [
        "# ATLAS // DOCUMENTATION AUDIT CHECKLIST",
        "",
        "**Legend:**",
        "*   **1/2/3**: Tier 1 (Basic), Tier 2 (More), Tier 3 (Full).",
        "*   **4**: Real-World Match (Functionality matches documentation).",
        "*   **A**: AI Generation (1st Turn).",
        "*   **B**: User Review (2nd Turn).",
        "*   **C**: Confirmation (Final Completion).",
        "",
        "**Status Marks:**",
        "*   `[ ]`: Unstarted",
        "*   `?`: Started / Unfinished",
        "*   `[x]`: Completed",
        ""
    ]

    for cat, files in categories.items():
        lines.append(f"## {cat}")
        lines.append("| File | 1A | 1B | 1C | 2A | 2B | 2C | 3A | 3B | 3C | 4A | 4B | 4C |")
        lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
        
        for f in files:
            # Check current status (very rough heuristic: if file exists and has content, mark 1A/2A/3A as ?)
            row = [f"[code]{f}[/code]"]
            for i in range(12):
                row.append("[ ]")
            lines.append(f"| {' | '.join(row)} |")
        lines.append("")

    with open("docs/documentation_audit.md", "w") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    generate_audit()
    print("[v] Audit Checklist generated at docs/documentation_audit.md")

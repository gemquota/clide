import json
import os
from datetime import datetime

REGISTRY_PATH = "/data/data/com.termux/files/home/meta/commands/vector_registry.json"
OUTPUT_PATH = "/data/data/com.termux/files/home/meta/docs/dashboard.md"

def generate_dashboard():
    if not os.path.exists(REGISTRY_PATH):
        print("Error: Registry not found.")
        return

    with open(REGISTRY_PATH, "r") as f:
        assets = json.load(f)

    toml_count = 0
    mcp_count = 0
    for a in assets:
        t = a.get('metadata', {}).get('type')
        if t == 'toml': toml_count += 1
        elif t == 'mcp': mcp_count += 1

    header = "# CLIDE Asset Dashboard\n"
    header += "*Generated on " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "*\n\n"
    
    summary = "## Summary\n"
    summary += "- **Total Assets**: " + str(len(assets)) + "\n"
    summary += "- **TOML Commands**: " + str(toml_count) + "\n"
    summary += "- **MCP Servers**: " + str(mcp_count) + "\n\n"
    
    table = "## Asset Registry\n\n| ID | Type | Description | Path/Source |\n|----|------|-------------|-------------|\n"
    
    for asset in assets:
        a_id = str(asset.get('id', 'unknown'))
        metadata = asset.get('metadata', {})
        a_type = str(metadata.get('type', 'unknown')).upper()
        a_desc = str(metadata.get('desc', 'No description'))
        a_path = str(metadata.get('path', 'N/A'))
        table += "| **" + a_id + "** | " + a_type + "| " + a_desc + " | `" + a_path + "` |\n"

    footer = "\n\n---\n*CLIDE v0.6.0 Visual Registry Prototype*"
    
    with open(OUTPUT_PATH, "w") as f:
        f.write(header + summary + table + footer)
    
    print("[v] Dashboard generated at " + OUTPUT_PATH)

if __name__ == "__main__":
    generate_dashboard()

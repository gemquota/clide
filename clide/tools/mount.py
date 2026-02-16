import os
import json
import yaml
import re

REGISTRY_PATH = "/data/data/com.termux/files/home/openclaw/meta/swarm/commands/vector_registry.json"

def get_asset_by_id(asset_id):
    if not os.path.exists(REGISTRY_PATH):
        return None
    with open(REGISTRY_PATH, "r") as f:
        registry = json.load(f)
    for item in registry:
        if item["id"] == asset_id:
            return item
    return None

def extract_instructions(file_path):
    if not os.path.exists(file_path):
        return f"Error: File {file_path} not found."
    with open(file_path, "r") as f:
        content = f.read()
    
    # Strip YAML frontmatter
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        return content[match.end():].strip()
    return content.strip()

def activate_asset(asset_id, raw=False):
    asset = get_asset_by_id(asset_id)
    if not asset:
        return f"Error: Asset '{asset_id}' not found in registry."
    
    metadata = asset.get("metadata", {})
    a_type = metadata.get("type")
    a_path = metadata.get("path")
    
    if not a_path:
         return f"Error: No path defined for asset '{asset_id}'."

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(project_root, a_path)
    
    if a_type == "skill":
        instructions = extract_instructions(full_path)
        if raw: return instructions
        return f"\n--- MOUNTING SKILL: {asset_id} ---\n{instructions}\n"
    elif a_type == "agent":
        persona = extract_instructions(full_path)
        if raw: return persona
        return f"\n--- SWITCHING PERSONA: {asset_id} ---\n{persona}\n"
    elif a_type == "mcp":
        # For MCP, we point to the README or the script itself
        readme_path = os.path.join(os.path.dirname(full_path), "README.md")
        desc = metadata.get("desc", "No description.")
        instructions = f"Type: MCP Server\nDescription: {desc}\nPath: {a_path}\n"
        if os.path.exists(readme_path):
            instructions += "\n--- README ---\n" + extract_instructions(readme_path)
        else:
            instructions += "\n--- SOURCE PREVIEW ---\n" + extract_instructions(full_path)[:500] + "..."
        
        if raw: return instructions
        return f"\n--- AGENTIC ASSET: {asset_id} ---\n{instructions}\n"
    elif a_type == "toml":
        from commands_loader import load_commands
        name = asset_id # Assuming ID is the filename
        cmds = load_commands(os.path.dirname(full_path))
        if name in cmds:
            prompt = cmds[name]['prompt']
            if raw: return prompt
            return f"\n--- COMMAND PROMPT: {name} ---\n{prompt}\n"
        return f"Error: TOML command '{name}' logic not found."
    
    return f"Activation for type '{a_type}' not yet implemented."

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: activator.py <asset_id>")
    else:
        print(activate_asset(sys.argv[1]))

import os
import json
import yaml
import re

REGISTRY_PATH = "/data/data/com.termux/files/home/meta/swarm/commands/vector_registry.json"

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

def activate_asset(asset_id):
    asset = get_asset_by_id(asset_id)
    if not asset:
        return f"Error: Asset '{asset_id}' not found in registry."
    
    metadata = asset.get("metadata", {})
    a_type = metadata.get("type")
    a_path = metadata.get("path")
    
    if not a_path:
         return f"Error: No path defined for asset '{asset_id}'."

    # Prepend project root if path is relative
    full_path = os.path.join("/data/data/com.termux/files/home/meta", a_path)
    
    if a_type == "skill":
        instructions = extract_instructions(full_path)
        return f"\n--- MOUNTING SKILL: {asset_id} ---\n{instructions}\n"
    elif a_type == "agent":
        persona = extract_instructions(full_path)
        return f"\n--- SWITCHING PERSONA: {asset_id} ---\n{persona}\n"
    elif a_type == "toml":
        from commands_loader import load_commands
        # For TOML, we might just want to show the prompt
        name = asset_id # Assuming ID is the filename
        cmds = load_commands(os.path.dirname(full_path))
        if name in cmds:
            return f"\n--- COMMAND PROMPT: {name} ---\n{cmds[name]['prompt']}\n"
        return f"Error: TOML command '{name}' logic not found."
    
    return f"Activation for type '{a_type}' not yet implemented."

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: activator.py <asset_id>")
    else:
        print(activate_asset(sys.argv[1]))

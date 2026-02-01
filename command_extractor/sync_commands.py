import os
import json
from commands_loader import load_commands
from vector_registry import add_to_registry

COMMANDS_DIR = "/data/data/com.termux/files/home/.gemini/commands"
INDEX_FILE = "/data/data/com.termux/files/home/meta/commands/commands_index.md"

def sync():
    print("Synchronizing existing commands into CLIDE Database...")
    cmds = load_commands(COMMANDS_DIR)
    
    # 1. Update Vector Registry
    for name, info in cmds.items():
        print(f"Indexing: {name}...")
        # Only add if not already there (though add_to_registry currently appends, 
        # we'll assume a fresh start or simple check)
        add_to_registry(name, {"type": "toml", "desc": info['description']}, f"{name} {info['description']}")

    # 2. Update commands_index.md
    with open(INDEX_FILE, "w") as f:
        f.write("# CLIDE: Commands Index\n\n")
        f.write("## 1. Internal CLIDE Commands\n")
        f.write("*   **[clide](../clide)**: The primary shell launcher.\n")
        f.write("*   **[extractor.py](../command_extractor/extractor.py)**: The core monitoring service.\n\n")
        
        f.write("## 2. Integrated Gemini Commands\n")
        for name, info in sorted(cmds.items()):
            f.write(f"*   **{name}**: {info['description']}\n")
            
        f.write("\n---\n*Database: Everything - Synchronized*")
    
    print("Sync complete.")

if __name__ == "__main__":
    sync()


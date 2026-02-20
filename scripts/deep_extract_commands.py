import os
import re

def extract_all_commands():
    all_cmds = {}
    log_dir = 'ingestion_logs'
    
    # regex for | "cmd" | in NEW_COMMAND sections
    # or | `cmd` | in tables
    
    for root, _, files in os.walk(log_dir):
        for f_name in files:
            if f_name.endswith('.md') and 'theorycrafting' not in f_name:
                path = os.path.join(root, f_name)
                with open(path, 'r', errors='ignore') as f:
                    content = f.read()
                
                # Look for command_name in JSON objects inside sections
                # { "command_name": "xyz" ... }
                json_cmds = re.findall(r'"command_name":\s*"([^"]+)"', content)
                for cmd in json_cmds:
                    if cmd and cmd != 'null':
                        all_cmds[cmd] = all_cmds.get(cmd, 0) + 1
                
                # Look for | `cmd` |
                table_cmds = re.findall(r'\| `([^`]+)` \|', content)
                for cmd in table_cmds:
                    if len(cmd) > 2 and not re.match(r'^[0-9a-f]{8}$', cmd):
                        all_cmds[cmd] = all_cmds.get(cmd, 0) + 1
                        
    return all_cmds

if __name__ == "__main__":
    cmds = extract_all_commands()
    # Filter common noise
    noise = {'null', 'string', 'command_name', 'None', 'MATCH', 'NEW_COMMAND', 'FACT', 'DISCOVERY', 'LESSON', 'TODO', 'NICHE'}
    filtered = {k: v for k, v in cmds.items() if k not in noise and not k.startswith('sh_')}
    
    # Sort by frequency
    sorted_cmds = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    
    # Output to a new inventory file
    output_path = 'ingestion_logs/2026-02/new_commands_inventory_part03.md'
    with open(output_path, 'w') as f:
        f.write("# 🚀 New Commands Inventory: February 2026 (Part 3 - Deep Extraction)\n\n")
        f.write("| Command | Occurrences | Status |\n")
        f.write("| :--- | :--- | :--- |\n")
        for cmd, occ in sorted_cmds:
            f.write(f"| `{cmd}` | {occ} | EXTRACTED |\n")
            
    print(f"Extracted {len(filtered)} unique commands to {output_path}")

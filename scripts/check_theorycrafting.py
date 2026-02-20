import re
import os

def extract_commands_from_report(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r') as f:
        content = f.read()
    # Matches: | `command_name` |
    return set(re.findall(r'\| `([^`]+)` \|', content))

def extract_commands_from_inventory(file_path):
    commands = set()
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Format 1: | `command` | ... | (part 01)
    commands.update(re.findall(r'\| `([^`]+)` \| [^|]+ \|', content))
    
    # Format 2: **COMMAND:** `` `command` `` (part 02)
    commands.update(re.findall(r'\*\*COMMAND:\*\* `` `([^`]+)` ``', content))
    
    return commands

report_path = 'ingestion_logs/theorycrafting_report.md'
reported = extract_commands_from_report(report_path)

inventory_dir = 'ingestion_logs/2026-02'
all_inventory = set()
if os.path.exists(inventory_dir):
    for f_name in os.listdir(inventory_dir):
        if f_name.startswith('new_commands_inventory'):
            all_inventory.update(extract_commands_from_inventory(os.path.join(inventory_dir, f_name)))

missing = all_inventory - reported
print(f'Reported: {len(reported)}')
print(f'Inventory Total: {len(all_inventory)}')
print(f'Missing: {len(missing)}')
if missing:
    # Filter out potential session IDs or noise (session IDs are often 8-char hex)
    hex_pattern = re.compile(r'^[0-9a-f]{8}$')
    filtered_missing = [m for h in [missing] for m in h if not hex_pattern.match(m)]
    print(f'Missing (filtered): {len(filtered_missing)}')
    print(f'Examples: {filtered_missing[:10]}')
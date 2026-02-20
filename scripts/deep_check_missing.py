import os
import re

def get_all_intended_commands():
    intents = set()
    log_dir = 'ingestion_logs'
    for root, _, files in os.walk(log_dir):
        for f_name in files:
            if f_name.endswith('.md') and 'theorycrafting_report' not in f_name:
                path = os.path.join(root, f_name)
                with open(path, 'r', errors='ignore') as f:
                    content = f.read()
                
                # Format 1: CATEGORY: NEW_COMMAND ... Ingested Snippet ... "cmd"
                sections = content.split('---')
                for section in sections:
                    if 'NEW_COMMAND' in section or 'TOOL_INTENT' in section:
                        match = re.search(r'\| "(.*?)" \|', section)
                        if match:
                            intents.add(match.group(1).strip())
                            
                # Format 2: | `command` | ... |
                matches = re.findall(r'\| `([^`]+)` \|', content)
                for m in matches:
                    if len(m) > 3 and not re.match(r'^[0-9a-f]{8}$', m):
                        intents.add(m)
    return intents

def get_reported_commands():
    report_path = 'ingestion_logs/theorycrafting_report.md'
    if not os.path.exists(report_path): return set()
    with open(report_path, 'r') as f:
        content = f.read()
    return set(re.findall(r'\| `([^`]+)` \|', content))

if __name__ == "__main__":
    intended = get_all_intended_commands()
    reported = get_reported_commands()
    missing = intended - reported
    
    print(f"Total Intended Commands: {len(intended)}")
    print(f"Reported Commands: {len(reported)}")
    print(f"Missing from Report: {len(missing)}")
    
    if missing:
        print(f"Sample missing: {list(missing)[:10]}")

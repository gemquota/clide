import re
import os

def get_inventory_details():
    details = {}
    inventory_dir = 'ingestion_logs/2026-02'
    if not os.path.exists(inventory_dir):
        return details
    
    for f_name in os.listdir(inventory_dir):
        if f_name.startswith('new_commands_inventory'):
            with open(os.path.join(inventory_dir, f_name), 'r') as f:
                content = f.read()
            
            matches = re.findall(r'| `([^`]+)` | \d+ | [^|]+ | (.*?) |', content)
            for cmd, desc in matches:
                details[cmd] = desc.strip()
            
            matches2 = re.findall(r'\*\*COMMAND:\*\* `` `([^`]+)` ``\s+\*\*Primary Definition:\* \*(.*?)\*', content)
            for cmd, desc in matches2:
                details[cmd] = desc.strip()
                
    return details

def update_report(missing_cmds, details):
    report_path = 'ingestion_logs/theorycrafting_report.md'
    with open(report_path, 'r') as f:
        content = f.read()
    
    section_header = "# 🌐 Remaining Unsorted Commands"
    if section_header not in content:
        print("Section not found")
        return
    
    parts = content.split(section_header)
    table_header = '| :--- | :--- | :--- | :--- |'
    table_start = parts[1].find(table_header)
    if table_start == -1:
        print("Table not found")
        return
    
    # Find end of table (empty line or new header)
    table_content = parts[1][table_start + len(table_header):]
    table_end = table_content.find('\n\n')
    if table_end == -1: table_end = len(table_content)
    
    new_rows = ""
    for cmd in missing_cmds:
        desc = details.get(cmd, "No description found in inventory.")
        new_rows += f"| `{cmd}` | **7.0** | 1 | {desc[:100]}... |\n"
    
    updated_table_section = parts[1][:table_start + len(table_header)] + table_content[:table_end].strip() + "\n" + new_rows + table_content[table_end:]
    
    new_report = parts[0] + section_header + updated_table_section
    
    # Update Totals - more robust regex
    total_match = re.search(r'TOTALS.*?(\d+).*?(\d+)', new_report)
    if total_match:
        old_occ = total_match.group(1)
        old_unique = total_match.group(2)
        new_occ = str(int(old_occ) + len(missing_cmds))
        new_unique = str(int(old_unique) + len(missing_cmds))
        
        # Replace the first occurrence of old values after TOTALS
        line_start = new_report.find("TOTALS")
        line_end = new_report.find("\n", line_start)
        line = new_report[line_start:line_end]
        new_line = line.replace(old_occ, new_occ).replace(old_unique, new_unique)
        new_report = new_report[:line_start] + new_line + new_report[line_end:]

    with open(report_path, 'w') as f:
        f.write(new_report)
    print(f"Added {len(missing_cmds)} commands to theorycrafting report.")

if __name__ == "__main__":
    hex_pattern = re.compile(r'^[0-9a-f]{8}$')
    
    import scripts.check_theorycrafting as checker
    reported = checker.extract_commands_from_report('ingestion_logs/theorycrafting_report.md')
    
    all_inventory = set()
    inventory_dir = 'ingestion_logs/2026-02'
    if os.path.exists(inventory_dir):
        for f_name in os.listdir(inventory_dir):
            if f_name.startswith('new_commands_inventory'):
                all_inventory.update(checker.extract_commands_from_inventory(os.path.join(inventory_dir, f_name)))
    
    missing = [m for m in (all_inventory - reported) if not hex_pattern.match(m)]
    
    if missing:
        details = get_inventory_details()
        update_report(missing, details)
    else:
        print("No missing commands to add.")
import re
import os

def update_report_with_all_missing():
    report_path = 'ingestion_logs/theorycrafting_report.md'
    with open(report_path, 'r') as f:
        report_content = f.read()
    reported = set(re.findall(r'| `([^`]+)` |', report_content))

    inventory_dir = 'ingestion_logs/2026-02'
    all_found = set()
    for f_name in os.listdir(inventory_dir):
        if f_name.startswith('new_commands_inventory'):
            with open(os.path.join(inventory_dir, f_name), 'r') as f:
                content = f.read()
            # Find in Part 03 format: | `cmd` | occ | EXTRACTED |
            matches = re.findall(r'| `([^`]+)` | \d+ | [^|]+ |', content)
            all_found.update(matches)
            # Find in Part 01 format: | `cmd` | occ | tags | desc |
            matches2 = re.findall(r'| `([^`]+)` | \d+ | [^|]+ | [^|]+ |', content)
            all_found.update(matches2)

    noise = {'null', 'string', 'command_name', 'None', 'MATCH', 'NEW_COMMAND', 'FACT', 'DISCOVERY', 'LESSON', 'TODO', 'NICHE'}
    missing = [m for m in (all_found - reported) if m not in noise and not m.startswith('[') and not re.match(r'^[0-9a-f]{8}$', m)]
    
    if not missing:
        print("No real missing commands found.")
        return

    # Add to Unsorted section
    section_header = "# 🌐 Remaining Unsorted Commands"
    parts = report_content.split(section_header)
    table_header = '| :--- | :--- | :--- | :--- |'
    table_start = parts[1].find(table_header)
    
    new_rows = ""
    for cmd in sorted(missing):
        new_rows += f"| `{cmd}` | **7.0** | 1 | Deep-extracted from historical logs. |\n"
    
    table_content = parts[1][table_start + len(table_header):]
    table_end = table_content.find('\n\n')
    if table_end == -1: table_end = len(table_content)
    
    updated_table_section = parts[1][:table_start + len(table_header)] + table_content[:table_end].strip() + "\n" + new_rows + table_content[table_end:]
    new_report = parts[0] + section_header + updated_table_section
    
    # Update Totals
    total_match = re.search(r'TOTALS.*?(\d+).*?(\d+)', new_report)
    if total_match:
        old_occ = total_match.group(1)
        old_unique = total_match.group(2)
        new_occ = str(int(old_occ) + len(missing))
        new_unique = str(int(old_unique) + len(missing))
        line_start = new_report.find("TOTALS")
        line_end = new_report.find("\n", line_start)
        line = new_report[line_start:line_end]
        new_line = line.replace(old_occ, new_occ).replace(old_unique, new_unique)
        new_report = new_report[:line_start] + new_line + new_report[line_end:]

    with open(report_path, 'w') as f:
        f.write(new_report)
    print(f"Added {len(missing)} real missing commands to theorycrafting report.")

if __name__ == "__main__":
    update_report_with_all_missing()

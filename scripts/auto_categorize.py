import os
import re

def auto_categorize():
    report_path = 'ingestion_logs/theorycrafting_report.md'
    with open(report_path, 'r') as f:
        lines = f.readlines()

    unsorted_start = -1
    for i, line in enumerate(lines):
        if line.startswith('# 🌐 General/Misc'):
            unsorted_start = i
            break
    
    if unsorted_start == -1:
        return

    unsorted_lines = lines[unsorted_start:]
    other_lines = lines[:unsorted_start]

    # Categories and their mapping (Target Header, Regex Keywords)
    mappings = {
        '## 💠 Advanced Analysis': r'(analyze|assessment|critique|audit|forensic)',
        '## 💠 Logic Refactoring': r'(refactor|clean|simplify|deconstruct|modernize|refine)',
        '## 💠 System Synthesis': r'(generate|create|build|design|mockup|forge|synthesize|template|prompt|automate)',
        '## 💠 General Utility': r'(config|settings|alias|setup|install|terminal|pkg|shell|venv|exit|quit|resume|pause|break)',
        '## 💠 Git & Remote': r'(git|push|pull|repo|remote|branch|commit|deploy|github)',
        '## 💠 Validation Core': r'(test|check|verify|ensure|validate|stress|audit|benchmark)',
        '## 💠 Strategic Ops': r'(roadmap|strategy|assess|plan|monitor|status|report|summary|analytical)',
        '## 💠 System Meta': r'(meta|about|describe|explain|documentation|readme|changelog|version)',
        '## 💠 Task Management': r'(todo|task|assignment|pending|approve|sequential|orchestrate|prioritize)',
        '## 💠 Browser Automation': r'(scrape|crawl|browser|url|link|extract|facebook|social|login)',
        '## 💠 Math & Financials': r'(metric|stats|calculate|math|probability|ratio|amount|bonus|value|price)',
        '## 💠 Social Automation': r'(post|comment|social|facebook|twitter|moltbook|message|engagement)',
        '## 💠 Clustering & Cleaning': r'(cluster|dedupe|filter|batch|prune|clean|sanitisation)',
        '## 💠 Storage & Persistence': r'(db|database|sqlite|save|archive|backup|export|import|persistence|storage)',
        '## 💠 Transformation': r'(format|parse|convert|transform|reformat|restructure|encode|decode)',
        '## 💠 Data Viz & Rendering': r'(graph|chart|plot|visual|image|screenshot|animation|render)',
        '## 💠 Interface Layout': r'(ui|ux|tui|gui|layout|panel|grid|modal|slider|window|resize|screen)',
        '## 💠 Visual Semantics': r'(emoji|icon|color|palette|gradient|theme|style|formatting)'
    }

    categorized = {k: [] for k in mappings.keys()}
    new_unsorted = []
    
    # Simple table parser for the unsorted section
    in_table = False
    for line in unsorted_lines:
        if '| `core_command` |' in line or '| Command |' in line: # Header
            continue
        if '| :--- |' in line:
            continue
        
        match = re.search(r'\| `([^`]+)` \|', line)
        if match:
            cmd_name = match.group(1).lower()
            found = False
            for header, pattern in mappings.items():
                if re.search(pattern, cmd_name):
                    categorized[header].append(line)
                    found = True
                    break
            if not found:
                new_unsorted.append(line)
        else:
            if line.strip() and not line.startswith('#') and not line.startswith('*') and '|' in line:
                new_unsorted.append(line)

    # Rebuild the file
    new_report = []
    for line in other_lines:
        new_report.append(line)
        header = line.strip()
        if header in categorized and categorized[header]:
            # If we just hit a header, add the categorized lines after the table header
            # But the table header is already there in the file.
            # We need to find where the table starts for this category.
            pass

    # Actually, it's easier to just overwrite the whole file by sections
    # Let's read the whole file and split by headers
    with open(report_path, 'r') as f:
        text = f.read()
    
    sections = re.split(r'\n(?=# |## )', text)
    final_sections = []
    
    for section in sections:
        header_match = re.match(r'(#+ .*)\n', section)
        if not header_match:
            final_sections.append(section)
            continue
            
        header = header_match.group(1).strip()
        if header in categorized:
            # Append new lines to the table in this section
            table_lines = section.split('\n')
            new_section_lines = []
            for line in table_lines:
                new_section_lines.append(line)
                if '| :--- |' in line:
                    for cat_line in categorized[header]:
                        new_section_lines.append(cat_line.strip())
            final_sections.append('\n'.join(new_section_lines))
        elif header == '# 🌐 General/Misc':
            # Overwrite with remaining unsorted
            new_misc = [header, '*Ordered by Avg Importance (Descending)*', '', '| Command | Imp | Recurrence | Context Snippet |', '| :--- | :--- | :--- | :--- |']
            for line in new_unsorted:
                if line.strip():
                    new_misc.append(line.strip())
            final_sections.append('\n'.join(new_misc))
        else:
            final_sections.append(section)

    with open(report_path, 'w') as f:
        f.write('\n'.join(final_sections))

if __name__ == "__main__":
    auto_categorize()

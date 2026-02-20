import re
import os

def fix_and_refresh():
    report_path = 'ingestion_logs/theorycrafting_report.md'
    with open(report_path, 'r') as f:
        text = f.read()

    # 1. Strip out all "Domain Overview" sections
    text = re.sub(r'## 📊 Domain Overview.*?(\n# |$)', r'\1', text, flags=re.DOTALL)
    # Fix double headers and weird fragments
    text = re.sub(r'# # 🧠', '# 🧠', text)
    text = re.sub(r'---\n\n---', '---', text)
    text = re.sub(r'---\s+\| :---', '| :---', text)
    
    # 2. Split by sections correctly
    sections = re.split(r'\n(?=# |## )', text)
    
    summary_data = []
    current_domain = None
    domain_total_occ = 0
    domain_total_unique = 0
    domain_total_imp = 0.0
    
    all_total_occ = 0
    all_total_unique = 0
    
    for section in sections:
        lines = section.strip().split('\n')
        if not lines: continue
        header = lines[0].strip()
        
        if header.startswith('# ') and 'Theorycrafting' not in header and 'Potential Duplicate' not in header and 'General/Misc' not in header:
            if current_domain:
                avg_imp = domain_total_imp / domain_total_unique if domain_total_unique > 0 else 0
                summary_data.append([f"**{current_domain}**", "*ALL*", int(domain_total_occ), domain_total_unique, f"{avg_imp:.1f}"])
                
            current_domain = header.replace('# ', '').strip()
            domain_total_occ = 0
            domain_total_unique = 0
            domain_total_imp = 0.0
            
        elif header.startswith('## 💠') or header == '# 🌐 General/Misc':
            if header == '# 🌐 General/Misc':
                if current_domain:
                    avg_imp = domain_total_imp / domain_total_unique if domain_total_unique > 0 else 0
                    summary_data.append([f"**{current_domain}**", "*ALL*", int(domain_total_occ), domain_total_unique, f"{avg_imp:.1f}"])
                    current_domain = None
                sub_domain = "General/Misc"
                label = "**🌐 General/Misc**"
            else:
                sub_domain = header.replace('## 💠 ', '').strip()
                label = current_domain
            
            section_occ = 0
            section_unique = 0
            section_imp = 0.0
            
            for row in lines:
                if '|' not in row or '`' not in row: continue
                match = re.search(r'\|\s*`([^`]+)`\s*\|\s*(\*\*)?([\d\.]+)(\*\*)?\s*\|\s*(\*\*)?(\d+)(\*\*)?', row)
                if match:
                    section_unique += 1
                    section_imp += float(match.group(3))
                    section_occ += int(match.group(6))
            
            avg_imp = section_imp / section_unique if section_unique > 0 else 0
            summary_data.append([label, sub_domain if sub_domain != "General/Misc" else "*ALL*", int(section_occ), section_unique, f"{avg_imp:.1f}"])
            
            if current_domain:
                domain_total_occ += section_occ
                domain_total_unique += section_unique
                domain_total_imp += section_imp
            
            all_total_occ += section_occ
            all_total_unique += section_unique

    if current_domain:
        avg_imp = domain_total_imp / domain_total_unique if domain_total_unique > 0 else 0
        summary_data.append([f"**{current_domain}**", "*ALL*", int(domain_total_occ), domain_total_unique, f"{avg_imp:.1f}"])

    new_table = "| Domain | Sub-Domain | Total Occ | Unique | Avg Imp |\n"
    new_table += "| :--- | :--- | :--- | :--- | :--- |\n"
    for row in summary_data:
        new_table += f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} |\n"
    
    new_table += f"| **TOTALS** | -- | **{int(all_total_occ)}** | **{all_total_unique}** | **6.5** |\n"

    # 3. Reconstruct file
    title_pattern = r'# 🧠 Theorycrafting: Hierarchical Command Map \(V2\)'
    match = re.search(title_pattern, text)
    if match:
        title_end = match.end()
        final_text = text[:title_end] + "\n\n## 📊 Domain Overview\n\n" + new_table + "\n---\n" + text[title_end:]
    else:
        final_text = "## 📊 Domain Overview\n\n" + new_table + "\n---\n" + text

    # Final Cleanup
    final_text = re.sub(r'\n{3,}', '\n\n', final_text)

    with open(report_path, 'w') as f:
        f.write(final_text)

if __name__ == "__main__":
    fix_and_refresh()
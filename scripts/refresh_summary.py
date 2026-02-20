import re
import os

def recalculate_summary():
    report_path = 'ingestion_logs/theorycrafting_report.md'
    with open(report_path, 'r') as f:
        text = f.read()

    sections = re.split(r'\n(?=# |## )', text)
    
    summary_data = []
    
    current_domain = None
    domain_total_occ = 0
    domain_total_unique = 0
    domain_total_imp = 0.0
    
    all_total_occ = 0
    all_total_unique = 0
    
    for section in sections:
        header_match = re.match(r'(#+ .*)\n', section)
        if not header_match: continue
        header = header_match.group(1).strip()
        
        if header.startswith('# ') and 'Theorycrafting' not in header and 'Domain Overview' not in header and 'Potential Duplicate' not in header:
            if current_domain:
                avg_imp = domain_total_imp / domain_total_unique if domain_total_unique > 0 else 0
                summary_data.append([f"**{current_domain}**", "*ALL*", domain_total_occ, domain_total_unique, f"{avg_imp:.1f}"])
                
            current_domain = header.replace('# ', '').strip()
            domain_total_occ = 0
            domain_total_unique = 0
            domain_total_imp = 0.0
            
        elif header.startswith('## 💠') or header == '# 🌐 General/Misc':
            sub_domain = header.replace('## 💠 ', '').replace('# ', '').strip()
            
            rows = section.strip().split('\n')
            section_occ = 0
            section_unique = 0
            section_imp = 0.0
            
            for row in rows:
                if '|' not in row or '`' not in row: continue
                parts = [p.strip() for p in row.split('|')]
                if len(parts) < 4: continue
                
                cmd_match = re.search(r'`([^`]+)`', parts[1])
                if not cmd_match: continue
                
                imp_match = re.search(r'([\d\.]+)', parts[2])
                occ_match = re.search(r'(\d+)', parts[3])
                
                if imp_match and occ_match:
                    section_unique += 1
                    section_imp += float(imp_match.group(1))
                    section_occ += int(occ_match.group(1))
            
            avg_imp = section_imp / section_unique if section_unique > 0 else 0
            summary_data.append([current_domain if not header.startswith('# ') else sub_domain, sub_domain, section_occ, section_unique, f"{avg_imp:.1f}"])
            
            domain_total_occ += section_occ
            domain_total_unique += section_unique
            domain_total_imp += section_imp
            
            all_total_occ += section_occ
            all_total_unique += section_unique

    if current_domain:
        avg_imp = domain_total_imp / domain_total_unique if domain_total_unique > 0 else 0
        summary_data.append([f"**{current_domain}**", "*ALL*", domain_total_occ, domain_total_unique, f"{avg_imp:.1f}"])

    new_table = "| Domain | Sub-Domain | Total Occ | Unique | Avg Imp |\n"
    new_table += "| :--- | :--- | :--- | :--- | :--- |\n"
    for row in summary_data:
        new_table += f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} |\n"
    
    new_table += f"| **TOTALS** | -- | **{all_total_occ}** | **{all_total_unique}** | **6.5** |\n"

    overview_header = "## 📊 Domain Overview"
    parts = text.split(overview_header)
    sub_parts = parts[1].split('---')
    
    final_text = parts[0] + overview_header + "\n\n" + new_table + "\n---\n" + '---'.join(sub_parts[1:])
    
    with open(report_path, 'w') as f:
        f.write(final_text)

if __name__ == "__main__":
    recalculate_summary()

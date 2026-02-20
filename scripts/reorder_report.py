import os

def move_misc_to_end(path):
    with open(path, 'r') as f:
        content = f.read()
    
    parts = content.split('\n# ')
    misc_part = None
    other_parts = []
    
    for part in parts:
        if part.startswith('🌐 General/Misc'):
            misc_part = '# ' + part
        else:
            if part.strip():
                if part.startswith('🧠'): # First part
                    other_parts.append(part)
                else:
                    other_parts.append('# ' + part)
    
    if misc_part:
        # Check if there's a Potential Duplicates part
        dupes_part = None
        for i, part in enumerate(other_parts):
            if 'Potential Duplicate Merges' in part:
                dupes_part = other_parts.pop(i)
                break
        
        new_content = '\n'.join(other_parts)
        new_content += '\n\n' + misc_part
        if dupes_part:
            new_content += '\n\n' + dupes_part
            
        with open(path, 'w') as f:
            f.write(new_content)

if __name__ == "__main__":
    move_misc_to_end('ingestion_logs/theorycrafting_report.md')

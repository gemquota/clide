import os
import re

DOCS_DIR = "docs/cli"

def parse_tiers(content):
    # Split by ## Tier: headers
    sections = re.split(r"## Tier: (Basic|More|Full)\n", content)
    
    tiers = {"Basic": "", "More": "", "Full": ""}
    for i in range(1, len(sections), 2):
        if sections[i] in tiers:
            tiers[sections[i]] = sections[i+1].strip()
            
    title_match = re.match(r"(# .*?)\n", content)
    title = title_match.group(1) if title_match else "# DOCUMENTATION"
    
    return title, tiers

def cascade_docs():
    for root, _, files in os.walk(DOCS_DIR):
        for f in files:
            if not f.endswith(".md"): continue
            path = os.path.join(root, f)
            
            with open(path, "r") as f_obj:
                content = f_obj.read()
            
            title, tiers = parse_tiers(content)
            
            b = tiers["Basic"]
            m = tiers["More"]
            fl = tiers["Full"]
            
            # Cascade Logic
            if b and b not in m:
                new_more = b + "\n\n" + m
            else:
                new_more = m
                
            if new_more and new_more not in fl:
                new_full = new_more + "\n\n" + fl
            else:
                new_full = fl
                
            output = f"{title}\n\n## Tier: Basic\n{b}\n\n## Tier: More\n{new_more}\n\n## Tier: Full\n{new_full}\n"
            
            with open(path, "w") as f_obj:
                f_obj.write(output)
    
    print("Documentation cascade complete. Each tier is now inclusive.")

if __name__ == "__main__":
    cascade_docs()
import os
import re

DOCS_DIR = "docs/cli"

def parse_tiers(content):
    # Regex to find sections between ## Tier: headers
    basic = re.search(r"## Tier: Basic\n(.*?)(?=## Tier:|$)", content, re.DOTALL)
    more = re.search(r"## Tier: More\n(.*?)(?=## Tier:|$)", content, re.DOTALL)
    full = re.search(r"## Tier: Full\n(.*?)(?=## Tier:|$)", content, re.DOTALL)
    
    return {
        "basic": basic.group(1).strip() if basic else "",
        "more": more.group(1).strip() if more else "",
        "full": full.group(1).strip() if full else ""
    }

def refactor_docs():
    ratios = []
    
    for root, _, files in os.walk(DOCS_DIR):
        for f in files:
            if not f.endswith(".md"): continue
            path = os.path.join(root, f)
            
            with open(path, "r") as f_obj:
                content = f_obj.read()
            
            tiers = parse_tiers(content)
            
            # Calculate length-based ratio for this file
            l_basic = len(tiers['basic']) if tiers['basic'] else 1
            l_more = len(tiers['more']) if tiers['more'] else 1
            l_full = len(tiers['full']) if tiers['full'] else 1
            
            # Ratio of expansion from tier to tier
            # We'll use (More/Basic) as the primary modifier for growth
            if l_more > 1 and l_basic > 1:
                ratios.append(l_more / l_basic)
            
            # Perform the Shift
            # New Basic = Old More
            # New More = Old Full
            # New Full = [PLACEHOLDER] 
            
            new_content = re.sub(r"# (.*?)\n", f"# \1\n\n", content, count=1) # Keep title
            # Actually simpler to just rebuild the string
            title_match = re.match(r"(# .*?)\n", content)
            title = title_match.group(1) if title_match else "# DOCUMENTATION"
            
            # Note: We want to preserve usage lines if possible
            usage = re.search(r"Usage: .*", tiers['basic'])
            usage_str = usage.group(0) if usage else ""
            
            shifted_basic = tiers['more']
            if usage_str and usage_str not in shifted_basic:
                shifted_basic += f"\n{usage_str}"
                
            shifted_more = tiers['full']
            
            # Construct updated file
            output = f"{title}\n\n## Tier: Basic\n{shifted_basic}\n\n## Tier: More\n{shifted_more}\n\n## Tier: Full\n[EXPANSION PENDING]\n"
            
            # Write back
            with open(path, "w") as f_obj:
                f_obj.write(output)
                
    avg_modifier = sum(ratios) / len(ratios) if ratios else 1.5
    print(f"Shift complete. Calculated Expansion Modifier: {avg_modifier:.2f}x")
    return avg_modifier

if __name__ == "__main__":
    refactor_docs()

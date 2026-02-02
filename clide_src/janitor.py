import json
import os
import subprocess
from vector_registry import search_registry

REGISTRY_PATH = "/data/data/com.termux/files/home/meta/swarm/commands/vector_registry.json"

def run_janitor():
    if not os.path.exists(REGISTRY_PATH):
        return

    with open(REGISTRY_PATH, "r") as f:
        assets = json.load(f)

    if len(assets) < 2:
        print("Janitor: Not enough assets to find overlaps.")
        return

    print("--- CLIDE Surgeon: Searching for overlapping tools ---")
    overlaps = []
    checked = set()

    for i, asset in enumerate(assets):
        a_id = asset['id']
        a_desc = asset['metadata'].get('desc', '')
        
        # Search for similar assets
        results = search_registry(a_desc, limit=3)
        for sim, item in results:
            b_id = item['id']
            if a_id == b_id: continue
            
            pair = tuple(sorted((a_id, b_id)))
            if pair in checked: continue
            checked.add(pair)

            if sim > 0.85: # High threshold for autonomous surgery
                overlaps.append((a_id, b_id, sim))

    if not overlaps:
        print("[v] No significant overlaps detected.")
        return

    for a, b, sim in overlaps:
        print(f"\n[!] OVERLAP DETECTED ({int(sim*100)}%): '{a}' and '{b}'")
        try:
            choice = input(f"[?] Perform autonomous Merge & Archive? (y/N): ").strip().lower()
        except EOFError:
            choice = 'n'
        if choice == 'y':
            perform_merge(a, b)

def archive_originals(id_a, id_b):
    archive_dir = "/data/data/com.termux/files/home/meta/swarm/commands/archive"
    os.makedirs(archive_dir, exist_ok=True)
    
    # Move TOMLs and MCPs
    for asset_id in [id_a, id_b]:
        # Move TOML
        toml_src = f"/data/data/com.termux/files/home/meta/swarm/commands/{asset_id}.toml"
        if os.path.exists(toml_src):
            os.rename(toml_src, os.path.join(archive_dir, f"{asset_id}.toml"))
        
        # Move MCP
        mcp_src = f"/data/data/com.termux/files/home/meta/swarm/commands/mcp_servers/{asset_id}.py"
        if os.path.exists(mcp_src):
            os.rename(mcp_src, os.path.join(archive_dir, f"{asset_id}.py"))

def perform_merge(id_a, id_b):
    print(f"[*] Creating safety checkpoint...")
    subprocess.run(["git", "add", "."], capture_output=True)
    subprocess.run(["git", "commit", "-m", f"Pre-merge backup: {id_a} & {id_b}"], capture_output=True)

    print(f"[*] Synthesizing merged logic...")
    prompt = f"Merge the following two tools into one robust tool. Return ONLY the new Python code for an MCP server.\nTool A: {id_a}\nTool B: {id_b}"
    try:
        result = subprocess.run(["gemini", "-p", prompt], capture_output=True, text=True)
        merged_code = result.stdout.strip()
        
        new_id = f"{id_a}_{id_b}_merged"
        from mcp_generator import save_mcp_server
        save_mcp_server(new_id, merged_code, is_complex=True, description=f"Merged from {id_a} and {id_b}")
        
        print(f"[*] Archiving originals...")
        archive_originals(id_a, id_b)
        print(f"[v] Merge complete. New tool: '{new_id}'")
        
    except Exception as e:
        print(f"[!] Merge failed: {e}. Use 'git reset --hard HEAD' to rollback.")

def propose_merge(id_a, id_b):
    # Fetch logic for both
    # (Simplified for now, just showing the concept)
    print(f"Janitor: Analyzing '{id_a}' and '{id_b}' for merging...")
    prompt = f"Propose a merged version of two CLI tools: '{id_a}' and '{id_b}'. Create a single, more robust tool that covers both use cases. Return a suggested name and description."
    try:
        result = subprocess.run(["gemini", "-p", prompt], capture_output=True, text=True)
        print("\n--- SUGGESTED MERGE PLAN ---")
        print(result.stdout.strip())
    except:
        print("Error generating merge plan.")

if __name__ == "__main__":
    run_janitor()

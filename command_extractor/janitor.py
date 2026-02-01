import json
import os
import subprocess
from vector_registry import search_registry

REGISTRY_PATH = "/data/data/com.termux/files/home/meta/commands/vector_registry.json"

def run_janitor():
    if not os.path.exists(REGISTRY_PATH):
        return

    with open(REGISTRY_PATH, "r") as f:
        assets = json.load(f)

    if len(assets) < 2:
        print("Janitor: Not enough assets to find overlaps.")
        return

    print("--- CLIDE Janitor: Searching for overlapping tools ---")
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

            if sim > 0.8:
                overlaps.append((a_id, b_id, sim))

    if not overlaps:
        print("[v] No significant overlaps detected.")
        return

    for a, b, sim in overlaps:
        print(f"\n[!] OVERLAP DETECTED ({int(sim*100)}%): '{a}' and '{b}'")
        choice = input(f"[?] Propose a Merge Plan for these two? (y/N): ").strip().lower()
        if choice == 'y':
            propose_merge(a, b)

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

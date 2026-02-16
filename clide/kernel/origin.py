import json
import os

PROVENANCE_DIR = "/data/data/com.termux/files/home/openclaw/meta/swarm/commands/provenance"

def save_provenance(asset_id, context_text):
    """Saves the agentic context/trigger for a specific asset."""
    os.makedirs(PROVENANCE_DIR, exist_ok=True)
    file_path = os.path.join(PROVENANCE_DIR, f"{asset_id}.json")
    data = {
        "asset_id": asset_id,
        "context_trigger": context_text,
        "timestamp": os.path.getmtime(PROVENANCE_DIR) if os.path.exists(PROVENANCE_DIR) else 0
    }
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def get_provenance(asset_id):
    """Retrieves the agentic trigger context for an asset."""
    file_path = os.path.join(PROVENANCE_DIR, f"{asset_id}.json")
    if not os.path.exists(file_path):
        return "No provenance trigger found for this asset."
    
    with open(file_path, "r") as f:
        data = json.load(f)
        return data.get("context_trigger", "Trigger context empty.")

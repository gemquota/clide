import json
import os

REGISTRY_PATH = "commands/vector_registry.json"

def add_mock_duplicate():
    with open(REGISTRY_PATH, "r") as f:
        data = json.load(f)
    
    # Mock a duplicate of the 'engineer' asset
    mock_asset = {
        "id": "engineer_clone",
        "metadata": {
            "type": "toml",
            "desc": "Activates the Termux Engineer persona for system work"
        },
        "embedding": data[0]["embedding"] # Copy embedding to ensure match
    }
    
    data.append(mock_asset)
    with open(REGISTRY_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print("Mock duplicate 'engineer_clone' added.")

if __name__ == "__main__":
    add_mock_duplicate()

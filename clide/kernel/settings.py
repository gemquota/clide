import json
import os

# Base directory relative to the clide/core/ folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_PATH = os.path.join(BASE_DIR, ".cliderc")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        # Return defaults if no config found
        return {
            "paths": {
                "commands": "swarm/commands",
                "core": "swarm/core",
                "memory": "clide/memory.db",
                "registry": "swarm/commands/vector_registry.json"
            },
            "extraction": {
                "repetition_limit": 1000,
                "complexity_threshold": 4
            }
        }
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def get_path(key):
    config = load_config()
    relative_path = config["paths"].get(key)
    # Ensure portability by joining with detected BASE_DIR
    return os.path.join(BASE_DIR, relative_path)
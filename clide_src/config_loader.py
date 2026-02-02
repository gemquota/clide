import json
import os

CONFIG_PATH = "/data/data/com.termux/files/home/meta/.cliderc"

def load_config():
    if not os.path.exists(CONFIG_PATH):
        # Return defaults if no config found
        return {
            "paths": {
                "commands": "swarm/commands",
                "core": "swarm/core",
                "memory": "clide_src/memory.db",
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
    return os.path.join("/data/data/com.termux/files/home/meta", relative_path)

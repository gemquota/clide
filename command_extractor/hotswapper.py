import json
import os

SETTINGS_PATH = "/data/data/com.termux/files/home/.gemini/settings.json"

def hotswap_mcp_server(server_name, file_path):
    """Registers a new MCP server in the Gemini CLI settings."""
    if not os.path.exists(SETTINGS_PATH):
        settings = {"mcpServers": {}}
    else:
        with open(SETTINGS_PATH, "r") as f:
            try:
                settings = json.load(f)
            except:
                settings = {"mcpServers": {}}

    if "mcpServers" not in settings:
        settings["mcpServers"] = {}

    # Register the server
    settings["mcpServers"][server_name] = {
        "command": "python",
        "args": [file_path]
    }

    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=2)
    
    print(f"Hot-swap successful: '{server_name}' is now active in Gemini CLI.")

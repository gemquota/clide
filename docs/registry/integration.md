# Registry: Integration & Hot-swapping

## The Hot-swapper (`hotswapper.py`)
### Mechanism
Modifies the global `~/.gemini/settings.json`.
### Process
1. Loads the settings JSON.
2. Identifies the `mcpServers` key.
3. Appends the new server name and its execution path (e.g., `python /path/to/server.py`).
4. Flushes the JSON to disk.

### Immediate Availability
Once the file is written, the Gemini CLI (or any MCP-compatible client reading that config) can immediately invoke the new tool without a restart of the CLIDE monitor.

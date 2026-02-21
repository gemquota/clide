# SYSTEM CONFIG

- Displays the current kernel configuration in a structured JSON format.
- Reads from the system's `config.ini` and environment variables.
- Provides visibility into active pathing, API keys (redacted), and model settings.
Usage: ./cli system config

### Configuration Variables

#### [paths]
- **commands**: Directory containing forged MCP server tools.
- **core**: Directory for system-critical core modules.
- **memory**: Path to the primary SQLite knowledge database (`memory.db`).
- **registry**: Path to the semantic vector registry (`vector_registry.json`).

#### [extraction]
- **repetition_limit**: Maximum number of similar items allowed before flagging as redundancy.
- **complexity_threshold**: Heuristic score (1-10) used to determine if a message warrants deep LLM analysis.

### Technical Deep-Dive
The `config` command is implemented in `clide.serve.portal.cmd_system`.

### Logic Flow
1. **Load**: Invokes `clide.kernel.settings.load_config()`.
2. **Parsing**: The configuration loader merges default settings with user-defined overrides in `config.ini`.
3. **Display**: Prints the resulting dictionary to the console with `json.dumps(indent=2)`.

### Code Reference
- **Implementation**: `clide/kernel/settings.py` -> `load_config`

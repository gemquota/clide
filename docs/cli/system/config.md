# SYSTEM CONFIG

- Displays the current kernel configuration in a structured JSON format.
- Reads from the system's `config.ini` and environment variables.
- Provides visibility into active pathing, API keys (redacted), and model settings.
Usage: ./cli system config

TECHNICAL DEEP-DIVE:
The `config` command is implemented in `clide.serve.portal.cmd_system`.

### Logic Flow
1. **Load**: Invokes `clide.kernel.settings.load_config()`.
2. **Parsing**: The configuration loader merges default settings with user-defined overrides in `config.ini`.
3. **Display**: Prints the resulting dictionary to the console with `json.dumps(indent=2)`.

### Code Reference
- **Implementation**: `clide/kernel/settings.py` -> `load_config`

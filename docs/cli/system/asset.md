# SYSTEM ASSET

- Provides a high-level inventory of all semantic assets currently indexed.
- Breaks down the count of units by their metadata type (e.g., FACT, TOOL, MCP).
- Displays the total volume of registered knowledge.
Usage: ./cli system asset

TECHNICAL DEEP-DIVE:
The `asset` command is implemented in `clide.serve.portal.cmd_system`.

### Logic Flow
1. **Telemetry**: Calls `clide.brain.memory.get_registry_stats()`.
2. **Aggregation**: Iterates through the distribution dictionary returned by the stats engine.
3. **Rendering**: Prints a formatted summary of the project's intellectual inventory.

### Code Reference
- **Stats Provider**: `clide/brain/memory.py` -> `get_registry_stats`

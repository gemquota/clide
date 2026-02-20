# FORGE ARCHIVE

- Safely moves a forged asset to the system archive.
- Prevents clutter in the active MCP servers directory while preserving the code for future reference.
- Appends a timestamp to the archived version to prevent collisions.
Usage: ./cli forge archive <asset_id>

- Safely moves a forged asset to the system archive.
- Prevents clutter in the active MCP servers directory while preserving the code for future reference.
- Appends a timestamp to the archived version to prevent collisions.
Usage: ./cli forge archive <asset_id>

TECHNICAL DEEP-DIVE:
The `archive` command is implemented in `clide.forge.master.SynthesisOrchestrator.archive_asset`.

### Logic Flow
1. **Search**: Checks for the existence of the asset in `swarm/commands/mcp_servers/` (handles both package directories and single `.py` files).
2. **Naming**: Generates a destination name: `{asset_id}_{YYYYMMDD}`.
3. **Relocation**: Uses `shutil.move()` to transfer the asset to `archive/forged_assets/`.
4. **Cleanup**: (Planned) Should remove the asset from `vector_registry.json` during archiving.

### Code Reference
- **Entry Point**: `clide/serve/portal.py` -> `cmd_forge` (archive)
- **Implementation**: `clide/forge/master.py` -> `archive_asset`
- **Destination**: `/archive/forged_assets/`

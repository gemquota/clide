# SYSTEM BACKUP

- Creates a timestamped full-state snapshot of the system's database.
- Ensures that the core knowledge base can be recovered in the event of corruption or data loss.
- Stores backups in the `clide/backups/` directory.
Usage: ./cli system backup

TECHNICAL DEEP-DIVE:
The `backup` command is implemented in `clide.serve.portal.cmd_system`.

### Logic Flow
1. **Directory Check**: Ensures `clide/backups/` exists.
2. **Timestamping**: Generates a string using `%Y%m%d_%H%M%S`.
3. **Copy**: Uses `shutil.copy2()` to perform a binary copy of the active `memory.db`.
4. **Confirmation**: Prints the destination path of the new backup file.

### Code Reference
- **Entry Point**: `clide/serve/portal.py` -> `cmd_system` (backup)
- **Target**: `clide/memory.db`
- **Destination**: `clide/backups/`

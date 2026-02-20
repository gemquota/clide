# AUTO SYNC

- Ensures that every active task in the database is reflected in the `todo.md` file.
- Rebuilds the markdown list to match the current 'Ground Truth'.
- Includes the source origin of each task for context.
Usage: ./cli auto sync

- Ensures that every active task in the database is reflected in the `todo.md` file.
- Rebuilds the markdown list to match the current 'Ground Truth'.
- Includes the source origin of each task for context.
Usage: ./cli auto sync

TECHNICAL DEEP-DIVE:
The `sync` command maintains 'File-to-DB Parity' by treating SQLite as the master source.
1. **Extraction:** Fetches all nodes with `category='TODO'` from `memory.db`.
2. **Formatting:** Generates Markdown list items containing the task content and the `original_msg` source.
3. **Overwrite:** Completely overwrites the `todo.md` file at the project root with the fresh list.

- Ensures that every active task in the database is reflected in the `todo.md` file.
- Rebuilds the markdown list to match the current 'Ground Truth'.
- Includes the source origin of each task for context.
Usage: ./cli auto sync

TECHNICAL DEEP-DIVE:
The `sync` command is implemented via the `TodoManager` class.

### Logic Flow
1. **DB Retrieval:** Executes `SELECT content, original_msg FROM knowledge WHERE category = 'TODO'`.
2. **File Generation:**
   - Opens `todo.md` in write mode (`"w"`).
   - Writes the header: `# CLIDE TODO (Synchronized)`.
   - For each row, writes a checkbox line: `- [ ] {content} (Extracted from: {orig[:30]}...)`.
3. **Automation:** This sync is triggered automatically by other `TodoManager` operations (like `remove_todo` or `complete_todo`) to ensure consistency.

### Code Reference
- **Entry Point:** `clide/serve/portal.py` -> `cmd_run`
- **Implementation:** `clide/tools/janitor.py` -> `TodoManager.sync_to_file`

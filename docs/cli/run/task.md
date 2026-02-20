# RUN TASK

- **list**: Show all active tasks with IDs.
- **add <txt>**: Manual task creation.
- **remove <id>**: Delete task.
- **complete <id>**: Mark as done (archives unit).
Usage: ./cli run task {list, add, remove, complete}

- **list**: Show all active tasks with IDs.
- **add <txt>**: Manual task creation.
- **remove <id>**: Delete task.
- **complete <id>**: Mark as done (archives unit).
Usage: ./cli run task {list, add, remove, complete}

TECHNICAL DEEP-DIVE:
The `task` subcommand manages the 'Operational Horizon'.
1. **DB Mapping**: Maps directly to nodes where `category='TODO'`.
2. **Side Effects**: `add` and `complete` trigger a sync to the physical `todo.md` file.
3. **Integrity**: `complete` changes the category to `COMPLETED` before triggering a file sync.
4. **Orchestration**: Used by the user to finalize goals that have been achieved.
Essential for 'Human-in-the-Loop' project governance.

- **list**: Show all active tasks with IDs.
- **add <txt>**: Manual task creation.
- **remove <id>**: Delete task.
- **complete <id>**: Mark as done (archives unit).
Usage: ./cli run task {list, add, remove, complete}

TECHNICAL DEEP-DIVE:
The `task` subcommand is implemented in `clide.tools.janitor.TodoManager`.

### Logic Flow
1. **List**: Executes `SELECT id, content, timestamp FROM knowledge WHERE category = 'TODO'`.
2. **Add**: Calls `storage.save_knowledge` with `category='TODO'`.
3. **Complete**: Executes `UPDATE knowledge SET category = 'COMPLETED' WHERE id = ?`.
4. **Sync**: After every mutation (`add`, `remove`, `complete`), `mgr.sync_to_file()` is called to rewrite `todo.md`.

### Code Reference
- **Entry Point**: `clide/serve/portal.py` -> `cmd_run`
- **Implementation**: `clide/tools/janitor.py` -> `TodoManager`
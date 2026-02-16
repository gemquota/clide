# CLIDE // MANUAL DOMAIN

## Tier: Basic
DETAILED USAGE
- './cli manual node get <id>' prints the full dictionary of a knowledge unit.
- './cli manual task add "Task"' bypasses the monitor for immediate entry.
- './cli manual node tag <id> bug,fix' manually appends metadata.

## Tier: More
DETAILED USAGE
- './cli manual node get <id>' prints the full dictionary of a knowledge unit.
- './cli manual task add "Task"' bypasses the monitor for immediate entry.
- './cli manual node tag <id> bug,fix' manually appends metadata.

TECHNICAL ARCHITECTURE: MANUAL
=====================================

1. GROUND TRUTH MODIFICATION
----------------------------
Manual acts as the bypass for the reasoning engine.
It uses 'clide/kernel/storage.py' directly to modify the SQLite database.

2. CRUD OPERATIONS
------------------
- NODE: edit, delete, move, get, tag.
- TASK: add, remove, complete, list.
- ASSET: list, archive, delete.

3. STATE SYNCHRONIZATION
------------------------
When a task is 'completed' via manual command, the system:
1. Deletes the row from memory.db.
2. Re-generates 'todo.md' to remove the line.
3. Records the action in the 'review' column of the audit logs.

## Tier: Full
DETAILED USAGE
- './cli manual node get <id>' prints the full dictionary of a knowledge unit.
- './cli manual task add "Task"' bypasses the monitor for immediate entry.
- './cli manual node tag <id> bug,fix' manually appends metadata.

TECHNICAL ARCHITECTURE: MANUAL
=====================================

1. GROUND TRUTH MODIFICATION
----------------------------
Manual acts as the bypass for the reasoning engine.
It uses 'clide/kernel/storage.py' directly to modify the SQLite database.

2. CRUD OPERATIONS
------------------
- NODE: edit, delete, move, get, tag.
- TASK: add, remove, complete, list.
- ASSET: list, archive, delete.

3. STATE SYNCHRONIZATION
------------------------
When a task is 'completed' via manual command, the system:
1. Deletes the row from memory.db.
2. Re-generates 'todo.md' to remove the line.
3. Records the action in the 'review' column of the audit logs.

[EXPANSION PENDING]

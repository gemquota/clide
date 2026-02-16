# MANUAL TASK

## Tier: Basic
- list        : Show all active tasks with IDs.
- add <txt>   : Manual task creation.
- remove <id> : Delete task.
- complete <id>: Mark as done (archives unit).
Usage: ./cli manual task {list, add, remove, complete}

## Tier: More
- list        : Show all active tasks with IDs.
- add <txt>   : Manual task creation.
- remove <id> : Delete task.
- complete <id>: Mark as done (archives unit).
Usage: ./cli manual task {list, add, remove, complete}

TECHNICAL DEEP-DIVE:
The 'task' subcommand manages the 'Operational Horizon'.
1. DB Mapping: Maps directly to nodes where category='TODO'.
2. Side Effects: 'add' and 'complete' trigger a sync to the physical 'todo.md' file.
3. Integrity: 'complete' moves the record to a 'history' status in the review column before deletion from the active set.
4. Orchestration: Used by the user to finalize goals that have been achieved.
Essential for 'Human-in-the-Loop' project governance.

## Tier: Full
- list        : Show all active tasks with IDs.
- add <txt>   : Manual task creation.
- remove <id> : Delete task.
- complete <id>: Mark as done (archives unit).
Usage: ./cli manual task {list, add, remove, complete}

TECHNICAL DEEP-DIVE:
The 'task' subcommand manages the 'Operational Horizon'.
1. DB Mapping: Maps directly to nodes where category='TODO'.
2. Side Effects: 'add' and 'complete' trigger a sync to the physical 'todo.md' file.
3. Integrity: 'complete' moves the record to a 'history' status in the review column before deletion from the active set.
4. Orchestration: Used by the user to finalize goals that have been achieved.
Essential for 'Human-in-the-Loop' project governance.

[EXPANSION PENDING]

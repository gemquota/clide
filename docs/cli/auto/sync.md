# AUTO SYNC

## Tier: Basic
- Ensures that every task in the database is reflected in the markdown file.
- Removes lines from 'todo.md' that have been deleted in SQLite.
- Repairs broken file paths or malformed TODO syntax.
Usage: ./cli auto sync

## Tier: More
- Ensures that every task in the database is reflected in the markdown file.
- Removes lines from 'todo.md' that have been deleted in SQLite.
- Repairs broken file paths or malformed TODO syntax.
Usage: ./cli auto sync

TECHNICAL DEEP-DIVE:
The 'sync' command maintains 'File-to-DB Parity'.
1. DB Truth: Treats SQLite as the primary 'Ground Truth'.
2. File Scan: Reads 'todo.md' and identifies manually added or removed lines.
3. Reconciliation:
   - Missing in File -> Appends to 'todo.md'.
   - Missing in DB -> Proposes ingestion as a new TODO.
4. Validation: Ensures that the 'todo.md' remains readable by humans while being synchronized with agentic state.
The primary mechanism for 'Executive Consistency' across the project.

## Tier: Full
- Ensures that every task in the database is reflected in the markdown file.
- Removes lines from 'todo.md' that have been deleted in SQLite.
- Repairs broken file paths or malformed TODO syntax.
Usage: ./cli auto sync

TECHNICAL DEEP-DIVE:
The 'sync' command maintains 'File-to-DB Parity'.
1. DB Truth: Treats SQLite as the primary 'Ground Truth'.
2. File Scan: Reads 'todo.md' and identifies manually added or removed lines.
3. Reconciliation:
   - Missing in File -> Appends to 'todo.md'.
   - Missing in DB -> Proposes ingestion as a new TODO.
4. Validation: Ensures that the 'todo.md' remains readable by humans while being synchronized with agentic state.
The primary mechanism for 'Executive Consistency' across the project.

[EXPANSION PENDING]

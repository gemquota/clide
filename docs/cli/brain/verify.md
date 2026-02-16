# BRAIN VERIFY

## Tier: Basic
- Checks for broken relationships or orphaned nodes.
- Validates that every entry has a valid 768D embedding.
- Repairs indices in the SQLite 'memory.db'.
Usage: ./cli brain verify

## Tier: More
- Checks for broken relationships or orphaned nodes.
- Validates that every entry has a valid 768D embedding.
- Repairs indices in the SQLite 'memory.db'.
Usage: ./cli brain verify

TECHNICAL DEEP-DIVE:
The 'verify' command is a structural health check.
1. DB Check: Runs 'PRAGMA integrity_check' on the SQLite database.
2. Embedding Validation: Scans the 'embedding' column for nulls or malformed binary blobs.
3. Relationship Sync: Ensures 'source_id' and 'target_id' in the relationship table actually exist in 'knowledge'.
4. Schema Check: Confirms all required SPA columns are present.
Essential for recovering from unexpected process termination or filesystem errors.

## Tier: Full
- Checks for broken relationships or orphaned nodes.
- Validates that every entry has a valid 768D embedding.
- Repairs indices in the SQLite 'memory.db'.
Usage: ./cli brain verify

TECHNICAL DEEP-DIVE:
The 'verify' command is a structural health check.
1. DB Check: Runs 'PRAGMA integrity_check' on the SQLite database.
2. Embedding Validation: Scans the 'embedding' column for nulls or malformed binary blobs.
3. Relationship Sync: Ensures 'source_id' and 'target_id' in the relationship table actually exist in 'knowledge'.
4. Schema Check: Confirms all required SPA columns are present.
Essential for recovering from unexpected process termination or filesystem errors.

[EXPANSION PENDING]

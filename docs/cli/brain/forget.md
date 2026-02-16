# BRAIN FORGET

## Tier: Basic
- Permanently removes a row from 'memory.db'.
- Automatically cleans up any associated relationships.
- Use when a fact was incorrectly classified or is no longer true.
Usage: ./cli brain forget <id>

## Tier: More
- Permanently removes a row from 'memory.db'.
- Automatically cleans up any associated relationships.
- Use when a fact was incorrectly classified or is no longer true.
Usage: ./cli brain forget <id>

TECHNICAL DEEP-DIVE:
The 'forget' command performs a cascaded deletion.
1. Pre-cleanup: Removes all rows in 'relationships' where the ID is source or target.
2. Deletion: Executes 'DELETE FROM knowledge WHERE id = ?'.
3. Index Update: Triggers a sync to the 'vector_registry.json' to remove the stale vector.
4. Logging: Records the deletion event in the system audit log.
The primary tool for 'Knowledge Pruning' and entropy management.

## Tier: Full
- Permanently removes a row from 'memory.db'.
- Automatically cleans up any associated relationships.
- Use when a fact was incorrectly classified or is no longer true.
Usage: ./cli brain forget <id>

TECHNICAL DEEP-DIVE:
The 'forget' command performs a cascaded deletion.
1. Pre-cleanup: Removes all rows in 'relationships' where the ID is source or target.
2. Deletion: Executes 'DELETE FROM knowledge WHERE id = ?'.
3. Index Update: Triggers a sync to the 'vector_registry.json' to remove the stale vector.
4. Logging: Records the deletion event in the system audit log.
The primary tool for 'Knowledge Pruning' and entropy management.

[EXPANSION PENDING]

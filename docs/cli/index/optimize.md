# INDEX OPTIMIZE

- Re-saves the 'vector_registry.json' with optimal sorting and indentation.
- Removes duplicate entries (keeping the latest version).
- Ensures the registry file is clean and readable.
Usage: ./cli index optimize

- Re-saves the 'vector_registry.json' with optimal sorting and indentation.
- Removes duplicate entries (keeping the latest version).
- Ensures the registry file is clean and readable.
Usage: ./cli index optimize

TECHNICAL DEEP-DIVE:
The `optimize` command performs structural maintenance on the Registry file.
1. **Deduplication:** Scans the registry and removes redundant entries sharing the same ID (keeping the most recent).
2. **Sorting:** Re-orders the file by ID to improve deterministic read behavior.
3. **Formatting:** Rewrites the JSON with standard indentation (indent=2) for human readability and git diff clarity.
A 'Housekeeping' command to be run after massive ingestion sessions where duplicates might occur.

- Re-saves the 'vector_registry.json' with optimal sorting and indentation.
- Removes duplicate entries (keeping the latest version).
- Ensures the registry file is clean and readable.
Usage: ./cli index optimize

TECHNICAL DEEP-DIVE:
The `optimize` command is mapped to `clide.brain.memory.optimize_registry`.

### Logic Flow
1. **Load:** Reads the full `vector_registry.json` into memory.
2. **Deduplicate:**
   - Iterates through all items.
   - Uses a dictionary `seen = {}` keyed by `item["id"]` to track uniqueness.
   - Since dictionaries overwrite existing keys, the *last* occurrence of an ID in the list (the latest) is preserved.
3. **Sort:**
   - Converts `seen.values()` back to a list.
   - Sorts the list alphabetically by `id`.
4. **Write:**
   - Dumps the optimized list back to `vector_registry.json` with `indent=2`.
   - Returns the count of removed items (`len(original) - len(optimized)`).

### Code Reference
- **Entry Point:** `clide/serve/portal.py` -> `cmd_index` (optimize)
- **Implementation:** `clide/brain/memory.py` -> `optimize_registry`

# INDEX PRUNE

- Removes low-value entries from the vector registry.
- Targets items with an importance score below 3.
- Helps keep search results relevant and high-quality.
Usage: ./cli index prune

- Removes low-value entries from the vector registry.
- Targets items with an importance score below 3.
- Helps keep search results relevant and high-quality.
Usage: ./cli index prune

TECHNICAL DEEP-DIVE:
The `prune` command performs semantic sanitation.
1. **Filtering:** Iterates through every item in the `vector_registry.json`.
2. **Threshold Check:** Inspects the `metadata.importance` field (defaults to 5 if missing).
3. **Action:** If importance is less than 3, the item is discarded from the registry.
4. **Persistence:** Writes the cleaned list back to disk.

- Removes low-value entries from the vector registry.
- Targets items with an importance score below 3.
- Helps keep search results relevant and high-quality.
Usage: ./cli index prune

TECHNICAL DEEP-DIVE:
The `prune` command is mapped to `clide.brain.memory.prune_registry`.

### Logic Flow
1. **Load:** Reads the `vector_registry.json`.
2. **Scan:** Iterates through the list using a list comprehension:
   `[item for item in registry if item.get('metadata', {}).get('importance', 5) >= min_importance]`
3. **Filter:**
   - Default `min_importance` is **3**.
   - Items without an explicit `importance` key are assumed to be **5** (safe).
4. **Update:**
   - If items were removed, the new list is saved to `vector_registry.json`.
   - Returns the count of pruned items (`initial_count - len(pruned)`).

### Code Reference
- **Entry Point:** `clide/serve/portal.py` -> `cmd_index` (prune)
- **Implementation:** `clide/brain/memory.py` -> `prune_registry`


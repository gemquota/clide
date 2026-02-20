# INDEX STATS

- Displays health metrics for the vector registry.
- Shows total asset count and file size.
- Breaks down the knowledge base by content type.
Usage: ./cli index stats

- Displays health metrics for the vector registry.
- Shows total asset count and file size.
- Breaks down the knowledge base by content type.
Usage: ./cli index stats

TECHNICAL DEEP-DIVE:
The `stats` command provides telemetry on the state of the semantic index.
1. **Volume:** Counts the total number of vectors in `vector_registry.json`.
2. **Storage:** Calculates the file size in KB.
3. **Distribution:** Aggregates counts by `metadata.type` (e.g., SHELL_HISTORY, FACT, TOOL).
4. **Dimensionality:** Confirms the vector width (fixed at 768).

- Displays health metrics for the vector registry.
- Shows total asset count and file size.
- Breaks down the knowledge base by content type.
Usage: ./cli index stats

TECHNICAL DEEP-DIVE:
The `stats` command is mapped to `clide.brain.memory.get_registry_stats`.

### Logic Flow
1. **Read:** Loads `vector_registry.json`. Handles JSON errors or lock contention (though rudimentary).
2. **Compute:**
   - `total_assets`: `len(registry)`
   - `file_size_kb`: `os.path.getsize(path) / 1024`
   - `dimensions`: Hardcoded to **768** (Gemini Embedding 001 standard).
   - `distribution`: Iterates through all items, tallying `item['metadata'].get('type', 'unknown')`.
3. **Render:** Displays a formatted `rich.table.Table` via `cmd_index`.

### Code Reference
- **Entry Point:** `clide/serve/portal.py` -> `cmd_index` (stats)
- **Implementation:** `clide/brain/memory.py` -> `get_registry_stats`


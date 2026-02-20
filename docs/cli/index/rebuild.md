# INDEX REBUILD

- Scans local shell history (`.zsh_history`, `.bash_history`) for command patterns.
- Embeds new unique commands into the vector registry.
- Stores historical commands in the `knowledge` database as `SHELL_HISTORY`.
Usage: ./cli index rebuild

- Scans local shell history (`.zsh_history`, `.bash_history`) for command patterns.
- Embeds new unique commands into the vector registry.
- Stores historical commands in the `knowledge` database as `SHELL_HISTORY`.
Usage: ./cli index rebuild

TECHNICAL DEEP-DIVE:
The `rebuild` command (currently scoped to Shell History ingestion) synchronizes external user activity with the internal knowledge base.
1. **History Scan:** Reads `~/.zsh_history` and `~/.bash_history`, filtering for unique commands > 3 chars.
2. **Deduplication:** Checks against existing `SHELL_HISTORY` entries in the SQLite DB to avoid re-embedding.
3. **Batch Embedding:** Sends new commands to the Gemini API (model: `gemini-embedding-001`) in batches of 50.
4. **Persistence:** Saves vectors to `vector_registry.json` and rows to `knowledge` table.

- Scans local shell history (`.zsh_history`, `.bash_history`) for command patterns.
- Embeds new unique commands into the vector registry.
- Stores historical commands in the `knowledge` database as `SHELL_HISTORY`.
Usage: ./cli index rebuild

TECHNICAL DEEP-DIVE:
The `rebuild` command is mapped to `scripts.batch_indexer.run_full_index`.

### Logic Flow
1. **Harvesting:**
   - Functions `get_shell_history()` parses raw history files, handling timestamps and multiline entries.
   - Filters out duplicates and short commands (< 3 chars).
2. **Delta Check:**
   - Queries `SELECT content FROM knowledge WHERE category='SHELL_HISTORY'` to build a local cache of known commands.
   - Identifies `new_items` = `history - existing`.
3. **Ingestion Loop:**
   - Iterates through `new_items` in batches (default: 50).
   - Calls `memory.get_embeddings(batch)` to generate 768D vectors.
   - Inserts into SQLite with `importance=3` and `category='SHELL_HISTORY'`.
   - Appends to `vector_registry.json` via `memory.add_to_registry_batch`.
4. **Constraints:**
   - Hard limit of 1000 items per run to prevent API rate limits or excessive latency.

### Code Reference
- **Entry Point:** `clide/serve/portal.py` -> `cmd_index` (rebuild)
- **Implementation:** `scripts/batch_indexer.py` -> `run_full_index`

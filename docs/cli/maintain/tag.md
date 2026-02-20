# AUTO TAG

- Scans the database for knowledge units that are currently untagged.
- Automatically generates 3-5 relevant keywords using the LLM.
- Persists tags to the database to improve search discoverability.
Usage: ./cli auto tag

- Scans the database for knowledge units that are currently untagged.
- Automatically generates 3-5 relevant keywords using the LLM.
- Persists tags to the database to improve search discoverability.
Usage: ./cli auto tag

TECHNICAL DEEP-DIVE:
The `tag` command implements 'Automated Metadata Enrichment'.
1. **Selection:** Fetches up to 500 recent nodes and filters for those with an empty `tags` column or no `TAGS:` prefix in the review metadata.
2. **Analysis:** Passes node content to the LLM with a specific categorization request.
3. **Keyword Generation:** LLM generates 3-5 project-relevant keywords.
4. **Update:** Persists the keywords as a JSON-encoded list in the SQLite `tags` column.

- Scans the database for knowledge units that are currently untagged.
- Automatically generates 3-5 relevant keywords using the LLM.
- Persists tags to the database to improve search discoverability.
Usage: ./cli auto tag

TECHNICAL DEEP-DIVE:
The `tag` command is implemented in `clide.brain.auto.auto_tag_nodes`.

### Logic Flow
1. **Filtering:** Iterates through the result of `storage.get_knowledge(limit=500)`. It checks both the dedicated `tags` column and legacy `review` metadata for existing tags.
2. **Batch Processing:**
   - For each untagged node, it constructs a prompt: "Analyze... and provide 3-5 succinct tags as a comma-separated list."
   - Uses `rich.progress` to provide real-time TUI feedback.
3. **Data Sanitization:**
   - Attempts to parse LLM output as a comma-separated list or JSON array.
   - Calls `storage.update_knowledge(id, tags=tags_list)` to commit changes.

### Code Reference
- **Entry Point:** `clide/serve/portal.py` -> `cmd_maintain`
- **Implementation:** `clide/brain/auto.py` -> `auto_tag_nodes`

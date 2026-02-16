# AUTO TAG

## Tier: Basic
- Scans 'memory.db' for units where 'review' is empty or untagged.
- Uses the LLM to generate 3-5 keywords for each unit.
- Improves the accuracy of semantic search and clustering.
Usage: ./cli auto tag

## Tier: More
- Scans 'memory.db' for units where 'review' is empty or untagged.
- Uses the LLM to generate 3-5 keywords for each unit.
- Improves the accuracy of semantic search and clustering.
Usage: ./cli auto tag

TECHNICAL DEEP-DIVE:
The 'tag' command implements 'Automated Metadata Enrichment'.
1. Selection: Fetches the last 50 entries with no 'TAGS:' string in the review column.
2. Context: Passes the content of each entry to 'gemini-2.0-flash'.
3. Prompting: Asks for succinct, project-relevant keywords.
4. Update: Executes 'storage.update_node_tags' to persist the findings.
This significantly reduces the 'Manual Management' debt required to keep a clean project brain.

## Tier: Full
- Scans 'memory.db' for units where 'review' is empty or untagged.
- Uses the LLM to generate 3-5 keywords for each unit.
- Improves the accuracy of semantic search and clustering.
Usage: ./cli auto tag

TECHNICAL DEEP-DIVE:
The 'tag' command implements 'Automated Metadata Enrichment'.
1. Selection: Fetches the last 50 entries with no 'TAGS:' string in the review column.
2. Context: Passes the content of each entry to 'gemini-2.0-flash'.
3. Prompting: Asks for succinct, project-relevant keywords.
4. Update: Executes 'storage.update_node_tags' to persist the findings.
This significantly reduces the 'Manual Management' debt required to keep a clean project brain.

[EXPANSION PENDING]

# INDEX TRACE

## Tier: Basic
- Explains *why* a vector exists and what data it was derived from.
- Shows the raw 768D coordinates (truncated for display).
- Lists the timestamp and source session of the original ingestion.
Usage: ./cli index trace <id>

## Tier: More
- Explains *why* a vector exists and what data it was derived from.
- Shows the raw 768D coordinates (truncated for display).
- Lists the timestamp and source session of the original ingestion.
Usage: ./cli index trace <id>

TECHNICAL DEEP-DIVE:
The 'trace' command provides 'Semantic Transparency'.
1. Map: Joins the 'vector_registry.json' entry with its SQLite 'knowledge' row.
2. Analytics: Displays the importance weight and how it affected the vector's ranking.
3. Verification: Confirms that the embedding on disk matches the content in the DB.
4. Debugging: Shows the full 'clide_metadata' block from 'enriched_logs.json'.
Essential for auditing the 'Cognitive Pipeline' and understanding model behavior.

## Tier: Full
- Explains *why* a vector exists and what data it was derived from.
- Shows the raw 768D coordinates (truncated for display).
- Lists the timestamp and source session of the original ingestion.
Usage: ./cli index trace <id>

TECHNICAL DEEP-DIVE:
The 'trace' command provides 'Semantic Transparency'.
1. Map: Joins the 'vector_registry.json' entry with its SQLite 'knowledge' row.
2. Analytics: Displays the importance weight and how it affected the vector's ranking.
3. Verification: Confirms that the embedding on disk matches the content in the DB.
4. Debugging: Shows the full 'clide_metadata' block from 'enriched_logs.json'.
Essential for auditing the 'Cognitive Pipeline' and understanding model behavior.

[EXPANSION PENDING]

# INDEX FULL

## Tier: Basic
- Re-reads every entry in 'memory.db' and the 'swarm/' directory.
- Re-generates all vectors using models/gemini-embedding-001.
- Required after upgrading the dimensionality or model version.
Usage: ./cli index full

## Tier: More
- Re-reads every entry in 'memory.db' and the 'swarm/' directory.
- Re-generates all vectors using models/gemini-embedding-001.
- Required after upgrading the dimensionality or model version.
Usage: ./cli index full

TECHNICAL DEEP-DIVE:
The 'full' command is a resource-intensive re-synchronization.
1. Clear Phase: Truncates 'vector_registry.json' to ensure a clean start.
2. Scan Phase: Iterates through all SQLite nodes and TOML/Python assets.
3. Batch Embedding: Sends text blocks to the Gemini SDK in batches of 10 to optimize latency.
4. Persistence: Writes the new 768D registry to disk and validates the file structure.
Essential for maintaining 'Semantic Accuracy' after logic or architectural changes.

## Tier: Full
- Re-reads every entry in 'memory.db' and the 'swarm/' directory.
- Re-generates all vectors using models/gemini-embedding-001.
- Required after upgrading the dimensionality or model version.
Usage: ./cli index full

TECHNICAL DEEP-DIVE:
The 'full' command is a resource-intensive re-synchronization.
1. Clear Phase: Truncates 'vector_registry.json' to ensure a clean start.
2. Scan Phase: Iterates through all SQLite nodes and TOML/Python assets.
3. Batch Embedding: Sends text blocks to the Gemini SDK in batches of 10 to optimize latency.
4. Persistence: Writes the new 768D registry to disk and validates the file structure.
Essential for maintaining 'Semantic Accuracy' after logic or architectural changes.

[EXPANSION PENDING]

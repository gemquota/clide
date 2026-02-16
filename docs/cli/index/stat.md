# INDEX STAT

## Tier: Basic
- Reports the total number of registered 768D vectors.
- Shows file size of 'vector_registry.json'.
- Displays the current embedding model being used.
Usage: ./cli index stat

## Tier: More
- Reports the total number of registered 768D vectors.
- Shows file size of 'vector_registry.json'.
- Displays the current embedding model being used.
Usage: ./cli index stat

TECHNICAL DEEP-DIVE:
The 'stat' command provides 'Telemetry' for the Index domain.
1. Counting: Counts assets by type (AGENT, SKILL, MCP, FACT).
2. Sizing: Calculates average vector size and total disk footprint.
3. Health: Reports the 'Density Ratio' (Relationships per Node).
4. Information: Lists environment variables affecting the index (e.g. GEMINI_API_KEY presence).
Provides the data needed to decide when a 'full' re-index or 'prune' is required.

## Tier: Full
- Reports the total number of registered 768D vectors.
- Shows file size of 'vector_registry.json'.
- Displays the current embedding model being used.
Usage: ./cli index stat

TECHNICAL DEEP-DIVE:
The 'stat' command provides 'Telemetry' for the Index domain.
1. Counting: Counts assets by type (AGENT, SKILL, MCP, FACT).
2. Sizing: Calculates average vector size and total disk footprint.
3. Health: Reports the 'Density Ratio' (Relationships per Node).
4. Information: Lists environment variables affecting the index (e.g. GEMINI_API_KEY presence).
Provides the data needed to decide when a 'full' re-index or 'prune' is required.

[EXPANSION PENDING]

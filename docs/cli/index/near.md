# INDEX NEAR

## Tier: Basic
- Identifies the 5 closest neighbors using vector similarity.
- Returns IDs and similarity scores (0.0 to 1.0).
- Useful for detecting redundant tools or related project facts.
Usage: ./cli index near <id>

## Tier: More
- Identifies the 5 closest neighbors using vector similarity.
- Returns IDs and similarity scores (0.0 to 1.0).
- Useful for detecting redundant tools or related project facts.
Usage: ./cli index near <id>

TECHNICAL DEEP-DIVE:
The 'near' command performs a 'K-Nearest Neighbor' scan.
1. Vector Retrieval: Fetches the 768D embedding for the target ID from the registry.
2. Comparison: Calculates Cosine Similarity against all other entries.
3. Sorting: Sorts the entire registry by similarity delta.
4. Output: Displays the top matches, highlighting those above the 0.85 auto-activation threshold.
This command is the 'Discovery Engine' for identifying internal project patterns.

## Tier: Full
- Identifies the 5 closest neighbors using vector similarity.
- Returns IDs and similarity scores (0.0 to 1.0).
- Useful for detecting redundant tools or related project facts.
Usage: ./cli index near <id>

TECHNICAL DEEP-DIVE:
The 'near' command performs a 'K-Nearest Neighbor' scan.
1. Vector Retrieval: Fetches the 768D embedding for the target ID from the registry.
2. Comparison: Calculates Cosine Similarity against all other entries.
3. Sorting: Sorts the entire registry by similarity delta.
4. Output: Displays the top matches, highlighting those above the 0.85 auto-activation threshold.
This command is the 'Discovery Engine' for identifying internal project patterns.

[EXPANSION PENDING]

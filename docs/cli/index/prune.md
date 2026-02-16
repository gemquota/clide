# INDEX PRUNE

## Tier: Basic
- Flags entries with very low similarity to the rest of the project.
- Identifies virtual duplicates (Similarity > 0.98) for merging.
- Keeps the 768D space clean and high-performance.
Usage: ./cli index prune

## Tier: More
- Flags entries with very low similarity to the rest of the project.
- Identifies virtual duplicates (Similarity > 0.98) for merging.
- Keeps the 768D space clean and high-performance.
Usage: ./cli index prune

TECHNICAL DEEP-DIVE:
The 'prune' command is the 'Garbage Collector' of the semantic registry.
1. Redundancy Scan: Performs an N-to-N comparison of all vectors.
2. Entropy Check: Detects nodes with 'Noise' content (one-word entries, malformed text).
3. Proposal: Lists candidates for deletion and asks for manual 'manual' confirmation.
4. Cleanup: Removes the vectors and updates the 'vector_registry.json' hash.
Essential for preventing 'Contextual Bloat' and keeping search latency low.

## Tier: Full
- Flags entries with very low similarity to the rest of the project.
- Identifies virtual duplicates (Similarity > 0.98) for merging.
- Keeps the 768D space clean and high-performance.
Usage: ./cli index prune

TECHNICAL DEEP-DIVE:
The 'prune' command is the 'Garbage Collector' of the semantic registry.
1. Redundancy Scan: Performs an N-to-N comparison of all vectors.
2. Entropy Check: Detects nodes with 'Noise' content (one-word entries, malformed text).
3. Proposal: Lists candidates for deletion and asks for manual 'manual' confirmation.
4. Cleanup: Removes the vectors and updates the 'vector_registry.json' hash.
Essential for preventing 'Contextual Bloat' and keeping search latency low.

[EXPANSION PENDING]

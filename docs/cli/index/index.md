# CLIDE // INDEX DOMAIN

## Tier: Basic
DETAILED USAGE
- './cli index full' is required after upgrading to 768D vectors.
- './cli index near <id>' helps identify candidates for merging or deduplication.
- './cli index stat' provides metadata on registry health and storage size.

## Tier: More
DETAILED USAGE
- './cli index full' is required after upgrading to 768D vectors.
- './cli index near <id>' helps identify candidates for merging or deduplication.
- './cli index stat' provides metadata on registry health and storage size.

TECHNICAL ARCHITECTURE: INDEX
====================================

1. VECTORIZATION (memory.py)
----------------------------
Uses 'models/gemini-embedding-001' to create semantic anchors.
- Dimensionality: Exactly 768 (Full resolution).
- Normality: Vectors are normalized before Cosine Similarity calculation.

2. SEARCH ENGINE
----------------
Performs a flat-file scan of 'vector_registry.json' using optimized Python math.
- Logic: dot_product(v1, v2) / (norm(v1) * norm(v2)).
- Performance: Registry is kept in JSON for portability but cached in memory during search.

3. OPTIMIZATION (tools/janitor.py)
----------------------------------
- Clustering: Identifies semantic 'hotspots' using nearest-neighbor logic.
- Pruning: Evicts vectors with low confidence or redundant content.
- Deduplication: Merges overlapping assets created by the Forge.

## Tier: Full
DETAILED USAGE
- './cli index full' is required after upgrading to 768D vectors.
- './cli index near <id>' helps identify candidates for merging or deduplication.
- './cli index stat' provides metadata on registry health and storage size.

TECHNICAL ARCHITECTURE: INDEX
====================================

1. VECTORIZATION (memory.py)
----------------------------
Uses 'models/gemini-embedding-001' to create semantic anchors.
- Dimensionality: Exactly 768 (Full resolution).
- Normality: Vectors are normalized before Cosine Similarity calculation.

2. SEARCH ENGINE
----------------
Performs a flat-file scan of 'vector_registry.json' using optimized Python math.
- Logic: dot_product(v1, v2) / (norm(v1) * norm(v2)).
- Performance: Registry is kept in JSON for portability but cached in memory during search.

3. OPTIMIZATION (tools/janitor.py)
----------------------------------
- Clustering: Identifies semantic 'hotspots' using nearest-neighbor logic.
- Pruning: Evicts vectors with low confidence or redundant content.
- Deduplication: Merges overlapping assets created by the Forge.

[EXPANSION PENDING]

# BRAIN // ANALYZE
Initiates deep semantic analysis of the current knowledge base.

Scans recent knowledge nodes to identify hidden patterns, cross-sector dependencies, and thematic clusters.

<card>
title: ⦗ DEEP ANALYSIS ⦘
Target: Recent Nodes (100)
Method: Semantic Clustering
Output: Relationship Index
</card>

### Usage
`./cli brain analyze`

### Technical Details
Fetches the latest 100 nodes and performs a cosine-similarity matrix calculation to find related concepts that are not explicitly linked.

<card>
title: ⦗ ANALYSIS PIPELINE ⦘
1. Fetch Vectors
2. Compute Similarity
3. Cluster (DBSCAN)
4. Update Metadata
</card>

### Code Internals
Calls `atlas.run_deep_analysis()`. Utilizes `clide.brain.memory.search_registry` for vector operations.
# [ SECTOR 02: COGNITIVE ] - INDEX
Vector lifecycle management, indexing telemetry, and registry optimization.

The `index` domain manages the health and performance of the vector registry.

<card>
title: INDEX OVERVIEW
Lifecycle: Rebuild, Cluster, Prune
Telemetry: Volume, Dimension
Integrity: Self-Optimizing
Status: HEALTHY
</card>

### Commands
*   **rebuild**: Performs a total rebuild of the vector registry using latest models.
*   **cluster**: Identifies knowledge hotspots and topical clusters.
*   **prune**: Evicts low-importance nodes from the registry.
*   **optimize**: Deduplicates entries and performs ID hot-swapping.
*   **stats**: Displays system telemetry and dimensionality metrics.

### Technical Specifications
Indexing operations are heavy and should be run during maintenance cycles.

<card>
title: OPERATIONAL CONTEXT
Model: Gemini-001 (Legacy) / text-embedding-004 (Current)
Clustering: K-Means / DBSCAN
Importance Threshold: 3 (Pruning)
</card>

### Usage Examples
1. System Stats: `./cli index stats`
2. Optimization: `./cli index optimize`
3. Rebuild (Long): `./cli index rebuild`

### Dependency Notes
Requires significant CPU/GPU resources for local rebuilds. Gemini API is used for cloud rebuilds.

### Architecture Internals
The index lifecycle is managed in `memory.py`. Optimization involves re-syncing the `SQLite` metadata with the `JSON` vector buffers.

<card>
title: NEURAL-KERNEL HOOKS
Rebuild Hook: scripts.batch_indexer.run_full_index
Cluster Hook: clide.brain.memory.cluster_registry
Optimize Hook: clide.brain.memory.optimize_registry
</card>

### API Hooks
*   `memory.get_registry_stats()`: Core telemetry source.
*   `memory.prune_registry(min_importance)`: Registry sanitation.

### Legacy Notes
`indexstats` was formerly a root-level script. It is now fully integrated into the `index` domain.
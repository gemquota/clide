# INDEX CLUSTER

- Automatically identifies themes in your project (e.g. 'Database', 'Frontend', 'Tests').
- Uses vector similarity to group related commands and knowledge.
- Helps visualize the 'Semantic Breadth' of your current knowledge base.
Usage: ./cli index cluster

- Automatically identifies themes in your project (e.g. 'Database', 'Frontend', 'Tests').
- Uses vector similarity to group related commands and knowledge.
- Helps visualize the 'Semantic Breadth' of your current knowledge base.
Usage: ./cli index cluster

TECHNICAL DEEP-DIVE:
The `cluster` command implements a greedy Leader Algorithm for semantic grouping.
1. **Normalization:** Standardizes all 768D vectors for cosine distance calculation.
2. **Leader Selection:** Iterates through unassigned vectors, designating the first encountered as a cluster centroid.
3. **Assignment:** Finds all unassigned vectors within a similarity threshold (default: 0.85) and assigns them to the current leader.
4. **Output:** Displays the top clusters, their size, and a sample description (centroid description).
Provides a high-level 'Conceptual Map' of the entire project repository.

- Automatically identifies themes in your project (e.g. 'Database', 'Frontend', 'Tests').
- Uses vector similarity to group related commands and knowledge.
- Helps visualize the 'Semantic Breadth' of your current knowledge base.
Usage: ./cli index cluster

TECHNICAL DEEP-DIVE:
The `cluster` command is mapped to `clide.brain.memory.cluster_registry`.

### Logic Flow
1. **Vector Preparation:**
   - Loads `vector_registry.json`.
   - Extracts 768D embeddings and normalizes them (L2 Norm) using `numpy`.
   - Handles dimensionality mismatch by truncating or padding to 768 dimensions.
2. **Algorithm (Leader):**
   - Iterates through the dataset. If a vector is unassigned, it becomes a new **Leader**.
   - Computes dot product (Cosine Similarity) against all other vectors.
   - Assigns any vector with similarity > `threshold` (0.85) to this leader's cluster.
   - Marks members as `assigned` to prevent them from becoming leaders or joining other clusters (Strict Partitioning).
3. **Sorting:**
   - Returns clusters sorted by `size` (descending).

### Code Reference
- **Entry Point:** `clide/serve/portal.py` -> `cmd_index` (cluster)
- **Implementation:** `clide/brain/memory.py` -> `cluster_registry`
- **Dependencies:** `numpy` (required for matrix operations).

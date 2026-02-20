# SEARCH // SEMANTIC RETRIEVAL

The `search` command provides the primary interface for manual knowledge retrieval, utilizing high-order semantic embeddings to find relevant information even when exact keywords are missing.

### Semantic Search Engine
Unlike traditional keyword search, CLIDE's search engine understands the *meaning* behind your query. It converts your text into a 768D vector and identifies the closest neighbors in the project's knowledge base.

<card>
title: SEARCH TELEMETRY
Algorithm: Cosine Similarity
Dimensions: 768D (Gemini v1)
Precision: Semantic-Aware
Latency: ~150ms (API Dependent)
</card>

### Usage
`./cli search "your search query"`

### Technical Specifications
The system leverages the **Gemini Embedding API** to vectorize incoming queries in real-time. The resulting vector is compared against the `vector_registry.json` cache using a flat k-NN scan.

<card>
title: OPERATIONAL CONTEXT
Primary Model: models/gemini-embedding-001
Threshold: 0.75 (Auto-Activation)
Storage: Flat JSON Vector Buffers
</card>

### Usage Examples
1.  **Concept Search**: `./cli search "what are the core design principles?"`
2.  **Technical Search**: `./cli search "how is the sqlite database structured"`
3.  **Command Discovery**: `./cli search "how do I archive a tool?"`

### Architecture Internals
The search pipeline is managed in `clide.brain.memory.search_registry`.

#### Logic Flow
1.  **Vectorization**: The query string is sent to `memory.get_embedding(query)`.
2.  **Comparison**: The system iterates through the registry, calculating the **Cosine Similarity** between the query vector and every stored node.
3.  **Ranking**: Results are sorted by similarity score (1.0 is a perfect match).
4.  **Display**: Returns the top `N` results (default: 3) with their similarity scores and node IDs.

### Code Reference
- **Entry Point**: `clide/serve/portal.py` -> `cmd_search`
- **Implementation**: `clide/brain/memory.py` -> `search_registry`
- **Math**: `clide/brain/memory.py` -> `cosine_similarity`
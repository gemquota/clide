# Technical Debt & Observations

## 1. Vector Search Performance
The linear scan of `vector_registry.json` is O(N).
- **Impact**: Negligible for <1000 assets.
- **Refactor**: Migrate to a specialized index (SQLite-vec or FAISS) for v1.0.

## 2. Insecure Logic Injection
`mcp_generator.py` injects raw shell logic from history into Python files.
- **Impact**: High risk of RCE if malicious commands are "accepted" by the user.
- **Mitigation**: Partially addressed in v0.6.0 via `security_auditor.py`, which performs a pre-synthesis risk assessment. Needs further "runtime" sandboxing.

## 3. Embedding Consistency
Prompt-based embeddings are non-deterministic and low-dimensional.
- **Impact**: Semantic search might be inaccurate.
- **Refactor**: Use a standard embedding model (e.g., `text-embedding-004`).

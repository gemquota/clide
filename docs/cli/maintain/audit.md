# MAINTAIN // AUDIT

Searches for 'semantic collisions' (near-duplicate knowledge) in the registry and resolves them through synthesis.

## Usage
`./cli maintain audit [--threshold T]`

## Description
This command uses vector similarity to detect nodes that are semantically near-duplicates. When a collision is detected, the system:
1. Reports the overlapping IDs.
2. Synthesizes a new "Master Node" using the LLM to preserve all unique facts.
3. Redirects relationships to the master node and prunes the redundant units.

## Arguments
- `--threshold T`: Similarity threshold for detection (default: 0.95). 
- **Safety Cap**: The threshold cannot be set lower than **0.80** to prevent over-aggressive merging.

<card>
Title: AUDIT PARAMETERS
Default Threshold: 0.95 (Near-Exact)
Minimum Threshold: 0.80 (Strongly Related)
Engine: clide.brain.auto.auto_audit_brain
</card>

### Technical Deep-Dive
1. **Loading**: Fetches knowledge units and decodes their semantic embeddings.
2. **Analysis**: Calculates **Cosine Similarity** between node pairs.
3. **Detection**: Any pair exceeding the threshold is flagged for merging.
4. **Resolution**: Merges content via `merge_knowledge_nodes` and updates relationship lineage.

### Code Reference
- **Entry Point**: `clide/serve/portal.py` -> `cmd_maintain`
- **Implementation**: `clide/brain/auto.py` -> `auto_audit_brain`
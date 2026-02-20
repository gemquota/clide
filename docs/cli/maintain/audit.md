# MAINTAIN AUDIT

- Searches for 'semantic collisions' (near-duplicate knowledge) in the registry.
- Uses vector similarity to detect nodes that are > 95% identical.
- Reports anomalies for manual review or automated merging.
Usage: ./cli maintain audit

- Searches for 'semantic collisions' (near-duplicate knowledge) in the registry.
- Uses vector similarity to detect nodes that are > 95% identical.
- Reports anomalies for manual review or automated merging.
Usage: ./cli maintain audit

TECHNICAL DEEP-DIVE:
The `audit` command is implemented in `clide.brain.auto.auto_audit_brain`.

### Logic Flow
1. **Loading**: Fetches up to 500 recent nodes and decodes their JSON embeddings.
2. **Analysis**:
   - Performs an $O(N^2)$ comparison across the selection (or optimized subset).
   - Calculates **Cosine Similarity** between every pair of nodes.
3. **Detection**:
   - Threshold: **0.95**. Any pair exceeding this is marked as an "anomaly".
4. **Reporting**: Prints node IDs and categories for detected duplicates to the TUI.

### Code Reference
- **Entry Point**: `clide/serve/portal.py` -> `cmd_maintain`
- **Implementation**: `clide/brain/auto.py` -> `auto_audit_brain`

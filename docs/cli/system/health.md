# SYSTEM HEALTH

- Displays standardized ingestion telemetry and kernel health metrics.
- Provides visibility into the success/failure rates of sensory ingestion.
- Summarizes the 'Knowledge Yield' of the current knowledge base.
Usage: ./cli system health

TECHNICAL DEEP-DIVE:
The `health` command is an alias for the ingestion reporting suite.

### Logic Flow
1. **Reporting**: Invokes `scripts.ingestion_stats.show_ingestion_stats()`.
2. **Analysis**: Scans the `ingestion_logs` and `memory.db` to calculate throughput and accuracy.
3. **Display**: Renders a TUI-based report showing the system's operational efficacy.

### Code Reference
- **Implementation**: `scripts/ingestion_stats.py` -> `show_ingestion_stats`

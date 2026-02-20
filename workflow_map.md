# CLIDE Data Ingestion Workflows

Standardized sequences for feeding and maintaining the CLIDE knowledge engine.

## 1. The Feed (Knowledge Intake)
**Purpose**: Primary path for moving raw data into indexed knowledge.
```bash
./cli probe scout <URL>  # or probe ingest <PATH>
./cli maintain clean     # Sanitize metadata
./cli maintain tag       # Generate tags with progress bar
./cli index optimize     # Remove duplicates
./cli index rebuild      # Sync vector registry
```

## 2. The Panopticon (Continuous Monitoring)
**Purpose**: Real-time project monitoring and automated log analysis.
```bash
./cli watch start        # Start the monitor
./cli watch logs --tail  # View incoming data
./cli maintain audit     # Scan logs for anomalies
```

## 3. The Archeologist (Knowledge Introspection)
**Purpose**: Identifying patterns in existing data.
```bash
./cli memory merge       # Consolidate fragmented history
./cli index cluster      # Group related nodes
./cli map graph          # Visualize relationships
```

## 4. The Janitor (System Hygiene)
**Purpose**: Deep cleaning and pruning of the registry.
```bash
./cli maintain audit     # Identify collisions
./cli index prune        # Remove low-importance nodes
./cli maintain clean     # Final sanitize pass
```

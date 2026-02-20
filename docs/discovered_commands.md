# DISCOVERED COMMANDS & GAP ANALYSIS

**Date:** 2026-02-18
**Status:** PHASE 1 COMPLETE
**Scope:** Static Analysis of `clide/serve/portal.py` and `scripts/`.

## 1. Discovered Command Registry (Current State)

The following commands are currently implemented in `clide/serve/portal.py`.

### [SECTOR 01: SENSORY]
| Command | Subcommand | Status | Logic Handler | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **watch** | `start` | ✅ Active | `clide.watch.stream.ClideExtractor` | |
| | `stop` | ✅ Active | `clide.watch.stream.stop_monitor` | |
| | `status` | ✅ Active | `clide.watch.stream.get_monitor_status` | |
| | `logs` | ✅ Active | `clide.watch.stream.tail_logs` | Args: `--tail`, `--limit` |
| **probe** | `scout` | ✅ Active | `clide.probe.scout.scout_url` | Args: `url` |
| | `ingest` | ✅ Active | `clide.probe.manual.extract_from_file` | Args: `path` |
| | `capture` | ⚠️ Pending | `print(...)` | Logic not implemented. |
| | `crawl` | ✅ Active | `clide.probe.crawl.crawl_site` | Args: `url`, `--depth` |

### [SECTOR 02: COGNITIVE]
| Command | Subcommand | Status | Logic Handler | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **search** | *(root)* | ✅ Active | `clide.brain.memory.search_registry` | Positional query. |
| **brain** | `analyze` | ✅ Active | `clide.serve.atlas.run_deep_analysis` | |
| | `summary` | ✅ Active | `clide.serve.atlas.generate_brain_summary` | |
| | `verify` | ✅ Active | `clide.serve.atlas.verify_facts` | |
| **map** | `graph` | ✅ Active | `clide.serve.atlas.generate_mermaid_graph` | Exports to `docs/brain_graph.mmd`. |
| | `cloud` | ✅ Active | `scripts.command_cloud` | Args: `--live`, `--html`. |
| | `trace` | ✅ Active | `clide.serve.atlas.trace_provenance` | Args: `id`. |
| **index** | `rebuild` | ✅ Active | `scripts.batch_indexer.run_full_index` | |
| | `cluster` | ✅ Active | `clide.brain.memory.cluster_registry` | |
| | `prune` | ✅ Active | `clide.brain.memory.prune_registry` | |
| | `optimize` | ✅ Active | `clide.brain.memory.optimize_registry` | |
| | `stats` | ✅ Active | `clide.brain.memory.get_registry_stats` | Uses `rich.table`. |

### [SECTOR 03: STATE]
| Command | Subcommand | Status | Logic Handler | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **memory** | `list` | ✅ Active | `clide.serve.atlas.list_brain_units` | |
| | `create` | ✅ Active | `clide.kernel.storage.save_knowledge` | |
| | `edit` | ✅ Active | `clide.kernel.storage.update_knowledge` | |
| | `delete` | ✅ Active | `clide.kernel.storage.delete_knowledge` | Soft delete. |
| | `connect` | ✅ Active | `clide.kernel.storage.add_relationship` | |
| | `merge` | ✅ Active | `scripts.merge_logs.run_log_merge` | |
| | `forget` | ✅ Active | `clide.kernel.storage.delete_knowledge` | Hard delete. |
| **run** | `plan` | ✅ Active | `clide.brain.auto.auto_prioritize_tasks` | |
| | `task` | ✅ Active | `clide.tools.janitor.TodoManager` | Ops: list, add, remove, complete. |
| | `sync` | ✅ Active | `clide.brain.auto.auto_sync_todos` | |
| **maintain**| `tag` | ✅ Active | `clide.brain.auto.auto_tag_nodes` | |
| | `clean` | ✅ Active | `clide.brain.auto.auto_clean_metadata` | |
| | `audit` | ✅ Active | `clide.brain.auto.auto_audit_brain` | |

### [SECTOR 04: EXECUTIVE]
| Command | Subcommand | Status | Logic Handler | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **forge** | `tool` | ✅ Active | `clide.forge.master.process_tool_request`| |
| | `evolve` | ✅ Active | `clide.forge.master.evolve_tool` | |
| | `design` | ✅ Active | `clide.forge.master.generate_design` | |
| | `skill` | ✅ Active | `clide.forge.master.create_skill` | |
| | `persona` | ✅ Active | `clide.forge.master.define_persona` | |
| | `test` | ✅ Active | `clide.forge.master.run_tests` | |
| | `bench` | ✅ Active | `clide.forge.master.run_benchmark` | |
| | `archive` | ✅ Active | `clide.forge.master.archive_asset` | |
| **system** | `dash` | ✅ Active | `clide.serve.dashboard.run_dashboard` | |
| | `status` | ⚠️ Duplicate | `scripts.ingestion_stats` | Duplicate of `health`. |
| | `config` | ✅ Active | `clide.kernel.settings.load_config` | |
| | `asset` | ✅ Active | `clide.brain.memory.get_registry_stats` | |
| | `health` | ✅ Active | `scripts.ingestion_stats` | |
| | `backup` | ✅ Active | `shutil.copy2` | |

## 2. Gap Analysis (vs Atlas Registry)

### Alignment Status
The current CLI implementation is **98% Aligned** with the Atlas Command Registry. The structure of Sectors (Sensory, Cognitive, State, Executive) and their commands is already in place.

### Discrepancies
1.  **`probe capture`**: Defined but pending implementation.
2.  **`system status`**: This command exists in `portal.py` but is not in the Atlas Registry (which uses `health`). It appears to be a duplicate alias for `health`.
3.  **`system asset`**: Uses `memory.get_registry_stats` which duplicates logic from `index stats` but presents it differently (inventory vs metrics).

### Structural Integrity
- **Logic Mapping**: All commands map to modular files in `clide/` or `scripts/`.
- **Arguments**: Argument parsing matches the functional requirements.

## 3. Recommendations (Phase 2)
1.  **Deprecate `system status`**: Remove or alias explicitly to `health` in the help docs.
2.  **Refine `system asset`**: Ensure it provides distinct value from `index stats` or merge them.
3.  **Implement `probe capture`**: Connect to `termux-clipboard-get` or similar mechanism.
4.  **Verification**: The system is ready for Phase 3 (Documentation) as the underlying logic is stable.

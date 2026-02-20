# [ SECTOR 04: EXECUTIVE ] - SYSTEM
Core kernel operations and high-level dashboard management.

The `system` domain provides access to kernel settings, backups, and status dashboards.

<card>
title: SYSTEM OVERVIEW
Dashboard: Neural TUI
Ops: Config, Asset, Backup
Telemetry: Health Metrics
Status: STABLE
</card>

### Commands
*   **dash**: Launches the high-fidelity Neural TUI Dashboard.
*   **config**: Manages kernel settings and configuration parameters.
*   **asset**: Displays an inventory of all registered assets and dimensions.
*   **health**: Displays standardized ingestion and kernel telemetry.
*   **backup**: Creates a full-state snapshot of the database.

### Technical Specifications
System operations are critical for kernel stability and disaster recovery.

<card>
title: OPERATIONAL CONTEXT
Dashboard: rich-tui / custom
Asset Registry: clide/brain/memory.py
Backup Path: clide/backups/
</card>

### Architecture Internals
System tasks are high-privilege operations handled in `portal.py` and `settings.py`.

<card>
title: NEURAL-KERNEL HOOKS
Dash Hook: clide.serve.dashboard.run_dashboard
Config Hook: clide.kernel.settings.load_config
Asset Hook: clide.brain.memory.get_registry_stats
Backup Hook: shutil.copy2 (Database Snapshot)
</card>

### API Reference
*   `ingestion_stats.show_ingestion_stats()`: Primary health source.
*   `dashboard.run_dashboard()`: Entry point for visual TUI.
*   `load_config()`: Configuration loader.

### Code Reference
- **Entry Point**: `clide/serve/portal.py` -> `cmd_system`
- **Settings**: `clide/kernel/settings.py`
- **Stats**: `scripts/ingestion_stats.py`
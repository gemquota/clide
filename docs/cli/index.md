# INTELLIGENCE PORTAL // CLIDE KOS

Welcome to the **CLIDE Knowledge Operating System**.
This documentation is rendered dynamically from the project's SSoT (Single Source of Truth) in `docs/cli/`.

<card>
title: ⦗ SYSTEM STATUS ⦘
Kernel: v1.0.0
Architecture: 768D Vector Registry
Sectors: Sensory, Cognitive, State, Executive
Status: OPERATIONAL
Uptime: 99.9%
</card>

### Basic Navigation
*   **Help**: `./cli help [domain] [command]`
*   **Atlas**: `./cli atlas [domain]` (Visual map)
*   **Search**: `./cli search "query"` (Semantic retrieval)

### Operational Context
The CLIDE ecosystem operates on a **Cyclical Intelligence Model**. Data flows from Sensory inputs, through Cognitive processing, into State persistence, and is acted upon by Executive agents.

```text
╭─── [ SENSORY ] ───╮       ╭── [ COGNITIVE ] ──╮
│  Watch  /  Probe  │ ────► │  Brain  /  Map    │
╰─────────┬─────────╯       ╰─────────┬─────────╯
          │                           │
          ▼                           ▼
╭─── [ EXECUTIVE ] ──╮      ╭──── [ STATE ] ────╮
│  Forge  /  System  │ ◄─── │  Memory /  Run    │
╰────────────────────╯      ╰───────────────────╯
```

### Neural-Kernel Deep-Dive
The CLIDE kernel is a documentation-driven interceptor. Commands are parsed via `portal.py` and documentation is extracted via `guide.py` to provide comprehensive context-aware information.

<card>
title: ⦗ KERNEL SPECIFICATIONS ⦘
Core Language: Python 3.12
UI Framework: Rich / Art
Database: SQLite (Memory) + Vector Registry (JSON)
AI Integration: Gemini-1.5-Pro / Gemini-2.0-Flash
Telemetry: ▅ ▆ ▇ █ ▇ ▆ ▅ ▄ (Simulated)
</card>

### Extensibility
Developers can add new capabilities by:
1.  Adding logic to `clide/` sectors.
2.  Registering the command in `portal.py`.
3.  Creating a corresponding `.md` file in `docs/cli/`.

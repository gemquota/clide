# CLIDE ATLAS

This document provides a comprehensive reference for the CLIDE (Command Line Interface - Database: Everything) command-line utility.

## Usage
```bash
./clide <command> [arguments]
```

## [ SECTOR 01: SENSORY ]

### `watch` (Sensory Stream)
Background monitoring of shell and logs.
- `start`: Launch monitor [Watchdog Core]
- `stop`: Terminate [SIGTERM]
- `status`: PID & Health metrics
- `logs`: Tail enriched logs [768D]

### `probe` (Targeted Extraction)
Active ingestion tools.
- `scout <url>`: Single URL analysis [LLM Synthesis]
- `ingest <file>`: Local file / buffer extraction
- `capture`: Clipboard / Termux-API ingest
- `crawl <url>`: Recursive site ingest [Depth-Limited]

## [ SECTOR 02: COGNITIVE ]

### `search <query>`
Unified semantic + k-NN retrieval across the entire knowledge base.

### `brain` (Cognitive Engine)
High-level analysis and reporting.
- `analyze`: Retroactive deep context
- `summary`: Executive multi-session reports
- `verify`: Fact validation + source checking

### `map` (Topology)
Visualization and lineage.
- `graph`: Relationship maps [Mermaid / Force-Graph]
- `cloud`: Dynamic TUI / D3.js visualisation
- `trace`: Full provenance & lineage

### `index` (Vector Lifecycle)
Vector database management.
- `rebuild`: Total rebuild [Gemini-001 / current model]
- `cluster`: Density-based hotspot detection
- `prune`: Evict low-importance nodes (≤ 3)
- `optimize`: Deduplicate + ID hot-swap
- `stats`: Volume / dimensionality telemetry

## [ SECTOR 03: STATE ]

### `memory` (State Management)
Direct manipulation of knowledge units.
- `list`: Recent units [chronological]
- `create`: Manual node init
- `edit`: Contextual CRUD
- `delete`: Soft-delete
- `connect`: Manual relational linking
- `merge`: Log → DB consolidation
- `forget`: Hard-delete

### `run` (Strategic Layer)
Task and strategy execution.
- `plan`: Prioritise tasks [importance/session map]
- `task`: Todo / strategy control
- `sync`: Harmonise todo.md ↔ memory.db

### `maintain` (Hygiene)
System self-maintenance.
- `tag`: Auto-categorisation
- `clean`: Metadata sanitisation
- `audit`: Self-correcting kernel integrity

## [ SECTOR 04: EXECUTIVE ]

### `forge` (Agentic Synthesis)
Creation and refinement of assets.
- `tool`: Synthesise Python / MCP tools
- `evolve`: Iterative AST refinement
- `design`: UI/UX (Rich / HTML)
- `skill`: Modular capability creation
- `persona`: System-prompt identities
- `test`: Pytest validation
- `bench`: Execution timing benchmarks
- `archive`: Safe deprecation storage

### `system` (Kernel Ops)
System-level operations.
- `dash`: Neural TUI Dashboard
- `config`: Kernel settings
- `asset`: Registry / file control
- `health`: Standardised ingestion telemetry
- `backup`: Full-state snapshot
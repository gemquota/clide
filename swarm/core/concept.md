# CLIDE: Command Line Interface - Database: Everything
**Version**: 0.6.0 | **Status**: Active Orchestrator

## 1. Vision
CLIDE is an autonomous documentation and tool-synthesis engine that bridges the gap between ephemeral shell history and a permanent, version-controlled repository of agentic capabilities. It transforms "how I did something" into "how it is done," creating a self-evolving library of TOML-based prompts and MCP-ready Python servers.

## 2. Core Pillars

### A. Passive Ingestion & Active Extraction
CLIDE monitors two primary streams:
- **Neural Stream**: Analyzes interaction logs between the user and LLM agents to detect high-value workflows.
- **Operational Stream**: Monitors shell history (`.zsh_history`) to identify complex command pipelines and repeated patterns.

### B. The Autonomous & Secure Era (v0.6.0+)
As of v0.6.0, CLIDE is no longer just a passive recorder. It incorporates:
- **Security Sandbox (Auditor)**: Every extracted tool undergoes a mandatory security risk assessment using LLM-based auditing before preservation.
- **Self-Healing (Healer Loop)**: Generated Python MCP servers are dry-run tested; if failures occur, CLIDE automatically attempts self-repair via recursive LLM debugging.
- **Dependency Isolation**: Uses PEP 723 inline script metadata (`uv` compatible) to ensure synthesized tools remain portable and execution-ready without polluting the host environment.

### C. Git-Integrated Memory
Every asset is committed to a git-backed repository. This enables:
- **One-Click Rollback**: Reverting corrupted or unwanted tool evolutions.
- **Interaction Provenance**: A "Replay" system (`./clide why <asset>`) that links a tool to the specific conversation or shell sequence that birthed it.

## 3. System Architecture

- **`clide/`**: The engine room containing intent classifiers, synthesis templates, and the monitor loop.
- **`swarm/commands/`**: The asset library containing TOML command definitions and the `mcp_servers/` subdirectory.
- **`vector_registry.json`**: A 32-dimensional semantic index of all tools, enabling RAG-based search and duplication detection.
- **`docs/`**: The project's self-documenting archive, including a visual dashboard for asset management.

## 4. Operational Commands
- `./clide monitor`: Activates the live ingestion and extraction loops.
- `./clide search <query>`: Semantic search for existing tools.
- `./clide dashboard`: Generates a Markdown-based visual registry of all assets.
- `./clide rollback <id>`: Reverts an asset to its previous git-state.
- `./clide why <id>`: Displays the origin context of a specific tool.
- `./clide janitor`: Identifies overlapping tools and proposes merge plans to reduce entropy.

## 5. Roadmap Trajectory
- **v0.5.0**: Passive ingestion and basic git syncing.
- **v0.6.0**: Security, self-healing, and provenance (Current).
- **v0.7.0 (Future)**: Deep RAG integration for "Agentic Help"—where CLIDE explains how to combine multiple tools to solve complex user requests.

---
*CLIDE: Evolution of the Shell.*
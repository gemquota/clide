# CLIDE Project Structure & Documentation

This document provides a comprehensive overview of the CLIDE (Command Line Interface - Database: Everything) project directory structure and detailed descriptions of each core component.

---

## 1. The Core Engine (`clide/`)
The `clide/` directory contains the primary logic for ingestion, classification, and asset synthesis.

```
clide/
├── __init__.py               # Package initialization and path exposure.
├── activator.py              # Handles the retrieval and mounting of Skill and Agent instructions.
├── brain.py                  # Generates Mermaid and ASCII visualizations of the Project Brain (memory.db).
├── clide_cli.py              # The primary CLI entry point and command router.
├── command_saver.py          # Formats and writes synthesized TOML commands to disk.
├── commands_loader.py        # Loads and parses TOML command definitions from the registry.
├── config_loader.py          # Manages project-wide configuration (paths, limits) from .cliderc.
├── dashboard_generator.py    # Generates the Markdown-based visual asset registry.
├── evictor.py                # Placeholder for context eviction and cleanup logic.
├── extractor.py              # The core heartbeat; manages the live ingestion loop for neural and shell streams.
├── git_monitor.py            # Analyzes git commit history for potential agentic asset extraction.
├── git_sync.py               # Automates git commits for new assets and handles temporal rollbacks.
├── hotswapper.py             # Manages the installation of MCP servers and Gemini Skills.
├── ingest_swarm.py           # A batch processing utility for importing large external libraries (e.g., Swarm V2).
├── intent_classifier.py      # LLM-based logic for categorizing neural stream inputs.
├── janitor.py                # Performs autonomous maintenance: deduplication and TODO pruning.
├── mcp_generator.py          # Synthesizes Python-based MCP servers with self-healing (Healer Loop).
├── memory.db                 # SQLite database storing Facts, Lessons, Discoveries, and TODOs.
├── provenance.py             # Links synthesized assets to their original birth-context for auditability.
├── recent_messages.json      # Cache of recent interactions used for repetition detection.
├── security_auditor.py       # Mandatory risk assessment engine for all synthesized code.
├── shell_ingestor.py         # Parses and groups shell history into logical work batches.
├── shell_intent_classifier.py # LLM-based logic specifically tuned for shell command extraction.
├── sync_commands.py          # Synchronizes disk-based assets with the vector registry.
├── template_generator.py     # Constructs high-fidelity system prompts using Brain facts.
└── vector_registry.py        # Manages the 32-dimensional semantic index of all project assets.
```

---

## 2. The Agent Swarm (`swarm/`)
The `swarm/` directory houses the library of agentic capabilities and shared persistent state.

```
swarm/
├── commands/                 # The integrated asset library.
│   ├── archive/              # Outdated or merged assets moved here for safety.
│   ├── mcp_servers/          # Synthesized Python-based Model Context Protocol servers.
│   ├── provenance/           # JSON files mapping tools to their original context.
│   ├── bug.toml              # Protocol 2.2: Bug/Hotfix Resolution Persona.
│   ├── commands_index.md     # A searchable index of all integrated assets.
│   ├── dev.toml              # Protocol 2.1: Feature Implementation Persona.
│   ├── engineer.toml         # Standard high-detail Engineering Persona.
│   └── vector_registry.json  # The semantic vector store (embeddings) for all assets.
├── core/                     # Shared agentic intelligence and state.
│   ├── agents.md             # The Agentic Constitution (Operating Principles).
│   ├── concept.md            # High-level architecture and vision documentation.
│   ├── state.db              # SQLite shared state for multi-agent workflows (Project Atlas).
│   └── state_manager.py      # Python utility for interacting with the shared state.
├── new/                      # Swarm V2 plugin library (Ingested).
└── self_refactor.py          # Utility for auditing documentation against actual source code.
```

---

## 3. Documentation (`docs/`)
The `docs/` directory contains the system's "North Star" protocols, design specs, and archived history.

```
docs/
├── architecture/             # Visual and structural design specifications.
├── archive/                  # Historical documents and deprecated prototypes.
├── dev/                      # Technical debt logs and integration reports.
├── modules/                  # Technical deep-dives into specific engine components.
├── registry/                 # Documentation on vector and database integration.
├── specs/                    # Detailed technical specifications for new features.
├── architectural_synthesis_protocol.md # Guide for mapping code to conceptual pillars.
├── brain_graph.mmd           # Mermaid graph representation of the Project Brain.
├── cli_ref.md                # Comprehensive CLI argument and command reference.
├── dashboard.md              # The visual registry of all project assets.
├── protocols.md              # Grouped operational protocols (Design/Implementation/Governance).
├── README.md                 # Project vision, pillars, and architecture overview.
└── system_blueprint_prompt.md # The "System Prompt" for LLMs interacting with CLIDE.
```

---

## 4. Combined Directory Tree
A unified view of the CLIDE ecosystem.

```
meta/
├── .cliderc                  # Project configuration.
├── .gitignore                # Git exclusion rules.
├── CHANGELOG.md              # Version-controlled history of changes.
├── cli                       # Root bash launcher (renamed from clide).
├── clide/                    # The Core Engine (renamed from clide_src).
├── docs/                     # Documentation and Protocols.
├── swarm/                    # Asset Library and Agent Swarm.
├── todo.md                   # Synchronized project task list.
└── VERSION                   # Current project version (v0.7.0).
```

---
*Generated by CLIDE v0.7.0*

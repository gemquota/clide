# Changelog

## [0.7.0] - 2026-02-03
### Added
- **Mounting & Hotswapping**: New `./clide activate` and `./clide hotswap` commands for Swarm V2 integration.
- **Skill Support**: Direct integration with `gemini skills` for local asset installation.
- **Brain Janitor**: Added `./clide todo clean` to automatically prune outdated or completed tasks from `memory.db` and `todo.md`.
- **Enhanced UI**: New ASCII banner and informative default output for the CLIDE entry point.
- **ATLAS**: Comprehensive `docs/atlas.md` detailing all system arguments.

## [0.6.0] - 2026-02-01
### Added
- **Auto-Repair (Healer Loop)**: Dry-runs and self-repair logic for generated MCP servers.
- **Security Auditor**: Integrated mandatory security risk assessment for all new agentic assets.
- **Dependency Management**: Support for PEP 723 inline script metadata (`uv` compatible) in synthesized servers.
- **Visual Registry**: Added `./clide dashboard` to generate a searchable Markdown summary of the asset database.
- **RAG Expansion**: Upgraded vector registry to 32-dimensional semantic embeddings for higher search accuracy.

... (rest of changelog)
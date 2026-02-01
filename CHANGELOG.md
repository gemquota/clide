# Changelog

## [0.6.0] - 2026-02-01
### Added
- **Auto-Repair (Healer Loop)**: Dry-runs and self-repair logic for generated MCP servers.
- **Security Auditor**: Integrated mandatory security risk assessment for all new agentic assets.
- **Dependency Management**: Support for PEP 723 inline script metadata (`uv` compatible) in synthesized servers.
- **Visual Registry**: Added `./clide dashboard` to generate a searchable Markdown summary of the asset database.
- **RAG Expansion**: Upgraded vector registry to 32-dimensional semantic embeddings for higher search accuracy.

## [0.5.0] - 2026-02-01
### Added
- **Git-Backed Asset Syncing**: Automatic git commits for every new TOML command or MCP server created.
- **Milestone Maturity**: Transitioned to a version-controlled repository system.
- **Enhanced Orchestration**: Unified neural and operational monitoring with real-time repo updates.

## [0.4.8] - 2026-02-01
### Added
- **Operational Stream**: Integrated `.zsh_history` monitoring into the main extractor loop.
- **MCP Generation**: Added `mcp_generator.py` to produce standardized FastMCP Python servers.
- **Semantic Registry**: Implemented `vector_registry.json` for indexing agentic assets with semantic embeddings.
- **Hot-Swapping**: Added `hotswapper.py` to automatically register new MCP servers in `settings.json`.
- **Branding**: Official launch of the **CLIDE** (Command Line Interface - Database: Everything) persona and launcher.

## [0.2.0] - 2026-02-01
### Added
- **Neural Stream**: Monitoring of `logs.json` for chat-based intent extraction.
- **Interactive Loop**: Added user confirmation before saving commands.
- **Template Engineering**: LLM-based system prompt generation for high-detail commands.

## [0.1.0] - Initial Prototype
- Basic log tailing and intent classification.

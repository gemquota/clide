# Changelog

## [0.4.8] - 2026-02-01
### Added
- **Skill Promotion**: Tracks command usage frequency and proposes converting popular TOML prompts into executable MCP servers.
- **Contextual Suggestions**: Analyzes the current directory/environment to suggest relevant tools from the Database of Everything.
- **Self-Refactor Tool**: Automated auditing of documentation vs. source code to ensure the "Source of Truth" remains accurate.
- **Usage Tracking**: Persistent storage of command invocation counts in `state.json`.

## [0.4.5] - 2026-02-01
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

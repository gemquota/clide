# Technology Stack: CLIDE

## Core Development
- **Primary Language:** Python 3.x - Used for the Extraction Engine, MCP Servers, and system utilities.
- **Automation:** Shell/Bash - Orchestrates the monitoring services and startup sequences (`cli`, `start_gemini_services.sh`).

## Data & Context Management
- **Persistence:** SQLite - Powers the "Project Brain" (`memory.db`) and the "Agent Swarm" state (`state.db`), now unified via a centralized state management service with WAL mode for concurrent access.
- **Configuration:** TOML - The primary format for hot-swappable agentic commands and persona definitions.
- **Interchange:** JSON - Used for enriched logs and recent message tracking.
- **Documentation:** Markdown - The format for all system logs, agent constitutions (`agents.md`), and ingestion reports.

## Execution Environment
- **Platform:** CLI-First (Optimized for Android/Termux and Linux environments).
- **Verification:** Automated Test-Driven Synthesis using `pytest` for all forged assets.
- **Architecture:** Decoupled Extraction (Forge) and Execution (Swarm) domains.

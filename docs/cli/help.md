# HELP // INTELLIGENCE PORTAL

The CLIDE help system is a **Documentation-Driven Interceptor**. Unlike traditional CLIs that use hardcoded strings, CLIDE generates its entire interface dynamically from the Markdown files stored in `docs/cli/`.

### Unified Help Model
The system has been simplified to provide comprehensive, high-fidelity information by default.

<card>
title: HELP COMMANDS
Primary: ./cli help [domain] [command]
Search: ./cli help search "keyword"
Index: ./cli help (Displays Global Atlas)
</card>

### Technical Architecture
The help engine operates as a middle-ware layer between the user's request and the file system.

1.  **INTERCEPTION**: `portal.py` catches any command containing `help`, `?`, or `atlas`.
2.  **RESOLUTION**: `guide.py` resolves the logical domain/command to a physical path in `docs/cli/`.
3.  **EXTRACTION**: The parser reads the `.md` file and extracts content under the `## Full` header (falling back to `## Tier: Basic` if necessary).
4.  **ENRICHMENT**: `pre_process_content()` applies semantic highlighting to technical terms (e.g., paths, commands, status keywords).
5.  **RENDERING**: The `rich` library renders the Markdown, including custom `<card>` components, with the **Cyber-Kernel Palette**.

### The Command Atlas
While `help` is functional and educational, the `atlas` command provides a structural map of the entire system.

-   **Usage**: `./cli atlas [domain]`
-   **Content**: High-level command trees and sector overviews.
-   **SSoT**: Both `help` and `atlas` pull from `docs/cli/atlas.md`, ensuring they are always in sync.

### Extensibility
To add help for a new command:
1.  Create a Markdown file in `docs/cli/[domain]/[command].md`.
2.  Add a `## Full` header followed by your documentation.
3.  The system will automatically detect and serve this content.

### Code Reference
- **Entry Point**: `clide/serve/portal.py` -> `intercept_info_requests`
- **Parser**: `clide/serve/guide.py` -> `show_help`
- **TUI Theme**: `clide/serve/guide.py` -> `vapor_theme`
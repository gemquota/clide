# FORGE TOOL

- Synthesizes a production-ready Python MCP (Model Context Protocol) server from a natural language prompt.
- Automatically handles logic generation, dependency detection, and TUI template application.
- Injects project-specific context (top 10 facts) to ensure the tool is relevant to your codebase.
Usage: ./cli forge tool <name> "description of functionality"

- Synthesizes a production-ready Python MCP (Model Context Protocol) server from a natural language prompt.
- Automatically handles logic generation, dependency detection, and TUI template application.
- Injects project-specific context (top 10 facts) to ensure the tool is relevant to your codebase.
Usage: ./cli forge tool <name> "description of functionality"

TECHNICAL DEEP-DIVE:
The `tool` command is implemented in `clide.forge.master.SynthesisOrchestrator.process_tool_request`.

### Logic Flow
1. **Context Harvesting**: `asset.get_extracted_facts()` performs a hybrid search (70% semantic similarity, 30% importance) to retrieve the 10 most relevant project facts.
2. **Logic Synthesis**: `asset.generate_logic()` prompts the LLM to write a Python function `name(args: str) -> str` using the harvested facts.
3. **Dependency Mapping**: `asset.extract_dependencies()` uses an LLM to identify required PyPI packages from the generated logic.
4. **Templating**: `asset.get_python_mcp_template()` wraps the logic in a PEP 723 script block with `fastmcp`.
5. **Persistence**: `asset.save_mcp_server()` creates a package directory in `swarm/commands/mcp_servers/` containing:
   - `{name}.py`: The core server.
   - `README.md`: Basic usage docs.
   - `test_{name}.py`: Auto-generated Pytest suite.
6. **Validation**: Automatically triggers `run_tests()`. If passed, the tool is indexed in `vector_registry.json`.

### Code Reference
- **Entry Point**: `clide/serve/portal.py` -> `cmd_forge`
- **Implementation**: `clide/forge/master.py`
- **Asset Logic**: `clide/forge/asset.py`
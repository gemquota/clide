# Specification: Automated MCP Synthesis Pipeline (The Forge)

## 1. Goal
The goal is to create a seamless, automated pipeline that:
1.  Detects when a user intent or repetitive pattern warrants a new tool.
2.  Generates a high-quality MCP server (Python) including docstrings, type hints, and dependencies.
3.  Automatically generates and runs unit tests to verify the generated tool.
4.  Deploys the verified tool to the `swarm/commands/mcp_servers` directory.

## 2. Requirements
- **Intent Integration:** Hook into `clide/intent_classifier.py` and `clide/extractor.py` to trigger synthesis.
- **Verification Loop:** Before saving, the pipeline must run `pytest` on the generated test file. Only "passing" tools are moved to production.
- **Project Context Injection:** The generator must use the Project Brain (via `query_project_knowledge`) to inform the tool's design.
- **Metadata Management:** Track the provenance of generated tools (e.g., "Why was this made?").

## 3. Technical Design
- **Trigger:** A new `synthesis_orchestrator.py` that listens for `TOOL_INTENT` messages.
- **Generator Update:** Enhance `clide/mcp_generator.py` with a `verify_and_deploy` method.
- **State Integration:** Record synthesis events in `swarm/core/state.db`.

## 4. Acceptance Criteria
- [ ] A tool-building request in the neural stream triggers the creation of a Python file in `swarm/commands/mcp_servers`.
- [ ] The generated tool includes a `README.md` and a `test_*.py` file.
- [ ] Synthesis fails (and reports the failure) if the generated unit tests do not pass.

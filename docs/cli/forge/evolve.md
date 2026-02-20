# FORGE EVOLVE

- Iteratively refines existing forged tools based on natural language instructions.
- Allows for bug fixes, feature additions, or UI improvements without manual editing.
- (Status: Implementation in progress).
Usage: ./cli forge evolve <asset_id> "instruction"

- Iteratively refines existing forged tools based on natural language instructions.
- Allows for bug fixes, feature additions, or UI improvements without manual editing.
- (Status: Implementation in progress).
Usage: ./cli forge evolve <asset_id> "instruction"

TECHNICAL DEEP-DIVE:
The `evolve` command is implemented in `clide.forge.master.SynthesisOrchestrator.evolve_tool`.

### Intended Workflow
1. **Source Loading**: Reads the current source code from `swarm/commands/mcp_servers/<asset_id>/`.
2. **Contextual Prompting**: Sends the [Existing Code] + [User Instruction] + [Project Facts] to the LLM.
3. **AST Patching**: The LLM generates a refined version of the logic.
4. **Validation Loop**: Triggers `run_tests()` on the new version. If tests fail, the refactor is aborted or retried.

### Code Reference
- **Entry Point**: `clide/serve/portal.py` -> `cmd_forge` (evolve)
- **Implementation**: `clide/forge/master.py` -> `evolve_tool` (Stubbed)
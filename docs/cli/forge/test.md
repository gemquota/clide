# FORGE TEST

- Executes an automated Pytest suite for a specific forged asset.
- Captures and displays execution logs and failure tracebacks.
- Serves as the quality gate for the production deployment of new tools.
Usage: ./cli forge test <asset_id>

- Executes an automated Pytest suite for a specific forged asset.
- Captures and displays execution logs and failure tracebacks.
- Serves as the quality gate for the production deployment of new tools.
Usage: ./cli forge test <asset_id>

TECHNICAL DEEP-DIVE:
The `test` command is implemented in `clide.forge.master.SynthesisOrchestrator.run_tests`.

### Logic Flow
1. **Discovery**: Locates the tool's package directory in `swarm/commands/mcp_servers/`.
2. **File Mapping**: Specifically looks for `test_{asset_id}.py` within that directory.
3. **Execution**: Uses `subprocess.run(["pytest", test_file])` to trigger the test runner.
4. **Reporting**:
   - **Success**: Returns `True` and prints a confirmation.
   - **Failure**: Captures `stdout` from pytest and prints the full error report.
5. **Automation**: This function is a mandatory step in `process_tool_request` and `verify_and_deploy`.

### Code Reference
- **Entry Point**: `clide/serve/portal.py` -> `cmd_forge` (test)
- **Implementation**: `clide/forge/master.py` -> `run_tests`
- **Verifier**: `clide/forge/asset.py` -> `verify_and_deploy`
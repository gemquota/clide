# System Design & Architecture

## Conceptual Grounding

### The Observer Pattern
CLIDE operates as a passive observer. It does not hook into system calls; instead, it monitors "State Artifacts" (log files and history files). This ensures compatibility across different Termux environments without requiring root or specialized shell plugins.

### Self-Evolutionary Loop
The system is architected to treat its own source code as an asset in the "Database: Everything." By allowing `extractor.py` to be a target for its own classification logic, CLIDE can theoretically propose its own refactors.

## Interoperability Matrix

### Data Flow Diagram (Logic)
1. **Source**: `.zsh_history` (Operational) / `logs.json` (Neural).
2. **Parser**: `shell_ingestor.py` / `extractor.py` (JSON loading).
3. **Filter**: `intent_classifier.py` / `shell_intent_classifier.py`.
4. **Synthesis**: `template_generator.py` (TOML) / `mcp_generator.py` (Python).
5. **Storage**: `command_saver.py` / `vector_registry.py`.
6. **Activation**: `hotswapper.py` -> `~/.gemini/settings.json`.

### Shared State
- **Offset Tracking**: Managed via `state.json` and `shell_state.json`.
- **Global Config**: CLIDE reads and writes to the Gemini CLI's root configuration to achieve hot-swapping.

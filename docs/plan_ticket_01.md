# Implementation Plan: Map Input Vectors (Automated)

## Overview
Develop a static analysis tool to automatically map all input vectors in `clide/serve/portal.py`. This ensures the input map remains up-to-date as the CLI evolves, rather than relying on a static manual list.

## Scope Definition
### In Scope
- Create `scripts/map_input_vectors.py`.
- Implement AST parsing to extract `argparse` definitions.
- Generate a structured report (Markdown) of all commands and arguments.
- Save the report to `docs/input_vectors.md`.

### Out of Scope
- modifying `portal.py`.
- implementing new input validation (that's a future ticket).

## Current State Analysis
- `clide/serve/portal.py` uses `argparse` inside `main()`.
- Manual research confirmed the structure.
- No existing tool automates this mapping.

## Implementation Phases

### Phase 1: The God Parser
- **Goal**: Create the extraction script.
- **Steps**:
    1.  [ ] Create `scripts/map_input_vectors.py`.
    2.  [ ] Implement `ast.NodeVisitor` to find `Call` nodes.
    3.  [ ] Filter for `add_parser` (commands) and `add_argument` (inputs).
    4.  [ ] Reconstruct the hierarchy (Command -> Subcommand -> Args).
    5.  [ ] formatting the output as a Markdown table.
- **Verification**: Run `python3 scripts/map_input_vectors.py` and check for syntax errors.

### Phase 2: Execution & Documentation
- **Goal**: Generate the artifact.
- **Steps**:
    1.  [ ] Run the script: `python3 scripts/map_input_vectors.py > docs/input_vectors.md`.
    2.  [ ] Verify the output against the manual research in `docs/research_ticket_01.md`.
- **Verification**: `cat docs/input_vectors.md` and ensure all commands (watch, probe, etc.) are listed.

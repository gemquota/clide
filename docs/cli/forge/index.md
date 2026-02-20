# [ SECTOR 04: EXECUTIVE ] - FORGE
Agentic synthesis and iterative tool development.

The `forge` domain is the birthplace of system capabilities and visual designs.

<card>
title: FORGE OVERVIEW
Capabilities: Tools, Skills, UI
Iteration: AST Refinement
Synthesis: LLM-Driven
Status: CREATIVE
</card>

### Commands
*   **tool**: Synthesizes a new Python or MCP tool from a prompt.
*   **evolve**: Iteratively refines existing assets based on instructions.
*   **design**: Generates UI/UX layouts and visual components.
*   **skill**: Creates modular capabilities for system agents.
*   **persona**: Defines system-prompt identities for specific roles.
*   **test**: Validates tool integrity via automated Pytest suites.
*   **bench**: Measures execution timings and performance.
*   **archive**: Safely stores deprecated or unstable assets.

### Technical Specifications
Forge uses an iterative loop: **Prompt -> Synthesize -> Test -> Evolve**.

<card>
title: OPERATIONAL CONTEXT
Language: Python 3.12 (AST-Aware)
UI Style: Rich / Material / Cyber
Testing: Pytest / Benchmark.py
</card>

### Architecture Internals
The forge uses the `SynthesisOrchestrator` in `master.py`. It leverages the `asset.py` templates for standardized asset generation.

<card>
title: NEURAL-KERNEL HOOKS
Forge Hook: clide.forge.master.SynthesisOrchestrator
Evolve Hook: clide.forge.master.evolve_tool
Design Hook: clide.forge.master.generate_design
</card>

### API Reference
*   `process_tool_request(name, prompt)`: The core synthesis entry.
*   `run_tests(id)`: Automated validation hook.
*   `archive_asset(id)`: System cleanup and relocation.

### Code Reference
- **Entry Point**: `clide/serve/portal.py` -> `cmd_forge`
- **Implementation**: `clide/forge/master.py`
- **Asset Logic**: `clide/forge/asset.py`

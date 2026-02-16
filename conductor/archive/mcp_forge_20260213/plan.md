# Implementation Plan: Automated MCP Synthesis Pipeline (The Forge)

## Phase 1: Trigger & Orchestration [checkpoint: 61e971d]
*Focus: Connecting the intent detection to the synthesis logic.*

- [x] Task: Create `clide/synthesis_orchestrator.py` to coordinate the flow. [8c85353]
    - [x] Write Tests: Mock `TOOL_INTENT` and verify orchestrator calls the generator.
    - [x] Implement: Logic to receive intent, gather context, and call `mcp_generator.py`.
- [x] Task: Update `clide/extractor.py` or `intent_classifier.py` to explicitly output a `TOOL_INTENT` signal. [7964373]
    - [x] Write Tests: Verify specific patterns trigger the correct signal.
    - [x] Implement: Enhanced regex or LLM prompt for tool intent classification.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Trigger & Orchestration' (Protocol in workflow.md)

## Phase 2: Verification Loop (Red/Green Synthesis) [checkpoint: 8d47627]
*Focus: Ensuring only working code is deployed.*

- [x] Task: Implement `verify_and_deploy` in `clide/mcp_generator.py`. [b9c9ebb]
    - [x] Write Tests: Mock a failing tool and verify it is NOT deployed.
    - [x] Implement: `subprocess.run(["pytest", ...])` logic and file movement.
- [x] Task: Enhance `generate_tests` to produce more robust, data-driven tests. [5668355]
    - [x] Write Tests: Verify generated tests cover basic edge cases.
    - [x] Implement: Improved LLM prompting for test generation.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Verification Loop' (Protocol in workflow.md)

## Phase 3: Provenance & Registry [checkpoint: 1b27450]
*Focus: Tracking and visualizing the forged assets.*

- [x] Task: Update the `vector_registry.py` to index generated tools. [63b5e0f]
    - [x] Write Tests: Verify tools can be searched via the existing vector engine.
    - [x] Implement: Hook into the deployment process to update the registry.
- [x] Task: Record synthesis success/failure in `swarm/core/state.db`. [2a4fadb]
    - [x] Write Tests: Verify state table entries for new tool events.
    - [x] Implement: Add `record_synthesis` tool to the state manager.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Provenance & Registry' (Protocol in workflow.md)

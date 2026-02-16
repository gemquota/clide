# Implementation Plan: Multi-Agent Collaboration & Simulation Framework

## Phase 1: Simulation Foundation [checkpoint: 56200c3]
*Focus: Creating the isolated sandbox and communication protocol.*

- [x] Task: Implement the `SimulationWorkspace` manager in `clide/sim_runner.py`. [5c15b5b]
    - [x] Write Tests: Verify creation and deletion of isolated temp directories.
    - [x] Implement: Logic to scaffold a minimal project structure for the agents.
- [x] Task: Add a `message_bus` table to `swarm/core/state.db`. [8a5ea3d]
    - [x] Write Tests: Verify agents can publish and subscribe to messages.
    - [x] Implement: SQL schema and corresponding tools in `state_manager.py`.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Simulation Foundation' (Protocol in workflow.md)

## Phase 2: Scenario Orchestration [checkpoint: a78848c]
*Focus: Defining and running collective challenges.*

- [x] Task: Define the `Scenario` schema (YAML or JSON) for specifying goals and constraints.
    - [x] Write Tests: Verify parser can load a complex scenario definition.
    - [x] Implement: Parser and validation logic in `sim_runner.py`.
- [x] Task: Implement the `Orchestrator` to sequence agent activations.
    - [x] Write Tests: Mock agent responses and verify orchestrator maintains flow.
    - [x] Implement: Activation loop that monitors the message bus for handoffs.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Scenario Orchestration' (Protocol in workflow.md)

## Phase 3: Analysis & Evolution [checkpoint: e6d0ffc]
*Focus: Learning from simulation failures.*

- [x] Task: Create the `CollaborationAnalyzer` to generate post-sim reports.
    - [x] Write Tests: Verify report accurately summarizes bus activity.
    - [x] Implement: Logic to trace the "path of intent" through multiple agents.
- [x] Task: Implement "Failure Hotswap" – trigger tool re-synthesis if a sim fails due to tool deficiency.
    - [x] Write Tests: Verify a sim failure triggers a `TOOL_INTENT` for a fix.
    - [x] Implement: Integration between `sim_runner.py` and `synthesis_orchestrator.py`.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Analysis & Evolution' (Protocol in workflow.md)

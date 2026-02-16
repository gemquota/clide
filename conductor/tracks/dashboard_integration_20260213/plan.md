# Implementation Plan: Integrated Dashboard & Control Center

## Phase 1: UI Foundation [checkpoint: pending]
- [x] Task: Create a unified HTML/JS entry point for the new dashboard in `viz/index.html`.
- [x] Task: Implement a modular layout system to host multiple "blades" (Sim Monitor, Brain View, Registry).
- [x] Task: Setup a WebSocket or periodic polling bridge in `viz/serve.py` for real-time state updates.

## Phase 2: Real-time Simulation Monitoring [checkpoint: pending]
- [x] Task: Implement the "Sim Blade" – a live view of the message bus and active simulations.
- [x] Task: Add visualization for the "Path of Intent" (agent flow) using Cytoscape.js or similar.
- [x] Task: Implement a "Scenario Launcher" UI to trigger simulations from the dashboard.

## Phase 3: Control & Evolution [checkpoint: pending]
- [x] Task: Implement a "Hotspot Editor" to manually adjust persona logic or tool synthesis prompts.
- [x] Task: Add a "Knowledge Auditor" blade to review and prune memory nodes.
- [x] Task: Integrate the CollaborationAnalyzer reports into the dashboard UI.

# Specification: Multi-Agent Collaboration & Simulation Framework

## 1. Goal
The objective is to move beyond individual tool verification and establish a "Collective Intelligence" testbed. This framework will simulate multi-agent workflows to ensure that forged assets (Prompts and MCP Servers) can collaborate, share context, and resolve dependencies without human intervention.

## 2. Requirements
- **Shared Workspace:** A virtualized directory or "sandbox" where multiple agents can read/write files and observe changes.
- **Inter-Agent Message Bus:** A mechanism for agents to "handoff" tasks or query each other for specialized knowledge.
- **Scenario Orchestrator:** A system to define "Challenges" (e.g., "Build a web scraper and save the data to a database") and measure success.
- **Rollback & Cleanup:** Automatic teardown of simulated environments after a scenario completes.

## 3. Technical Design
- **Core Component:** `clide/sim_runner.py` to manage the lifecycle of a simulation.
- **Communication:** Use the existing `swarm/core/state.db` as a shared message board for agents.
- **Isolation:** Use temporary directories (`/data/data/com.termux/files/home/.gemini/tmp/sim_X`) for file-system operations during simulations.

## 4. Acceptance Criteria
- [ ] A simulation can be triggered with a defined goal and a list of participant agents.
- [ ] Agents can successfully exchange data via the shared state manager during the simulation.
- [ ] The system generates a "Collaboration Report" detailing the interaction steps and the final outcome.

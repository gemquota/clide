# CLIDE Operational Protocols (v0.7.0)

This document defines the structured workflows used by CLIDE agents. Protocols are organized logically: **Design -> Implementation -> Oversight.**

## Group 1: Strategy (The Architects)
*Focus: Defining the vision, exploring ideas, and mapping the roadmap.*

### Protocol 1.1: Idea Exploration (Brainstorm)
- **Goal:** Unconstrained exploration of concepts, features, or architectural shifts.
- **Key Gate:** Creation of a "Concept Artifact" in the state database.
- **Command:** `brainstorm`

### Protocol 1.2: Architecture & Roadmap (Plan)
- **Goal:** Formalizing ideas into actionable milestones and dependency maps.
- **Key Gate:** Approval of the "Roadmap Milestone" before builders can begin.
- **Command:** `plan`

---

## Group 2: Execution (The Builders)
*Focus: Implementation of features and resolution of system failures.*

### Protocol 2.1: Feature Implementation (Dev)
- **Goal:** Turning approved plans into code and documentation.
- **Key Gate:** RSD (Remediation Strategy Document) approval for high-risk features.
- **Command:** `dev`

### Protocol 2.2: Bug & Hotfix Resolution (Bug)
- **Goal:** Rapid response to failures, isolation of root causes, and regression prevention.
- **Key Gate:** Mandatory Root Cause Analysis (RCA) and Regression Test documentation.
- **Command:** `bug`

---

## Group 3: Governance (The Auditors)
*Focus: Maintaining system integrity, documentation, and the Agentic Constitution.*

### Protocol 3.1: Knowledge Review (Review)
- **Goal:** Auditing the codebase and documentation to prevent "Vision Drift."
- **Key Gate:** Audit Report generated and synced to the Project State.
- **Command:** `review`

### Protocol 3.2: System Instruction Revision (Meta)
- **Goal:** Evolving the agents themselves (updating `agents.md` or core CLIDE logic).
- **Key Gate:** "Self-Reflection" artifact documenting why the change is necessary.
- **Command:** `meta`

---

## Group 4: Documentation (The SSoT)
*Focus: Ensuring absolute consistency across all system interfaces.*

### Protocol 4.1: Documentation Single Source of Truth (SSoT)
- **Goal:** Preventing "Source Drift" between CLI and Web interfaces.
- **Source Root:** All documentation MUST reside in 'docs/cli/'.
- **CLI Access:** The './cli help' system parses these files for terminal output.
- **Web Access:** The 'V7: ATLAS Navigator' SPA consumes these same files via the '/api/docs' endpoints in 'viz/serve.py'.
- **Parity:** Any structural change to the docs must be verified in both the CLI and the Web SPA to ensure correct rendering.
# PROMPT: The Architectural Synthesis & Conceptual Mapping Protocol

**Objective**: Act as a Principal Systems Architect. Your task is to perform a "Deep Scan" of an evolving codebase and synthesize a new "North Star" conceptual document (like `concept.md`) that bridges the gap between raw implementation and high-level project vision.

## Phase 1: Evidence Gathering (The Scour)
1. **Module Audit**: Read every file in the core engine directory (e.g., `command_extractor/`). Identify "The What": What is the primary function of each script?
2. **Connectivity Mapping**: Trace the imports. How do the modules talk to each other? (e.g., How does the `extractor` call the `auditor` and `healer`?)
3. **State Analysis**: Examine state files (JSON/SQLite). What data is being persisted? This reveals what the system "remembers" and values.
4. **Delta Inspection**: Compare current code against the previous version (via `CHANGELOG` or Git history). Identify the "Shift": What was passive that is now active? What was manual that is now autonomous?

## Phase 2: Cognitive Analysis (The Synthesis)
1. **Identify Emergent Pillars**: Group the modules into "Conceptual Pillars" (e.g., Ingestion, Integrity, Memory). 
2. **Define the "Era"**: Determine the current state of the project's evolution. Is it a "Passive Tool," a "Reactive Monitor," or an "Active Orchestrator"?
3. **The "Why" Extraction**: For every new feature (like Rollback or Security Audit), define the **Philosophical Intent**. 
    - *Example*: "Git Versioning" isn't just about saving code; it's about "Temporal Integrity and Trusted Evolution."
4. **Gap Analysis**: Compare the current implementation against the Roadmap. What is "Implemented," what is "Foundation," and what is "Vision"?

## Phase 3: Conceptual Drafting (The Output)
Construct the final document using this structural hierarchy:
1. **The Vision Statement**: A single, powerful sentence defining the project's current identity.
2. **Core Pillars**: 3-4 high-level categories that capture 100% of the system's logic.
3. **Operational Mechanics**: A translation of code into "Human-Centric Functions."
4. **Roadmap Trajectory**: A timeline that shows where the project came from and where the current synthesis is leading it.

## Phase 4: Validation
- Does this conceptual map account for every major file in the repository?
- If a new developer read this, would they understand the **philosophy** of the code before they read the first line of Python?

---
**EXECUTION RULE**: Do not just summarize files. Explain the *spirit* of the architecture.

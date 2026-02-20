# CLIDE (v0.7.0)
**Command Line Interface - Database: Everything**

## Project Thesis
CLIDE is an **Autonomous Knowledge & Asset Forge**. It solves the "Ephemeral Intent Gap" by monitoring user interactions and shell history to formalize them into two distinct outputs:
1. **Agentic Assets:** Hot-swappable Prompts (TOML) and MCP Servers (Python).
2. **Project Brain:** A persistent knowledge base of Facts, Discoveries, Lessons, and TODOs.

## 🧠 Massive Scale: The 1.5M Brain
CLIDE has scaled to ingest **1.5M+ lines of code and interaction history** into its persistent memory.
- **Dynamic Context:** 1.5M lines of project-wide source code and logs are indexed for real-time RAG.
- **Persistent Memory:** High-density vector registry for sub-second retrieval across the entire knowledge base.
- **Forge Velocity:** Capable of synthesizing assets from a context window that spans the entire project history.

## 🚦 Quick Start
1. **Start the Brain Monitor:**
   ```bash
   ./cli monitor
   ```
2. **View Project Progress:**
   Check `ingestion_logs/progress.md` for live status.
3. **Visualize Knowledge:**
   ```bash
   ./cli brain
   ```
4. **Full Documentation:**
   See [The In-Depth Manual](manual.md) for detailed workflows and database architecture.

---

## 🛠 Architecture: The Forge & The Swarm
The system is partitioned into two discrete domains to ensure stability and focus:

### 1. The Extraction Engine (`clide/`)
A self-contained utility that observes the neural stream and executes the **Forge Workflow**:
- **Pattern Detection:** Monitors last 100 messages for repetitive tasks.
- **Intent Classification:** Recognizes `COMMAND`, `FACT`, `DISCOVERY`, `LESSON`, and `TODO`.
- **Memory Layer:** Stores non-tool knowledge in `memory.db`.
- **Asset Synthesis:** Uses the `agents.md` Constitution and `memory.db` Facts to generate context-aware agentic tools.

---

## 📖 Terminology
In the CLIDE ecosystem, we distinguish between different types of context to ensure clarity for agentic workflows:
- **Agentic Context (or simply "Context"):** Refers to components that enhance LLM intelligence, such as system prompts, custom commands, MCP tools, and specialized agent personas.
- **Project Source:** Refers to the actual codebase, scripts, and non-agentic files of the application.

---

## The Agent Swarm (`swarm/`)
The library of generated tools and their persistent execution state:
- **`commands/`**: The library of TOML and MCP assets.
- **`core/state.db`**: Shared memory for agents (Project Atlas) to track multi-day features and bugs.
- **`agents.md`**: The behavioral constitution every agent inherits.

---

## 🚦 Operational Protocols
Agents follow a standardized taxonomy to ensure engineering rigor:
- **Group 1: Strategy (Architects)** - `brainstorm` (1.1), `plan` (1.2).
- **Group 2: Execution (Builders)** - `dev` (2.1), `bug` (2.2).
- **Group 3: Governance (Auditors)** - `review` (3.1), `meta` (3.2).

---

## 🧠 Smart Integration
- **Fact Injection:** Every tool synthesized by the Forge is automatically injected with the latest 10 facts from the Project Brain.
- **TODO Sync:** Any detected task is simultaneously saved to `memory.db` and appended to the local `todo.md`.
- **Repetition Override:** If you ask for the same thing 3 times, CLIDE overrides normal monitoring to force a command extraction proposal.

---
*Identity: CLIDE v0.7.0 - "The 1.5M Brain Ingestion"*
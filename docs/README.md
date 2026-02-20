# CLIDE (v0.7.0)
**Command Line Interface - Database: Everything**

## Project Thesis
CLIDE is an **Autonomous Knowledge & Asset Forge**. It solves the "Ephemeral Intent Gap" by monitoring user interactions and shell history to formalize them into two distinct outputs:
1. **Agentic Assets:** Hot-swappable Prompts (TOML) and MCP Servers (Python).
2. **Project Brain:** A persistent knowledge base of Facts, Discoveries, Lessons, and TODOs.

---

## 🧠 Massive Scale: The 1.5M Brain
CLIDE has scaled to ingest **1.5M+ lines of code and interaction history** into its persistent memory.
- **Dynamic Context:** 1.5M lines of project-wide source code and logs are indexed for real-time RAG.
- **Persistent Memory:** High-density vector registry for sub-second retrieval across the entire knowledge base.
- **Forge Velocity:** Capable of synthesizing assets from a context window that spans the entire project history.
- **Volume:** Over 6,700 unique knowledge units stored in the SQL-backed Cognitive Layer.

---

## 🏗 Modular Architecture: The Four Sectors
The system is partitioned into four functional sectors to ensure high-density logic and operational rigor:

### [ SECTOR 01: SENSORY ]
Background monitoring and targeted extraction.
- **`watch`**: Monitors shell history and Interaction logs.
- **`probe`**: Active ingestion via `scout`, `crawl`, and `capture` (Clipboard/API).

### [ SECTOR 02: COGNITIVE ]
Semantic search and deep analytical processing.
- **`brain`**: Retroactive analysis, executive reporting, and fact verification.
- **`map`**: Relational topology mapping (Mermaid / Force-Graph / Trace).
- **`search`**: Unified semantic + k-NN retrieval.

### [ SECTOR 03: STATE ]
Persistent state management and strategic control.
- **`memory`**: Direct manipulation of knowledge nodes (CRUD + Relational Linking).
- **`run`**: Strategy execution, task prioritization, and TODO synchronization.
- **`maintain`**: System hygiene (Auto-tagging, Metadata cleaning, Kernel Audit).

### [ SECTOR 04: EXECUTIVE ]
Asset synthesis and kernel operations.
- **`forge`**: Synthesis of hot-swappable TOML prompts and Python MCP servers.
- **`system`**: Dashboard (Neural TUI), Kernel configuration, and state snapshots.

---

## 🛠 Core Components: The Forge & The Swarm

### 1. The Extraction Engine (`clide/`)
A self-contained utility that observes the interaction stream and executes the **Forge Workflow**:
- **Pattern Detection:** Monitors recent messages for repetitive intents.
- **Intent Classification:** Standardizes input into `COMMAND`, `FACT`, `DISCOVERY`, `LESSON`, and `TODO`.
- **Memory Layer:** Persists non-tool knowledge in `memory.db` with vector embeddings.
- **Asset Synthesis:** Generates context-aware tools using the `agents.md` Constitution.

### 2. The Agent Swarm (`swarm/`)
The library of generated tools and their persistent execution state:
- **`commands/`**: A library of production-ready TOML and MCP assets (e.g., `engineer`, `dev`, `bug`, `review`).
- **`core/`**: Shared memory and the "Project Atlas" state manager.
- **`new/`**: V2 Plugin Ecosystem featuring 70+ specialized plugins across domains (Blockchain, LLM-Dev, quantitative-trading, etc.).

---

## 🚦 Operational Protocols (Zero-Series)
Agents follow a standardized taxonomy to ensure engineering rigor:
- **Group 1: Strategy (Architects)** - `STRATEGIST-ZERO` (2.1), `TPM-ZERO` (2.2).
- **Group 2: Execution (Builders)** - `DEV-ZERO` (2.1), `SRE-ZERO` (1.2).
- **Group 3: Governance (Auditors)** - `AUDITOR-ZERO` (3.1), `GOVERNOR-ZERO` (3.2).

---

## 🧠 Smart Integration & Neural Parity
- **Fact Injection:** Tools are automatically injected with the latest relevant facts from the Project Brain.
- **TODO Sync:** Detected tasks are simultaneously saved to `memory.db` and appended to the local `todo.md`.
- **Hotswapping**: Live-swappable agent personas and tool capabilities via `./clide activate` and `./clide hotswap`.
- **Neural Parity Status**:
  - **Unique Command Intent**: ~800 consolidated unique signatures.
  - **Shell History Saturation**: 1,700+ unique historical signatures ingested.
  - **Total Kernel Saturation**: 52%+ (Consolidated and categorized).
- **Self-Healing**: Automated dry-runs and repair logic for generated assets.

---

## 🚀 Quick Start
1. **Start the Brain Monitor:**
   ```bash
   ./clide watch start
   ```
2. **Search the Knowledge Base:**
   ```bash
   ./clide search "V14 value formula"
   ```
3. **Visualize the Brain:**
   ```bash
   ./clide map graph
   ```
4. **View System Dashboard:**
   ```bash
   ./clide system dash
   ```

---
*Identity: CLIDE v0.7.0 - "The 1.5M Brain Ingestion"*
*Version tracking: Refer to [VERSION](../VERSION) and [CHANGELOG](../CHANGELOG.md)*

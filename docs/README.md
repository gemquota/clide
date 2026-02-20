# CLIDE (v0.7.0)
**Command Line Interface - Database: Everything**

## 📜 Project Thesis: Bridging the Intent Gap
CLIDE is an **Autonomous Knowledge & Asset Forge** designed to solve the "Ephemeral Intent Gap"—the systematic loss of critical engineering decisions, creative insights, and architectural rationale that occurs during high-velocity interaction with Large Language Models (LLMs).

Existing agentic tools treat user interactions as transient logs. CLIDE elevates them to **Primary Source Material**, formalizing ephemeral "neural streams" into two persistent, high-utility outputs:
1.  **Agentic Assets:** Hot-swappable Prompts (TOML) and MCP Servers (Python) synthesized directly from detected user patterns and task repetitions.
2.  **Project Brain:** A persistent, SQL-backed knowledge base of Facts, Discoveries, Lessons, and TODOs that enforces a Documentation Single Source of Truth (SSoT) across CLI and Web interfaces.

---

## 🏛️ Project Philosophy: Sovereignty through Rigor
CLIDE is built on the principle of **Code Sovereignty**. It rejects "AI Slop" (bloated, un-audited boilerplate) in favor of high-density, purpose-built logic.
-   **Rigor > Vibes:** Every system decision is grounded in the SQL-backed memory, preventing the "hallucination drift" common in stateless agents.
-   **Dependencies as Choices:** CLIDE prefers local, pure-Python solutions but maintains a library of 70+ "hardened" plugins for complex tasks.
-   **The SSoT Imperative:** Documentation is not a byproduct; it is the kernel. All interfaces (CLI, TUI, Web) consume the same documented protocols.

---

## 🧠 Massive Scale: The 1.5M Brain
CLIDE has scaled to manage industrial-grade cognitive loads, transforming from a simple monitor into a project-wide intelligence layer.
-   **Dynamic Context:** Over **1.5M+ lines of project-wide source code** and interaction history are indexed for real-time Retrieval-Augmented Generation (RAG).
-   **High-Density Memory:** Utilizing **32-dimensional semantic embeddings** via a custom vector registry for sub-second retrieval across the entire multi-year knowledge base.
-   **Cognitive Volume:** Over **6,700 unique knowledge units** stored in the SQL-backed layer, tracking the evolution of the system from version 0.1.0 to present.
-   **Forge Velocity:** Capable of synthesizing production-ready tools from a context window that spans the entire project history, effectively preventing "Vision Drift."

---

## 📈 Project Lineage & Evolution
The 1.5M lines of ingested context represent the cumulative intelligence of the project since v0.1.0. 
-   **Legacy Integration:** Includes historical logs from the initial scraper prototypes and early TUI experiments.
-   **Version Jump:** The transition from v0.6.0 to v0.7.0 marks the shift from *passive monitoring* to *stateful orchestration*, where the Project Brain actively influences tool synthesis.
-   **Dimensionality:** Upgraded from 16D to 32D embeddings to handle the increased semantic complexity of the massive node-pool.

---

## 🏗 Modular Architecture: The Four Sectors
The CLIDE kernel is partitioned into four functional sectors to ensure high-density logic, modular expansion, and operational rigor.

### [ SECTOR 01: SENSORY ]
*Continuous background monitoring and targeted extraction.*
-   **`watch`**: Background daemon monitoring `~/.zsh_history` and interaction logs. It detects complex command sequences and intent shifts in real-time.
-   **`probe`**: Active ingestion suite. Features `scout` (deep URL analysis), `crawl` (recursive site indexing), and `capture` (direct integration with Termux-API for clipboard and sensor data).

### [ SECTOR 02: COGNITIVE ]
*Semantic retrieval and deep analytical processing.*
-   **`brain`**: The analytical core. Performs retroactive analysis, generates executive multi-session reports, and executes fact-verification loops.
-   **`map`**: Topology engine. Visualizes project relationships via Mermaid graphs, 3D Force-Graphs (`galaxy`), or dynamic TUI clouds.
-   **`search`**: Unified semantic + k-NN retrieval engine, providing instant access to any decision ever saved to the Project Brain.

### [ SECTOR 03: STATE ]
*Persistent state management and strategic control.*
-   **`memory`**: Direct node manipulation. Supports high-signal CRUD, manual relational linking, and log-to-DB consolidation.
-   **`run`**: Strategic execution layer. Manages task prioritization via session maps and synchronizes the local `todo.md` with the global `memory.db` state.
-   **`maintain`**: System hygiene. Automates metadata sanitization, auto-tagging, and kernel integrity audits.

### [ SECTOR 04: EXECUTIVE ]
*Asset synthesis and kernel operations.*
-   **`forge`**: The synthesis engine. Generates hot-swappable TOML prompts and Python MCP servers via iterative AST refinement and the "Healer Loop."
-   **`system`**: Kernel operations. Includes the Neural TUI Dashboard, kernel configuration, and full-state snapshots (backups).

---

## 🛠 Core Components: The Forge & The Swarm

### 1. The Forge Workflow (Extraction Engine)
The extraction core (`clide/`) operates as a self-healing pipeline:
1.  **Pattern Detection:** Monitors history for repetitive intents (e.g., asking for the same refactor 3 times).
2.  **Intent Classification:** Categorizes insights into `COMMAND`, `FACT`, `DISCOVERY`, `LESSON`, or `TODO`.
3.  **Security Audit:** Proposed assets are scanned for dangerous shell commands or secret exposure before synthesis.
4.  **AST Evolution:** Iteratively refines the Abstract Syntax Tree of generated code to ensure idiomatic output.
5.  **Healer Loop:** Automated dry-runs fix `ImportError` or `SyntaxError` issues before final registration.

### 2. The Agent Swarm (`swarm/`)
The library of generated tools and their persistent execution state:
-   **Production Assets:** Includes the "Big Five" core tools: `engineer` (coding), `dev` (implementation), `bug` (debugging), `review` (auditing), and `plan` (architecting).
-   **Project Atlas:** The centralized state manager in `swarm/core/` that allows agents to maintain context across disconnected sessions.
-   **V2 Plugin Ecosystem**: features 70+ specialized plugins across domains from **Blockchain/Web3** and **LLM-Dev** to **Quantitative Trading** and **Systems Programming**.

---

## 🚦 Operational Protocols (The Zero-Series)
CLIDE agents follow the "Zero-Series" protocols—a set of stateless behavioral directives that ensure absolute engineering rigor.

| Persona | Protocol | Focus Domain | Primary Goal |
| :--- | :--- | :--- | :--- |
| `STRATEGIST-ZERO` | **2.1** | Innovation Funnels | Concept validation and unconstrained exploration. |
| `TPM-ZERO` | **2.2** | Roadmap & State | Managing milestones and dependency mapping. |
| `DEV-ZERO` | **2.1** | Implementation | High-fidelity coding and TUI design. |
| `SRE-ZERO` | **1.2** | Incident Response | Deep root cause analysis (RCA) and hotfixing. |
| `AUDITOR-ZERO` | **3.1** | Knowledge Review | Documentation auditing and vision alignment. |
| `GOVERNOR-ZERO` | **3.2** | Alignment | Revision of instructions and agent evolution. |

---

## 🧠 Smart Integration Features
-   **Fact Injection:** Every synthesized tool automatically inherits the 10 most relevant facts from the Project Brain via RAG.
-   **TODO Synchronization:** Any detected task is simultaneously saved to `memory.db` and appended to the local `todo.md`.
-   **Hotswapping:** Live-swappable agent personas and tool capabilities via `./clide activate` and `./clide hotswap`.
-   **Self-Healing (Healer Loop):** Generated MCP servers undergo automated dry-runs and self-repair logic before deployment.
-   **Neural Parity Status:** Currently tracking ~800 consolidated unique command intents with 52%+ total kernel saturation.

---

## 🎨 Visualization & Dashboarding
CLIDE provides multiple high-fidelity interfaces for interacting with the Project Brain:
-   **Neural TUI Dashboard (`./clide system dash`)**: A dense, real-time dashboard displaying kernel health, worker status, and recent ingestion metrics.
-   **ATLAS Navigator**: A web-based SPA (`viz/`) that provides a modern, searchable interface for all project protocols.
-   **The Galaxy View**: A 3D Force-Directed graph of the Project Brain, visualizing the complex web of facts and their semantic relationships.

---

## 💻 Technical Stack
-   **Language:** Python 3.12+ (Optimized for Android/Termux)
-   **Persistence:** SQLite 3 (Knowledge Graph) + JSONB (Vector Metadata)
-   **Intelligence:** Google Gemini (2.0 Flash / Pro)
-   **Frontend:** Textual (TUI), Rich (CLI), FastAPI (Web API)
-   **Libraries:** NumPy (Math), Asciimatics (Animation), Pydantic (Validation).

---

## 🚀 Quick Start & Sector Command Reference

### Sector 01: Sensory (Input)
```bash
./clide watch start          # Launch background interaction monitor
./clide probe scout <url>    # targeted deep-extraction from URL
```

### Sector 02: Cognitive (Retrieval)
```bash
./clide search "V14 formula" # Semantic retrieval from Project Brain
./clide brain summary       # Generate executive progress report
./clide map galaxy          # Launch 3D Force-Graph visualization
```

### Sector 03: State (Control)
```bash
./clide memory list         # View recent knowledge units
./clide run plan            # Prioritize tasks via session mapping
./clide maintain audit      # Execute kernel integrity check
```

### Sector 04: Executive (Synthesis)
```bash
./clide forge tool --new    # Synthesize a new Python/MCP tool
./clide system dash         # Launch real-time Neural TUI Dashboard
```

---
## 📅 Roadmap: The Path to v1.0
-   [ ] **Phase 1: Cognitive Saturation:** Ingest remaining project history to reach 100% kernel saturation.
-   [ ] **Phase 2: Autonomous Synthesis:** Move from *suggesting* commands to *auto-drafting* and *self-testing* entire module refactors.
-   [ ] **Phase 3: Mesh-Ready Containers:** Wrap Grouped Logic into encrypted SPX containers for decentralized mesh-readiness.

---
*Identity: CLIDE v0.7.0 - "The 1.5M Brain Ingestion"*
*Full Documentation: [The In-Depth Manual](manual.md) | [Operational Protocols](protocols.md) | [ATLAS Reference](atlas.md)*

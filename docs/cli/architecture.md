# ARCHITECTURE // SYSTEM DESIGN

CLIDE is built on the **Single Purpose Architecture (SPA)** pattern, emphasizing strict domain isolation and unidirectional data flow. This modularity ensures that intelligence layers can be upgraded or replaced without compromising the core persistence engine.

### Structural Domains (The Sectors)
The system is divided into four high-level sectors, each containing specialized modules:

<card>
title: DOMAIN REGISTRY
Sensory: watch, probe (Data Ingestion)
Cognitive: brain, index, map (Processing & Retrieval)
State: memory, run, maintain (Persistence & Execution)
Executive: forge, system (Synthesis & Operations)
</card>

### The Intelligence Pipeline
Data flows through the system in a linear, predictable sequence:

1.  **SENSORY [WATCH/PROBE]**: Detects external changes (filesystem events, URL scouts, clipboard captures) and extracts raw text.
2.  **COGNITIVE [BRAIN]**: Analyzes raw input using LLM synthesis to classify intent into SPA categories (FACT, TODO, LESSON).
3.  **PERSISTENCE [KERNEL]**: Saves the formalized knowledge to the SQLite `memory.db` via `storage.py`.
4.  **INDEXING [INDEX]**: Generates a 768D semantic embedding using `gemini-embedding-001` and anchors it in `vector_registry.json`.
5.  **MANUFACTURING [FORGE]**: Synthesizes functional Python/MCP tools based on project context and stored knowledge.
6.  **ACTUATION [TOOLS]**: Executes the forged capabilities, providing immediate feedback to the user or system.

### Technical Implementation
*   **Decoupled Logic**: Modules communicate via standardized APIs in the `kernel` and `brain` packages.
*   **Hot-Swapping**: New logic can be injected into the `swarm/` directory and indexed in real-time without restarting the core daemon.
*   **Documentation-Driven**: The system interface (CLI help and Atlas Navigator) is generated directly from these Markdown files, ensuring parity between documentation and code reality.

### Module Map
- `clide/kernel/`: SQLite schema management and configuration.
- `clide/brain/`: LLM integration, semantic clustering, and relationship mapping.
- `clide/watch/`: Real-time filesystem observers and log enrichment.
- `clide/forge/`: AST-aware code synthesis and testing.
- `clide/serve/`: TUI rendering, help systems, and visualization APIs.
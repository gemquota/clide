# CLIDE // ROOT DOCUMENTATION

## Tier: Basic
CLIDE // FUNCTIONAL ARCHITECTURE
CLIDE implements the Single Purpose Architecture (SPA) to isolate functional domains.
- Sensory: watch/ and probe/ capture data streams.
- Cognitive: brain/ parses intent and manages 768D vector memory.
- Manufacturing: forge/ synthesizes agentic assets (MCP/TOML).
- Executive: auto/ and manual/ handle orchestration and overrides.
- Persistence: kernel/ manages the SQLite 'memory.db' ground truth.
Usage: ./cli <domain> <command> [args]

## Tier: More
CLIDE // FUNCTIONAL ARCHITECTURE
CLIDE implements the Single Purpose Architecture (SPA) to isolate functional domains.
- Sensory: watch/ and probe/ capture data streams.
- Cognitive: brain/ parses intent and manages 768D vector memory.
- Manufacturing: forge/ synthesizes agentic assets (MCP/TOML).
- Executive: auto/ and manual/ handle orchestration and overrides.
- Persistence: kernel/ manages the SQLite 'memory.db' ground truth.
Usage: ./cli <domain> <command> [args]

CLIDE // THE TOTAL SPA ENCYCLOPEDIA
=========================================

1. CONCEPTUAL GROUNDING
-----------------------
The "Database: Everything" philosophy treats all project interaction as a searchable artifact.
Passive monitoring ensures that no detail is lost to ephemeral memory.

2. DOMAIN DEEP-DIVE
-------------------
[DOMAIN 01] KERNEL (GROUND TRUTH)
- Path: clide/kernel/
- Responsibility: Persistence, Config, and Logic Routing.
- Schema: SQLite handles relational knowledge; JSON handles high-speed vector registry.

[DOMAIN 02] BRAIN (INTELLIGENCE)
- Path: clide/brain/
- Responsibility: Semantic vectorization (768D) and LLM-driven intent classification.
- Pipeline: raw_text -> embed_content -> cosine_similarity -> router.

[DOMAIN 03] WATCH (SENSORY)
- Path: clide/watch/
- Responsibility: Real-time event-driven ingestion.
- Mechanism: Python-Watchdog observers monitor mtime changes in temp log files.

[DOMAIN 04] FORGE (MANUFACTURING)
- Path: clide/forge/
- Responsibility: Asset synthesis.
- Workflow: Detect Intent -> Code Generator -> Pytest Verification -> Indexing.

[DOMAIN 05] TOOLS (ACTUATORS)
- Path: clide/tools/
- Responsibility: External state modification.
- Action: Hotswapping Gemini settings and committing assets to Git.

[DOMAIN 06] SERVE (INTERFACES)
- Path: clide/serve/
- Responsibility: User interaction surfaces (CLI/Web).

3. LOGIC PATHWAYS (PASSIVE INGESTION)
--------------------------------------
1. Watchdog detects filesystem event in /tmp/logs.json.
2. Ingestor reads new lines and sends to clide.brain.reason.
3. Classifier returns category (e.g. FACT).
4. Storage engine vectorizes content (768D) and saves to memory.db.
5. Ingestion reports are updated in ingestion_logs/.

## Tier: Full
CLIDE // FUNCTIONAL ARCHITECTURE
CLIDE implements the Single Purpose Architecture (SPA) to isolate functional domains.
- Sensory: watch/ and probe/ capture data streams.
- Cognitive: brain/ parses intent and manages 768D vector memory.
- Manufacturing: forge/ synthesizes agentic assets (MCP/TOML).
- Executive: auto/ and manual/ handle orchestration and overrides.
- Persistence: kernel/ manages the SQLite 'memory.db' ground truth.
Usage: ./cli <domain> <command> [args]

CLIDE // THE TOTAL SPA ENCYCLOPEDIA
=========================================

1. CONCEPTUAL GROUNDING
-----------------------
The "Database: Everything" philosophy treats all project interaction as a searchable artifact.
Passive monitoring ensures that no detail is lost to ephemeral memory.

2. DOMAIN DEEP-DIVE
-------------------
[DOMAIN 01] KERNEL (GROUND TRUTH)
- Path: clide/kernel/
- Responsibility: Persistence, Config, and Logic Routing.
- Schema: SQLite handles relational knowledge; JSON handles high-speed vector registry.

[DOMAIN 02] BRAIN (INTELLIGENCE)
- Path: clide/brain/
- Responsibility: Semantic vectorization (768D) and LLM-driven intent classification.
- Pipeline: raw_text -> embed_content -> cosine_similarity -> router.

[DOMAIN 03] WATCH (SENSORY)
- Path: clide/watch/
- Responsibility: Real-time event-driven ingestion.
- Mechanism: Python-Watchdog observers monitor mtime changes in temp log files.

[DOMAIN 04] FORGE (MANUFACTURING)
- Path: clide/forge/
- Responsibility: Asset synthesis.
- Workflow: Detect Intent -> Code Generator -> Pytest Verification -> Indexing.

[DOMAIN 05] TOOLS (ACTUATORS)
- Path: clide/tools/
- Responsibility: External state modification.
- Action: Hotswapping Gemini settings and committing assets to Git.

[DOMAIN 06] SERVE (INTERFACES)
- Path: clide/serve/
- Responsibility: User interaction surfaces (CLI/Web).

3. LOGIC PATHWAYS (PASSIVE INGESTION)
--------------------------------------
1. Watchdog detects filesystem event in /tmp/logs.json.
2. Ingestor reads new lines and sends to clide.brain.reason.
3. Classifier returns category (e.g. FACT).
4. Storage engine vectorizes content (768D) and saves to memory.db.
5. Ingestion reports are updated in ingestion_logs/.

CLIDE // ADVANCED ARCHITECTURAL KERNEL [2.13x EXPANSION]
========================================================================

1. KERNEL SYSTEM SCHEMA (SQLite3)
---------------------------------
The permanent memory is stored in 'clide/memory.db' with the following structural constraints:
- knowledge: Primary unit storage.
  * embedding (BLOB): 768D Float32 JSON-encoded binary.
  * importance (INT): Range 1-10 (Weighted prioritization).
  * category (TEXT): {FACT, TODO, DISCOVERY, LESSON, NEW_COMMAND, MATCH, BUG, ERROR}.
  * review (TEXT): Stores LLM reasoning and semantic tags.
- relationships: Directed graph edges.
  * rel_type: {DEPENDS_ON, SIMILAR_TO, CONTRADICTS, BLOCKS}.

2. SEMANTIC VECTOR SPACE (768D)
--------------------------------
The 'vector_registry.json' acts as a high-speed k-NN index.
- Model: models/gemini-embedding-001.
- Precision: Normalized Cosine Similarity [-1.0, 1.0].
- Activation Threshold: >0.85 for auto-triggers; >0.35 for query results.
- Performance: Registry uses atomic 'temp-write-hotswap' pattern to prevent JSON corruption during mass ingestion.

3. THE CONSOLIDATION PROTOCOL (Phase 4)
---------------------------------------
Data follows a strictly tiered lifecycle from Sensory to Cognitive:
A. VOLATILE (Raw Logs): /tmp/logs.json (Discarded after session).
B. ENRICHED (Telemetry): clide/enriched_logs.json (Aggregated JSON history).
C. PERMANENT (Neural): clide/memory.db (The Ground Truth).
D. INDEXED (Registry): vector_registry.json (Searchable anchors).

4. INTENT CLASSIFICATION PIPELINE
---------------------------------
The brain uses a multi-shot prompt structure located in 'brain/reason.py':
1. Input Extraction: Strips shell noise and system boilerplate.
2. Context Injection: Injects recent 5 nodes for temporal continuity.
3. Logical Inference: Maps text to one of 8 SPA categories.
4. Payload Generation: Returns structured JSON for storage injection.

5. FORGE MANUFACTURING LOGIC
-----------------------------
Tool synthesis is gated by the 'Verification Protocol':
- Intent -> Blueprint (spec.md) -> Asset (.py) -> Test (test_.py).
- Deployment: FastMCP servers are automatically indexed into the registry upon successful 'pytest' passing.
- Evolution: 'evolve' command uses AST parsing to preserve function signatures while rewriting logic.

6. COMMAND ROUTING & PORTAL INTERCEPTION
----------------------------------------
Internal dispatch flow:
[USER] -> ./cli (portal.py) -> Interceptor (guide.py) -> Domain Handler -> persistence.
Shortcut Logic: 'dash', 'cli', 'atlas', 'ref', and 'map' are intercepted at the root level to minimize latency.
Default: Running without arguments triggers the Cyber-Dashboard (TUI).

# CLIDE // COMMAND ATLAS
The master architectural mapping of the CLIDE intelligence-operating system.
Accessible via: ./cli {ref, atlas, map}

## Tier: Basic
TOTAL SYSTEM COMMAND TREE // FUNCTIONAL MAP
========================================================================
cli
├── watch ............. Passive background log/shell monitoring
│   ├── start ......... Launch the Watchdog extractor
│   ├── stop .......... Terminate background extraction
│   ├── status ........ Health and PID verification
│   └── logs .......... Tail the enriched ingestion stream
├── probe ............. Active targeted data ingestion
│   ├── scout ......... Single-URL deep analysis
│   ├── manual ........ Selective file-based extraction
│   ├── capture ....... Snapshot current system state
│   └── crawl ......... Recursive web-domain ingestion
├── brain ............. Cognitive intent and vector memory
│   ├── query ......... Semantic search across all knowledge
│   ├── graph ......... Generate Mermaid/HTML relationship maps
│   ├── merge ......... Consolidate enriched logs into DB
│   ├── cloud ......... Dynamic Word Cloud {--live|--html}
│   ├── analyze ....... Run LLM synthesis on specific clusters
│   ├── summary ....... Generate executive project reports
│   ├── audit ......... Verify data integrity and conflict detection
│   ├── verify ........ Validation of stored facts
│   ├── list .......... Enumerate recent knowledge units
│   ├── connect ....... Manually link semantic nodes
│   └── forget ........ Selective memory deletion
├── index ............. 768D Vector Space Lifecycle
│   ├── full .......... Global vector rebuild
│   ├── near .......... Find nearest semantic neighbors
│   ├── trace ......... Track unit provenance
│   ├── cluster ....... Identify knowledge hotspots
│   ├── prune ......... Evict low-importance nodes
│   ├── optimize ...... Deduplicate and sort registry
│   └── stat .......... Dimensionality and volume telemetry
├── auto .............. Autonomous orchestration
│   ├── tag ........... Automatic node categorization
│   ├── plan .......... Generate prioritized task strategies
│   ├── sync .......... Harmonize todo.md with memory.db
│   ├── audit ......... Self-correcting kernel integrity
│   └── clean ......... Automated metadata sanitization
├── dash/cli .......... Neural-Kernel Command Center Dashboard
├── system ............ Root system status and config
│   ├── status ........ Standardized ingestion telemetry
│   └── config ........ Kernel settings management
├── manual ............ Human intervention and CRUD
│   ├── node .......... CRUD operations on knowledge units
│   ├── task .......... Direct todo/strategy management
│   ├── config ........ View/Modify system kernel settings
│   └── asset ......... Direct registry/file management
└── forge ............. Agentic asset and tool synthesis
    ├── tool .......... Synthesize new Python/MCP tools
    ├── evolve ........ Iterative refinement of existing tools
    ├── design ........ UI/UX layout generation
    ├── skill ......... Create new modular capabilities
    ├── persona ....... Define specialized agentic identities
    ├── test .......... Automated tool validation
    ├── bench ......... Performance and logic benchmarking
    └── archive ....... Safe storage of deprecated assets

## Tier: More
TOTAL SYSTEM COMMAND TREE // TECHNICAL MAP [INCLUSIVE]
========================================================================
cli
├── watch (Sensory Stream)
│   ├── start ......... Launch monitor [Watchdog Core]
│   ├── stop .......... Terminate process [SIGTERM]
│   ├── status ........ PID & Health metrics
│   └── logs .......... Tail enriched logs [768D Enriched]
├── probe (Targeted Extraction)
│   ├── scout ......... Single URL analysis [LLM Synthesis]
│   ├── manual ........ Local file extraction [Regex/Buffer]
│   ├── capture ....... Clipboard ingest [Termux-API]
│   └── crawl ......... Recursive site ingest [Depth-Limited]
├── brain (Cognitive Engine)
│   ├── query ......... Semantic search [768D Cosine Similarity]
│   ├── graph ......... Relationship maps [Mermaid/Force-Graph]
│   ├── merge ......... Consolidate telemetry [Log -> DB/Registry]
│   ├── cloud ......... Dynamic visualization [Live TUI / D3.js]
│   ├── analyze ....... Retroactive processing [Deep Context]
│   ├── summary ....... Executive reports [Multi-Session]
│   ├── audit ......... Integrity verification [Conflict Resolving]
│   ├── verify ........ Fact validation [Source Checking]
│   ├── list .......... Recent units [Chronological]
│   ├── connect ....... Manual node linking [Relational]
│   └── forget ........ Memory deletion [Permanent]
├── index (Vector Lifecycle)
│   ├── full .......... Total vector rebuild [Models/Gemini-001]
│   ├── near .......... Find similar units [k-NN Search]
│   ├── trace ......... Show provenance [Lineage Tracking]
│   ├── cluster ....... Identify hotspots [Density-Based]
│   ├── prune ......... Evict low-imp nodes [Importance <= 3]
│   ├── optimize ...... Deduplicate registry [ID-Hotswap]
│   └── stat .......... System telemetry [Volume/Dimensionality]
├── auto (Strategic Orchestration)
│   ├── tag ........... Automatic node tagging [Classifier-Based]
│   ├── plan .......... Prioritize tasks [Impact/Effort Mapping]
│   ├── sync .......... Todo/DB sync [Bidirectional]
│   ├── audit ......... Kernel integrity check [Conflict Analysis]
│   └── clean ......... Metadata sanitization [Z-Score Outliers]
├── dash / cli (Neural Dashboard)
│   └── [DEFAULT] ..... Launch the Cyber-Kernel Command Center
├── system (Kernel Status)
│   ├── status ........ Ingestion telemetry [Spectral Table]
│   └── config ........ Kernel settings management [TUI]
├── manual (Human Override)
│   ├── node .......... CRUD units [Knowledge Access]
│   ├── task .......... Strategy management [Todo Control]
│   ├── config ........ Settings access [Kernel Settings]
│   └── asset ......... Registry management [File Control]
└── forge (Agentic Synthesis)
    ├── tool .......... Synthesize tools [Python/MCP]
    ├── evolve ........ Refine assets [Iterative/AST]
    ├── design ........ UI/UX layout generation [Rich/HTML]
    ├── skill ......... Create capabilities [Modular]
    ├── persona ....... Define identities [System Prompts]
    ├── test .......... Automated validation [Pytest]
    ├── bench ......... Performance testing [Latency/Tokens]
    └── archive ....... Asset deprecation [Safe-Store]

## Tier: Full
TOTAL SYSTEM COMMAND TREE // ARCHITECTURAL MAP [SPA KERNEL]
========================================================================
cli
├── watch (Sensory Stream)
│   ├── start ......... Launch monitor [Watchdog Core]
│   ├── stop .......... Terminate process [SIGTERM]
│   ├── status ........ PID & Health metrics
│   └── logs .......... Tail enriched logs [768D Enriched]
├── probe (Targeted Extraction)
│   ├── scout ......... Single URL analysis [LLM Synthesis]
│   ├── manual ........ Local file extraction [Regex/Buffer]
│   ├── capture ....... Clipboard ingest [Termux-API]
│   └── crawl ......... Recursive site ingest [Depth-Limited]
├── brain (Cognitive Engine)
│   ├── query ......... Semantic search [768D Cosine Similarity]
│   ├── graph ......... Relationship maps [Mermaid/Force-Graph]
│   ├── merge ......... Consolidate telemetry [Log -> DB/Registry]
│   ├── cloud ......... Dynamic visualization [Live TUI / D3.js]
│   ├── analyze ....... Retroactive processing [Deep Context]
│   ├── summary ....... Executive reports [Multi-Session]
│   ├── audit ......... Integrity verification [Conflict Resolving]
│   ├── verify ........ Fact validation [Source Checking]
│   ├── list .......... Recent units [Chronological]
│   ├── connect ....... Manual node linking [Relational]
│   └── forget ........ Memory deletion [Permanent]
├── index (Vector Lifecycle)
│   ├── full .......... Total vector rebuild [Models/Gemini-001]
│   ├── near .......... Find similar units [k-NN Search]
│   ├── trace ......... Show provenance [Lineage Tracking]
│   ├── cluster ....... Identify hotspots [Density-Based]
│   ├── prune ......... Evict low-imp nodes [Importance <= 3]
│   ├── optimize ...... Deduplicate registry [ID-Hotswap]
│   └── stat .......... System telemetry [Volume/Dimensionality]
├── auto (Strategic Orchestration)
│   ├── tag ........... Automatic node categorization
│   ├── plan .......... Prioritize tasks [Importance/Session Mapping]
│   ├── sync .......... Harmonize todo.md with memory.db
│   ├── audit ......... Self-correcting kernel integrity
│   └── clean ......... Automated metadata sanitization
├── dash / cli (Neural Dashboard)
│   └── [DEFAULT] ..... Launch the Cyber-Kernel Command Center
├── system (Kernel Status)
│   ├── status ........ Standardized ingestion telemetry
│   └── config ........ Kernel settings management
├── manual (Human Override)
│   ├── node .......... CRUD units [Knowledge Access]
│   ├── task .......... Strategy management [Todo Control]
│   ├── config ........ Settings access [Kernel Settings]
│   └── asset ......... Registry management [File Control]
└── forge (Agentic Synthesis)
    ├── tool .......... Synthesize tools [Python/MCP]
    ├── evolve ........ Refine assets [Iterative/AST]
    ├── design ........ UI/UX layout generation [Rich/HTML]
    ├── skill ......... Create capabilities [Modular]
    ├── persona ....... Define identities [System Prompts]
    ├── test .......... Automated tool validation [Pytest]
    ├── bench ......... Performance testing [Execution Timings]
    └── archive ....... Safe storage of deprecated assets

[SPA ARCHITECTURAL ROUTING]
Internal dispatch flow: 
PORTAL (portal.py) -> Interceptor (guide.py) -> Handler (domain logic) -> Persistence (kernel/storage.py)
All domain-specific documentation is co-located with functional code to ensure 1:1 parity between logic and definition.
The Command Atlas serves as the global registry used by the Intent Classifier to route user requests.

[SEMANTIC INTERACTION PROTOCOLS]
CLIDE operates on three distinct layers of semantic depth:
1. SENSORY (watch/probe) : High-frequency data ingestion.
2. COGNITIVE (brain/index) : Contextual synthesis and vector mapping.
3. EXECUTIVE (auto/manual/forge) : Strategic execution and asset manufacturing.

Each command in the Atlas is mapped to a 768D vector space, allowing the system to understand natural language intent even when the exact command syntax is not known.
This enables "Fuzzy Execution" where CLIDE can suggest or auto-correct commands based on observed user behavior and historical performance.

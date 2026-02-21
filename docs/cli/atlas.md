# [ SECTOR 01: SENSORY ] ───────────────────────────────────────────────
cli
├── watch (Sensory Stream)
│   ├── go ............ Launch monitor [Watchdog Core]
│   ├── off ........... Terminate [SIGTERM]
│   ├── status ........ PID & Health metrics
│   ├── progress ...... Ingestion metrics & status
│   └── logs .......... Tail enriched logs [768D]
└── probe (Targeted Extraction)
    ├── scout ......... Single URL analysis [LLM Synthesis]
    ├── ingest ........ Local file / buffer extraction
    ├── capture ....... Clipboard / Termux-API ingest
    └── crawl ......... Recursive site ingest [Depth-Limited]

# [ SECTOR 02: COGNITIVE ] ─────────────────────────────────────────────
cli
├── search ............ Unified semantic + k-NN retrieval
├── brain (Cognitive Engine)
│   ├── analyze ....... Retroactive deep context
│   ├── summary ....... Executive multi-session reports
│   └── verify ........ Fact validation + source checking
├── map (Topology)
│   ├── graph ......... Relationship maps [Mermaid / Force-Graph]
│   ├── cloud ......... Dynamic TUI / D3.js visualisation
│   └── trace ......... Full provenance & lineage
└── index (Vector Lifecycle)
    ├── rebuild ....... Total rebuild [Gemini-001 / current model]
    ├── cluster ....... Density-based hotspot detection
    ├── prune ......... Evict low-importance nodes (≤ 3)
    ├── optimize ...... Deduplicate + ID hot-swap
    └── stats ......... Volume / dimensionality telemetry

# [ SECTOR 03: STATE ] ─────────────────────────────────────────────────
cli
├── memory (State Management)
│   ├── list .......... Recent units [chronological]
│   ├── create ........ Manual node init
│   ├── edit .......... Contextual CRUD
│   ├── delete ........ Soft-delete
│   ├── connect ....... Manual relational linking
│   ├── merge ......... Log → DB consolidation
│   └── forget ........ Hard-delete
├── run (Strategic Layer)
│   ├── plan .......... Prioritise tasks [importance/session map]
│   ├── task .......... Todo / strategy control
│   └── sync .......... Harmonise todo.md ↔ memory.db
└── maintain (Hygiene)
    ├── tag ........... Auto-categorisation
    ├── clean ......... Metadata sanitisation
    └── audit ......... Self-correcting kernel integrity

# [ SECTOR 04: EXECUTIVE ] ─────────────────────────────────────────────
cli
├── forge (Agentic Synthesis)
│   ├── tool .......... Synthesise Python / MCP tools
│   ├── evolve ........ Iterative AST refinement
│   ├── design ........ UI/UX (Rich / HTML)
│   ├── skill ......... Modular capability creation
│   ├── persona ....... System-prompt identities
│   ├── test .......... Pytest validation
│   ├── bench ......... Execution timing benchmarks
│   └── archive ....... Safe deprecation storage
└── system (Kernel Ops)
    ├── dash .......... Neural TUI Dashboard
    ├── config ........ Kernel settings
    ├── asset ......... Registry / file control
    ├── health ........ Standardised ingestion telemetry
    ├── backup ........ Full-state snapshot
    └── resume ........ Session context restoration

MENU_STRUCTURE = {
    "SENSORY": {
        "watch": {
            "go": "Start monitoring Gemini log streams for autonomous ingestion",
            "off": "Deactivate background log monitor and cleanup PID",
            "status": "Check operational status of the log monitor",
            "logs": "Tail enriched ingestion logs with optional limit and follow",
            "progress": "Show high-level ingestion progress from monitor history"
        },
        "probe": {
            "scout": "Scout a specific URL for metadata and initial context",
            "ingest": "Manually ingest facts and insights from a local file",
            "capture": "Extract knowledge from system clipboard (Termux:API)",
            "crawl": "Recursively crawl a website for knowledge extraction"
        }
    },
    "COGNITIVE": {
        "brain": {
            "analyze": "Perform retroactive deep context processing on unlinked facts",
            "summary": "Generate executive brain state and session reports",
            "verify": "Validate fact consistency, source checking, and trust scores",
            "approve": "Review and formalize pending command and fact proposals"
        },
        "search": "Semantic vector search across knowledge base and registry",
        "map": {
            "graph": "Render neural relationship graph in ASCII or Mermaid format",
            "cloud": "Generate command and concept word clouds (Static/HTML/Live)",
            "trace": "Trace lineage and relationships of a specific node",
            "stats": "Show global knowledge distribution and telemetry"
        },
        "index": {
            "rebuild": "Re-index all brain nodes from raw storage (API intensive)",
            "archives": "Rebuild long-term ingestion archives from history",
            "cluster": "Identify and label semantic clusters within the registry",
            "optimize": "Deduplicate and sort vector registry for peak performance",
            "prune": "Remove low-importance or stale knowledge units",
            "stats": "Show detailed telemetry on registry health and distribution"
        }
    },
    "STATE": {
        "memory": {
            "list": "List recent knowledge units with optional limit",
            "create": "Manually create a new knowledge node with category and tags",
            "edit": "Modify content or metadata of an existing node",
            "delete": "Soft-delete a node (mark as inactive)",
            "forget": "Permanently purge a node from storage",
            "connect": "Establish a neural link between two knowledge nodes",
            "merge": "Deduplicate and merge scattered ingestion logs into memory"
        },
        "run": {
            "plan": "Auto-prioritize system tasks based on brain state",
            "task": "Manage system todo list (list, add, remove, complete)",
            "sync": "Synchronize brain state with external task trackers"
        },
        "maintain": {
            "tag": "Auto-tag nodes via LLM analysis of content",
            "clean": "Sanitize and normalize metadata fields across the brain",
            "audit": "Run brain integrity and redundancy audit",
            "strategist": "Execute the high-level strategist agent for system assessment"
        }
    },
    "EXECUTIVE": {
        "forge": {
            "tool": "Synthesize a new autonomous MCP tool or script",
            "evolve": "Iteratively refine an existing asset via LLM evolution",
            "design": "Generate blueprint designs and ASCII mockups",
            "skill": "Create a new modular skill for the agent swarm",
            "persona": "Define a new system-prompt persona and directive",
            "test": "Run verification tests for a forged asset",
            "bench": "Benchmark asset execution performance and latency",
            "archive": "Safely archive a forged asset to historical storage"
        },
        "system": {
            "dash": "Launch the interactive neural-kernel management dashboard",
            "config": "View current kernel configuration and path settings",
            "health": "Check system health and database integrity",
            "backup": "Create a full-state timestamped backup of the brain",
            "resume": "Resume the last cognitive session (Dashboard load)",
            "asset": "Show system-wide statistics for all synthesized assets"
        },
        "dash": "Direct alias to launch the system dashboard (Executive Hub)"
    }
}


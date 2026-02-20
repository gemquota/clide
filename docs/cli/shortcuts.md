# SHORTCUTS // POWER USER REFERENCE

Efficiency in CLIDE is achieved by combining domain-specific commands into cohesive workflows. This document outlines common shortcuts, aliases, and "Power-Workflows" used for advanced project management.

### Common Aliases
The CLI includes several top-level aliases for frequently used commands:

<card>
title: COMMAND SHORTCUTS
dash: ./cli system dash (TUI Dashboard)
help: ./cli help (Intelligence Portal)
atlas: ./cli atlas (Structural Map)
? [query]: ./cli search [query]
</card>

### Power-User Workflows

#### 1. The Synthesis Gate (Build & Verify)
Rapidly create a tool and ensure it's production-ready in one sequence:
`./cli forge tool <name> <prompt> && ./cli forge test <name>`
*(Note: Successful tool synthesis automatically triggers testing and indexing).*

#### 2. The Maintenance Cycle (Total System Hygiene)
Run this sequence weekly to keep the brain clean and the registry optimized:
`./cli maintain audit && ./cli maintain clean && ./cli index optimize`
- **Audit**: Detects semantic collisions.
- **Clean**: Trims metadata and removes junk.
- **Optimize**: Deduplicates and sorts the vector registry.

#### 3. Strategic Execution
Synchronize your plan before starting a deep-work session:
`./cli auto plan && ./cli run sync && ./cli run task list`
- **Plan**: Ranks todos by project importance.
- **Sync**: Rebuilds `todo.md`.
- **List**: Displays your prioritized roadmap.

#### 4. The Ingestion Loop (Active Research)
Combine background monitoring with active data gathering:
`./cli watch go && ./cli probe scout "https://docs.api.com"`
- **Watch**: Monitors your terminal/filesystem.
- **Scout**: Performs deep LLM synthesis on documentation.

### Environment Control
- **`./cli system backup`**: Always run before major refactors.
- **`./cli system config`**: Quick check of API keys and pathing.
- **`./cli watch off`**: Silences the sensory monitor.

### System Overrides
- **`./cli memory forget <id>`**: Use this for sensitive data that should never be in the LLM context.
- **`./cli index rebuild`**: Forces a fresh ingestion of shell history.
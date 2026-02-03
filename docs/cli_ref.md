# CLIDE CLI Reference

This document provides a comprehensive reference for the CLIDE (Command Line Interface - Database: Everything) command-line utility.

## Usage
```bash
./clide <command> [arguments]
```

## Primary Commands

### `monitor` (Default)
Activates the live ingestion and extraction loops.
- **Neural Stream**: Monitors chat logs for high-value workflows and knowledge.
- **Operational Stream**: Monitors shell history for complex command patterns.
- **Usage**: `./clide` or `./clide monitor`

### `list`
Displays a grouped summary of all assets currently indexed in the vector registry.
- **Usage**: `./clide list`

### `search <query>`
Performs a semantic (vector-based) search across all integrated assets.
- **Arguments**: `<query>` - The search term or natural language request.
- **Usage**: `./clide search "calculate file hash"`

### `activate` | `mount`
Retrieves and displays the operational instructions for a specific asset without modifying the system state.
- **Arguments**: `<asset_id>` - The ID of the skill, agent, or command (e.g., `skill:conductor:track-management`).
- **Usage**: `./clide activate skill:conductor:track-management`

### `hotswap`
Dynamically installs or enables an asset within the Gemini CLI environment.
- **Skills**: Installs the skill to the project scope and enables it.
- **Agents**: Displays the agent persona and provides instructions for switching.
- **Arguments**: `<asset_id>`
- **Usage**: `./clide hotswap skill:conductor:track-management`

### `dashboard`
Generates a Markdown-based visual registry (`docs/dashboard.md`) summarizing all assets, their types, and descriptions.
- **Usage**: `./clide dashboard`

## Maintenance & Intelligence

### `brain`
Visualizes the "Project Brain" (extracted knowledge).
- **Output**: Generates a Mermaid graph (`docs/brain_graph.mmd`) and renders an ASCII relationship map to the terminal.
- **Usage**: `./clide brain`

### `janitor`
Identifies overlapping or redundant tools in the registry and proposes merge plans to reduce system entropy.
- **Usage**: `./clide janitor`

### `why <asset_id>`
Displays the "Interaction Provenance"—the original chat snippet or shell sequence that triggered the creation of the tool.
- **Arguments**: `<asset_id>`
- **Usage**: `./clide why my-weather-tool`

### `rollback <asset_id>`
Uses the Git backend to revert a specific asset (and its associated memory state) to its previous version.
- **Arguments**: `<asset_id>`
- **Usage**: `./clide rollback my-weather-tool`

---
*CLIDE v0.6.0 Reference Guide*

# [ SECTOR 02: COGNITIVE ] - MAP
Topological mapping and relationship visualization of the system brain.

The `map` domain visualizes relationships, command clouds, and data provenance.

<card>
title: MAP OVERVIEW
Visuals: Graph, Cloud, Trace
Formats: Mermaid, HTML, TUI
Purpose: Relationship Analysis
Status: ONLINE
</card>

### Commands
*   **graph**: Generates a relationship map in Mermaid format (exported to `docs/brain_graph.mmd`).
*   **cloud**: Generates a dynamic command cloud (Live TUI or HTML).
*   **trace**: Shows the full provenance and lineage of a specific knowledge ID.

### Technical Specifications
Mapping leverages the metadata in the `Vector Registry` to build directional graphs.

<card>
title: OPERATIONAL CONTEXT
Graph: Mermaid.js / Force-Graph
Cloud: D3.js / rich.columns
Tracing: ID Provenance (UUID Lineage)
</card>

### Usage Examples
1. Generate Graph: `./cli map graph`
2. View Cloud (HTML): `./cli map cloud --html`
3. Trace Node: `./cli map trace [node_id]`

### Dependency Notes
`graph` requires `mermaid-cli` for image export. `cloud` --live requires a high-refresh rate terminal.

### Architecture Internals
The mapping engine utilizes `atlas.py` to extract relationships based on shared tags and similarity scores.

<card>
title: NEURAL-KERNEL HOOKS
Mapping Hook: clide.serve.atlas.generate_mermaid_graph
Cloud Hook: scripts.command_cloud.generate_live
Provenance Hook: clide.serve.atlas.trace_provenance
</card>

### API Hooks
*   `atlas.get_brain_data(limit)`: Raw node retrieval for mapping.
*   `command_cloud.generate_html(data)`: SPA component generation.

### Legacy Notes
Original map command was a simple directory `tree`. Now it is a full-scale neural topology.
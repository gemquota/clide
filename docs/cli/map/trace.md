# MAP TRACE

- Explains *why* a vector exists and what data it was derived from.
- Visualizes the semantic lineage of a knowledge node as a tree.
- Lists the timestamp, importance score, and source session.
Usage: ./cli map trace <id>

- Explains *why* a vector exists and what data it was derived from.
- Visualizes the semantic lineage of a knowledge node as a tree.
- Lists the timestamp, importance score, and source session.
Usage: ./cli map trace <id>

TECHNICAL DEEP-DIVE:
The 'trace' command provides 'Semantic Transparency' via a structured visualization.
1. Database Query: Fetches the target node from the SQLite `knowledge` table by ID.
2. Provenance Tree: Uses the `rich.tree` library to render a hierarchical view of the node's history.
3. Metadata Display: Shows critical attributes like category, timestamp, and importance.
4. Relationship Mapping: Queries the `relationships` table to display incoming and outgoing links (←/→) to other nodes.
Essential for auditing the 'Cognitive Pipeline' and understanding how knowledge is connected.

- Explains *why* a vector exists and what data it was derived from.
- Visualizes the semantic lineage of a knowledge node as a tree.
- Lists the timestamp, importance score, and source session.
Usage: ./cli map trace <id>

TECHNICAL DEEP-DIVE:
The `trace` command (mapped to `clide.serve.atlas.render_trace_tree`) constructs a forensic view of a knowledge unit.

### Logic Flow
1. **Node Retrieval:** Executes `SELECT * FROM knowledge WHERE id = ?`.
2. **Tree Construction:** Instantiates a `rich.tree.Tree` rooted at "PROVENANCE TRACE: Node #{id}".
3. **Metadata Branch:** Populates a subtree with `category`, `timestamp`, and `importance`.
4. **Source Branch:** Extracts and displays the `original_msg` (truncated to 100 chars) to show user intent.
5. **Relationship Branch:** Calls `db_manager.get_relationships(node_id)` to fetch adjacency data.
   - Renders directional arrows (`→` for outgoing, `←` for incoming) to visualize the local graph topology.

### Code Reference
- **Entry Point:** `clide/serve/portal.py` -> `cmd_map`
- **Implementation:** `clide/serve/atlas.py` -> `render_trace_tree`
- **Data Source:** `clide/kernel/storage.py` (SQLite `knowledge` & `relationships` tables)

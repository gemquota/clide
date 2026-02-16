# BRAIN GRAPH

## Tier: Basic
- Exports a 'brain_graph.mmd' file for Mermaid.js.
- Generates a 'brain_graph.html' for interactive 3D viewing.
- Visualizes the relationships between different facts and tools.
Usage: ./cli brain graph

## Tier: More
- Exports a 'brain_graph.mmd' file for Mermaid.js.
- Generates a 'brain_graph.html' for interactive 3D viewing.
- Visualizes the relationships between different facts and tools.
Usage: ./cli brain graph

TECHNICAL DEEP-DIVE:
The 'graph' command maps the logical connectivity of your project.
1. Node Collection: Fetches all nodes from the 'knowledge' table in SQLite.
2. Similarity Matrix: Uses NumPy to perform a vectorized cross-comparison of all 768D embeddings.
3. Edge Creation: Generates 'SIMILAR_TO' links if similarity > 0.85 and 'DEPENDS_ON' based on manual linking.
4. Output:
   - Mermaid: A TD graph representing categories as clusters.
   - HTML: A Force-Graph implementation for real-time physics-based exploration.
This provides an 'At-a-Glance' view of the semantic density of your project.

## Tier: Full
- Exports a 'brain_graph.mmd' file for Mermaid.js.
- Generates a 'brain_graph.html' for interactive 3D viewing.
- Visualizes the relationships between different facts and tools.
Usage: ./cli brain graph

TECHNICAL DEEP-DIVE:
The 'graph' command maps the logical connectivity of your project.
1. Node Collection: Fetches all nodes from the 'knowledge' table in SQLite.
2. Similarity Matrix: Uses NumPy to perform a vectorized cross-comparison of all 768D embeddings.
3. Edge Creation: Generates 'SIMILAR_TO' links if similarity > 0.85 and 'DEPENDS_ON' based on manual linking.
4. Output:
   - Mermaid: A TD graph representing categories as clusters.
   - HTML: A Force-Graph implementation for real-time physics-based exploration.
This provides an 'At-a-Glance' view of the semantic density of your project.

[EXPANSION PENDING]

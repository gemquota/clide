# BRAIN CONNECT

## Tier: Basic
- Creates a directed relationship between two nodes in the graph.
- Defaults to 'RELATED_TO', but can be configured for 'DEPENDS_ON'.
- Essential for manually mapping dependencies that the LLM might miss.
Usage: ./cli brain connect <id1> <id2>

## Tier: More
- Creates a directed relationship between two nodes in the graph.
- Defaults to 'RELATED_TO', but can be configured for 'DEPENDS_ON'.
- Essential for manually mapping dependencies that the LLM might miss.
Usage: ./cli brain connect <id1> <id2>

TECHNICAL DEEP-DIVE:
The 'connect' command modifies the 'relationships' table in the Kernel.
1. Validation: Verifies that both IDs exist in the 'knowledge' table.
2. Link Creation: Inserts a row mapping source_id to target_id.
3. Semantic Weight: Optionally calculates the similarity delta to justify the link.
4. Visualization: Newly created links will appear in the 'brain graph' output.
Allows the user to act as the 'Orchestrator' of project topology.

## Tier: Full
- Creates a directed relationship between two nodes in the graph.
- Defaults to 'RELATED_TO', but can be configured for 'DEPENDS_ON'.
- Essential for manually mapping dependencies that the LLM might miss.
Usage: ./cli brain connect <id1> <id2>

TECHNICAL DEEP-DIVE:
The 'connect' command modifies the 'relationships' table in the Kernel.
1. Validation: Verifies that both IDs exist in the 'knowledge' table.
2. Link Creation: Inserts a row mapping source_id to target_id.
3. Semantic Weight: Optionally calculates the similarity delta to justify the link.
4. Visualization: Newly created links will appear in the 'brain graph' output.
Allows the user to act as the 'Orchestrator' of project topology.

[EXPANSION PENDING]

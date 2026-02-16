# INDEX CLUSTER

## Tier: Basic
- Automatically identifies themes in your project (e.g. 'Database', 'Frontend', 'Tests').
- Lists IDs that belong to each cluster.
- Helps visualize the 'Semantic Breadth' of your current knowledge base.
Usage: ./cli index cluster

## Tier: More
- Automatically identifies themes in your project (e.g. 'Database', 'Frontend', 'Tests').
- Lists IDs that belong to each cluster.
- Helps visualize the 'Semantic Breadth' of your current knowledge base.
Usage: ./cli index cluster

TECHNICAL DEEP-DIVE:
The 'cluster' command implements unsupervised semantic grouping.
1. Normalization: Standardizes all 768D vectors for distance calculation.
2. Centroid Search: Uses K-Means (via SciPy if available, else simple distance logic) to find density centers.
3. Assignment: Maps every registry ID to its nearest centroid.
4. Naming: Sends the top 3 content snippets from each cluster to the LLM to generate a 'Cluster Name'.
Provides a high-level 'Conceptual Map' of the entire project repository.

## Tier: Full
- Automatically identifies themes in your project (e.g. 'Database', 'Frontend', 'Tests').
- Lists IDs that belong to each cluster.
- Helps visualize the 'Semantic Breadth' of your current knowledge base.
Usage: ./cli index cluster

TECHNICAL DEEP-DIVE:
The 'cluster' command implements unsupervised semantic grouping.
1. Normalization: Standardizes all 768D vectors for distance calculation.
2. Centroid Search: Uses K-Means (via SciPy if available, else simple distance logic) to find density centers.
3. Assignment: Maps every registry ID to its nearest centroid.
4. Naming: Sends the top 3 content snippets from each cluster to the LLM to generate a 'Cluster Name'.
Provides a high-level 'Conceptual Map' of the entire project repository.

[EXPANSION PENDING]

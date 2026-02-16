# BRAIN QUERY

## Tier: Basic
- Uses 768D vector similarity to find facts, not just keywords.
- Returns the 5 most relevant units from 'memory.db'.
- Best for finding 'How-to' notes or project environment details.
Usage: ./cli brain query <text>

## Tier: More
- Uses 768D vector similarity to find facts, not just keywords.
- Returns the 5 most relevant units from 'memory.db'.
- Best for finding 'How-to' notes or project environment details.
Usage: ./cli brain query <text>

TECHNICAL DEEP-DIVE:
The 'query' command is the primary RAG (Retrieval-Augmented Generation) entry point.
1. Vectorization: Converts your query string into a 768D embedding using Gemini-Embedding-001.
2. Search: Loads the 'vector_registry.json' into memory and calculates Cosine Similarity against all registered assets.
3. Ranking: Sorts results by similarity score (Default threshold: 0.35 for display).
4. Formatting: Outputs the content along with its ID, category, and importance.
This command allows you to 'ask' your project about its own history.

## Tier: Full
- Uses 768D vector similarity to find facts, not just keywords.
- Returns the 5 most relevant units from 'memory.db'.
- Best for finding 'How-to' notes or project environment details.
Usage: ./cli brain query <text>

TECHNICAL DEEP-DIVE:
The 'query' command is the primary RAG (Retrieval-Augmented Generation) entry point.
1. Vectorization: Converts your query string into a 768D embedding using Gemini-Embedding-001.
2. Search: Loads the 'vector_registry.json' into memory and calculates Cosine Similarity against all registered assets.
3. Ranking: Sorts results by similarity score (Default threshold: 0.35 for display).
4. Formatting: Outputs the content along with its ID, category, and importance.
This command allows you to 'ask' your project about its own history.

[EXPANSION PENDING]

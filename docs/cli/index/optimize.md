# INDEX OPTIMIZE

## Tier: Basic
- Re-saves the 'vector_registry.json' with optimal sorting and indentation.
- Removes orphaned vectors that no longer have source files or DB rows.
- Compresses the binary blobs in the registry if possible.
Usage: ./cli index optimize

## Tier: More
- Re-saves the 'vector_registry.json' with optimal sorting and indentation.
- Removes orphaned vectors that no longer have source files or DB rows.
- Compresses the binary blobs in the registry if possible.
Usage: ./cli index optimize

TECHNICAL DEEP-DIVE:
The 'optimize' command is a structural cleanup of the Registry file.
1. Orphan Scan: Cross-references every ID in the registry against the 'swarm/' folder and 'knowledge' table.
2. Compaction: Removes whitespace and unnecessary metadata fields from the JSON.
3. Sorting: Re-orders the file by ID to improve file-read speed during initialization.
4. Validation: Ensures the resulting file is syntactically valid JSON.
A 'Housekeeping' command to be run after massive ingestion or synthesis sessions.

## Tier: Full
- Re-saves the 'vector_registry.json' with optimal sorting and indentation.
- Removes orphaned vectors that no longer have source files or DB rows.
- Compresses the binary blobs in the registry if possible.
Usage: ./cli index optimize

TECHNICAL DEEP-DIVE:
The 'optimize' command is a structural cleanup of the Registry file.
1. Orphan Scan: Cross-references every ID in the registry against the 'swarm/' folder and 'knowledge' table.
2. Compaction: Removes whitespace and unnecessary metadata fields from the JSON.
3. Sorting: Re-orders the file by ID to improve file-read speed during initialization.
4. Validation: Ensures the resulting file is syntactically valid JSON.
A 'Housekeeping' command to be run after massive ingestion or synthesis sessions.

[EXPANSION PENDING]

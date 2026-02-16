# PROBE MANUAL

## Tier: Basic
- Reads the content of a local text or markdown file.
- Performs a deep-scan for missed facts or technical insights.
- Bypasses the passive monitor for immediate ingestion.
Usage: ./cli probe manual <path>

## Tier: More
- Reads the content of a local text or markdown file.
- Performs a deep-scan for missed facts or technical insights.
- Bypasses the passive monitor for immediate ingestion.
Usage: ./cli probe manual <path>

TECHNICAL DEEP-DIVE:
The 'manual' command provides a high-priority injection path for existing data.
1. Buffer Management: Uses memory-efficient reading to handle files up to 50MB.
2. Encoding: Automatically detects and handles UTF-8 vs ASCII encodings.
3. Processing: Pipes file content into the classification pipeline, treating every paragraph as a potential knowledge unit.
4. Indexing: Re-vectorizes the file content to ensure it's available for semantic search.
This command is essential for 'priming' a new project with existing documentation or requirements.

## Tier: Full
- Reads the content of a local text or markdown file.
- Performs a deep-scan for missed facts or technical insights.
- Bypasses the passive monitor for immediate ingestion.
Usage: ./cli probe manual <path>

TECHNICAL DEEP-DIVE:
The 'manual' command provides a high-priority injection path for existing data.
1. Buffer Management: Uses memory-efficient reading to handle files up to 50MB.
2. Encoding: Automatically detects and handles UTF-8 vs ASCII encodings.
3. Processing: Pipes file content into the classification pipeline, treating every paragraph as a potential knowledge unit.
4. Indexing: Re-vectorizes the file content to ensure it's available for semantic search.
This command is essential for 'priming' a new project with existing documentation or requirements.

[EXPANSION PENDING]

# PROBE SCOUT

## Tier: Basic
- Downloads the target page and extracts visible text.
- Hands the content to the Brain for fact extraction.
- Useful for ingesting external documentation or API references.
Usage: ./cli probe scout <url>

## Tier: More
- Downloads the target page and extracts visible text.
- Hands the content to the Brain for fact extraction.
- Useful for ingesting external documentation or API references.
Usage: ./cli probe scout <url>

TECHNICAL DEEP-DIVE:
The 'scout' command initiates an active network request to pull external context.
1. Networking: Uses 'requests' with a randomized User-Agent to avoid blocking.
2. Parsing: Leverages 'BeautifulSoup4' to strip HTML tags and scripts, leaving only relevant text.
3. Intelligence: Sends the sanitized text to 'brain.reason.classify_intent' in chunks of 2000 tokens.
4. Storage: Every fact or discovery found in the URL is embedded (768D) and saved to 'memory.db'.
This is the primary tool for expanding the project's knowledge beyond the local environment.

## Tier: Full
- Downloads the target page and extracts visible text.
- Hands the content to the Brain for fact extraction.
- Useful for ingesting external documentation or API references.
Usage: ./cli probe scout <url>

TECHNICAL DEEP-DIVE:
The 'scout' command initiates an active network request to pull external context.
1. Networking: Uses 'requests' with a randomized User-Agent to avoid blocking.
2. Parsing: Leverages 'BeautifulSoup4' to strip HTML tags and scripts, leaving only relevant text.
3. Intelligence: Sends the sanitized text to 'brain.reason.classify_intent' in chunks of 2000 tokens.
4. Storage: Every fact or discovery found in the URL is embedded (768D) and saved to 'memory.db'.
This is the primary tool for expanding the project's knowledge beyond the local environment.

[EXPANSION PENDING]

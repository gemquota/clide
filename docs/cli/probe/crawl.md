# PROBE CRAWL

## Tier: Basic
- Regularly checks RSS, Git logs, or other external feeds.
- Keeps project context updated with latest changes.
- Requires configuration in the 'probe' section of .cliderc.
Usage: ./cli probe crawl

## Tier: More
- Regularly checks RSS, Git logs, or other external feeds.
- Keeps project context updated with latest changes.
- Requires configuration in the 'probe' section of .cliderc.
Usage: ./cli probe crawl

TECHNICAL DEEP-DIVE:
The 'crawl' command automates the monitoring of dynamic project sources.
1. Feed Parsing: Uses 'feedparser' or raw Git API calls to fetch recent entries.
2. Delta Detection: Compares the latest entry ID against 'state.json' to prevent duplicate ingestion.
3. Synthesis: Converts feed entries into 'DISCOVERY' nodes within the project brain.
4. Automation: Designed to be run via 'cron' or as a low-priority background thread in the monitor.
This ensures the brain stays synchronized with external repositories and dependencies.

## Tier: Full
- Regularly checks RSS, Git logs, or other external feeds.
- Keeps project context updated with latest changes.
- Requires configuration in the 'probe' section of .cliderc.
Usage: ./cli probe crawl

TECHNICAL DEEP-DIVE:
The 'crawl' command automates the monitoring of dynamic project sources.
1. Feed Parsing: Uses 'feedparser' or raw Git API calls to fetch recent entries.
2. Delta Detection: Compares the latest entry ID against 'state.json' to prevent duplicate ingestion.
3. Synthesis: Converts feed entries into 'DISCOVERY' nodes within the project brain.
4. Automation: Designed to be run via 'cron' or as a low-priority background thread in the monitor.
This ensures the brain stays synchronized with external repositories and dependencies.

[EXPANSION PENDING]

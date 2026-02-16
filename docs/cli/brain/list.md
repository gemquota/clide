# BRAIN LIST

## Tier: Basic
- Shows the 10-20 most recent entries added to the brain.
- Displays category, timestamp, and a short snippet of content.
- Best for verifying that the passive monitor is correctly capturing data.
Usage: ./cli brain list

## Tier: More
- Shows the 10-20 most recent entries added to the brain.
- Displays category, timestamp, and a short snippet of content.
- Best for verifying that the passive monitor is correctly capturing data.
Usage: ./cli brain list

TECHNICAL DEEP-DIVE:
The 'list' command provides a linear view of the 'Neural Stream'.
1. Selection: Executes 'SELECT * FROM knowledge ORDER BY timestamp DESC LIMIT 20'.
2. Rendering: Uses rich console formatting to color-code rows by category.
3. Metadata: Includes the message ID and session hash for traceability.
4. Filtering: Can be combined with '--category' to see only specific types (e.g. only LESSONs).
Provides the 'Last Seen' context for the entire SPA environment.

## Tier: Full
- Shows the 10-20 most recent entries added to the brain.
- Displays category, timestamp, and a short snippet of content.
- Best for verifying that the passive monitor is correctly capturing data.
Usage: ./cli brain list

TECHNICAL DEEP-DIVE:
The 'list' command provides a linear view of the 'Neural Stream'.
1. Selection: Executes 'SELECT * FROM knowledge ORDER BY timestamp DESC LIMIT 20'.
2. Rendering: Uses rich console formatting to color-code rows by category.
3. Metadata: Includes the message ID and session hash for traceability.
4. Filtering: Can be combined with '--category' to see only specific types (e.g. only LESSONs).
Provides the 'Last Seen' context for the entire SPA environment.

[EXPANSION PENDING]

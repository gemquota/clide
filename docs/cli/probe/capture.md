# PROBE CAPTURE

## Tier: Basic
- Grabs text directly from your clipboard.
- Ideal for quick snippets or ideas found in a browser or other app.
- Immediately processes and embeds the captured data.
Usage: ./cli probe capture

## Tier: More
- Grabs text directly from your clipboard.
- Ideal for quick snippets or ideas found in a browser or other app.
- Immediately processes and embeds the captured data.
Usage: ./cli probe capture

TECHNICAL DEEP-DIVE:
The 'capture' command bridges the gap between external apps and the project brain.
1. Integration: Leverages 'termux-clipboard-get' on Android or 'pbpaste/xclip' on desktop.
2. Sanitization: Removes leading/trailing whitespace and non-printable characters.
3. Analysis: Triggers the full intent classification loop on the captured string.
4. Notification: Prints a summary of what was found (e.g. '1 TODO detected').
This provides an 'Immediate Ingest' path for transient thoughts and snippets.

## Tier: Full
- Grabs text directly from your clipboard.
- Ideal for quick snippets or ideas found in a browser or other app.
- Immediately processes and embeds the captured data.
Usage: ./cli probe capture

TECHNICAL DEEP-DIVE:
The 'capture' command bridges the gap between external apps and the project brain.
1. Integration: Leverages 'termux-clipboard-get' on Android or 'pbpaste/xclip' on desktop.
2. Sanitization: Removes leading/trailing whitespace and non-printable characters.
3. Analysis: Triggers the full intent classification loop on the captured string.
4. Notification: Prints a summary of what was found (e.g. '1 TODO detected').
This provides an 'Immediate Ingest' path for transient thoughts and snippets.

[EXPANSION PENDING]

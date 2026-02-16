# WATCH LOGS

## Tier: Basic
- Shows what the system is currently 'thinking' and 'hearing'.
- Displays classification results (e.g. FACT detected).
- Use '--tail' for a live, scrolling view of new messages.
Usage: ./cli watch logs [--tail]

## Tier: More
- Shows what the system is currently 'thinking' and 'hearing'.
- Displays classification results (e.g. FACT detected).
- Use '--tail' for a live, scrolling view of new messages.
Usage: ./cli watch logs [--tail]

TECHNICAL DEEP-DIVE:
The 'logs' command acts as a portal into the 'enriched_logs.json' telemetry file.
1. Filtering: Filters out internal system messages to show only user-facing logic.
2. Metadata: Displays similarity scores and LLM reasoning for each ingested unit.
3. Tail Logic: Leverages Python's 'tail -f' emulation to pipe new events to the terminal.
4. Formatting: Color-codes events by category (Green for FACT, Yellow for TODO, Cyan for MATCH).
This command provides the primary window into the Brain's real-time reasoning process.

## Tier: Full
- Shows what the system is currently 'thinking' and 'hearing'.
- Displays classification results (e.g. FACT detected).
- Use '--tail' for a live, scrolling view of new messages.
Usage: ./cli watch logs [--tail]

TECHNICAL DEEP-DIVE:
The 'logs' command acts as a portal into the 'enriched_logs.json' telemetry file.
1. Filtering: Filters out internal system messages to show only user-facing logic.
2. Metadata: Displays similarity scores and LLM reasoning for each ingested unit.
3. Tail Logic: Leverages Python's 'tail -f' emulation to pipe new events to the terminal.
4. Formatting: Color-codes events by category (Green for FACT, Yellow for TODO, Cyan for MATCH).
This command provides the primary window into the Brain's real-time reasoning process.

[EXPANSION PENDING]

# BRAIN SUMMARY

## Tier: Basic
- Summarizes the last 50-100 ingested knowledge units.
- Highlights major milestones, pending TODOs, and new technical discoveries.
- Uses the LLM to synthesize disparate facts into a coherent narrative.
Usage: ./cli brain summary

## Tier: More
- Summarizes the last 50-100 ingested knowledge units.
- Highlights major milestones, pending TODOs, and new technical discoveries.
- Uses the LLM to synthesize disparate facts into a coherent narrative.
Usage: ./cli brain summary

TECHNICAL DEEP-DIVE:
The 'summary' command is the 'Executive Layer' of project awareness.
1. Context Gathering: Aggregates the most important (Imp > 7) units from the last 7 days.
2. Synthesis: Passes the raw knowledge units to 'gemini-2.0-flash' with a 'Project Manager' instruction set.
3. Categorization: Breaks the summary into 'Accomplishments', 'Roadblock/TODOs', and 'System Changes'.
4. Export: Saves the resulting text to 'ingestion_logs/theorycrafting_report.md' for persistent tracking.
This command turns raw logs into actionable project status.

## Tier: Full
- Summarizes the last 50-100 ingested knowledge units.
- Highlights major milestones, pending TODOs, and new technical discoveries.
- Uses the LLM to synthesize disparate facts into a coherent narrative.
Usage: ./cli brain summary

TECHNICAL DEEP-DIVE:
The 'summary' command is the 'Executive Layer' of project awareness.
1. Context Gathering: Aggregates the most important (Imp > 7) units from the last 7 days.
2. Synthesis: Passes the raw knowledge units to 'gemini-2.0-flash' with a 'Project Manager' instruction set.
3. Categorization: Breaks the summary into 'Accomplishments', 'Roadblock/TODOs', and 'System Changes'.
4. Export: Saves the resulting text to 'ingestion_logs/theorycrafting_report.md' for persistent tracking.
This command turns raw logs into actionable project status.

[EXPANSION PENDING]

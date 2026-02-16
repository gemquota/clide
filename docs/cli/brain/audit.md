# BRAIN AUDIT

## Tier: Basic
- Compares facts to find inconsistencies (e.g. 'Project root is X' vs 'Project root is Y').
- Flags entries that have been manually marked for review.
- Highlights low-confidence classifications from the LLM.
Usage: ./cli brain audit

## Tier: More
- Compares facts to find inconsistencies (e.g. 'Project root is X' vs 'Project root is Y').
- Flags entries that have been manually marked for review.
- Highlights low-confidence classifications from the LLM.
Usage: ./cli brain audit

TECHNICAL DEEP-DIVE:
The 'audit' command ensures the 'Ground Truth' remains accurate.
1. Conflict Detection: Uses semantic similarity to find nodes with high similarity (>0.9) but potentially differing content.
2. LLM Review: Pairs of suspicious nodes are sent to the LLM to determine if one contradicts or supersedes the other.
3. Reporting: Lists all 'Knowledge Failures' and asks for manual 'manage' resolution.
4. Maintenance: Part of the 'entropy reduction' strategy in the Project Brain.
This command is the primary defense against 'Knowledge Drift' in long-running projects.

## Tier: Full
- Compares facts to find inconsistencies (e.g. 'Project root is X' vs 'Project root is Y').
- Flags entries that have been manually marked for review.
- Highlights low-confidence classifications from the LLM.
Usage: ./cli brain audit

TECHNICAL DEEP-DIVE:
The 'audit' command ensures the 'Ground Truth' remains accurate.
1. Conflict Detection: Uses semantic similarity to find nodes with high similarity (>0.9) but potentially differing content.
2. LLM Review: Pairs of suspicious nodes are sent to the LLM to determine if one contradicts or supersedes the other.
3. Reporting: Lists all 'Knowledge Failures' and asks for manual 'manage' resolution.
4. Maintenance: Part of the 'entropy reduction' strategy in the Project Brain.
This command is the primary defense against 'Knowledge Drift' in long-running projects.

[EXPANSION PENDING]

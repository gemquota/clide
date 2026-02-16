# BRAIN ANALYZE

## Tier: Basic
- Re-reads log history and shell batches.
- Uses advanced classification prompts to find logic the passive monitor might have skipped.
- Useful after updating your 'agents.md' constitution or classifier logic.
Usage: ./cli brain analyze

## Tier: More
- Re-reads log history and shell batches.
- Uses advanced classification prompts to find logic the passive monitor might have skipped.
- Useful after updating your 'agents.md' constitution or classifier logic.
Usage: ./cli brain analyze

TECHNICAL DEEP-DIVE:
The 'analyze' command performs a 'Deep Sweep' of existing telemetry.
1. Cold Reading: Iterates through all *.json and .zsh_history files in the archive.
2. Batching: Groups text into 100-line windows to preserve context.
3. Re-classification: Calls 'brain.reason.classify_intent' with a 'retrospective' persona that prioritizes discovery over filtering.
4. Deduplication: Compares new findings against existing DB entries using 768D similarity to prevent double-entry.
This ensures that the project brain evolves as the reasoning engine becomes more sophisticated.

## Tier: Full
- Re-reads log history and shell batches.
- Uses advanced classification prompts to find logic the passive monitor might have skipped.
- Useful after updating your 'agents.md' constitution or classifier logic.
Usage: ./cli brain analyze

TECHNICAL DEEP-DIVE:
The 'analyze' command performs a 'Deep Sweep' of existing telemetry.
1. Cold Reading: Iterates through all *.json and .zsh_history files in the archive.
2. Batching: Groups text into 100-line windows to preserve context.
3. Re-classification: Calls 'brain.reason.classify_intent' with a 'retrospective' persona that prioritizes discovery over filtering.
4. Deduplication: Compares new findings against existing DB entries using 768D similarity to prevent double-entry.
This ensures that the project brain evolves as the reasoning engine becomes more sophisticated.

[EXPANSION PENDING]

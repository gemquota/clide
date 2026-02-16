# FORGE EVOLVE

## Tier: Basic
- Refactors code based on user feedback or bug reports.
- Preserves existing function signatures while improving internal logic.
- Automatically re-runs unit tests after the refactor.
Usage: ./cli forge evolve <id> <instruction>

## Tier: More
- Refactors code based on user feedback or bug reports.
- Preserves existing function signatures while improving internal logic.
- Automatically re-runs unit tests after the refactor.
Usage: ./cli forge evolve <id> <instruction>

TECHNICAL DEEP-DIVE:
The 'evolve' command implements 'Semantic Code Evolution'.
1. Context: Reads the current content of the .py or .toml file.
2. Prompting: Sends [Current Code] + [User Instruction] to the LLM.
3. Patching: Overwrites the target file with the improved logic.
4. Regression: Executes 'forge test' to ensure no functional breakage.
This allows CLIDE to 'Learn' and 'Correct' its own creations over time.

## Tier: Full
- Refactors code based on user feedback or bug reports.
- Preserves existing function signatures while improving internal logic.
- Automatically re-runs unit tests after the refactor.
Usage: ./cli forge evolve <id> <instruction>

TECHNICAL DEEP-DIVE:
The 'evolve' command implements 'Semantic Code Evolution'.
1. Context: Reads the current content of the .py or .toml file.
2. Prompting: Sends [Current Code] + [User Instruction] to the LLM.
3. Patching: Overwrites the target file with the improved logic.
4. Regression: Executes 'forge test' to ensure no functional breakage.
This allows CLIDE to 'Learn' and 'Correct' its own creations over time.

[EXPANSION PENDING]

# AUTO PLAN

## Tier: Basic
- Analyzes all active tasks in the 'TODO' category.
- Assigns importance weights (1-10) based on project dependencies.
- Generates a 'Logical Sequencing' for future work.
Usage: ./cli auto plan

## Tier: More
- Analyzes all active tasks in the 'TODO' category.
- Assigns importance weights (1-10) based on project dependencies.
- Generates a 'Logical Sequencing' for future work.
Usage: ./cli auto plan

TECHNICAL DEEP-DIVE:
The 'plan' command is the 'Strategic Orchestrator' of the SPA.
1. Data Gathering: Collects every TODO from 'memory.db' and recent FACTS.
2. Strategic Analysis: Sends the task list to the LLM with a 'Product Manager' persona.
3. Scoring: LLM evaluates each task for 'Impact' vs 'Effort'.
4. Result: Updates the 'importance' column in the database, directly affecting which tasks appear in './cli manual task list'.
Essential for converting 'Chaotic Ingestion' into a structured engineering roadmap.

## Tier: Full
- Analyzes all active tasks in the 'TODO' category.
- Assigns importance weights (1-10) based on project dependencies.
- Generates a 'Logical Sequencing' for future work.
Usage: ./cli auto plan

TECHNICAL DEEP-DIVE:
The 'plan' command is the 'Strategic Orchestrator' of the SPA.
1. Data Gathering: Collects every TODO from 'memory.db' and recent FACTS.
2. Strategic Analysis: Sends the task list to the LLM with a 'Product Manager' persona.
3. Scoring: LLM evaluates each task for 'Impact' vs 'Effort'.
4. Result: Updates the 'importance' column in the database, directly affecting which tasks appear in './cli manual task list'.
Essential for converting 'Chaotic Ingestion' into a structured engineering roadmap.

[EXPANSION PENDING]

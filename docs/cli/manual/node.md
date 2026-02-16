# MANUAL NODE

## Tier: Basic
- get <id>    : View the complete JSON record.
- edit <id>   : Open content in your system editor.
- move <id> <cat> : Change category (e.g. FACT to LESSON).
- delete <id> : Permanent removal.
- tag <id> <t> : Manually add keywords.
Usage: ./cli manual node {get, edit, move, delete, tag} <id>

## Tier: More
- get <id>    : View the complete JSON record.
- edit <id>   : Open content in your system editor.
- move <id> <cat> : Change category (e.g. FACT to LESSON).
- delete <id> : Permanent removal.
- tag <id> <t> : Manually add keywords.
Usage: ./cli manual node {get, edit, move, delete, tag} <id>

TECHNICAL DEEP-DIVE:
The 'node' subcommand provides 'Surgical Database Control'.
1. Direct Access: Bypasses the LLM classification loop.
2. Logic Path: Invokes functions in 'clide/kernel/storage.py'.
3. State Management: Every change triggers a timestamp update.
4. Validation: 'move' checks against allowed SPA categories.
This is the 'Expert Override' for correcting model misclassifications or stale facts.
Primary Script: clide/kernel/storage.py.

## Tier: Full
- get <id>    : View the complete JSON record.
- edit <id>   : Open content in your system editor.
- move <id> <cat> : Change category (e.g. FACT to LESSON).
- delete <id> : Permanent removal.
- tag <id> <t> : Manually add keywords.
Usage: ./cli manual node {get, edit, move, delete, tag} <id>

TECHNICAL DEEP-DIVE:
The 'node' subcommand provides 'Surgical Database Control'.
1. Direct Access: Bypasses the LLM classification loop.
2. Logic Path: Invokes functions in 'clide/kernel/storage.py'.
3. State Management: Every change triggers a timestamp update.
4. Validation: 'move' checks against allowed SPA categories.
This is the 'Expert Override' for correcting model misclassifications or stale facts.
Primary Script: clide/kernel/storage.py.

[EXPANSION PENDING]

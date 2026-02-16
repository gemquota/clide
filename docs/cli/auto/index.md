# CLIDE // AUTO DOMAIN

## Tier: Basic
DETAILED USAGE
The Auto domain runs batch-processing tasks that would otherwise require manual CRUD.
- './cli auto plan' sorts your TODO list by project importance.
- './cli auto sync' ensures your 'todo.md' file reflects the 'memory.db' state.

## Tier: More
DETAILED USAGE
The Auto domain runs batch-processing tasks that would otherwise require manual CRUD.
- './cli auto plan' sorts your TODO list by project importance.
- './cli auto sync' ensures your 'todo.md' file reflects the 'memory.db' state.

TECHNICAL ARCHITECTURE: AUTO
===================================

1. DESIGN PHILOSOPHY
--------------------
Automates the 'Administrative Overhead' of knowledge management.
It acts as the executive liaison between the Sensory (Watch) and Cognitive (Brain) layers.

2. LOGIC IMPLEMENTATION (auto.py)
---------------------------------
- Class: 'IntelligentOrchestrator'
- Mechanism: Fetches chunks of un-processed data -> Constructs multi-shot LLM prompts -> Executes DB updates.
- Safety: All auto-updates are logged in the 'review' column of storage.py.

3. WORKFLOWS
------------
- ROADMAP: Scans category=TODO -> LLM ranks by urgency -> updates importance column.
- GRAPH: Scans for missing links -> similarity checks -> creates relationship edges.
- CLEANUP: Finds duplicate facts -> proposes merge IDs -> handles deletion.

## Tier: Full
DETAILED USAGE
The Auto domain runs batch-processing tasks that would otherwise require manual CRUD.
- './cli auto plan' sorts your TODO list by project importance.
- './cli auto sync' ensures your 'todo.md' file reflects the 'memory.db' state.

TECHNICAL ARCHITECTURE: AUTO
===================================

1. DESIGN PHILOSOPHY
--------------------
Automates the 'Administrative Overhead' of knowledge management.
It acts as the executive liaison between the Sensory (Watch) and Cognitive (Brain) layers.

2. LOGIC IMPLEMENTATION (auto.py)
---------------------------------
- Class: 'IntelligentOrchestrator'
- Mechanism: Fetches chunks of un-processed data -> Constructs multi-shot LLM prompts -> Executes DB updates.
- Safety: All auto-updates are logged in the 'review' column of storage.py.

3. WORKFLOWS
------------
- ROADMAP: Scans category=TODO -> LLM ranks by urgency -> updates importance column.
- GRAPH: Scans for missing links -> similarity checks -> creates relationship edges.
- CLEANUP: Finds duplicate facts -> proposes merge IDs -> handles deletion.

[EXPANSION PENDING]

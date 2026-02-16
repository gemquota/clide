# ARCHITECTURE // SINGLE PURPOSE (SPA)

## Tier: Basic
DOMAIN ISOLATION:
- kernel : Storage logic.
- brain  : Reasoning logic.
- watch  : Ingestion logic.
- forge  : Synthesis logic.
- tools  : Actuator logic.
- serve  : Interface logic.

This prevents circular dependencies and allows for 'hot-swappable' intelligence modules.

## Tier: More
DOMAIN ISOLATION:
- kernel : Storage logic.
- brain  : Reasoning logic.
- watch  : Ingestion logic.
- forge  : Synthesis logic.
- tools  : Actuator logic.
- serve  : Interface logic.

This prevents circular dependencies and allows for 'hot-swappable' intelligence modules.

THE DATA PIPELINE (SEQUENCE):
1. SENSORY [WATCH/PROBE]: Filesystem events or active scrapes pull raw text.
2. COGNITIVE [BRAIN]: 2.0-flash classifies the text into SPA categories.
3. PERSISTENCE [KERNEL]: storage.py saves the formalized result to memory.db.
4. INDEXING [INDEX]: Vector registry creates a 768D anchor for search.
5. MANUFACTURING [FORGE]: Synthesis engine builds tools based on the DB.
6. ACTUATION [TOOLS]: Hotswapper injects the tool into the Gemini runtime.

By isolating these phases, CLIDE can scale its intelligence without breaking the core storage engine.

## Tier: Full
DOMAIN ISOLATION:
- kernel : Storage logic.
- brain  : Reasoning logic.
- watch  : Ingestion logic.
- forge  : Synthesis logic.
- tools  : Actuator logic.
- serve  : Interface logic.

This prevents circular dependencies and allows for 'hot-swappable' intelligence modules.

THE DATA PIPELINE (SEQUENCE):
1. SENSORY [WATCH/PROBE]: Filesystem events or active scrapes pull raw text.
2. COGNITIVE [BRAIN]: 2.0-flash classifies the text into SPA categories.
3. PERSISTENCE [KERNEL]: storage.py saves the formalized result to memory.db.
4. INDEXING [INDEX]: Vector registry creates a 768D anchor for search.
5. MANUFACTURING [FORGE]: Synthesis engine builds tools based on the DB.
6. ACTUATION [TOOLS]: Hotswapper injects the tool into the Gemini runtime.

By isolating these phases, CLIDE can scale its intelligence without breaking the core storage engine.

[EXPANSION PENDING]

# Specification: Centralized State Management Service

## 1. Goal
The objective is to unify the project's knowledge layer (`clide/memory.db`) and its execution/task layer (`swarm/core/state.db`) into a single, cohesive interface. This ensures that agents in the Swarm can leverage "Facts," "Lessons," and "Discoveries" extracted by the CLIDE engine during their task execution.

## 2. Requirements
- **Unified Query Interface:** Agents must be able to query project knowledge through the same MCP server used for task management.
- **Knowledge Bridge:** High-importance items (Importance >= 7) from `clide/memory.db` should be accessible or automatically prioritized for agents.
- **Contextual Retrieval:** Support for retrieving knowledge by category (FACT, LESSON, TODO, DISCOVERY) and importance score.
- **Stability:** Ensure that reading from `memory.db` does not interfere with the Extraction Engine's write operations (use WAL mode or read-only connections).

## 3. Technical Design
- **Core Component:** Enhance `swarm/core/state_manager.py` to handle connections to both SQLite databases.
- **New MCP Tools:**
    - `query_project_knowledge`: Search for specific terms or categories in the knowledge base.
    - `get_recent_context`: Fetch the latest 5-10 facts/lessons to prime agent memory.
- **Schema Alignment:** Map Clide's `knowledge` table categories to Swarm's internal context representations.

## 4. Acceptance Criteria
- [ ] An agent can successfully retrieve a "Fact" stored in `memory.db` using an MCP tool.
- [ ] The `state_manager.py` can report both task status and relevant project knowledge in a single summary.
- [ ] Tests verify that the bridge correctly handles multi-database connections without locks.

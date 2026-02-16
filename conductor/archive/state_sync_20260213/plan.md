# Implementation Plan: Centralized State Management Service

## Phase 1: Foundation & Dual-DB Connectivity [checkpoint: 53d4c4c]
*Focus: Establishing the connection layer between the Extraction Engine and the Swarm state.*

- [x] Task: Configure SQLite WAL mode for both `memory.db` and `state.db` to prevent locking issues. [d216e93]
    - [x] Write Tests: Verify concurrent read/write across both databases.
    - [x] Implement: Update `get_db` logic in `state_manager.py` to handle both paths and modes.
- [x] Task: Implement the `KnowledgeProvider` class in `swarm/core/state_manager.py`. [4aeec50]
    - [x] Write Tests: Test retrieval of sample records from `memory.db`.
    - [x] Implement: Add methods to query Clide's `knowledge` table.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Foundation & Dual-DB Connectivity' (Protocol in workflow.md)

## Phase 2: Knowledge Extraction & Synchronization Tools [checkpoint: 21c9b15]
*Focus: Exposing knowledge through the MCP interface for the Agent Swarm.*

- [x] Task: Add the `query_project_knowledge` tool to the FastMCP server. [88006d4]
    - [x] Write Tests: Verify tool returns expected JSON structure for varied queries.
    - [x] Implement: Add `@mcp.tool()` with filtering by category and importance.
- [x] Task: Add the `get_recent_lessons` tool for automated context injection. [88006d4]
    - [x] Write Tests: Verify it fetches the latest $N$ items of category 'LESSON'.
    - [x] Implement: Logic to sort by timestamp and filter by category.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Knowledge Extraction & Synchronization Tools' (Protocol in workflow.md)

## Phase 3: Integration & Agent Prime [checkpoint: 8937588]
*Focus: Enabling the agents to actually use the new knowledge bridge.*

- [x] Task: Update the `get_project_status` tool to include a "Recent Knowledge" summary. [fe4eca7]
    - [x] Write Tests: Verify summary includes both Entity status and top Knowledge items.
    - [x] Implement: Refactor tool to join context from both databases.
- [x] Task: Update `swarm/agents.md` (The Constitution) to explicitly guide agents to use knowledge tools. [7764236]
    - [x] Write Tests: (Manual Verification preferred for behavioral changes).
    - [x] Implement: Add instructions for semantic context retrieval before task execution.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Integration & Agent Prime' (Protocol in workflow.md)

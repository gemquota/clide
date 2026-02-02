# Specification: State Management MCP (Project Atlas)

## 1. Overview
The **State Management MCP** is a centralized service designed to decouple project state from AI agent personas. It provides a robust, SQLite-backed persistence layer for tracking features, bugs, tasks, and protocol-specific gates (e.g., RSD approvals).

**Author:** Engineer Persona (CLIDE Integrated)
**Status:** Draft
**Database Location:** `core/state.db`

## 2. Goals
- **Persistence:** Ensure project state survives across chat sessions and different agent personas.
- **Decoupling:** Remove complex SQL logic from `.toml` command prompts.
- **Uniformity:** Provide a single source of truth for `dev`, `bug`, and `engineer` workflows.
- **Auditability:** Maintain a clear log of status changes and approvals.

## 3. Database Schema
### 3.1 `entities` Table (Features/Bugs)
Tracks the high-level items being worked on.
- `id`: INTEGER (PK)
- `type`: TEXT ('FEATURE', 'BUG')
- `name`: TEXT
- `status`: TEXT ('DEFINING', 'PLANNING', 'IMPLEMENTING', 'QA', 'RELEASED')
- `risk_score`: INTEGER (1-10)
- `created_at`: DATETIME

### 3.2 `artifacts` Table
Stores documents related to an entity (User Stories, RSDs, Rollback Plans).
- `id`: INTEGER (PK)
- `entity_id`: INTEGER (FK)
- `type`: TEXT
- `content`: TEXT
- `is_approved`: BOOLEAN (Default: 0)

### 3.3 `tasks` Table
Micro-tasks for execution.
- `id`: INTEGER (PK)
- `entity_id`: INTEGER (FK)
- `description`: TEXT
- `track`: TEXT ('A_CODE', 'B_DOCS')
- `status`: TEXT ('PENDING', 'DONE')
- `weight`: INTEGER

## 4. MCP Tools (API)
### `init_entity(name, type, risk_score)`
Initializes a new feature or bug in the database.

### `add_artifact(entity_id, type, content)`
Saves a document (like an RSD) associated with an entity.

### `approve_artifact(artifact_id)`
Sets `is_approved` to true. Acts as a gate for state transitions.

### `sync_tasks(entity_id, tasks_list)`
Bulk inserts or updates tasks for a specific entity.

### `get_project_status()`
Returns a summary of all active entities and their current phase.

## 5. Protocol Gates (Logic)
The MCP will enforce the following:
- **RSD Gate:** If `risk_score >= 7`, the `status` cannot move to `PLANNING` unless an artifact of type `RSD` exists and is `approved`.
- **Completion Gate:** Status cannot move to `RELEASED` if there are `PENDING` tasks in the `tasks` table.

## 6. Implementation Plan
1. **Bootstrap:** Create `core/state_manager.py` using the FastMCP framework.
2. **Schema Init:** Implement auto-migration/creation of `core/state.db`.
3. **Tool Implementation:** Code the Python logic for each tool defined in Section 4.
4. **Registry:** Register the MCP with CLIDE.
5. **Prompt Refactoring:** Update `dev.toml` and `bug.toml` to remove SQL blocks and instead call `mcp:state_manager`.

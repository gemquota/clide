# CLIDE // MEMORY DOMAIN
State management, knowledge CRUD, and relational linking.

The `memory` domain provides direct manual control over the system's knowledge base (`memory.db`).

<card>
title: MEMORY OVERVIEW
Backend: SQLite
Categories: FACT, LESSON, TODO, DISCOVERY, SHELL_HISTORY
Sync: Automatic todo.md reconciliation
</card>

### Commands
*   **list**: Lists recent knowledge units chronologically.
*   **create**: Manually adds a new knowledge node.
*   **edit**: Updates the content of an existing node.
*   **delete**: Performs a soft-delete (marks as deleted).
*   **forget**: Performs a hard-delete (permanent removal).
*   **connect**: Establishes a relationship between two nodes.
*   **merge**: Consolidates temporary logs into the database.

### Technical Specifications
Knowledge is stored in a relational schema with associated 768D embeddings for semantic retrieval.

<card>
title: STORAGE SCHEMA
Table: knowledge (content, category, importance, embedding)
Table: relationships (source_id, target_id, rel_type)
Index: timestamp DESC
</card>

### Usage Examples
1. List Units: `./cli memory list --limit 10`
2. Create Fact: `./cli memory create "The sky is blue" --category FACT`
3. Connect Nodes: `./cli memory connect 101 105`
4. Hard Delete: `./cli memory forget 42`

### Architecture Internals
The memory layer is managed via `clide.kernel.storage`. Every write operation to the `content` field triggers an automatic re-embedding using `gemini-embedding-001`.

<card>
title: STORAGE HOOKS
Save: clide.kernel.storage.save_knowledge
Update: clide.kernel.storage.update_knowledge
Delete: clide.kernel.storage.delete_knowledge
Relationships: clide.kernel.storage.add_relationship
</card>

### State Synchronization
- **TODO Sync**: When a node is saved with `category='TODO'`, it is appended to the root `todo.md` file automatically.
- **Soft Delete**: Uses the `is_deleted` flag in SQLite to preserve audit trails.
- **Hard Delete**: Removes the row and its associated relationships from the DB.

### API Reference
*   `get_knowledge(category, min_importance, limit)`: Flexible query engine for cognitive tasks.
*   `update_knowledge(id, content, ...)`: Updates node fields and re-syncs vectors.
# [ SECTOR 03: STATE ] - RUN
Strategic orchestration and execution of persistent task workflows.

The `run` domain manages task prioritization and strategy management.

<card>
title: RUN OVERVIEW
Core: Task Prioritization
Tracking: todo.md
Sync: Memory-Aware
Status: ACTIVE
</card>

### Commands
*   **plan**: Automatically prioritizes tasks based on importance and session mapping.
*   **task**: Strategy management tool (list, add, remove, complete).
*   **sync**: Harmonizes the `todo.md` file with the `memory.db` state.

### Technical Specifications
Strategic orchestration ensures that system goals are aligned with ingested data.

<card>
title: OPERATIONAL CONTEXT
Prioritization: Session Density + Importance
File Source: todo.md
State Source: memory.db (TODO Category)
</card>

### Usage Examples
1. Auto-plan: `./cli run plan`
2. Add task: `./cli run task add "implement new API hook"`
3. Sync state: `./cli run sync`

### Dependency Notes
Requires write access to `todo.md`. Prioritization uses the `Cognitive Engine` for context analysis.

### Architecture Internals
The `run` domain acts as the bridge between the system's "intent" and "action".

<card>
title: NEURAL-KERNEL HOOKS
Auto Hook: clide.brain.auto.auto_prioritize_tasks
Sync Hook: clide.brain.auto.auto_sync_todos
Task Hook: clide.tools.janitor.TodoManager
</card>

### API Hooks
*   `janitor.TodoManager()`: Core task control class.
*   `auto.auto_prioritize_tasks()`: Strategic update.

### Legacy Notes
Previously handled manually in `todo.md`. `v1.0.0` introduces automated context-aware prioritization.
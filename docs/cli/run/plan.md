# AUTO PLAN

- Analyzes all active tasks in the 'TODO' category.
- Assigns importance weights (1-10) based on project state.
- Helps prioritize work using LLM strategic analysis.
Usage: ./cli auto plan

- Analyzes all active tasks in the 'TODO' category.
- Assigns importance weights (1-10) based on project state.
- Helps prioritize work using LLM strategic analysis.
Usage: ./cli auto plan

TECHNICAL DEEP-DIVE:
The `plan` command is the 'Strategic Orchestrator' of the project.
1. **Data Collection:** Fetches all knowledge units with `category='TODO'` from the database.
2. **Context Construction:** Builds a list of task IDs and descriptions.
3. **LLM Evaluation:** Sends the list to the LLM with a prompt to rank tasks by importance (1-10).
4. **Update:** Parses the returned JSON mapping and updates the `importance` column for each node.

- Analyzes all active tasks in the 'TODO' category.
- Assigns importance weights (1-10) based on project state.
- Helps prioritize work using LLM strategic analysis.
Usage: ./cli auto plan

TECHNICAL DEEP-DIVE:
The `plan` command is implemented in `clide.brain.auto.auto_prioritize_tasks`.

### Logic Flow
1. **Selection:** Retrieves todos via `storage.get_knowledge(category="TODO")`.
2. **Prompting:**
   - Prompt includes the ID and content of every todo.
   - Specifically requests a JSON response: `{"id": score, ...}`.
3. **Parsing:**
   - Uses robust string searching (`find('{')`, `rfind('}')`) to isolate the JSON block from LLM output.
   - Iterates through the mapping and calls `storage.update_knowledge(id, importance=score)`.

### Code Reference
- **Entry Point:** `clide/serve/portal.py` -> `cmd_run`
- **Implementation:** `clide/brain/auto.py` -> `auto_prioritize_tasks`

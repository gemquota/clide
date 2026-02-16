# CLIDE: The In-Depth Manual (v0.6.0)

Welcome to CLIDE. This manual covers the operational workflows, database synchronization, and reporting mechanisms of the system.

## 1. Core Workflows

### 🔄 The Neural Sync (Background Monitoring)
CLIDE automatically monitors your interactions to build the **Project Brain**.

**How to start the monitor:**
```bash
./cli monitor
```
This starts `clide/extractor.py` which:
1.  **Polls Gemini Logs:** Watches `~/.gemini/tmp/*/logs.json` for new messages.
2.  **Polls Shell History:** Watches `~/.zsh_history` for complex command sequences.
3.  **Analyzes Intent:** Uses Gemini to categorize input as FACT, LESSON, TODO, or NEW_COMMAND.
4.  **Updates Database:** Saves insights to `clide/memory.db`.
5.  **Progress Heartbeat:** Updates `ingestion_logs/progress.md` every 15 seconds.
6.  **Auto-Report:** Generates fresh markdown reports every 5 minutes.

---

### 🚀 Creating New Commands
When the monitor detects a repetitive pattern, it will suggest a `NEW_COMMAND`.

**Manual Creation Workflow:**
If you want to force a command extraction from your recent history:
1.  Run `clide/extractor.py` (Monitor) - it will eventually catch it.
2.  Or use the CLI (future feature): `clide ingest --name my-new-cmd`.

---

### 📊 Visualizing the Brain
To see the semantic connections in your project's knowledge base:

```bash
./cli brain
```
-   **Terminal:** Shows an ASCII map of facts and their relationships.
-   **File:** Generates `docs/brain_graph.mmd` (Mermaid format) which can be viewed in GitHub or any Mermaid editor.

---

## 2. Database & Data Flow

### 🗄️ Storage Locations
-   **Primary Knowledge:** `clide/memory.db` (SQLite). Stores categorized facts, lessons, and embeddings.
-   **Asset Registry:** `swarm/commands/vector_registry.json`. Stores metadata and embeddings for agents and tools.
-   **Enriched Logs:** `clide/enriched_logs.json`. A flat-file mirror of analyzed interactions.

### 🔄 Synchronizing Injections
"Live injections" refers to the process of feeding your current activity into the long-term memory.
-   **Automatic:** Handled by `./cli monitor`.
-   **Manual Sync:** You can trigger a report refresh by running:
    ```bash
    python clide/report_generator.py
    ```

---

## 3. Viewing Progress & Reports

CLIDE outputs structured reports into `ingestion_logs/`:

1.  **`ingestion_logs/progress.md`**: Real-time status of the monitoring loop.
2.  **`ingestion_logs/all/`**: Grand Total (All Time) reports for Commands and Roles.
3.  **`ingestion_logs/YYYY-MM/ingestion_log_partXX.md`**: Detailed breakdown of every ingested snippet.
3.  **`ingestion_logs/YYYY-MM/new_commands_inventory_partXX.md`**: Summary of potential new tools detected.
4.  **`ingestion_logs/YYYY-MM/system_roles_inventory_partXX.md`**: Record of persona and protocol changes.

---

## 🛠 Troubleshooting

### "Brain" command is slow
The brain visualization performs O(N^2) similarity checks to find connections. If you have >500 items, it may take a few seconds. We have optimized this by pre-decoding embeddings.

### Monitor not catching shell commands
Ensure your shell is writing to `~/.zsh_history` immediately. You can add `setopt INC_APPEND_HISTORY` to your `.zshrc`.

### Permission Errors
On Android/Termux, ensure you have given storage permissions if you are working outside the home directory.

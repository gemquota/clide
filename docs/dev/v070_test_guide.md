# CLIDE v0.7.0 Comprehensive System Verification Guide

This guide covers ALL functional areas of CLIDE. Perform these tests to ensure the entire system is stable before the 0.7.0 release.

---

## SECTION 1: THE EXTRACTION ENGINE (clide/)

### 1.1 Neural Stream Monitoring (Logs)
- **Action:** Run `./clide monitor`. In your chat, type a clear command request: "Create a command called 'weather' that fetches the current temperature for a city."
- **Verify:** CLIDE detects the `NEW_COMMAND` intent, prompts for save type (T/M), and shows reasoning.

### 1.2 Shell History Ingestion
- **Action:** Run a unique shell command, e.g., `curl -I https://google.com`. Wait 10 seconds.
- **Verify:** Monitor output shows `[Shell Ingestor] Found new commands`.

### 1.3 Deep Pattern Detection (Repetition)
- **Action:** In chat, ask for similar but distinct things 3 times (e.g., "List the python files", "Show me the py files", "Find all .py files").
- **Verify:** Monitor should trigger `[!] REPETITIVE PATTERN DETECTED` and force an extraction analysis.

### 1.4 Knowledge Extraction (Brain Ingestion)
- **Action:** Type a fact: "The staging server is at 192.168.1.50".
- **Verify:** Monitor shows `[Memory] Saved FACT`.
- **Action:** Type a lesson: "Never use 'shell=True' in subprocess calls."
- **Verify:** Monitor shows `[Memory] Saved LESSON` and asks if you want to refactor existing assets.

---

## SECTION 2: THE ASSET FORGE (Synthesis & Registry)

### 2.1 TOML Command Generation
- **Action:** Save the 'weather' request from 1.1 as a `(T)OML Command`.
- **Verify:** `swarm/commands/weather.toml` exists and contains the constitution (`agents.md`) and any extracted `FACTS`.

### 2.2 MCP Server Generation (Simple)
- **Action:** Ask for a tool to "Calculate the SHA256 of a file." Save as `(M)CP Server`.
- **Verify:** `swarm/commands/mcp_servers/sha256.py` exists. The Healer loop runs a dry-run.

### 2.3 Complex Package Forge & Auto-Verify
- **Action:** Ask for a "Full project documentation generator that scans the src folder and outputs a summary.md."
- **Verify:** CLIDE creates a directory in `mcp_servers/`. It should run `pytest` automatically.

### 2.4 Vector Registry & Search
- **Action:** Run `./clide list`.
- **Verify:** Assets are grouped by `[TOML]` and `[MCP]`.
- **Action:** Run `./clide search "calculate hash"`.
- **Verify:** The `sha256` tool appears with a high similarity score.

---

## SECTION 3: MAINTENANCE & SAFETY

### 3.1 The Surgeon Janitor
- **Action:** Create two overlapping tools (e.g., `lister_v1` and `lister_v2`). Run `./clide janitor`.
- **Verify:** Janitor detects overlap, proposes a merge, creates a git commit backup, and moves originals to `swarm/commands/archive/`.

### 3.2 Temporal Rollback
- **Action:** Run `./clide rollback <id_of_merged_tool>`.
- **Verify:** Git restores the previous state. Check if `clide/memory.db` was reverted (if applicable).

### 3.3 The Project Brain (Graph)
- **Action:** Run `./clide brain`.
- **Verify:** ASCII map displays relationships based on importance and semantic similarity.

---

## SECTION 4: THE AGENT SWARM (swarm/)

### 4.1 State Management (Project Atlas)
- **Action:** Activate the `engineer` command. Ask it to "Initialize Feature: Dashboard Redesign."
- **Verify:** The agent uses the `state_manager` MCP to write to `swarm/core/state.db`.
- **Action:** Run `./clide brain` or query the DB to see the new `FEATURE` entity.

### 4.2 Cross-Agent Persistence
- **Action:** Activate the `bug` command. Ask it "What is the status of the Dashboard feature?"
- **Verify:** The `bug` agent should be able to read the state created by the `engineer` agent from the shared `state.db`.

---
**FINAL RELEASE CHECK:**
- [ ] No `ImportError` or `ModuleNotFoundError` during any test.
- [ ] `todo.md` is correctly populated.
- [ ] `.cliderc` correctly routes all paths.
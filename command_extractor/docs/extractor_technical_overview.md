# CLIDE Core: Extractor Module Documentation

**File:** `extractor.py`

## Overview
The `extractor.py` script is the central nervous system of CLIDE (Command Line Interface - Database: Everything). It acts as a real-time monitor that observes the Gemini CLI's interaction logs, identifying when a user's request is a candidate for automation (a new command) or matches an existing tool.

## Architecture

The script operates on an infinite loop, performing the following key phases:
1.  **Discovery**: Locating the active Gemini session log.
2.  **Ingestion**: Reading new user messages since the last check.
3.  **Analysis**: delegating content to the `IntentAnalyzer` to determine if it's a "Command".
4.  **Action**: Triggering interactive generation and saving of new commands.

## Key Functions

### 1. Dynamic Log Discovery
**Function:** `get_latest_log_file()`
- **Purpose**: To find the `logs.json` file for the *current* or most recent active session.
- **Logic**: Scans `~/.gemini/tmp/` for subdirectories, sorts them by modification time (newest first), and returns the path to `logs.json`.
- **Robustness**: If no session or log file is found, it returns `None`, allowing the loop to retry gracefully.

### 2. State Management
**Functions:** `get_last_processed_id()`, `save_last_processed_id(msg_id)`
- **Purpose**: To ensure messages are processed exactly once.
- **Mechanism**: Persists the integer `messageId` of the last handled message to `state.json`. On restart, CLIDE resumes from this ID, avoiding re-processing old history.

### 3. The Monitor Loop
**Function:** `monitor()`
- **Purpose**: The main execution flow.
- **Flow**:
    1.  **Polls** for the log file every 5 seconds.
    2.  **Filters** logs for `type: "user"` and `messageId > last_id`.
    3.  **Ignores** short chatter or meta-commands (like "monitor gemini").
    4.  **Calls `classify_intent`** to determine if the text is a `MATCH`, `NEW_COMMAND`, or `NICHE`.
    5.  **Interactive Trigger**: If `NEW_COMMAND` is detected:
        - It halts the loop to ask the user: `[?] Generate and save command...?`
        - If 'y', calls `generate_command_template` (LLM-based) and `save_new_command`.

## Dependencies

- **`commands_loader`**: Fetches the list of currently existing commands to prevent duplicates.
- **`intent_classifier`**: The "Brain" (using `gemini -p`) that categorizes the text.
- **`template_generator`**: Constructs the high-quality system prompt for new commands.
- **`command_saver`**: Writes the final `.toml` file to the command registry.

## Usage
Executed via the wrapper script `clide`:
```bash
./clide
```
This runs the module as `__main__`, starting the infinite monitoring loop.

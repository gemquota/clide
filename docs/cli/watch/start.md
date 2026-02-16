# WATCH START

## Tier: Basic
- Spawns a dedicated process to observe filesystem changes.
- Initializes the Watchdog Observer on the project's temporary directory.
- Use 'watch status' to verify the process is alive.
Usage: ./cli watch start

## Tier: More
- Spawns a dedicated process to observe filesystem changes.
- Initializes the Watchdog Observer on the project's temporary directory.
- Use 'watch status' to verify the process is alive.
Usage: ./cli watch start

TECHNICAL DEEP-DIVE:
The 'start' command invokes the 'ClideExtractor.run()' method within 'clide/watch/stream.py'.
1. Environment Setup: Reads GEMINI_TMP_DIR to locate session logs.
2. Threading: Renders the Watchdog observer into a non-blocking background thread.
3. Persistence: Updates 'state.json' with the new process start time.
4. Error Handling: Gracefully exits if the directory is inaccessible or another monitor is already running.
This is the foundational entry point for passive knowledge acquisition in the SPA.

## Tier: Full
- Spawns a dedicated process to observe filesystem changes.
- Initializes the Watchdog Observer on the project's temporary directory.
- Use 'watch status' to verify the process is alive.
Usage: ./cli watch start

TECHNICAL DEEP-DIVE:
The 'start' command invokes the 'ClideExtractor.run()' method within 'clide/watch/stream.py'.
1. Environment Setup: Reads GEMINI_TMP_DIR to locate session logs.
2. Threading: Renders the Watchdog observer into a non-blocking background thread.
3. Persistence: Updates 'state.json' with the new process start time.
4. Error Handling: Gracefully exits if the directory is inaccessible or another monitor is already running.
This is the foundational entry point for passive knowledge acquisition in the SPA.

[EXPANSION PENDING]

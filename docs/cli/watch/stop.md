# WATCH STOP

## Tier: Basic
- Sends a termination signal to the active Watchdog process.
- Ensures all pending log lines are flushed to the database before exiting.
- Cleans up temporary lock files in the 'watch' domain.
Usage: ./cli watch stop

## Tier: More
- Sends a termination signal to the active Watchdog process.
- Ensures all pending log lines are flushed to the database before exiting.
- Cleans up temporary lock files in the 'watch' domain.
Usage: ./cli watch stop

TECHNICAL DEEP-DIVE:
The 'stop' command performs a graceful shutdown of the 'ClideExtractor' instance.
1. Signal Handling: Triggers 'observer.stop()' within the Watchdog loop.
2. Resource Cleanup: Closes active SQLite connections in the 'kernel' domain.
3. Thread Join: Waits for the background shell-polling thread to finalize its current batch.
4. State Update: Marks the monitor as 'offline' in the system status telemetry.
This command ensures data integrity by preventing partial ingestion during process termination.

## Tier: Full
- Sends a termination signal to the active Watchdog process.
- Ensures all pending log lines are flushed to the database before exiting.
- Cleans up temporary lock files in the 'watch' domain.
Usage: ./cli watch stop

TECHNICAL DEEP-DIVE:
The 'stop' command performs a graceful shutdown of the 'ClideExtractor' instance.
1. Signal Handling: Triggers 'observer.stop()' within the Watchdog loop.
2. Resource Cleanup: Closes active SQLite connections in the 'kernel' domain.
3. Thread Join: Waits for the background shell-polling thread to finalize its current batch.
4. State Update: Marks the monitor as 'offline' in the system status telemetry.
This command ensures data integrity by preventing partial ingestion during process termination.

[EXPANSION PENDING]

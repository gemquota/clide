# CLIDE // WATCH DOMAIN

## Tier: Basic
- start  : Launches the Watchdog process to monitor logs.json.
- stop   : Gracefully terminates the background monitor.
- status : Displays the process PID and uptime health.
- logs   : Prints the most recent ingestion events. Use --tail for a live stream.

## Tier: More
- start  : Launches the Watchdog process to monitor logs.json.
- stop   : Gracefully terminates the background monitor.
- status : Displays the process PID and uptime health.
- logs   : Prints the most recent ingestion events. Use --tail for a live stream.

The Watch domain utilizes the 'watchdog' library to observe filesystem modifications.
Logic: OS Event -> Cooldown (2s) -> Ingest -> clide.brain.reason -> clide.kernel.storage.
Primary Script: clide/watch/stream.py
Terminal Hook: clide/watch/terminal.py (Polls shell history).

## Tier: Full
- start  : Launches the Watchdog process to monitor logs.json.
- stop   : Gracefully terminates the background monitor.
- status : Displays the process PID and uptime health.
- logs   : Prints the most recent ingestion events. Use --tail for a live stream.

The Watch domain utilizes the 'watchdog' library to observe filesystem modifications.
Logic: OS Event -> Cooldown (2s) -> Ingest -> clide.brain.reason -> clide.kernel.storage.
Primary Script: clide/watch/stream.py
Terminal Hook: clide/watch/terminal.py (Polls shell history).

[EXPANSION PENDING]

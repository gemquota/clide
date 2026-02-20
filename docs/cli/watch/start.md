# WATCH // START
Initiates the high-frequency background monitoring daemon.

Launches the project's background monitor for real-time ingestion.

<card>
title: ⦗ OPERATION: START ⦘
Daemon: Watchdog
State: Initializing...
Target: /ingestion_logs/
</card>

### Usage
`./cli watch start`

### Technical Details
Checks for existing PIDs before spawning. If already running, returns status.

<card>
title: ⦗ START SEQUENCE ⦘
1. Lock check
2. Stream init
3. Enrichment hook bind
</card>

### Code Internals
Calls `stream.ClideExtractor().run()`. Spawns a background process if not already detached.
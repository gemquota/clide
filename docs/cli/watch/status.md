# WATCH // STATUS
Retrieves health and connectivity metrics for the background monitor.

Displays whether the monitor is active and its current performance.

<card>
title: ⦗ MONITOR HEALTH ⦘
PID: [Active]
Uptime: HH:MM:SS
Status: OPERATIONAL
</card>

### Usage
`./cli watch status`

### Technical Details
Reads from the PID lock file and checks `psutil` for process existence.

### Code Internals
Calls `stream.get_monitor_status()`.
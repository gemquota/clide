# WATCH // STOP
Gracefully terminates the background monitor.

Stops the background extraction and monitoring processes.

<card>
title: ⦗ OPERATION: STOP ⦘
Method: SIGTERM
State: Shutdown...
Target: ClideExtractor
</card>

### Usage
`./cli watch off`

### Technical Details
Sends a termination signal to the PID found in the lock file. Cleans up temporary resources.

### Code Internals
Calls `stream.off_monitor()`. Ensures file handles are closed properly.
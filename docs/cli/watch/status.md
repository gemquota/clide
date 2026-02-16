# WATCH STATUS

## Tier: Basic
- Returns real-time metrics including process ID and uptime.
- Checks connectivity to the 'memory.db' ground truth.
- Reports the last time a Gemini log was successfully ingested.
Usage: ./cli watch status

## Tier: More
- Returns real-time metrics including process ID and uptime.
- Checks connectivity to the 'memory.db' ground truth.
- Reports the last time a Gemini log was successfully ingested.
Usage: ./cli watch status

TECHNICAL DEEP-DIVE:
The 'status' command queries the system environment and internal state files.
1. Process Detection: Uses 'ps' or 'proc' to verify if the monitor PID is active.
2. Heartbeat Analysis: Reads 'ingestion_logs/progress.md' to extract the 'Last Heartbeat' timestamp.
3. DB Integrity: Performs a quick 'SELECT 1' on the 'knowledge' table to ensure storage readiness.
4. Latency Metrics: Calculates the delta between the current time and the last ingestion event.
This command is critical for verifying the reliability of the passive sensory layer.

## Tier: Full
- Returns real-time metrics including process ID and uptime.
- Checks connectivity to the 'memory.db' ground truth.
- Reports the last time a Gemini log was successfully ingested.
Usage: ./cli watch status

TECHNICAL DEEP-DIVE:
The 'status' command queries the system environment and internal state files.
1. Process Detection: Uses 'ps' or 'proc' to verify if the monitor PID is active.
2. Heartbeat Analysis: Reads 'ingestion_logs/progress.md' to extract the 'Last Heartbeat' timestamp.
3. DB Integrity: Performs a quick 'SELECT 1' on the 'knowledge' table to ensure storage readiness.
4. Latency Metrics: Calculates the delta between the current time and the last ingestion event.
This command is critical for verifying the reliability of the passive sensory layer.

[EXPANSION PENDING]

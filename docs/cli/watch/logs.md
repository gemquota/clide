# WATCH // LOGS
Tails and displays enriched telemetry from the background monitor.

Views real-time ingestion logs with 768D semantic enrichment.

<card>
title: ⦗ LOG VIEWER ⦘
Format: Enriched TUI
Buffer: Tail-mode
Level: INFO
</card>

### Usage
`./cli watch logs [--tail] [--limit N]`

### Technical Details
Parses `ingestion_logs/enriched_logs.json` for live display.

### Code Internals
Calls `stream.tail_logs()`.
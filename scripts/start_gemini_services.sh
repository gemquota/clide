#!/bin/bash

# Configuration
PROJECT_DIR="$HOME/openclaw/meta"
LOG_DIR="$PROJECT_DIR/clide"
MONITOR_LOG="$LOG_DIR/monitor.log"
INGEST_LOG="$LOG_DIR/ingest_periodic.log"

# Function to start monitor
start_monitor() {
    if pgrep -f "clide_cli.py monitor" > /dev/null; then
        echo "Clide Monitor is already running."
    else
        echo "Starting Clide Monitor..."
        nohup $PROJECT_DIR/cli monitor > "$MONITOR_LOG" 2>&1 &
    fi
}

# Function to run ingestion loop
start_ingestion_loop() {
    if pgrep -f "ingest_loop" > /dev/null; then
        return
    fi
    
    (
        while true; do
            # Run ingestion
            python "$PROJECT_DIR/clide/ingest_swarm.py" >> "$INGEST_LOG" 2>&1
            
            # Regenerate Viz Data (to keep viz updated)
            python "$PROJECT_DIR/viz/generate_semantic_data.py" >> "$INGEST_LOG" 2>&1
            
            # Sleep for 10 minutes
            sleep 600
        done
    ) &
    echo "Started Ingestion Loop (Background)."
}

# Main execution
cd "$PROJECT_DIR" || exit
start_monitor
start_ingestion_loop

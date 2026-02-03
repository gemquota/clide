# Module: Core Monitor (extractor.py)

## Responsibility
The heartbeat of the system. It manages the infinite polling loop and coordinates between ingestion, classification, and registration.

## Algorithmic Flow
1. **Directory Scanning**: Uses `glob` to find the newest session in `~/.gemini/tmp/`.
2. **Persistence Check**: Reads the last processed ID to skip already-analyzed content.
3. **Neural Stream Processing**: 
   - Reads `logs.json`.
   - Filters for `user` messages.
   - Passes text to `intent_classifier`.
4. **Operational Stream Processing**:
   - Calls `shell_ingestor`.
   - Passes batches to `shell_intent_classifier`.
5. **Ingestion Gating**: Implements a non-blocking notification for new assets. Users are prompted to run `clide ingest` to review and finalize detected commands, ensuring the monitor loop remains resilient and autonomous.
6. **Post-Processing**: Updates both Neural and Operational offsets in their respective state files.

## State Management
- **Reads**: `state.json`, `shell_state.json`, `logs.json`, `~/.zsh_history`.
- **Writes**: `state.json`, `shell_state.json`.

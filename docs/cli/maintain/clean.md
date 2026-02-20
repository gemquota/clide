# MAINTAIN CLEAN

- Trims leading and trailing whitespace from all knowledge content.
- Removes extremely short or low-quality nodes (less than 10 characters).
- Ensures the database remains free of 'noise' and garbage entries.
Usage: ./cli maintain clean

- Trims leading and trailing whitespace from all knowledge content.
- Removes extremely short or low-quality nodes (less than 10 characters).
- Ensures the database remains free of 'noise' and garbage entries.
Usage: ./cli maintain clean

TECHNICAL DEEP-DIVE:
The `clean` command is implemented in `clide.brain.auto.auto_clean_metadata`.

### Logic Flow
1. **Fetch**: Retrieves all knowledge nodes from the database.
2. **Sanitization**:
   - **Trimming**: Applies `.strip()` to the `content` field. If changed, calls `storage.update_knowledge`.
   - **Quality Check**: Identifies nodes with content length < 10 characters.
3. **Purge**: Hard-deletes low-quality nodes using `storage.delete_knowledge(id, soft=False)`.
4. **Reporting**: Returns counts of cleaned and removed nodes.

### Code Reference
- **Entry Point**: `clide/serve/portal.py` -> `cmd_maintain`
- **Implementation**: `clide/brain/auto.py` -> `auto_clean_metadata`

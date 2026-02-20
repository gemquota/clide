# [ SECTOR 03: STATE ] - MAINTAIN
System hygiene and automated kernel integrity management.

The `maintain` domain ensures the cleanliness and integrity of the neural registry.

<card>
title: MAINTAIN OVERVIEW
Hygiene: Tagging, Cleaning
Audit: Integrity Checks
Mode: Automated
Status: OPTIMIZED
</card>

### Commands
*   **tag**: Automatically categorizes nodes based on content analysis.
*   **clean**: Sanitizes metadata and removes orphan pointers.
*   **audit**: Performs self-correcting kernel integrity checks.

### Technical Specifications
Maintenance tasks are scheduled to run during idle periods to prevent performance degradation.

<card>
title: OPERATIONAL CONTEXT
Tagging: LLM-Assisted
Cleaning: Regex Sanitization
Audit: Schema Validation + File Verification
</card>

### Usage Examples
1. Run Audit: `./cli maintain audit`
2. Tagging: `./cli maintain tag`
3. Metadata Clean: `./cli maintain clean`

### Dependency Notes
High-frequency tagging requires Gemini API credits. Audit is a purely local operation.

### Architecture Internals
Maintenance operations are orchestrated via `auto.py`. 

<card>
title: NEURAL-KERNEL HOOKS
Tag Hook: clide.brain.auto.auto_tag_nodes
Clean Hook: clide.brain.auto.auto_clean_metadata
Audit Hook: clide.brain.auto.auto_audit_brain
</card>

### API Hooks
*   `auto.auto_audit_brain()`: Full system integrity check.

### Legacy Notes
Maintenance used to be part of the `index` domain but was separated for better sector alignment in `v1.0.0`.
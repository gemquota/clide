# BRAIN // VERIFY
Audits the knowledge base for factual contradictions and integrity.

Cross-references `FACT` and `LESSON` nodes to ensure consistency.

<card>
title: ⦗ INTEGRITY CHECK ⦘
Target: FACT / LESSON
Check: Contradiction Detection
Action: Flag / Report
</card>

### Usage
`./cli brain verify`

### Technical Details
Retrieves all nodes categorized as FACT or LESSON and checks for semantic conflicts (e.g., "The sky is blue" vs "The sky is green").

<card>
title: ⦗ VERIFICATION LOGIC ⦘
Scope: Global Registry
Method: LLM Evaluation
Threshold: High Confidence
</card>

### Code Internals
Calls `atlas.verify_facts()`.
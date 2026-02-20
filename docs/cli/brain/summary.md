# BRAIN // SUMMARY
Generates a high-level executive report of the system's current state.

Synthesizes recent activities, facts, and lessons into a coherent Markdown report.

<card>
title: ⦗ EXECUTIVE REPORT ⦘
Source: Last 30 Nodes
Format: Markdown / Console
Focus: Accomplishments & TODOs
</card>

### Usage
`./cli brain summary`

### Technical Details
Constructs a prompt with the content of the last 30 knowledge nodes and asks the LLM to summarize key developments.

<card>
title: ⦗ SYNTHESIS LOGIC ⦘
Context: 30 Nodes
Prompt: Executive Summary Template
Model: Gemini-1.5-Pro
</card>

### Code Internals
Calls `atlas.generate_brain_summary()`. Uses `clide.brain.model.call_llm`.
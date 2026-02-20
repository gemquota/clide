# PROBE // SCOUT
Performs deep-dive analysis on a single URL using LLM synthesis.

Extracts content, summarizes key points, and identifies potential knowledge nodes from a webpage.

<card>
title: ⦗ SCOUT MISSION ⦘
Target: Single URL
Method: LLM Synthesis
Output: Summary + Nodes
</card>

### Usage
`./cli probe scout "https://example.com"`

### Technical Details
Fetches HTML content, strips boilerplate, and feeds the core text to the Cognitive Engine for structured extraction.

<card>
title: ⦗ EXTRACTION PIPELINE ⦘
1. GET Request
2. DOM Parsing (BS4)
3. Tokenization
4. LLM Analysis
</card>

### Code Internals
Calls `scout.scout_url(url)`. Utilizes `clide.brain.model.call_llm` with a specific `extraction_prompt`.
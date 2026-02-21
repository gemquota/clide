# MAP // TRACE

Displays the full provenance and relational lineage of a specific knowledge node.

## Usage
`./cli map trace <id>`

## Description
This command builds a hierarchical tree visualization for a specific ID, showing its metadata, original source content, and all semantic or manual relationships (links) to other nodes in the brain.

<card>
Title: TRACE METRICS
Root: Target Node ID
Branches: Metadata, Content, Source, Relationships
Engine: clide.serve.atlas.render_trace_tree
</card>
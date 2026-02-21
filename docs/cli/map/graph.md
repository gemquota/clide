# MAP // GRAPH

Generates a relationship map in Mermaid format to visualize the neural topology of the project brain.

## Usage
`./cli map graph [--mermaid] [--amount N]`

## Description
This command analyzes semantic relationships between knowledge units and renders an ASCII relationship graph in the TUI by default. 

With the `--mermaid` flag, it generates a `docs/brain_graph.mmd` file that can be rendered in Mermaid-compatible viewers.

## Arguments
- `--mermaid`: Export to Mermaid syntax file.
- `--amount N`: Number of nodes to analyze (default: 100).

<card>
Title: TOPOLOGY METRICS
Clustering: Leader Algorithm (0.85 Threshold)
Persistence: docs/brain_graph.mmd
Visual: ASCII Panels (Standard Mode)
</card>

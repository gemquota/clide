# ATLAS VISUALIZATION STRATEGY

**Date:** 2026-02-18
**Project:** ATLAS // NEURAL-KERNEL v1.0.0
**Status:** PHASE 4 - STRATEGIC REPORT

## 1. Objective
Transform the `map` command from a directory listing into a high-fidelity architectural analysis interface. The goal is to provide multiple "viewports" into the system's state, structure, and data lineage.

## 2. Target Visualizations

### A. Command Flow Charts (Functional)
*   **Goal:** Visualize how data moves from `cli` -> `logic (sectors)` -> `storage (registry/db)`.
*   **Method:** Directional Flow Graphs.
*   **Tools:** Mermaid.js (Web/Markdown), ASCII Arrows (TUI).

### B. System Architecture (Structural)
*   **Goal:** Show the relationship between Sensory, Cognitive, State, and Executive sectors.
*   **Method:** Nested Box Diagrams / Sector Maps.
*   **Tools:** `rich.Panel` (TUI), React Flow (SPA).

### C. Neural Topology (Data)
*   **Goal:** Visualize the k-NN relationship between knowledge nodes (clusters).
*   **Method:** Force-Directed Graphs / Word Clouds.
*   **Tools:** D3.js (Web), `rich.columns` (TUI).

### D. Provenance Trace (Lineage)
*   **Goal:** Trace the origin of a specific ID back to its raw ingestion source.
*   **Method:** Linear Timeline / Lineage Tree.
*   **Tools:** ASCII Trees (TUI).

## 3. Tool Selection & Rendering Matrix

| Viewport | TUI (CLI) Strategy | SPA (Web) Strategy |
| :--- | :--- | :--- |
| **Graph** | ASCII Tree / Mermaid Code | Mermaid.js / Live Render |
| **Cloud** | `rich.columns` (Keyword Heatmap) | D3.js (Interactive Cloud) |
| **Trace** | `rich.tree` (Lineage) | React Flow (Node Path) |
| **Stats** | `rich.table` (Metrics) | Chart.js (Trends) |

## 4. Implementation Plan

### Phase 4.1: TUI Enhancements (Current)
*   Refactor `clide/serve/atlas.py` to support granular data extraction for graphs and traces.
*   Implement `map --graph` to output Mermaid code or a simplified ASCII representation.
*   Enhance `map --cloud` with frequency weighting using `rich`.

### Phase 4.2: SPA Bridge
*   Ensure all `map` outputs are compatible with the Documentation SPA.
*   Generate JSON snapshots of the system topology for Web consumption.

## 5. Metadata Integration
Visualizations must leverage:
*   `tags`: For clustering and sector grouping.
*   `importance`: For node sizing in clouds/graphs.
*   `timestamp`: For chronological lineage tracing.
*   `similarity`: For edge weights in topological maps.

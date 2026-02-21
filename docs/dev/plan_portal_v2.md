# Unified Intelligence Portal v2 Implementation Plan

## Overview
Upgrade the "Frankenstein" web UI into a cohesive, high-fidelity Command Center. This includes fixing layout distortions, enhancing graph interactivity, styling the documentation, and deepening the functional depth of the main dashboard.

## Scope Definition (CRITICAL)
### In Scope
- Fix CSS layout/distortion in `viz/integrated.html`.
- Enhance Neural Map with legend, filtering, and selection details.
- Upgrade Atlas with rich styling, Mermaid diagrams, and formatted tables.
- Expand Dashboard with real-time charts and deeper system insights.
- Update `scripts/serve_integrated.py` to support new data requirements.

### Out of Scope
- Changing the core `memory.db` schema.
- Implementing a full write-capable terminal in the browser (read-only command execution only).

## Current State Analysis
- `viz/integrated.html`: Basic Tailwind grid, unstyled markdown, limited graph interaction.
- `scripts/serve_integrated.py`: Basic API for stats, stream, and nodes.

## Implementation Phases

### Phase 1: Layout Core & Dashboard Overhaul
- **Goal**: Resolve distortion and add functional depth.
- **Steps**:
  1. [ ] Rewrite `viz/integrated.html` layout to use a fixed sidebar + flexible flex/grid body.
  2. [ ] Implement `Chart.js` for real-time CPU/MEM line charts in the dashboard.
  3. [ ] Add "Kernel Stats" and "Command Distribution" panels with rich visuals.
  4. [ ] Fix modal/panel stretching by using constrained `max-w` and `overflow-y-auto`.
- **Verification**: Run `./cli dash` and verify the UI looks stable on different screen sizes.

### Phase 2: Neural Map Interactivity
- **Goal**: Make the graph a tool for exploration, not just a screensaver.
- **Steps**:
  1. [ ] Add a floating "Category Toggle" panel to the Navigator module.
  2. [ ] Implement `onNodeClick` to open a "Neural Node Inspector" panel.
  3. [ ] Add a color legend for node categories.
  4. [ ] Implement category-based filtering in the graph's `nodeVisibility` logic.
- **Verification**: Click a node, see its content; Toggle "TODO" category, see them disappear/reappear.

### Phase 3: Rich Atlas Documentation
- **Goal**: Transform white text walls into professional documentation.
- **Steps**:
  1. [ ] Integrate `@tailwindcss/typography` or custom CSS classes for markdown rendering.
  2. [ ] Add `mermaid.js` integration to automatically render `mermaid` code blocks.
  3. [ ] Style tables with cyber-noir theme (neon borders, semi-transparent headers).
  4. [ ] Implement a "Breadcrumb" header for the Atlas viewer.
- **Verification**: Navigate to `brain/analyze` in Atlas; verify it looks structured and colorful.

### Phase 4: API Enrichment
- **Goal**: Provide the data needed for Phase 1-3.
- **Steps**:
  1. [ ] Update `/api/stats` to return historical CPU/MEM points for charting.
  2. [ ] Update `/api/nodes` to include relationship data from the `relationships` table.
  3. [ ] Add `/api/run` endpoint to execute non-destructive commands (e.g. `c system health`).
- **Verification**: Test endpoints with `curl` or browser console.

## Finalize
- Move status to 'Plan in Review'.

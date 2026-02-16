# Gemini V2 Neural Map: Interactivity & Interpretability Overhaul Specification

**Version:** 1.0 (Final)
**Status:** Approved for Implementation
**Date:** 2026-02-11
**Target Module:** `viz/modules/v2_neural`

---

## 1. Executive Summary
This document outlines the comprehensive roadmap and technical specification for the "V2 Neural Map" visualization overhaul. The primary goal is to transform the current static display into a highly interactive, interpretable, and user-centric data exploration tool. This overhaul prioritizes deep filtering, structural organization, and enhanced UI/UX patterns suited for complex dataset navigation.

## 2. Product Concept & Vision
The **Neural Map** serves as the topological interface for the Gemini system. Unlike the chaos of the V1 Swarm or the rigidity of the V4 Construct, the V2 Neural Map must provide **clarity through connection**. It is the tool for understanding relationships, clusters, and dependencies.

**Core Pillars:**
1.  **Interpretability:** Users must instantly understand *why* nodes are grouped and *how* they are related.
2.  **Interactivity:** Passive viewing is replaced by active querying, filtering, and manipulating.
3.  **Context:** Metadata is not hidden; it is contextual and available on demand.

## 3. Grand Roadmap

### Phase 1: Foundation & Filtering (Immediate)
*   **Objective:** Enable basic data segmentation.
*   **Features:**
    *   **Group Toggles:** Sidebar control to show/hide specific clusters.
    *   **Meta-Node Filtering:** Toggle to hide/show "Meta" (hub) nodes versus leaf nodes.
    *   **Orphan Management:** Option to hide unconnected nodes to reduce noise.
    *   **Dynamic Stats:** Real-time update of visible node/edge counts.

### Phase 2: Enhanced Layouts & Organization
*   **Objective:** Provide multiple perspectives on the same data.
*   **Features:**
    *   **Layout Switcher:** Toggle between `cose` (physics), `circle` (structural), `breadthfirst` (hierarchical), and `grid` (catalog) layouts.
    *   **Cluster Boxing:** Visual bounding boxes or convex hulls around node groups to clearly delineate territories.
    *   **Edge Weight Thresholding:** Slider to filter edges based on strength/weight.

### Phase 3: Deep Inspection & Analytics
*   **Objective:** Turn the map into an analytical tool.
*   **Features:**
    *   **Pathfinding:** "Select two nodes to find the shortest path" mode.
    *   **Neighborhood Focus:** Double-click a node to fade out everything except its direct neighbors (1st and 2nd degree).
    *   **Annotation Mode:** Ability for users to "pin" nodes or add local notes (persisted to local storage).

### Phase 4: UI/UX Polish
*   **Objective:** Professional-grade usability.
*   **Features:**
    *   **Minimap:** Small navigational map for large datasets.
    *   **Theme Switcher:** Independent dark/light mode toggle for this specific module.
    *   **Context Menu:** Right-click menu for node actions (Focus, Hide, Details).
    *   **Keyboard Shortcuts:** `F` (Find), `R` (Relayout), `H` (Home/Fit).

---

## 4. Technical Specification

### 4.1. Architecture
The overhaul will continue to use **Cytoscape.js** as the core rendering engine due to its performance with graph topology.

*   **State Management:**
    A simple state object will replace scattered variables to manage UI state.
    ```javascript
    const State = {
        filters: {
            activeGroups: new Set([0, 1, 2, ...]),
            showMeta: true,
            minWeight: 0.0
        },
        layout: 'cose',
        selection: null,
        theme: 'light'
    };
    ```

*   **DOM Structure:**
    *   `#cy`: Canvas container.
    *   `#ui-layer`: Pointer-events pass-through layer.
    *   `.sidebar`: Collapsible left panel containing:
        *   Search
        *   Group Toggles (Checkbox list)
        *   Layout Controls
    *   `.inspector`: Right panel (current info-panel) for node details.

### 4.2. Implementation Details

#### A. Group Filtering Logic
Instead of removing elements from the graph (which triggers expensive re-simulations), we will use CSS-like styling classes or direct style updates to manage visibility.
*   **Technique:** `cy.style().selector(...)` updates are efficient.
*   **Filter Function:**
    ```javascript
    function applyFilters() {
        cy.batch(() => {
            cy.nodes().forEach(node => {
                const group = node.data('group');
                const isMeta = node.data('is_meta');
                
                const visible = State.filters.activeGroups.has(group) &&
                                (State.filters.showMeta || !isMeta);
                
                if (visible) {
                    node.style('display', 'element');
                } else {
                    node.style('display', 'none');
                }
            });
        });
    }
    ```

#### B. Layout Management
Switching layouts requires ensuring the simulation stops before starting a new one.
*   **Configuration:**
    *   `cose`: Physics-based, good for general overview.
    *   `concentric`: Good for visualizing hierarchy from a central meta-node.
    *   `grid`: Good for checking inventory without topological noise.

#### C. Pathfinding (Phase 3)
Utilize Cytoscape's A* algorithm.
*   `cy.elements().aStar({ root: sourceNode, goal: targetNode })`
*   Highlight the resulting path with a distinct class `.path-highlight`.

### 4.3. Data Structure Enhancements
The `graph_data.json` should ideally be augmented in the future to include:
*   `group_labels`: Map of `group_id` -> `String Name` (currently inferred or numeric).
*   `metrics`: Centrality scores pre-calculated for coloring important nodes.

---

## 5. UI/UX Design System

### 5.1. Sidebar Control Panel
*   **Location:** Left side, absolute position, collapsible.
*   **Style:** Glassmorphism (blur background), consistent with the new Light Mode theme.
*   **Components:**
    *   **Accordion** sections for "Filters", "Layout", "Settings".
    *   **Color-coded Checkboxes** matching the node colors.

### 5.2. Node Details (Inspector)
*   **Location:** Bottom Right (existing).
*   **Enhancement:** Add "Focus" button to zoom into the node and "Isolate" button to hide unrelated nodes.

### 5.3. Interactivity
*   **Hover:** Instant tooltip, highlight direct connections.
*   **Click:** Persistent selection, opens Inspector.
*   **Background Click:** Clear selection.

---

## 6. Conclusion
This overhaul represents a shift from "visualization" to "exploration application". By implementing Phase 1 immediately, we unlock the ability for users to dissect complex datasets. Subsequent phases will build upon this foundation to provide analytical depth.

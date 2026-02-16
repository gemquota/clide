# Visualization Architecture Specification (V1-V3)

## 1. Overview
The Gemini Visualization Architecture is a modular R&D framework designed to represent high-dimensional semantic command data through various visual metaphors. The system decouples data generation from visual representation, allowing for multiple concurrent "lenses" on the same dataset.

## 2. Data Layer
**Source:** `viz/data/graph_data.json`
**Generator:** `viz/data/generate_semantic_data.py`

### 2.1 Data Schema
The JSON data structure is standardized across all visualization modules.

*   **`nodes` Array:**
    *   `id` (string): Unique identifier (e.g., "command:git_status").
    *   `name` (string): Display label (e.g., "git_status").
    *   `val` (number): Weight/Importance, derived from command occurrence frequency. Range: ~5 to 150.
    *   `group` (integer): Cluster ID (0-11) derived from K-Means clustering of semantic embeddings.
    *   `group_name` (string): Semantic label for the cluster (e.g., "Engineering Cluster").
    *   `description` (string): Full description or docstring of the command.
    *   `is_meta` (boolean): `true` if the node represents a cluster center/hub, `false` for leaf nodes.
    *   `color` (hex string): Pre-calculated color based on group ID (used in some modules).

*   **`links` Array:**
    *   `source` (string): ID of source node.
    *   `target` (string): ID of target node.
    *   `value` (number): Cosine similarity score (0.0 - 1.0).
    *   `is_meta` (boolean): `true` if the link connects a node to its cluster hub.

## 3. Visualization Modules

### 3.1 V1: Semantic Swarm (Legacy)
**Metaphor:** Particle Cloud
**Technology:** `3d-force-graph` (Three.js abstraction)
**File:** `viz/modules/v1_swarm/index.html`

*   **Visual Style:** 3D space, nodes as sprites/spheres.
*   **Interaction:** 
    *   Rotate/Zoom/Pan in 3D.
    *   Hover for floating label.
    *   Click to focus/center camera.
    *   "2D/3D" Toggle button.
*   **Key Logic:**
    *   Uses a force-directed layout where link strength pulls related nodes together.
    *   Meta-nodes serve as gravitational centers for groups.

### 3.2 V2: Neural Map (Backup)
**Metaphor:** Cyberpunk Network / Circuit Board
**Technology:** `Cytoscape.js`
**File:** `viz/modules/v2_neural/index.html`

*   **Visual Style:** 
    *   High-contrast "Neon" aesthetic (Green/Black).
    *   Hexagonal Meta-nodes.
    *   Edges blend colors between source and target groups.
*   **Interaction:**
    *   Sidebar "HUD" for details.
    *   Search filter dims non-matching nodes.
    *   "Relayout" button triggers COSE (Compound Spring Embedder) simulation.
*   **Key Logic:**
    *   Uses `cose` layout for compound packing.
    *   Explicitly visualizes clusters as grouped regions.

### 3.3 V3: Deep Space Observatory (Active)
**Metaphor:** Celestial Star Chart
**Technology:** `D3.js v7`
**File:** `viz/modules/v3_observatory/index.html`

*   **Visual Style:**
    *   Dark "Void" background.
    *   Nodes are "Stars", Clusters are "Galaxies".
    *   "Reticle" overlay follows cursor for a HUD/Sci-Fi scanning effect.
*   **Interaction:**
    *   Pan/Zoom (Geometric Zoom).
    *   "Scanning" (Hover) reveals details in a corner panel.
    *   Draggable nodes with elastic physics.
*   **Key Logic:**
    *   D3 Force Simulation (`d3-force`).
    *   Collision detection preventing overlap (`forceCollide`).
    *   Custom drag behaviors.

## 4. Extrapolation & Derived Requirements
Any future module (V4+) must adhere to the following constraints derived from V1-V3 analysis:

1.  **Data Agnosticism:** Must consume `viz/data/graph_data.json` without modification.
2.  **Cluster Awareness:** Must visually distinguish the 12 semantic groups (`group` ID).
3.  **Meta-Structure:** Must handle `is_meta` nodes differently (e.g., as hubs, containers, or landmarks) or filter them out if inappropriate for the metaphor.
4.  **Interactivity:** Must support:
    *   Node inspection (Details on demand).
    *   Search/Filtering by name.
    *   Navigation (Zoom/Pan or Scroll).
5.  **Performance:** Must handle ~500+ nodes and ~1000+ links at 60fps.

## 5. Proposed V4 Methodology: "The Construct"
**Metaphor:** Isometric Data City
**Technology:** HTML5 Canvas (No framework or minimal wrapper)

*   **Concept:**
    *   Data is physical. Nodes are "Buildings".
    *   Height of building = `val` (Frequency/Importance).
    *   Color of building = `group` (Domain).
    *   Clusters are "Districts" laid out on an isometric grid.
    *   Links are "Skybridges" or "Power lines".
*   **Differentiation:**
    *   Depart from "floating circles" (V1-V3).
    *   Use rigid, orthogonal geometry (Isometric projection).
    *   Focus on "Density" and "Urban Planning" rather than "Gravity".

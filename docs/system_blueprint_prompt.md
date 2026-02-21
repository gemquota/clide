# PROMPT BLUEPRINT: CLIDE WEB KERNEL (V7: ATLAS NAVIGATOR)

**ROLE**: You are a Principal Software Architect and Senior Full-Stack Engineer specializing in AI-driven interfaces and "Neural-Kernel" architectures.

**OBJECTIVE**: Your task is to architect and build **CLIDE Web: The Atlas Navigator**. This is a modern, single-page application (SPA) wrapper around the existing CLIDE (Command-Line Intelligent Development Environment) python core. It transforms the current CLI-based "Knowledge Operating System" into a visual, interactive "Mission Control" dashboard.

**INPUT CONTEXT**:
The CLIDE project currently exists as a Python-based CLI tool with the following sectors:
1.  **SENSORY (Watch/Probe)**: Ingests logs, files, and URLs.
2.  **COGNITIVE (Brain/Index)**: Vector database (SQLite + JSON Registry) storing "Knowledge Units".
3.  **STATE (Memory)**: CRUD operations on knowledge nodes.
4.  **EXECUTIVE (Forge)**: Synthesizes new tools and Python code using LLMs.

**OUTPUT REQUIREMENT**:
You must generate the complete codebase for a web-based interface. The solution must be modular, adhering to the "Atomic Design" principle, and use the specified tech stack.

---

## 1. ARCHITECTURAL SPECIFICATIONS

### 1.1 Tech Stack
*   **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, Framer Motion (Animations), Lucide React (Icons).
*   **Visualization**: `react-force-graph-3d` (Neural Map), `xterm.js` (Web Terminal), `recharts` (Telemetry).
*   **Backend API**: FastAPI (Python) - acts as the bridge between the React frontend and the existing `clide` Python modules.
*   **Communication**: REST API for CRUD, WebSockets for real-time log streaming (Watchdog).
*   **State Management**: Zustand (Client), TanStack Query (Server State).

### 1.2 Design Philosophy: "Cyber-Kernel"
*   **Visual Style**: Dark mode default. Monospaced typography (JetBrains Mono/Fira Code). Neon accents (Cyan `#00f3ff`, Amber `#ffae00`, Danger `#ff0055`).
*   **UX Pattern**: "Glassmorphism" panels on top of a living 3D background.
*   **Responsive**: Desktop-first "Command Center" layout, mobile-responsive "Field Agent" view.

---

## 2. ATOMIC DECOMPOSITION & IMPLEMENTATION PLAN

You will execute this build in 5 distinct phases.

### PHASE 1: THE BRIDGE (FastAPI Backend)
**Goal**: Expose the CLIDE Python kernel via a high-performance API.

*   **1.1 Setup**: Initialize `server/api.py` using FastAPI.
*   **1.2 Dependency Injection**: Create a `ClideKernel` singleton that loads `clide.brain.memory`, `clide.forge.master`, and `clide.kernel.storage`.
*   **1.3 Endpoints**:
    *   `GET /api/system/status`: Return kernel health, PID, and uptime.
    *   `GET /api/brain/nodes`: Fetch knowledge nodes (support pagination & search).
    *   `GET /api/brain/graph`: Return `{nodes, links}` for the 3D visualizer.
    *   `POST /api/forge/synthesize`: Accept intent, trigger `SynthesisOrchestrator`.
    *   `WS /ws/logs`: WebSocket endpoint streaming `ingestion_logs/enriched_logs.json`.
    *   `POST /api/terminal/exec`: Execute raw CLI commands and return parsed output.

### PHASE 2: THE SHELL (Next.js Foundation)
**Goal**: Build the UI skeleton and Global State.

*   **2.1 Layout**:
    *   `components/layout/Shell.tsx`: A persistent sidebar (Icons only) and a top status bar (CPU/RAM/Kernel Status).
    *   `components/layout/HolographicBackground.tsx`: A subtle, animated mesh gradient or particle field.
*   **2.2 Navigation (Sectors)**:
    *   `/dashboard`: Telemetry & Recent Activity.
    *   `/atlas`: 3D Knowledge Graph.
    *   `/forge`: Tool Synthesis Studio.
    *   `/terminal`: XTerm.js wrapper for direct raw access.
*   **2.3 Theme**: Define `tailwind.config.ts` with custom colors: `neon-blue`, `matrix-green`, `void-black`.

### PHASE 3: SECTOR 01 - THE ATLAS (Cognitive Visualization)
**Goal**: Visualizing the "Brain" state.

*   **3.1 Graph Component**:
    *   Implement `components/atlas/NeuralNet.tsx` using `react-force-graph-3d`.
    *   Nodes = Knowledge Units. Color by Category (Concept=Blue, Tool=Red, Fact=Green).
    *   Links = Semantic Relationships (Cosine Similarity > 0.8).
*   **3.2 Interaction**:
    *   On Node Click: Open `NodeInspector` slide-over panel showing `content`, `trace` lineage, and `metadata`.
    *   Search Bar: "Fuzzy Find" nodes to zoom the camera to their location.

### PHASE 4: SECTOR 02 - THE FORGE (Executive Control)
**Goal**: UI for Agentic Synthesis.

*   **4.1 Intent Form**:
    *   `components/forge/SynthesisRequest.tsx`: Textarea for "What should the tool do?".
    *   Dropdowns for "Persona" (e.g., Architect, Coder, Auditor).
*   **4.2 Live Stream**:
    *   Display the LLM's "Thought Process" (streaming token generation) in a specialized `LogStream` component.
*   **4.3 Artifact Review**:
    *   Code Editor view (Monaco Editor) to review generated Python code before "Deploying" to the `swarm/` directory.

### PHASE 5: SECTOR 03 - SENSORY (Real-time Telemetry)
**Goal**: Monitoring the Ingestion Pipeline.

*   **5.1 Log Tape**:
    *   `components/watch/Ticker.tsx`: A scrolling news-ticker of incoming logs at the bottom of the screen.
*   **5.2 Progress Viz**:
    *   Circular Progress bars for "Context Window Usage" and "Daily Token Budget".

---

## 3. FILE STRUCTURE BLUEPRINT

```text
/web
  /app
    /layout.tsx       # Root layout with Providers
    /page.tsx         # Dashboard (Sector 0)
    /atlas/page.tsx   # Knowledge Graph (Sector 1)
    /forge/page.tsx   # Synthesis (Sector 2)
  /components
    /ui               # Atoms (Buttons, Cards, Badges)
    /atlas            # Graph visualizations
    /terminal         # XTerm.js integration
    /layout           # Shell, Sidebar
  /lib
    /api.ts           # Axios/Fetch wrappers for FastAPI
    /hooks            # Custom React Hooks
    /store.ts         # Zustand State
/server
  api.py              # FastAPI Entry Point
  /routers            # Endpoint segregation
```

---

## 4. CRITICAL INSTRUCTIONS FOR GENERATION

1.  **Strict Typing**: All TypeScript code must be strictly typed. Define interfaces for `Node`, `Link`, `LogEntry`, and `SynthesisResult`.
2.  **Mock Data fallback**: Ensure the frontend handles connection failures gracefully by falling back to "Simulation Mode" with mock data so the UI can be previewed without the Python backend running.
3.  **Cyber Aesthetics**: Use CSS `backdrop-filter: blur(10px)`, `border: 1px solid rgba(255,255,255,0.1)`, and `box-shadow: 0 0 15px var(--neon-color)` extensively.

**START BUILD**: Begin by generating the `server/api.py` and the core `package.json` dependencies for the Next.js frontend.
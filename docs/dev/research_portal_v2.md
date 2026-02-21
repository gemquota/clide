# Research: Unified Intelligence Portal v2

## Layout & UX (Issue: Distortion)
- **Problem**: The current dashboard uses a simple Tailwind `grid-cols-3` which can stretch unevenly depending on window size.
- **Solution**: Use a more rigid layout structure with defined widths for side panels and auto-scaling for main content. Implement "Modal" fixes using fixed positioning and centered flex containers.

## Neural Map (Issue: Lack of Control)
- **Problem**: No legend, no filtering, no interaction detail.
- **Solution**:
    - **Legend**: Floating semi-transparent panel with color-coded categories.
    - **Selection**: On node click, populate a detail panel with:
        - Content (formatted)
        - Metadata (ID, Importance, Category)
        - Connected nodes list.
    - **Filtering**: Add toggle switches for each category (FACT, TODO, etc.) to hide/show nodes in real-time.

## Command Atlas (Issue: White Text Wall)
- **Problem**: Unstyled raw markdown.
- **Solution**:
    - Use `@tailwindcss/typography` (via CDN or custom rules).
    - Implement syntax highlighting for code blocks (already using Prism, but needs better integration).
    - **Visual Elements**:
        - **Mermaid**: Use `mermaid.js` to render diagrams defined in docs.
        - **Tables**: Style with neon borders and zebra striping.
        - **Charts**: Use `Chart.js` to display stats if embedded in markdown via special tags (e.g. `<chart type="bar" data="...">`).

## Dashboard (Issue: Lack of Depth)
- **New Features**:
    - **System Health Monitor**: Moving line charts for CPU/MEM over time.
    - **Recent Discoveries**: A "Ticker" or card-based feed of newly ingested facts.
    - **Activity Map**: A heatmap of where/when knowledge was added.
    - **Kernel Config**: Live view of active paths and settings.

## Technical Stack Additions
- **Chart.js**: For real-time telemetry.
- **Mermaid.js**: For architectural diagrams in Atlas.
- **Animate.css**: For smooth transitions between modules.

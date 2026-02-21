# MAP // CLOUD

Generates a dynamic command cloud based on usage frequency and neural importance.

## Usage
`./cli map cloud [--live] [--html] [--amount N] [--min M]`

## Description
This command visualizes the "active centers" of the system by generating a word cloud of commands and keywords. 

- **Static (Default)**: Renders a structured ASCII cloud in the TUI.
- **Live**: Renders a high-refresh TUI visualization (Requires terminal support).
- **HTML**: Generates an interactive SPA visualization in the `viz/` directory.

## Arguments
- `--live`: Real-time TUI visualization.
- `--html`: Export to an interactive HTML/D3.js dashboard.
- `--amount N`: Top N keywords/commands to include (default: 100).
- `--min M`: Minimum frequency count to be included (default: 1).

<card>
Title: VISUALIZATION ENGINE
Static: Rich Columns / ASCII
Live: Framebuffer Streaming
HTML: D3.js Force-Directed Cloud
</card>

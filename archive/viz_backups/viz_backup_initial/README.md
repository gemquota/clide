# Gemini CLI Command Visualization

This directory contains a visualization of the Gemini CLI commands as a 3D node graph.

## How to View

1.  **Start a local web server:**
    Run the following command from the project root:
    ```bash
    python3 -m http.server 8000 --directory viz
    ```

2.  **Open in Browser:**
    Open your web browser and navigate to:
    [http://localhost:8000](http://localhost:8000)

## Features

-   **3D Force-Directed Graph:** Commands are nodes, linked to their Tags.
-   **Search:** Type in the top-left box to find and focus on a specific command.
-   **Details:** Click a node to see its description and full list of tags.
-   **Navigation:** Click and drag to rotate, scroll to zoom.

## Data Source

The data is generated from `ingestion_logs/commands.csv`.
To regenerate the data (if the CSV changes), run:
```bash
python3 viz/generate_data.py
```

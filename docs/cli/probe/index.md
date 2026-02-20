# [ SECTOR 01: SENSORY ] - PROBE
Targeted extraction and precise ingestion from manual sources, URLs, and clipboard.

The `probe` domain provides manual and automated ingestion tools for specific targets.

<card>
title: ⦗ PROBE OVERVIEW ⦘
Capabilities: Web, File, Clipboard
Methods: LLM Synthesis, Regex
Targeting: Selective
Status: OPERATIONAL
</card>

### Commands
*   **scout**: Analyzes a single URL using LLM synthesis for deep extraction.
*   **ingest**: Ingests a local file or directory buffer.
*   **capture**: Ingests content directly from the system clipboard.
*   **crawl**: Recursively ingests a site up to a specified depth.

### Technical Specifications
Probes are high-precision instruments for targeted data gathering.

<card>
title: ⦗ OPERATIONAL CONTEXT ⦘
Web: BeautifulSoup4 / Selenium
File: Multi-buffer Regex
Clipboard: Termux:API Integration
</card>

### Usage Examples
1. Scout a target: `./cli probe scout "https://target.url"`
2. Ingest a document: `./cli probe ingest "data.txt"`
3. Clipboard sync: `./cli probe capture`
4. Site crawl: `./cli probe crawl "https://site.com" --depth 2`

### Architecture Internals
The `probe` sector is modular. Each command utilizes a specific engine (e.g., `scout.py`, `crawl.py`). 

<card>
title: ⦗ NEURAL-KERNEL HOOKS ⦘
Web Hook: clide.probe.web_driver
Ingest Hook: clide.probe.manual.extract
Capture Hook: clide.probe.manual.extract_from_text
</card>

### API Hooks
*   `manual.extract_from_text(content, source)`: Direct text ingestion.
*   `scout.scout_url(url)`: Full web analysis pipeline.

### Code Reference
- **Entry Point**: `clide/serve/portal.py` -> `cmd_probe`
- **Scout**: `clide/probe/scout.py`
- **Manual**: `clide/probe/manual.py`
- **Crawl**: `clide/probe/crawl.py`
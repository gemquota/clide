# Research: Map Input Vectors

**Date**: 2026-02-17
**Ticket**: ticket_01

## 1. Executive Summary
The system uses `clide/serve/portal.py` as the primary CLI entry point. Input is handled via two mechanisms:
1.  **Raw Argument Interception**: `intercept_info_requests` scans `sys.argv` directly for help/reference keywords.
2.  **Structured Parsing**: `argparse` manages the bulk of command execution across 4 sectors.

No direct `input()` calls were found in the entry points. Data ingestion is primarily via command-line arguments (strings, file paths, URLs).

## 2. Technical Context
**File**: `clide/serve/portal.py`
- **Mechanism 1 (Pre-Parse)**: `intercept_info_requests(argv)`
    - **Trigger**: `help`, `?`, `ref`, `atlas`
    - **Modifiers**: `more`, `all`, `full`
    - **Input**: Reads `sys.argv` directly.
- **Mechanism 2 (Main Parse)**: `main()` -> `argparse.ArgumentParser`
    - **Sectors**: Sensory, Cognitive, State, Executive.
    - **Dispatch**: Routes `args` objects to specific command functions (e.g., `cmd_watch`, `cmd_probe`).

**File**: `clide/serve/guide.py`
- **Role**: Output formatter/renderer.
- **Input**: Receives `domain`, `command`, `level` from `portal.py`.
- **File System Access**: Reads `docs/` based on inputs.

## 3. Findings & Analysis
### Input Vectors List

#### A. Raw Interception (`sys.argv`)
| Trigger | Handler | Source |
| :--- | :--- | :--- |
| `help`, `?` | `guide.show_help` | `sys.argv` |
| `ref`, `atlas` | `guide.show_ref` | `sys.argv` |

#### B. Argparse Commands (`portal.py`)

**Sector 01: Sensory**
| Command | Subcommands | Arguments | Potential Risk |
| :--- | :--- | :--- | :--- |
| `watch` | `start`, `stop`, `status`, `logs` | `tail`, `limit` | Low |
| `probe` | `scout` | `url` | **High** (External URL) |
| `probe` | `ingest` | `path` | **High** (File Read) |
| `probe` | `crawl` | `url`, `depth` | **High** (External URL) |

**Sector 02: Cognitive**
| Command | Subcommands | Arguments | Potential Risk |
| :--- | :--- | :--- | :--- |
| `search` | - | `query` | Medium (DB Query) |
| `brain` | `analyze`, `summary`, `verify` | - | Low |
| `map` | `graph`, `cloud`, `trace` | `id`, `live`, `html`, `min`, `top` | Low |
| `index` | `rebuild`, `cluster`, `prune`... | - | Low |

**Sector 03: State**
| Command | Subcommands | Arguments | Potential Risk |
| :--- | :--- | :--- | :--- |
| `memory` | `create`, `edit` | `content`, `category`, `tags` | Medium (DB Write) |
| `memory` | `connect`, `delete` | `id`, `id1`, `id2` | Low |
| `run` | `task` (`add`) | `content` | Medium (DB Write) |

**Sector 04: Executive**
| Command | Subcommands | Arguments | Potential Risk |
| :--- | :--- | :--- | :--- |
| `forge` | `tool`, `evolve`, `design` | `prompt`, `instruction`, `desc` | **High** (LLM Injection/Gen) |
| `forge` | `skill`, `persona` | `name` | Low |
| `system` | `config`, `backup` | - | Low |

## 4. Technical Constraints
- **Validation**: Minimal validation observed in `portal.py`. Most args are passed directly to backend modules.
- **Paths**: `probe ingest` takes a `path`. Path traversal vulnerability checks should be verified in `clide.probe.manual`.

## 5. Architecture Documentation
The pattern is `Command -> Argparse -> Dispatch Function -> Backend Module`.
Input sanitization is largely delegated to the backend modules (if it exists).

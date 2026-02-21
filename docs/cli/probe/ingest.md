# PROBE // INGEST

Extracts project knowledge from a local file and processes it into the neural brain.

## Usage
`./cli probe ingest <path>`

## Description
This command reads the content of the specified file, cleans it of metadata or "slop", and uses the LLM to categorize and index it into `memory.db`.

## Examples
- `./cli probe ingest README.md`
- `./cli probe ingest scripts/engine.py`

<card>
Title: INGESTION PIPELINE
Source: Local Filesystem
Process: LLM Distillation -> Vectorization -> Storage
Format: .py, .md, .json, .txt, .log
</card>

# PROBE // MANUAL (INGEST)
Manually ingests a local file or directory buffer into the knowledge base.

Reads a local file, analyzes its content, and categorizes it as a knowledge node.

<card>
title: ⦗ INGEST OPERATION ⦘
Source: Local File System
Method: Read + Analyze
Dest: Vector Registry
</card>

### Usage
`./cli probe ingest "path/to/file.txt"`

### Technical Details
Supports text-based formats (.txt, .md, .py, .json). Binary files are ignored.

<card>
title: ⦗ FILE HANDLING ⦘
Mode: Read-Only (r)
Limit: 3000 chars (Sample)
</card>

### Code Internals
Calls `manual.extract_from_file(path)`.
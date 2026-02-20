# PROBE // CAPTURE
Ingests content directly from the system clipboard (Termux/Android).

Rapidly saves clipboard contents as a knowledge node.

<card>
title: ⦗ CLIPBOARD SYNC ⦘
Source: Termux API
Method: termux-clipboard-get
Latency: < 200ms
</card>

### Usage
`./cli probe capture`

### Technical Details
Executes the `termux-clipboard-get` shell command via subprocess to retrieve text.

<card>
title: ⦗ API BRIDGE ⦘
Shell: subprocess.run
Command: termux-clipboard-get
Fallback: None (Req: Termux:API)
</card>

### Code Internals
Calls `manual.extract_from_text(content, source="clipboard")`.
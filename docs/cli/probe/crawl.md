# PROBE // CRAWL
Recursively ingests a website up to a specified depth.

Crawls a target domain, following internal links and ingesting content.

<card>
title: ⦗ CRAWL OPERATION ⦘
Target: Domain Root
Depth: User Defined
Limit: Safety Cap (50 pages)
</card>

### Usage
`./cli probe crawl "https://site.com" --depth 2`

### Technical Details
Uses a breadth-first search (BFS) algorithm to traverse links. Respects `robots.txt` where possible.

<card>
title: ⦗ TRAVERSAL LOGIC ⦘
Queue: FIFO
Filter: Same-Domain Only
Delay: 1s (Politeness)
</card>

### Code Internals
Calls `crawl.crawl_site(url, depth)`. Manages a `visited` set to prevent cycles.
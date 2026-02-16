# CLIDE // PROBE DOMAIN

## Tier: Basic
- scout <url>   : Forced web scrape of a specific URL.
- manual <path> : Targeted extraction from a local file.
- capture       : Immediate ingest from the system clipboard.
- crawl         : Scheduled feed ingestion (Git/RSS).
Usage: ./cli probe {scout, manual, capture, crawl}

## Tier: More
- scout <url>   : Forced web scrape of a specific URL.
- manual <path> : Targeted extraction from a local file.
- capture       : Immediate ingest from the system clipboard.
- crawl         : Scheduled feed ingestion (Git/RSS).
Usage: ./cli probe {scout, manual, capture, crawl}

TECHNICAL ARCHITECTURE:
Unlike the passive Watch domain, Probe initiates connections to pull data.
- Scout uses 'requests' and 'beautifulsoup4' for DOM parsing.
- Manual uses custom buffer reading to handle large legacy documentation files.
- Clipboard ingestion leverages 'termux-clipboard-get' on Android.
Primary Directory: clide/probe/

## Tier: Full
- scout <url>   : Forced web scrape of a specific URL.
- manual <path> : Targeted extraction from a local file.
- capture       : Immediate ingest from the system clipboard.
- crawl         : Scheduled feed ingestion (Git/RSS).
Usage: ./cli probe {scout, manual, capture, crawl}

TECHNICAL ARCHITECTURE:
Unlike the passive Watch domain, Probe initiates connections to pull data.
- Scout uses 'requests' and 'beautifulsoup4' for DOM parsing.
- Manual uses custom buffer reading to handle large legacy documentation files.
- Clipboard ingestion leverages 'termux-clipboard-get' on Android.
Primary Directory: clide/probe/

[EXPANSION PENDING]

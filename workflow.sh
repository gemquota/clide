#!/bin/bash
# CLIDE Workflow Automation Script
# Usage: ./workflow.sh [feed|passive|archeology|clean] [arg]

MODE=$1
ARG=$2

case $MODE in
  feed)
    echo "Running 'The Feed' workflow..."
    if [[ -z "$ARG" ]]; then echo "Error: URL/Path required"; exit 1; fi
    if [[ "$ARG" == http* ]]; then ./cli probe scout "$ARG"; else ./cli probe ingest "$ARG"; fi
    ./cli maintain clean
    ./cli maintain tag
    ./cli index optimize
    ./cli index rebuild
    ;;
  passive)
    echo "Running 'The Panopticon' workflow..."
    ./cli watch start
    ./cli maintain audit
    ;;
  archeology)
    echo "Running 'The Archeologist' workflow..."
    ./cli memory merge
    ./cli index cluster
    ./cli map graph
    ;;
  clean)
    echo "Running 'The Janitor' workflow..."
    ./cli maintain clean
    ./cli maintain audit
    ./cli index prune
    ;;
  *)
    echo "Usage: ./workflow.sh [feed|passive|archeology|clean] [arg]"
    exit 1
    ;;
esac

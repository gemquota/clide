import os
import json
import time
from clide.brain.reason import classify_intent
from clide.kernel import storage
from clide.brain.memory import get_embedding
from clide.kernel.engine import handle_analysis

def extract_from_text(content, source="clipboard"):
    """Manually ingests raw text content into the brain."""
    if not content.strip():
        print("[!] Content is empty.")
        return

    print(f"[Probe] Ingesting from {source}...")
    try:
        # Take first 3000 chars for analysis
        sample = content[:3000]
        print(f"  [>] Analyzing {len(sample)} chars...")
        
        analysis = classify_intent(f"Extract project knowledge from this content: {sample}", {})
        
        if analysis.get("category") in ["FACT", "DISCOVERY", "TODO", "LESSON"]:
            msg = {
                "message": f"Manual ingestion from {source}",
                "sessionId": f"manual_ingest_{source}",
                "messageId": int(time.time()),
                "type": "user"
            }
            embedding = get_embedding(sample[:500])
            handle_analysis(analysis, msg, embedding)
            print(f"[v] Ingestion complete. Saved as {analysis.get('category')}.")
        else:
            print("[!] No significant knowledge extracted from content.")
            
    except Exception as e:
        print(f"[Error] Ingestion failed: {e}")

def extract_from_file(path):
    """Manually reads a file and extracts knowledge into the brain."""
    if not os.path.exists(path):
        print(f"[!] File not found: {path}")
        return

    print(f"[Probe] Reading file: {path}...")
    try:
        with open(path, 'r', errors='ignore') as f:
            content = f.read()
        extract_from_text(content, source=os.path.basename(path))
            
    except Exception as e:
        print(f"[Error] File reading failed: {e}")

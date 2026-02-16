import requests
from bs4 import BeautifulSoup
from clide.brain.reason import classify_intent
from clide.kernel import storage
import json

def scout_url(url):
    """Proactively scrapes a URL and ingests findings into the brain."""
    print(f"[Probe] Scouting URL: {url}...")
    
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "CLIDE-Scout/1.0"})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Strip scripts and styles
        for script in soup(["script", "style"]):
            script.extract()
            
        text = soup.get_text(separator=' ')
        # Simple chunking
        lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 20]
        full_text = " ".join(lines)
        
        # Send to brain in chunks if very large, otherwise process the first 3000 chars
        sample = full_text[:3000]
        print(f"  [>] Analyzing {len(sample)} chars of content...")
        
        # For simplicity in this CLI trigger, we ask for a broad classification
        analysis = classify_intent(f"Extract project knowledge from this web content: {sample}", {})
        
        if analysis.get("category") in ["FACT", "DISCOVERY", "TODO"]:
            from clide.kernel.engine import handle_analysis
            # Mock a message object for the handler
            msg = {
                "message": sample[:100] + "...",
                "sessionId": "scout_session",
                "messageId": 0,
                "type": "user"
            }
            from clide.brain.memory import get_embedding
            embedding = get_embedding(sample[:500])
            handle_analysis(analysis, msg, embedding)
            print(f"[v] Scouting complete. Category: {analysis.get('category')}")
        else:
            print("[!] No significant knowledge extracted from URL.")
            
    except Exception as e:
        print(f"[Error] Scouting failed: {e}")

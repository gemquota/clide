import subprocess
import json

def get_extracted_facts(query=""):
    import sqlite3
    import json
    from vector_registry import get_embedding, cosine_similarity
    
    facts = []
    
    try:
        conn = sqlite3.connect("/data/data/com.termux/files/home/meta/clide_src/memory.db")
        # Optimization: Check if any facts exist before calling embedding engine
        count = conn.execute("SELECT COUNT(*) FROM knowledge WHERE category = 'FACT'").fetchone()[0]
        if count == 0:
            conn.close()
            return "No specific project context found."

        query_emb = get_embedding(query)
        cursor = conn.execute("SELECT content, importance, embedding FROM knowledge WHERE category = 'FACT'")
        
        candidates = []
        for row in cursor.fetchall():
            content, importance, emb_blob = row
            emb = json.loads(emb_blob.decode('utf-8'))
            similarity = cosine_similarity(query_emb, emb)
            
            # Hybrid Score: 70% Similarity, 30% Importance
            score = (similarity * 0.7) + ((importance / 10.0) * 0.3)
            candidates.append((score, content))
        
        conn.close()
        
        # Sort by score and take top 10
        candidates.sort(key=lambda x: x[0], reverse=True)
        facts = [c[1] for c in candidates[:10]]
        
    except Exception as e:
        # Fallback to latest 5 if semantic search fails
        try:
            conn = sqlite3.connect("/data/data/com.termux/files/home/meta/clide_src/memory.db")
            cursor = conn.execute("SELECT content FROM knowledge WHERE category = 'FACT' ORDER BY timestamp DESC LIMIT 5")
            facts = [row[0] for row in cursor.fetchall()]
            conn.close()
        except: pass
        
    return "\n".join([f"- {f}" for f in facts]) if facts else "No relevant project context found."

def generate_command_template(command_name, description, user_request):
    # Load the agent constitution (agents.md)
    guidelines = ""
    try:
        with open("/data/data/com.termux/files/home/meta/swarm/core/agents.md", "r") as f:
            guidelines = f.read()
    except Exception as e:
        guidelines = "No specific guidelines found."

    # Use user_request to find semantically relevant facts
    facts = get_extracted_facts(user_request)

    prompt = f"""
# ... (same prompt content) ...
"""

    try:
        import os
        env = os.environ.copy()
        env["GEMINI_SANDBOX"] = "false"
        result = subprocess.run(
            ["gemini", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=90,
            env=env
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error generating template: {e}"

if __name__ == "__main__":
    # Test
    print(generate_command_template("test_cmd", "Tests the generator", "Make a command that tests things"))

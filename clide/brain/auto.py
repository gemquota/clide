import json
from clide.kernel import storage
from clide.brain.model import call_llm

def auto_tag_nodes():
    """Fetches nodes without tags and generates them using the LLM."""
    print("[Brain] Scanning for untagged knowledge...")
    nodes = storage.get_knowledge(limit=50) # Get recent nodes
    
    for node in nodes:
        # Check if already tagged in the 'review' column
        if "TAGS:" in (node['review'] or ""):
            continue
            
        print(f"  [>] Generating tags for Node #{node['id']}...")
        prompt = f"Analyze this project knowledge and provide 3-5 succinct tags as a comma-separated list.\n\nContent: {node['content']}"
        tags = call_llm(prompt).strip()
        storage.update_node_tags(node['id'], tags.split(","))

def auto_prioritize_tasks():
    """Uses LLM to assign importance scores to TODOs based on current project state."""
    print("[Brain] Re-prioritizing task queue...")
    todos = storage.get_knowledge(category="TODO")
    
    context = "\n".join([f"- [{t['id']}] {t['content']}" for t in todos])
    prompt = f"""Analyze these project tasks and assign an importance score (1-10) to each. 
    Return ONLY a JSON mapping: {{"id": score, ...}}
    
    Tasks:
    {context}
    """
    
    try:
        res = call_llm(prompt)
        scores = json.loads(res[res.find("{"):res.rfind("}")+1])
        for tid, score in scores.items():
            storage.update_node_importance(int(tid), int(score))
        print("[v] Task prioritization complete.")
    except Exception as e:
        print(f"[!] Prioritization failed: {e}")

def auto_audit_brain():
    print("[Brain] Searching for knowledge contradictions...")
    # Semantic match logic would go here
    pass

def auto_sync_todos():
    """Reconciles memory.db and todo.md."""
    print("[Brain] Synchronizing task state...")
    from clide.tools.janitor import TodoManager
    mgr = TodoManager()
    mgr.sync_to_file()
    print("[v] DB and todo.md are now in parity.")

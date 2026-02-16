from swarm.core.state_manager import get_project_status, KnowledgeProvider, MEMORY_DB_PATH, get_db
import os

def verify_phase3():
    print("--- Phase 3 Manual Verification ---")
    
    # 1. Ensure there is some knowledge data
    with get_db(MEMORY_DB_PATH) as conn:
        conn.execute("INSERT INTO knowledge (category, content, importance) VALUES (?, ?, ?)", 
                     ('LESSON', 'Phase 3 Verification: Integration is key.', 9))
    
    # 2. Check project status output
    print("\nChecking 'get_project_status' output:")
    status = get_project_status()
    print(status)
    
    if "Recent Knowledge:" in status:
        print("\nSUCCESS: 'Recent Knowledge' section found in status.")
    else:
        print("\nFAILURE: 'Recent Knowledge' section NOT found.")

    # 3. Verify agents.md update
    print("\nVerifying 'swarm/core/agents.md' update:")
    with open('swarm/core/agents.md', 'r') as f:
        content = f.read()
        if "Semantic Context Retrieval:" in content:
            print("SUCCESS: Instruction for Semantic Context Retrieval found in agents.md.")
        else:
            print("FAILURE: Instruction NOT found in agents.md.")

if __name__ == "__main__":
    verify_phase3()


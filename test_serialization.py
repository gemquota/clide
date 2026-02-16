import json
import os
import sys

# Ensure project root is in path
sys.path.append(os.getcwd())

try:
    from swarm.core.state_manager import query_project_knowledge
    print("Testing query_project_knowledge...")
    data = query_project_knowledge(limit=5)
    print("Data type:", type(data))
    
    # Try to serialize
    serialized = json.dumps(data)
    print("Successfully serialized to JSON.")
    print("Snippet:", serialized[:200])
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()

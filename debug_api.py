import sys
import os
import json

sys.path.append(os.getcwd())
from swarm.core.state_manager import query_project_knowledge

try:
    print("Calling query_project_knowledge...")
    result = query_project_knowledge(limit=5)
    print("Result (first 500 chars):")
    print(result[:500])
except Exception as e:
    print(f"Error caught: {e}")
    import traceback
    traceback.print_exc()

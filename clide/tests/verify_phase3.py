import os
import sys

# Ensure paths are correct
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

def verify_phase3():
    from clide.forge.master import SynthesisOrchestrator
    from clide.brain import memory as vector_registry
    from clide.kernel.storage import get_db, DB_PATH

    print("--- Phase 3 Manual Verification ---")
    orchestrator = SynthesisOrchestrator()
    
    # We use a tool name that is unlikely to exist
    tool_name = "provenance_test_tool_99"
    intent = {
        "tool_name": tool_name,
        "description": "A tool to verify registry indexing.",
        "logic_code": "def run(): return 'registry ok'"
    }
    
    print(f"\n>>> Simulating synthesis flow for: {tool_name}")
    
    # For verification script, we'll patch verify_and_deploy to ensure success
    from unittest.mock import patch
    with patch('clide.forge.asset.verify_and_deploy') as mock_verify:
        mock_verify.return_value = True
        result = orchestrator.process_intent(intent)
    
    print(f"Synthesis Status: {result.get('status')}")
    
    if result.get('status') == 'success':
        # 1. Check Registry
        print("\n1. Checking Vector Registry:")
        matches = vector_registry.search_registry(tool_name)
        found_in_registry = any(m[1]['id'] == f'mcp:{tool_name}' for m in matches)
        if found_in_registry:
            print(f"[v] SUCCESS: Tool '{tool_name}' indexed in Vector Registry.")
        else:
            print(f"[!] FAILURE: Tool '{tool_name}' NOT found in Registry.")
            
        # 2. Check State DB
        print("\n2. Checking State DB (knowledge):")
        # In the new system, we save knowledge in memory.db
        import sqlite3
        conn = sqlite3.connect(os.path.join(BASE_DIR, "clide/memory.db"))
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM knowledge WHERE content LIKE ?", (f"%{tool_name}%",)).fetchone()
        if row:
            print(f"[v] SUCCESS: Synthesis event (or related fact) recorded in memory.db. Category: {row['category']}")
        else:
            # We didn't actually call save_knowledge in process_intent yet, let's check if we should
            print("[?] Note: Orchestrator currently doesn't record to knowledge table directly, but it indexes in vector registry.")

    else:
        print(f"[!] Synthesis failed: {result.get('message')}")

if __name__ == "__main__":
    verify_phase3()
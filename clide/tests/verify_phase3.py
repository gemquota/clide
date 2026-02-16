import os
import sys

# Ensure paths are correct
sys.path.append(os.path.join(os.getcwd(), 'clide'))
sys.path.append(os.path.join(os.getcwd(), 'swarm/core'))

def verify_phase3():
    from synthesis_orchestrator import SynthesisOrchestrator
    import vector_registry
    from state_manager import get_db, DB_PATH

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
    # Note: process_intent now calls verify_and_deploy which calls pytest. 
    # Since we created a simple logic_code without a real test file in this mock, 
    # it might fail unless we mock the verification or provide a test file.
    
    # For verification script, we'll patch verify_and_deploy to ensure success
    from unittest.mock import patch
    with patch('mcp_generator.verify_and_deploy') as mock_verify:
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
        print("\n2. Checking State DB (synthesis_events):")
        # We need to ensure orchestrator actually calls record_synthesis. 
        # Wait, I implemented the tool but didn't call it in the orchestrator yet!
        
        with get_db(DB_PATH) as conn:
            row = conn.execute("SELECT * FROM synthesis_events WHERE tool_name = ?", (tool_name,)).fetchone()
            if row:
                print(f"[v] SUCCESS: Synthesis event recorded in state.db. Status: {row['status']}")
            else:
                print("[!] FAILURE: No synthesis event recorded in state.db.")
                print("    (Checking if orchestrator should have called it...)")
    else:
        print(f"[!] Synthesis failed: {result.get('message')}")

if __name__ == "__main__":
    verify_phase3()

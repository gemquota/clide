import os
import shutil
import sys

# Ensure clide is in path
sys.path.append(os.path.join(os.getcwd(), 'clide'))

def verify_phase2():
    from mcp_generator import verify_and_deploy

    print("--- Phase 2 Manual Verification ---")
    test_dir = os.path.join(os.getcwd(), "swarm/commands/mcp_servers/test_manual_verify")
    os.makedirs(test_dir, exist_ok=True)
    
    # 1. Create a PASSING test
    with open(os.path.join(test_dir, "test_test_manual_verify.py"), "w") as f:
        f.write("def test_always_pass(): assert True")
    
    print("\n>>> Testing Scenario: PASSING")
    success = verify_and_deploy("test_manual_verify", test_dir)
    if success:
        print("[v] SUCCESS: verify_and_deploy correctly identified a passing tool.")
    else:
        print("[!] FAILURE: verify_and_deploy rejected a passing tool.")

    # 2. Create a FAILING test
    with open(os.path.join(test_dir, "test_test_manual_verify.py"), "w") as f:
        f.write("def test_always_fail(): assert False")
    
    print("\n>>> Testing Scenario: FAILING")
    success = verify_and_deploy("test_manual_verify", test_dir)
    if not success:
        print("[v] SUCCESS: verify_and_deploy correctly rejected a failing tool.")
    else:
        print("[!] FAILURE: verify_and_deploy accepted a failing tool.")
    
    shutil.rmtree(test_dir)

if __name__ == "__main__":
    verify_phase2()

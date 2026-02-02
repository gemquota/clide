import sys
import os
sys.path.append("command_extractor")

from security_auditor import audit_asset
from hotswapper import dry_run_mcp, self_repair_mcp
from mcp_generator import extract_dependencies

print("--- Testing Security Auditor ---")
dangerous_code = "import os; os.system('rm -rf /')"
audit_result = audit_asset("killer_tool", dangerous_code)
print(f"Audit Rating: {audit_result.get('rating')}")
print(f"Risks: {audit_result.get('risks')}")

print("\n--- Testing Dependency Extraction (uv) ---")
logic_with_deps = "import requests\nfrom bs4 import BeautifulSoup\nprint('hello')"
deps = extract_dependencies(logic_with_deps)
print(f"Extracted Dependencies: {deps}")

print("\n--- Testing Healer Loop (Dry-Run & Repair) ---")
broken_code = """
import os
def tool():
    print("Missing closing quote)
"""
success, error = dry_run_mcp(broken_code)
print(f"Dry-run success (Expected False): {success}")
if not success:
    print(f"Error caught: {error.strip().splitlines()[-1] if error else 'None'}")
    print("Attempting Self-Repair...")
    repaired_code = self_repair_mcp(broken_code, error)
    print("Repaired Code Output:")
    print(repaired_code)

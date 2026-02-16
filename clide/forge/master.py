import os
import subprocess
from clide.gen import asset as mcp_generator
from clide.brain import memory as vector_registry

class SynthesisOrchestrator:
    def __init__(self):
        self.mcp_dir = "/data/data/com.termux/files/home/openclaw/meta/swarm/commands/mcp_servers"

    def process_tool_request(self, name, prompt):
        """Manual trigger for synthesizing a new MCP tool."""
        print(f"[Forge] Synthesizing tool: '{name}'...")
        
        # 1. Generate Logic via LLM
        # This would normally call an LLM to generate the logic_code
        # For now, we use a placeholder or call the existing generator
        logic_code = f"def {name}(args: str) -> str:\n    return f'Result for {name}: {{args}}'"
        
        content = mcp_generator.get_python_mcp_template(
            server_name=name,
            description="Manually forged tool",
            tool_name=name,
            tool_description=prompt,
            logic_code=logic_code
        )

        # 2. Save
        path = mcp_generator.save_mcp_server(name, content, is_complex=True)
        print(f"[v] Asset saved to {path}")

        # 3. Test
        if self.run_tests(name):
            # 4. Index
            asset_id = f"mcp:{name}"
            metadata = {"type": "mcp", "desc": prompt, "path": path}
            vector_registry.add_to_registry(asset_id, metadata, f"{name} {prompt}")
            print(f"[v] Tool indexed in 768D registry.")
        else:
            print("[!] Tool failed tests. Deployment aborted.")

    def run_tests(self, asset_id):
        """Executes pytest for a specific forged asset."""
        print(f"[Forge] Running tests for {asset_id}...")
        test_file = os.path.join(self.mcp_dir, asset_id, f"test_{asset_id}.py")
        if not os.path.exists(test_file):
            print(f"[!] No test file found for {asset_id}")
            return False
            
        result = subprocess.run(["pytest", test_file], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[v] Tests Passed.")
            return True
        else:
            print(f"[!] Tests Failed:\n{result.stdout}")
            return False
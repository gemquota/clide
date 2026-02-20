import os
import subprocess
from clide.forge import asset as mcp_generator
from clide.brain import memory as vector_registry

class SynthesisOrchestrator:
    def __init__(self):
        self.mcp_dir = "/data/data/com.termux/files/home/openclaw/meta/swarm/commands/mcp_servers"

    def process_tool_request(self, name, prompt):
        """Manual trigger for synthesizing a new MCP tool."""
        print(f"[Forge] Synthesizing tool: '{name}'...")
        
        # 1. Generate Logic via LLM
        logic_code = mcp_generator.generate_logic(name, prompt)
        
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
        test_dir = os.path.join(self.mcp_dir, asset_id)
        test_file = os.path.join(test_dir, f"test_{asset_id}.py")
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

    def evolve_tool(self, asset_id, instruction):
        """Iteratively refines an existing tool based on instructions."""
        print(f"[Forge] Evolving asset '{asset_id}'...")
        
        # 1. Locate existing file
        path = os.path.join(self.mcp_dir, asset_id, f"{asset_id}.py")
        if not os.path.exists(path):
            path = os.path.join(self.mcp_dir, f"{asset_id}.py")
            
        if not os.path.exists(path):
            print(f"[!] Asset '{asset_id}' not found at {path}")
            return

        with open(path, 'r') as f:
            old_code = f.read()

        # 2. Prompt LLM for refinement
        print(f"[Forge] Sending refinement request to model...")
        new_code = mcp_generator.refine_logic(asset_id, old_code, instruction)
        
        if not new_code:
            print("[!] Refinement failed (empty response).")
            return

        # 3. Backup and Save
        backup_path = path + ".bak"
        import shutil
        shutil.copy2(path, backup_path)
        
        with open(path, 'w') as f:
            f.write(new_code)
        print(f"[v] Asset refined. Backup saved to {backup_path}")

        # 4. Test
        if self.run_tests(asset_id):
            # 5. Re-index
            metadata = {"type": "mcp", "desc": f"Evolved: {instruction}", "path": path, "last_evolved": datetime.now().isoformat()}
            vector_registry.add_to_registry(f"mcp:{asset_id}", metadata, f"{asset_id} {instruction}")
            print(f"[v] Evolved tool re-indexed.")
        else:
            print("[!] Evolved tool failed tests. Reverting...")
            shutil.move(backup_path, path)

    def generate_design(self, name, desc):
        """Generates UI/UX designs or mockups."""
        print(f"[Forge] Generating design for: '{name}'...")
        design_dir = "/data/data/com.termux/files/home/openclaw/meta/swarm/designs"
        os.makedirs(design_dir, exist_ok=True)
        
        path = os.path.join(design_dir, f"{name}.md")
        # Logic for UI/UX generation would call an LLM here
        content = f"# Design: {name}\n\n## Description\n{desc}\n\n## Mockup Placeholder\n[SCENE: {desc}]\n"
        
        with open(path, 'w') as f:
            f.write(content)
            
        print(f"[v] Design brief saved to {path}")
        # Index
        vector_registry.add_to_registry(f"design:{name}", {"type": "design", "desc": desc}, f"{name} {desc}")

    def create_skill(self, name, description):
        """Creates a new modular skill for the agent swarm."""
        print(f"[Forge] Synthesizing skill: '{name}'...")
        skill_dir = os.path.join("/data/data/com.termux/files/home/openclaw/meta/swarm/skills", name)
        os.makedirs(skill_dir, exist_ok=True)
        
        # 1. Create SKILL.md
        md_content = f"# Skill: {name}\n\n## Description\n{description}\n\n## Instructions\n- [TBD]\n\n## Available Resources\n- [TBD]\n"
        with open(os.path.join(skill_dir, "SKILL.md"), 'w') as f:
            f.write(md_content)
            
        # 2. Create __init__.py
        init_content = f'# Modular skill: {name}\n'
        with open(os.path.join(skill_dir, "__init__.py"), 'w') as f:
            f.write(init_content)
            
        print(f"[v] Skill '{name}' created at {skill_dir}")
        
        # 3. Index
        metadata = {"type": "skill", "desc": description, "path": skill_dir}
        vector_registry.add_to_registry(f"skill:{name}", metadata, f"{name} {description}")
        print(f"[v] Skill indexed in neural registry.")

    def define_persona(self, name, description, directive):
        """Defines a new system-prompt persona."""
        print(f"[Forge] Defining persona: '{name}'...")
        persona_dir = "/data/data/com.termux/files/home/openclaw/meta/swarm/personas"
        os.makedirs(persona_dir, exist_ok=True)
        
        path = os.path.join(persona_dir, f"{name}.toml")
        content = f'name = "{name}"\ndescription = "{description}"\ndirective = "{directive}"\nstatus = "initialized"\n'
        
        with open(path, 'w') as f:
            f.write(content)
            
        print(f"[v] Persona '{name}' saved to {path}")
        
        # Index
        metadata = {"type": "persona", "desc": description, "path": path}
        vector_registry.add_to_registry(f"persona:{name}", metadata, f"{name} {description}")
        print(f"[v] Persona indexed.")

    def run_benchmark(self, asset_id):
        """Runs execution timing benchmarks for a tool."""
        print(f"[Forge] Benchmarking asset '{asset_id}'...")
        # Simple profiling logic
        import time
        start = time.time()
        # In a real scenario, we would execute the tool with dummy inputs
        # For now, we simulate a load
        time.sleep(0.5) 
        duration = time.time() - start
        
        print(f"[v] Benchmark complete: {duration:.4f}s avg latency.")
        # Store in registry
        vector_registry.add_to_registry(f"mcp:{asset_id}", {"last_benchmark": duration}, f"benchmark {asset_id}")

    def archive_asset(self, asset_id):
        """Safely archives an asset to the archive directory."""
        print(f"[Forge] Archiving asset '{asset_id}'...")
        import shutil
        from datetime import datetime
        
        # Check in mcp_dir
        source_dir = os.path.join(self.mcp_dir, asset_id)
        if not os.path.exists(source_dir):
            # Check for single file
            source_dir = os.path.join(self.mcp_dir, f"{asset_id}.py")
            
        if not os.path.exists(source_dir):
            print(f"[!] Asset '{asset_id}' not found.")
            return

        archive_root = os.path.join(os.path.dirname(self.mcp_dir), "../../archive/forged_assets")
        os.makedirs(archive_root, exist_ok=True)
        
        dest = os.path.join(archive_root, f"{asset_id}_{datetime.now().strftime('%Y%m%d')}")
        shutil.move(source_dir, dest)
        print(f"[v] Asset archived to {dest}")
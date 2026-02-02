import subprocess
import json
import os

def get_extracted_facts(query=""):
    import sqlite3
    import json
    from vector_registry import get_embedding, cosine_similarity
    
    query_emb = get_embedding(query)
    facts = []
    
    try:
        conn = sqlite3.connect("/data/data/com.termux/files/home/meta/clide_src/memory.db")
        cursor = conn.execute("SELECT content, importance, embedding FROM knowledge WHERE category = 'FACT'")
        
        candidates = []
        for row in cursor.fetchall():
            content, importance, emb_blob = row
            emb = json.loads(emb_blob.decode('utf-8'))
            similarity = cosine_similarity(query_emb, emb)
            
            # Hybrid Score: 70% Similarity, 30% Importance
            score = (similarity * 0.7) + ((importance / 10.0) * 0.3)
            candidates.append((score, content))
        
        conn.close()
        
        # Sort by score and take top 10
        candidates.sort(key=lambda x: x[0], reverse=True)
        facts = [c[1] for c in candidates[:10]]
        
    except Exception as e:
        pass
        
    return "\n".join([f"- {f}" for f in facts]) if facts else "No relevant project context found."

def generate_tool_metadata(tool_name, logic_code):
    """Uses Gemini to generate docstrings and type hints for the tool."""
    # Load guidelines
    guidelines = ""
    try:
        with open("/data/data/com.termux/files/home/meta/swarm/core/agents.md", "r") as f:
            guidelines = f.read()
    except:
        guidelines = "Follow standard best practices."

    # Use tool logic/name as query context
    facts = get_extracted_facts(f"{tool_name} {logic_code}")

    prompt = f"""
Generate a professional Python docstring and suggest a type-hinted function signature for this logic:
Logic: {logic_code}
Tool Name: {tool_name}

### PROJECT GUIDELINES (CONSTITUTION)
{guidelines}

### EXTRACTED PROJECT CONTEXT (FACTS)
{facts}

Return ONLY the docstring and the signature line (e.g. def tool(args: str) -> str:).
"""
    try:
        result = subprocess.run(["gemini", "-p", prompt], capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return f'def {tool_name}(args: str) -> str:\n    """Logic for {tool_name}"""'

def extract_dependencies(logic_code):
    """Uses Gemini to detect required external libraries."""
    prompt = f"""
Identify the Python external libraries (PyPI package names) required to run this code:
Code:
{logic_code}

Return ONLY a comma-separated list of package names (e.g., "requests,beautifulsoup4"). If none, return "None".
"""
    try:
        result = subprocess.run(["gemini", "-p", prompt], capture_output=True, text=True)
        deps = result.stdout.strip()
        if deps.lower() == "none": return []
        return [d.strip() for d in deps.split(",")]
    except:
        return []

def get_python_mcp_template(server_name, description, tool_name, tool_description, logic_code):
    metadata = generate_tool_metadata(tool_name, logic_code)
    deps = extract_dependencies(logic_code)
    # Always include fastmcp if it's the framework used
    if "mcp" not in [d.lower() for d in deps]: deps.append("mcp[cli]")
    
    dep_string = "\n".join([f'#   "{d}",' for d in deps])
    
    return f'''# /// script
# requires-python = ">=3.10"
# dependencies = [
{dep_string}
# ]
# ///
import asyncio
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server synthesized by CLIDE
mcp = FastMCP("{server_name}")

@mcp.tool()
{metadata}
    # {tool_description}
    {logic_code}

if __name__ == "__main__":
    mcp.run()
'''

def generate_tests(tool_name, logic_code):
    """Uses Gemini to generate a basic unit test for the logic."""
    prompt = f"Generate a basic Python unit test using 'pytest' for this logic: {logic_code}. Ensure it tests the '{tool_name}' function. Return ONLY the code."
    try:
        result = subprocess.run(["gemini", "-p", prompt], capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return f"# Manual test required for {tool_name}"

def generate_readme(name, description, tool_details):
    """Generates a brief README.md for the package."""
    return f"# {name}\n\n{description}\n\n## Usage\nThis is an MCP tool synthesized by CLIDE.\n\n### Logic Overview\n{tool_details}"

def save_mcp_server(server_name, content, is_complex=False, description=""):
    mcp_dir = "/data/data/com.termux/files/home/meta/swarm/commands/mcp_servers"
    os.makedirs(mcp_dir, exist_ok=True)
    
    if not is_complex:
        file_path = os.path.join(mcp_dir, f"{server_name}.py")
        with open(file_path, "w") as f:
            f.write(content)
        print(f"MCP Server '{server_name}' saved to {file_path}")
        return file_path
    else:
        # Create a Package Directory
        package_dir = os.path.join(mcp_dir, server_name)
        os.makedirs(package_dir, exist_ok=True)
        
        # 1. Logic
        logic_path = os.path.join(package_dir, f"{server_name}.py")
        with open(logic_path, "w") as f:
            f.write(content)
        
        # 2. README
        with open(os.path.join(package_dir, "README.md"), "w") as f:
            f.write(generate_readme(server_name, description, "Synthesized MCP Logic"))
            
        # 3. Tests
        test_content = generate_tests(server_name, content)
        with open(os.path.join(package_dir, f"test_{server_name}.py"), "w") as f:
            f.write(test_content)
            
        print(f"Complex MCP Package '{server_name}' saved to {package_dir}")
        return logic_path
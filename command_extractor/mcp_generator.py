import subprocess
import json
import os

def generate_tool_metadata(tool_name, logic_code):
    """Uses Gemini to generate docstrings and type hints for the tool."""
    prompt = f"""
Generate a professional Python docstring and suggest a type-hinted function signature for this logic:
Logic: {logic_code}
Tool Name: {tool_name}

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

def save_mcp_server(server_name, content):
    mcp_dir = "/data/data/com.termux/files/home/meta/commands/mcp_servers"
    os.makedirs(mcp_dir, exist_ok=True)
    file_path = os.path.join(mcp_dir, f"{server_name}.py")
    with open(file_path, "w") as f:
        f.write(content)
    print(f"MCP Server '{server_name}' saved to {file_path}")
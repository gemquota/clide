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

def get_python_mcp_template(server_name, description, tool_name, tool_description, logic_code):
    metadata = generate_tool_metadata(tool_name, logic_code)
    
    return f'''
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
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "None",
#   "mcp[cli]",
# ]
# ///
import asyncio
from mcp.server.fastmcp import FastMCP


# Initialize FastMCP server synthesized by CLIDE
mcp = FastMCP("debug_tool")

@mcp.tool()
def debug_tool(args: str) -> str:
    return 'debug ok'

if __name__ == "__main__":
    mcp.run()

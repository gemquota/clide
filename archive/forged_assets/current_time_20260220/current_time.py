# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "None",
#   "mcp[cli]",
# ]
# ///
import asyncio
from mcp.server.fastmcp import FastMCP
import datetime

# Initialize FastMCP server synthesized by CLIDE
mcp = FastMCP("current_time")

@mcp.tool()

def current_time(args: str) -> str:
    """
    Returns the current date and time as a string.

    Args:
        args: (str) Any arguments passed to the function (ignored).

    Returns:
        str: A string representing the current date and time in ISO format,
             or an error message if an exception occurs.
    """
    try:
        now = datetime.datetime.now()
        return now.isoformat()
    except Exception as e:
        return f"Error getting current time: {e}"

if __name__ == "__main__":
    mcp.run()

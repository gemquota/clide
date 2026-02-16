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
mcp = FastMCP("provenance_test_tool_99")

@mcp.tool()
```python
def run() -> str:
    """
    This tool checks the status of the registry.

    Returns:
        str: A string indicating the registry status. Currently, it always returns 'registry ok'.
    """
    return 'registry ok'
```

    # A tool to verify registry indexing.
    def run(): return 'registry ok'

if __name__ == "__main__":
    mcp.run()

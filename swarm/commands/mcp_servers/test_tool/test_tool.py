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
mcp = FastMCP("test_tool")

@mcp.tool()
```python
def test_tool() -> None:
    """Prints "hello" to the console.

    This tool serves as a basic example for testing and demonstration purposes.
    It performs a simple print operation.

    Tool Name: test_tool
    """
```

```python
def test_tool() -> None:
```
    # A tool for testing
    print('hello')

if __name__ == "__main__":
    mcp.run()

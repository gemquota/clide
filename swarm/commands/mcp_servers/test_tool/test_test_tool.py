```python
import pytest
from mcp.server.fastmcp import FastMCP
import asyncio
from io import StringIO
import sys

# Capture stdout for testing print statements
@pytest.fixture
def capture_stdout(monkeypatch):
    buffer = StringIO()
    monkeypatch.setattr(sys.stdout, 'buffer', buffer)
    return buffer

def test_tool_output(capture_stdout):
    """Tests that the test_tool function prints 'hello' to stdout."""

    # Initialize FastMCP server synthesized by CLIDE - minimal implementation for testing
    class MockFastMCP:
        def __init__(self, tool_name):
            self.tool_name = tool_name
            self.tools = {}

        def tool(self):
            def decorator(func):
                self.tools[func.__name__] = func
                return func
            return decorator
        
        def run(self):
            if "test_tool" in self.tools:
                self.tools["test_tool"]()


    mcp = MockFastMCP("test_tool")

    @mcp.tool()
    def test_tool() -> None:
        print('hello')

    mcp.run()

    assert capture_stdout.getvalue().strip() == 'hello'
```
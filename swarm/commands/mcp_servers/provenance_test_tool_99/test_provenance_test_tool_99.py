```python
import pytest
import asyncio
from mcp.server.fastmcp import FastMCP

@pytest.fixture
def mcp_instance():
    """Fixture to create a FastMCP instance for testing."""
    mcp = FastMCP("provenance_test_tool_99")
    return mcp

@pytest.fixture
def run_tool(mcp_instance):
    """Fixture to execute the 'run' tool via FastMCP."""
    async def _run_tool():
      # Capture stdout and stderr
      original_stdout = mcp_instance.sys.stdout
      original_stderr = mcp_instance.sys.stderr
      try:
        mcp_instance.sys.stdout = mcp_instance.sys.stderr = StringIO()
        result = await mcp_instance.handle_cli_command(["run"])
        return result
      finally:
        mcp_instance.sys.stdout = original_stdout
        mcp_instance.sys.stderr = original_stderr

    from io import StringIO
    return _run_tool

@pytest.mark.asyncio
async def test_run_success(mcp_instance, run_tool):
    """Test the standard success case for the 'run' tool."""
    result = await run_tool()
    assert result == "registry ok"

# Note: The tool provided doesn't take any input, so edge cases like empty/large input don't apply directly.
#       If the tool *did* have an input, we'd add tests here to cover those.
#       For instance, if the tool took a string argument:
#
# async def test_run_edge_empty_input(mcp_instance, run_tool):
#     # This test doesn't work since "run" doesn't take arguments, but shows the structure for if it did.
#     # We'd need to simulate calling run with the appropriate arguments via handle_cli_command
#     with pytest.raises(TypeError): #Or whatever exception is raised for a missing argument.
#         await run_tool()


@pytest.mark.asyncio
async def test_run_failure_invalid_type(mcp_instance):
    """Test potential failure modes (e.g., if the registry check raised an exception)."""
    # This test demonstrates how to mock the internal function and force a specific error.
    # It doesn't test *this* specific code directly, but illustrates how to test failures.
    from unittest.mock import patch

    @mcp_instance.tool()
    def faulty_run() -> str:
       raise ValueError("Simulated error during registry check")

    async def _run_faulty_tool():
      original_stdout = mcp_instance.sys.stdout
      original_stderr = mcp_instance.sys.stderr
      try:
        from io import StringIO
        mcp_instance.sys.stdout = mcp_instance.sys.stderr = StringIO()
        result = await mcp_instance.handle_cli_command(["faulty_run"])
        return result
      finally:
        mcp_instance.sys.stdout = original_stdout
        mcp_instance.sys.stderr = original_stderr


    with pytest.raises(ValueError, match="Simulated error during registry check"):
        await _run_faulty_tool()
```
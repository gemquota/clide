import pytest
from debug_tool import debug_tool

def test_debug_tool_success():
    assert debug_tool("any_string") == "debug ok"

def test_debug_tool_empty_input():
    assert debug_tool("") == "debug ok"

def test_debug_tool_large_input():
    large_input = "a" * 1000
    assert debug_tool(large_input) == "debug ok"

# The debug_tool function doesn't really have a failure mode based on input string, 
# as it always returns "debug ok" regardless of the input.  However, if we *expected* it
# to do something different for specific inputs, we could write a test to check for that.

# For example, if the intent was that debug_tool should raise an exception if the input is too long,
# we could write a test like this (but it will fail with the current implementation):
#def test_debug_tool_large_input_raises_exception():
#    with pytest.raises(ValueError): # or whatever exception type is appropriate
#        large_input = "a" * 2000 # Assuming 2000 is above the limit
#        debug_tool(large_input)


# To simulate a failure mode, let's mock the function to raise an exception under certain conditions:

def test_debug_tool_simulated_failure():
    # Create a mock function that raises an exception for specific input
    def mock_debug_tool(args: str) -> str:
        if args == "fail":
            raise ValueError("Simulated failure")
        else:
            return "debug ok"

    # Test the success case with the mock
    assert mock_debug_tool("success") == "debug ok"

    # Test the failure case with the mock
    with pytest.raises(ValueError) as excinfo:
        mock_debug_tool("fail")
    assert str(excinfo.value) == "Simulated failure"
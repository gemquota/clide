import pytest
from current_time import current_time
import datetime

def test_current_time_success():
    """Test that current_time returns a string."""
    result = current_time("")
    assert isinstance(result, str)
    try:
        datetime.datetime.fromisoformat(result)
    except ValueError:
        pytest.fail("current_time did not return a valid ISO formatted datetime string")


def test_current_time_with_empty_input():
    """Test that current_time works with an empty string as input."""
    result = current_time("")
    assert isinstance(result, str)
    try:
        datetime.datetime.fromisoformat(result)
    except ValueError:
        pytest.fail("current_time did not return a valid ISO formatted datetime string with empty input")


def test_current_time_with_large_input():
    """Test that current_time works with a large string as input (which should be ignored)."""
    large_input = "This is a very long string that should be ignored by the function."
    result = current_time(large_input)
    assert isinstance(result, str)
    try:
        datetime.datetime.fromisoformat(result)
    except ValueError:
        pytest.fail("current_time did not return a valid ISO formatted datetime string with large input")

def test_current_time_failure_no_exception():
    """Test that current_time handles exceptions gracefully.  This test is somewhat artificial because datetime.datetime.now() very rarely errors, but tests the error handling code path."""
    #Note:  Directly mocking datetime.datetime.now() is generally not recommended in unit tests unless absolutely necessary and well-justified. This would create tight coupling and complex setup and teardown that overshadows the core logic of the function being tested.  It's best to test that the function handles exceptions gracefully if one were to occur, rather than trying to force one.

    original_datetime = datetime.datetime

    class MockDatetime:
        @staticmethod
        def now():
            raise ValueError("Simulated datetime error")

    datetime.datetime = MockDatetime # type: ignore

    result = current_time("")
    assert "Error getting current time" in result

    datetime.datetime = original_datetime # type: ignore
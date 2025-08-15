import sys
import os
import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from modes.cpu.cpu_usage import get_cpu_usage

def test_get_cpu_usage_structure_and_types():
    """
    Tests the basic structure and data types of the get_cpu_usage() response.
    """
    result = get_cpu_usage()

    # Check that no error was returned
    assert "error" not in result, f"Function returned an error: {result.get('error')}"

    # Check that the result is a dictionary
    assert isinstance(result, dict)

    # Check for the presence of required keys
    required_keys = ["usage_percent", "per_core", "core_count"]
    for key in required_keys:
        assert key in result, f"Required key '{key}' is missing from the result"

    # Check the types of the values
    assert isinstance(result["usage_percent"], float), "usage_percent should be a float"
    assert isinstance(result["per_core"], list), "per_core should be a list"
    assert isinstance(result["core_count"], int), "core_count should be an int"

    # Check the validity of the usage percentage
    assert 0 <= result["usage_percent"] <= 100, "usage_percent must be between 0 and 100"

    # Check that the per_core list has the correct number of items
    assert len(result["per_core"]) == result["core_count"], "Length of 'per_core' list should match 'core_count'"

    # Check that all items in per_core are floats or ints (psutil can return both)
    for core_usage in result["per_core"]:
        assert isinstance(core_usage, (float, int)), "All items in 'per_core' should be numbers"
        assert 0 <= core_usage <= 100, "All core usage values must be between 0 and 100"

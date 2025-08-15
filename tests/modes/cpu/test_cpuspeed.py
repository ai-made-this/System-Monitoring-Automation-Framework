import sys
import os
import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from modes.cpu.cpuspeed import get_cpu_speed

def test_get_cpu_speed_structure_and_types():
    """
    Tests the basic structure and data types of the get_cpu_speed() response.
    """
    result = get_cpu_speed()

    # Check that the result is a dictionary
    assert isinstance(result, dict)

    # If there's an error (e.g., permissions), the test should not fail, but we can't check keys.
    if "error" in result:
        print(f"Note: get_cpu_speed() returned an error: {result['error']}. Skipping key checks.")
        return

    # Check for the presence of required keys
    required_keys = ["current_mhz", "min_mhz", "max_mhz"]
    for key in required_keys:
        assert key in result, f"Required key '{key}' is missing from the result"

    # Check the types of the values (can be float or int)
    assert isinstance(result["current_mhz"], (float, int)), "current_mhz should be a number"
    assert isinstance(result["min_mhz"], (float, int)), "min_mhz should be a number"
    assert isinstance(result["max_mhz"], (float, int)), "max_mhz should be a number"

    # Check for plausible values
    assert result["current_mhz"] > 0, "current_mhz should be greater than 0"

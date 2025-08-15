import sys
import os
import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from modes.cpu.cputemp import get_cpu_temp

def test_get_cpu_temp_structure_and_types():
    """
    Tests the basic structure and data types of the get_cpu_temp() response.
    """
    result = get_cpu_temp()

    # Check that the result is a dictionary
    assert isinstance(result, dict)

    # It's common for temp sensors to be unavailable. If so, an error is expected.
    if "error" in result:
        print(f"Note: get_cpu_temp() returned an error: {result['error']}. This may be expected.")
        assert "No compatible temperature sensors found" in result['error'] or "can't find any physical temperature sensors" in result['error']
        return

    # If there is no error, check for the presence of required keys
    required_keys = ["temp_celsius", "high_threshold", "critical_threshold"]
    for key in required_keys:
        assert key in result, f"Required key '{key}' is missing from the result"

    # Check the types of the values
    assert isinstance(result["temp_celsius"], (float, int)), "temp_celsius should be a number"

    # The thresholds can be None, so we check for number or NoneType
    assert isinstance(result["high_threshold"], (float, int, type(None))), "high_threshold should be a number or None"
    assert isinstance(result["critical_threshold"], (float, int, type(None))), "critical_threshold should be a number or None"

    # Check for a plausible temperature
    assert -20 < result["temp_celsius"] < 120, "CPU temperature seems implausible"

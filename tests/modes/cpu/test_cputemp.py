import unittest
import sys
import os

# Add the parent directory of `modes` to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from modes.cpu.cputemp import get_cpu_temp

class TestCpuTemp(unittest.TestCase):

    def test_get_cpu_temp_structure(self):
        """
        Test the structure of the dictionary returned by get_cpu_temp, including fallback to py_cpuinfo.
        """
        temp_data = get_cpu_temp()
        if "error" in temp_data:
            self.assertIsInstance(temp_data["error"], str)
        else:
            self.assertIn("temp_celsius", temp_data)
            self.assertIsInstance(temp_data["temp_celsius"], (int, float))
            # If thresholds are present, check their types
            if "high_threshold" in temp_data:
                if temp_data["high_threshold"] is not None:
                    self.assertIsInstance(temp_data["high_threshold"], (int, float))
            if "critical_threshold" in temp_data:
                if temp_data["critical_threshold"] is not None:
                    self.assertIsInstance(temp_data["critical_threshold"], (int, float))

if __name__ == '__main__':
    unittest.main()
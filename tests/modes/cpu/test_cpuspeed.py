import unittest
import sys
import os

# Add the parent directory of `modes` to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from modes.cpu.cpuspeed import get_cpu_speed

class TestCpuSpeed(unittest.TestCase):

    def test_get_cpu_speed_structure_and_values(self):
        """
        Test the structure and values of the dictionary returned by get_cpu_speed.
        """
        speed_data = get_cpu_speed()
        if "error" in speed_data:
            self.assertIsInstance(speed_data["error"], str)
        else:
            self.assertIn("current_mhz", speed_data)
            self.assertIn("min_mhz", speed_data)
            self.assertIn("max_mhz", speed_data)

            self.assertIsInstance(speed_data["current_mhz"], (int, float))
            self.assertGreater(speed_data["current_mhz"], 0)

            # min and max can be 0 on some systems
            self.assertIsInstance(speed_data["min_mhz"], (int, float))
            self.assertGreaterEqual(speed_data["min_mhz"], 0)

            self.assertIsInstance(speed_data["max_mhz"], (int, float))
            self.assertGreaterEqual(speed_data["max_mhz"], 0)

if __name__ == '__main__':
    unittest.main()
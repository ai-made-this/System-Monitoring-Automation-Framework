import unittest
import sys
import os

# Add the parent directory of `modes` to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from modes.cpu.cpu_usage import get_cpu_usage

class TestCpuUsage(unittest.TestCase):

    def test_get_cpu_usage_structure_and_values(self):
        """
        Test the structure and values of the dictionary returned by get_cpu_usage.
        """
        usage_data = get_cpu_usage()
        if "error" in usage_data:
            self.assertIsInstance(usage_data["error"], str)
        else:
            self.assertIn("usage_percent", usage_data)
            self.assertIn("per_core", usage_data)
            self.assertIn("core_count", usage_data)

            self.assertIsInstance(usage_data["usage_percent"], (int, float))
            self.assertGreaterEqual(usage_data["usage_percent"], 0)
            self.assertLessEqual(usage_data["usage_percent"], 100)

            self.assertIsInstance(usage_data["per_core"], list)
            if usage_data["per_core"]:
                self.assertIsInstance(usage_data["per_core"][0], (int, float))

            self.assertIsInstance(usage_data["core_count"], int)
            self.assertGreater(usage_data["core_count"], 0)
            self.assertEqual(len(usage_data["per_core"]), usage_data["core_count"])

if __name__ == '__main__':
    unittest.main()
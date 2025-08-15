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
        Handles None and error cases for Pylance compatibility.
        """
        usage_data = get_cpu_usage()
        self.assertIsInstance(usage_data, dict)
        if usage_data is None:
            self.fail("get_cpu_usage() returned None")
        if "error" in usage_data:
            self.assertIsInstance(usage_data["error"], str)
        else:
            self.assertIn("usage_percent", usage_data)
            self.assertIn("per_core", usage_data)
            self.assertIn("core_count", usage_data)

            self.assertIsInstance(usage_data.get("usage_percent"), (int, float))
            self.assertGreaterEqual(usage_data.get("usage_percent", 0), 0)
            self.assertLessEqual(usage_data.get("usage_percent", 100), 100)

            per_core = usage_data.get("per_core")
            core_count = usage_data.get("core_count")
            self.assertIsInstance(per_core, list)
            if per_core and len(per_core) > 0:
                self.assertIsInstance(per_core[0], (int, float))
            self.assertIsInstance(core_count, int)
            self.assertGreater(core_count, 0)
            self.assertEqual(len(per_core), core_count)

if __name__ == '__main__':
    unittest.main()
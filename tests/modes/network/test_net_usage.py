import unittest
from modes.network import net_usage

class TestNetUsage(unittest.TestCase):
    def test_net_usage_output(self):
        result = net_usage.get_net_usage()
        self.assertIsInstance(result, dict)
        self.assertIn('total_usage', result)
        self.assertIn('interfaces', result)

if __name__ == "__main__":
    unittest.main()

import unittest
from modes.network import net_latency

class TestNetLatency(unittest.TestCase):
    def test_net_latency_output(self):
        result = net_latency.get_net_latency()
        self.assertIsInstance(result, dict)
        self.assertIn('latency_ms', result)

if __name__ == "__main__":
    unittest.main()

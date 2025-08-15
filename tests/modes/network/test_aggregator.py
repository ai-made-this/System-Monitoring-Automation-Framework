import unittest
from modes.network import aggregator

class TestNetworkAggregator(unittest.TestCase):
    def test_aggregator_output(self):
        result = aggregator.aggregate_network_data()
        self.assertIsInstance(result, dict)

if __name__ == "__main__":
    unittest.main()

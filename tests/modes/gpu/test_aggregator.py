import unittest
from modes.gpu import aggregator

class TestGPUAggregator(unittest.TestCase):
    def test_aggregator_output(self):
        result = aggregator.aggregate_gpu_data()
        self.assertIsInstance(result, dict)

if __name__ == "__main__":
    unittest.main()

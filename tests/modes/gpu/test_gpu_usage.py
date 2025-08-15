import unittest
from modes.gpu import gpu_usage

class TestGPUUsage(unittest.TestCase):
    def test_gpu_usage_output(self):
        result = gpu_usage.get_gpu_usage()
        self.assertIsInstance(result, dict)
        self.assertIn('gpu_usage', result)

if __name__ == "__main__":
    unittest.main()

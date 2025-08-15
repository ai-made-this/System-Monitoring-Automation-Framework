import unittest
from modes.gpu import gpuspeed

class TestGPUSpeed(unittest.TestCase):
    def test_gpu_speed_output(self):
        result = gpuspeed.get_gpu_speed()
        self.assertIsInstance(result, dict)
        self.assertIn('gpu_speed', result)

if __name__ == "__main__":
    unittest.main()

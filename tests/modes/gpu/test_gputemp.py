import unittest
from modes.gpu import gputemp

class TestGPUTemp(unittest.TestCase):
    def test_gpu_temperature_output(self):
        result = gputemp.get_gpu_temperature()
        self.assertIsInstance(result, dict)
        self.assertIn('gpu_temperature', result)

if __name__ == "__main__":
    unittest.main()

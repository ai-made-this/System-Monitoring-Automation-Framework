import unittest
from modes.network import net_speed

class TestNetSpeed(unittest.TestCase):
    def test_net_speed_output(self):
        result = net_speed.get_net_speed()
        self.assertIsInstance(result, dict)
        self.assertIn('upload_mbps', result)
        self.assertIn('download_mbps', result)

if __name__ == "__main__":
    unittest.main()

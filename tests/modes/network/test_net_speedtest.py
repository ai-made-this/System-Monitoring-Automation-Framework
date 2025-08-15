import unittest
from modes.network import net_speedtest

class TestNetSpeedtest(unittest.TestCase):
    def test_net_speedtest_output(self):
        result = net_speedtest.get_net_speedtest()
        self.assertIsInstance(result, dict)
        self.assertIn('download_mbps', result)
        self.assertIn('upload_mbps', result)
        self.assertIn('ping_ms', result)

if __name__ == "__main__":
    unittest.main()

import unittest
import sys
import os
import json

# Add the parent directory of `modes` to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from modes.cpu import aggregator

class TestCpuAggregator(unittest.TestCase):

    def test_list_modes(self):
        """Test that list_modes returns the correct list of modes."""
        modes = aggregator.list_modes()
        self.assertEqual(sorted(modes), sorted(['all', 'basic', 'detailed']))

    def test_list_modules(self):
        """Test that list_modules returns the correct list of modules."""
        modules = aggregator.list_modules()
        self.assertEqual(sorted(modules), sorted(['cpu_usage', 'cpuspeed', 'cputemp']))

    def test_run_mode_all(self):
        """Test the 'all' mode of the aggregator."""
        results = aggregator.run_mode('all')
        self.assertIn('cpuspeed', results)
        self.assertIn('cputemp', results)
        self.assertIn('cpu_usage', results)
        # Check that the results are dictionaries (not error strings)
        self.assertIsInstance(results['cpuspeed'], dict)
        self.assertIsInstance(results['cputemp'], dict)
        self.assertIsInstance(results['cpu_usage'], dict)

    def test_run_mode_basic(self):
        """Test the 'basic' mode of the aggregator."""
        results = aggregator.run_mode('basic')
        self.assertIn('cpuspeed', results)
        self.assertIn('cputemp', results)
        self.assertNotIn('cpu_usage', results)

    def test_run_mode_invalid(self):
        """Test running an invalid mode."""
        with self.assertRaises(ValueError):
            aggregator.run_mode('invalid_mode')

if __name__ == '__main__':
    unittest.main()

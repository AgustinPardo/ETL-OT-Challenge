import sys
import os
sys.path.insert(1, os.path.dirname(os.getcwd()))

import unittest
from code.parser import Parser
from code.cpu import CPU


class HiddenPrints:
    """Utility Class to prevent prints"""

    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class TestTransformation(unittest.TestCase):
    """Test trasformation process on minimal mock datasets"""

    @classmethod
    def setUpClass(self):
        """Create Parser for later use in the tests"""

        self.parser = Parser("mock_data", CPU.count_cpus())

    def test_transform(self):
        """Run transform_data on mock datasets"""

        with HiddenPrints():
            self.parser.transform_data()
        print(self.parser.data_transformed)

    def test_target_target_pair(self):
        """Check target_target_pair value on mock datasets"""

        with HiddenPrints():
            self.assertEqual(self.parser.target_target_pair(), 4)

if __name__ == "__main__":
    unittest.main()

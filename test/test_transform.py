import sys
import os
sys.path.insert(1, os.path.dirname(os.getcwd()))

import unittest
from code.parser import Parser
from code.cpu import CPU


class TestTransformation(unittest.TestCase):
    """ """

    @classmethod
    def setUpClass(self):
        """Create Parser for later use in the tests"""
        self.parser = Parser("mock_data", CPU.count_cpus())

    def test_transform(self):
        """ """
        self.parser.transform_data()
        print(self.parser.data_transformed)

    def test_target_target_pair(self):
        """ """
        self.assertEqual(self.parser.target_target_pair(), 2)

if __name__ == "__main__":
    unittest.main()

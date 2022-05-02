import sys
import os
sys.path.insert(1, os.path.dirname(os.getcwd()))

import unittest
from code.parser import Parser
from code.cpu import CPU

class TestMetadata(unittest.TestCase):
    """Test datasets metadata format and quality input as the parser expects to oprate correctly"""

    @classmethod
    def setUpClass(self):
        """Create Parser for later use in the tests"""
        self.parser = Parser("../data", CPU.count_cpus())
        self.parser.parse_data(self.parser.evidence)
        self.parser.parse_data(self.parser.target)
        self.parser.parse_data(self.parser.disease)

        self.evidence_df = self.parser.evidence.df
        self.target_df = self.parser.target.df
        self.disease_df = self.parser.disease.df

    def test_empty_dataframe(self):
        """Test if a dataframe is empty"""
        self.assertEqual(self.evidence_df.empty, False)
        self.assertEqual(self.target_df.empty, False)
        self.assertEqual(self.disease_df.empty, False)

    def test_columns_exist(self):
        """Test existing columns"""
        self.assertEqual(list(self.evidence_df), ['targetId', 'diseaseId', 'score'])
        self.assertEqual(list(self.target_df.columns), ["id", "approvedSymbol"])
        self.assertEqual(list(self.disease_df.columns), ["id", "name"])
    
    def test_columns_type(self):
        """Test type of columns"""
        self.assertEqual(self.evidence_df.score.dtype, float)
        self.assertEqual(self.evidence_df.targetId.dtype.name, "object")
        self.assertEqual(self.evidence_df.diseaseId.dtype.name, "object")
        self.assertEqual(self.target_df.id.dtype.name, "object")
        self.assertEqual(self.disease_df.id.dtype.name, "object")

    def test_empty_values(self):
        """Test if exist empty values on the columns"""
        self.assertEqual((self.evidence_df.score == '').any(), False)
        self.assertEqual((self.evidence_df.targetId == '').any(), False)
        self.assertEqual((self.evidence_df.diseaseId == '').any(), False)
        self.assertEqual((self.target_df.id == '').any(), False)
        self.assertEqual((self.disease_df.id == '').any(), False)
        
    def test_null_values(self):
        """Test if exist null values on the columns"""
        self.assertEqual(self.evidence_df.score.isnull().any(), False)
        self.assertEqual(self.evidence_df.targetId.isnull().any(), False)
        self.assertEqual(self.evidence_df.diseaseId.isnull().any(), False)
        self.assertEqual(self.target_df.id.isnull().any(), False)
        self.assertEqual(self.disease_df.id.isnull().any(), False)

    def test_score_range(self):
        """Test score column range between 0 and 1"""
        self.assertEqual(self.evidence_df.score.between(0,1).all(), True)

    def test_duplicated_rows(self):
        """Test if exist duplcated rows"""
        self.assertEqual(self.target_df.duplicated().all(), False)
        self.assertEqual(self.disease_df.duplicated().all(), False)

if __name__ == "__main__":
    unittest.main()

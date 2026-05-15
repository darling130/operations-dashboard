"""
Unit Tests for Data Validation Module
Author: Gnanachandu Kalla
Organization: Arrowcosta Technology Pvt Ltd
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from validation import DataValidator


class TestDataValidator(unittest.TestCase):
    """Test cases for DataValidator class"""

    def setUp(self):
        """Set up test data before each test"""
        self.test_data = pd.DataFrame({
            'date': pd.date_range('2026-02-01', periods=10),
            'shift': ['Morning'] * 10,
            'production_line': ['Line_A'] * 10,
            'units_produced': [1000, 1100, 900, 1050, 1200, 950, 1080, 1150, 990, 1020],
            'planned_production': [1100] * 10,
            'defect_count': [20, 25, 15, 22, 30, 18, 24, 28, 16, 21],
            'downtime_minutes': [30, 45, 20, 35, 50, 25, 40, 48, 22, 32],
            'oee': [85.5, 82.3, 88.1, 84.7, 79.5, 86.8, 83.2, 80.9, 87.4, 85.0],
            'defect_rate': [2.0, 2.3, 1.7, 2.1, 2.5, 1.9, 2.2, 2.4, 1.6, 2.1],
            'throughput_efficiency': [90.9, 100.0, 81.8, 95.5, 109.1, 86.4, 98.2, 104.5, 90.0, 92.7]
        })
        self.validator = DataValidator(self.test_data)

    def test_check_missing_values_none(self):
        """Test missing value check with no missing data"""
        result = self.validator.check_missing_values()
        self.assertEqual(result['total_missing'], 0)
        self.assertEqual(len(result['columns_with_missing']), 0)

    def test_check_missing_values_with_missing(self):
        """Test missing value check with missing data"""
        data_with_missing = self.test_data.copy()
        data_with_missing.loc[0:2, 'units_produced'] = np.nan

        validator = DataValidator(data_with_missing)
        result = validator.check_missing_values()

        self.assertEqual(result['total_missing'], 3)
        self.assertIn('units_produced', result['columns_with_missing'])

    def test_check_data_types(self):
        """Test data type validation"""
        result = self.validator.check_data_types()
        self.assertTrue(result['passed'])
        self.assertEqual(len(result['type_issues']), 0)

    def test_check_value_ranges_valid(self):
        """Test value range validation with valid data"""
        result = self.validator.check_value_ranges()
        self.assertTrue(result['passed'])
        self.assertEqual(len(result['violations']), 0)

    def test_check_value_ranges_invalid(self):
        """Test value range validation with invalid data"""
        invalid_data = self.test_data.copy()
        invalid_data.loc[0, 'oee'] = 150  # Above maximum

        validator = DataValidator(invalid_data)
        result = validator.check_value_ranges()

        self.assertFalse(result['passed'])
        self.assertGreater(len(result['violations']), 0)

    def test_check_business_rules(self):
        """Test business rule validation"""
        result = self.validator.check_business_rules()
        self.assertTrue(result['passed'])
        self.assertEqual(len(result['violations']), 0)

    def test_check_business_rules_violation(self):
        """Test business rule validation with violations"""
        invalid_data = self.test_data.copy()
        invalid_data.loc[0, 'defect_count'] = 1200  # More defects than units produced

        validator = DataValidator(invalid_data)
        result = validator.check_business_rules()

        self.assertFalse(result['passed'])
        self.assertGreater(len(result['violations']), 0)

    def test_check_duplicates_none(self):
        """Test duplicate check with no duplicates"""
        result = self.validator.check_duplicates()
        self.assertEqual(result['duplicate_count'], 0)

    def test_check_duplicates_with_duplicates(self):
        """Test duplicate check with duplicates"""
        data_with_dupes = pd.concat([self.test_data, self.test_data.iloc[[0]]])

        validator = DataValidator(data_with_dupes)
        result = validator.check_duplicates()

        self.assertGreater(result['duplicate_count'], 0)

    def test_run_all_checks(self):
        """Test comprehensive validation"""
        results = self.validator.run_all_checks()

        self.assertIn('missing_values', results)
        self.assertIn('data_types', results)
        self.assertIn('value_ranges', results)
        self.assertIn('business_rules', results)
        self.assertIn('duplicates', results)
        self.assertIn('overall_status', results)
        self.assertEqual(results['overall_status'], 'PASSED')


if __name__ == '__main__':
    unittest.main()

"""
M2: Data Validation Module
Purpose: Validate data quality, check constraints, and flag anomalies
Author: Gnanachandu Kalla
Organization: Arrowcosta Technology Pvt Ltd
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataValidator:
    """Validates production data quality and business rules"""

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.validation_results = {}

    def check_missing_values(self) -> Dict:
        """Check for missing values in dataset"""
        missing = self.data.isnull().sum()
        missing_pct = (missing / len(self.data) * 100).round(2)

        result = {
            'total_missing': int(missing.sum()),
            'columns_with_missing': missing[missing > 0].to_dict(),
            'missing_percentage': missing_pct[missing_pct > 0].to_dict()
        }

        self.validation_results['missing_values'] = result
        logger.info(f"Missing values check: {result['total_missing']} total missing")
        return result

    def check_data_types(self) -> Dict:
        """Verify data types match expectations"""
        expected_types = {
            'date': 'datetime64[ns]',
            'shift': 'object',
            'production_line': 'object',
            'units_produced': ['int64', 'int32'],
            'planned_production': ['int64', 'int32'],
            'defect_count': ['int64', 'int32'],
            'downtime_minutes': ['int64', 'int32']
        }

        type_issues = []
        for col, expected in expected_types.items():
            if col in self.data.columns:
                actual_type = str(self.data[col].dtype)
                expected_list = [expected] if isinstance(expected, str) else expected
                if actual_type not in expected_list:
                    type_issues.append({
                        'column': col,
                        'expected': expected,
                        'actual': actual_type
                    })

        result = {
            'type_issues': type_issues,
            'passed': len(type_issues) == 0
        }

        self.validation_results['data_types'] = result
        logger.info(f"Data type check: {len(type_issues)} issues found")
        return result

    def check_value_ranges(self) -> Dict:
        """Check if values are within expected ranges"""
        range_checks = {
            'units_produced': (0, 2000),
            'planned_production': (0, 2000),
            'defect_count': (0, None),
            'downtime_minutes': (0, 480),
            'oee': (0, 100),
            'defect_rate': (0, 100),
            'throughput_efficiency': (0, 200)
        }

        violations = []
        for col, (min_val, max_val) in range_checks.items():
            if col in self.data.columns:
                if min_val is not None:
                    below_min = (self.data[col] < min_val).sum()
                    if below_min > 0:
                        violations.append({
                            'column': col,
                            'violation': f'{below_min} values below minimum {min_val}'
                        })

                if max_val is not None:
                    above_max = (self.data[col] > max_val).sum()
                    if above_max > 0:
                        violations.append({
                            'column': col,
                            'violation': f'{above_max} values above maximum {max_val}'
                        })

        result = {
            'violations': violations,
            'passed': len(violations) == 0
        }

        self.validation_results['value_ranges'] = result
        logger.info(f"Range check: {len(violations)} violations found")
        return result

    def check_business_rules(self) -> Dict:
        """Validate business logic rules"""
        violations = []

        # Rule 1: Defects cannot exceed units produced
        rule1_violations = (self.data['defect_count'] > self.data['units_produced']).sum()
        if rule1_violations > 0:
            violations.append({
                'rule': 'Defects ≤ Units Produced',
                'violations': int(rule1_violations)
            })

        # Rule 2: Units produced should not exceed planned by more than 50%
        rule2_violations = (self.data['units_produced'] > self.data['planned_production'] * 1.5).sum()
        if rule2_violations > 0:
            violations.append({
                'rule': 'Units Produced ≤ 150% of Planned',
                'violations': int(rule2_violations)
            })

        # Rule 3: Downtime should not exceed shift duration (480 minutes)
        rule3_violations = (self.data['downtime_minutes'] > 480).sum()
        if rule3_violations > 0:
            violations.append({
                'rule': 'Downtime ≤ Shift Duration',
                'violations': int(rule3_violations)
            })

        result = {
            'violations': violations,
            'passed': len(violations) == 0
        }

        self.validation_results['business_rules'] = result
        logger.info(f"Business rules check: {len(violations)} rule violations")
        return result

    def check_duplicates(self) -> Dict:
        """Check for duplicate records"""
        key_columns = ['date', 'shift', 'production_line']
        duplicates = self.data.duplicated(subset=key_columns, keep=False)

        result = {
            'duplicate_count': int(duplicates.sum()),
            'duplicate_records': self.data[duplicates].index.tolist() if duplicates.sum() > 0 else []
        }

        self.validation_results['duplicates'] = result
        logger.info(f"Duplicate check: {result['duplicate_count']} duplicates found")
        return result

    def run_all_checks(self) -> Dict:
        """Run all validation checks"""
        logger.info("Starting comprehensive validation...")

        self.check_missing_values()
        self.check_data_types()
        self.check_value_ranges()
        self.check_business_rules()
        self.check_duplicates()

        # Overall validation status
        all_passed = all([
            self.validation_results['missing_values']['total_missing'] == 0,
            self.validation_results['data_types']['passed'],
            self.validation_results['value_ranges']['passed'],
            self.validation_results['business_rules']['passed'],
            self.validation_results['duplicates']['duplicate_count'] == 0
        ])

        self.validation_results['overall_status'] = 'PASSED' if all_passed else 'FAILED'
        logger.info(f"Validation complete: {self.validation_results['overall_status']}")

        return self.validation_results


if __name__ == "__main__":
    from ingestion import DataIngestion

    # Load and validate data
    ingestion = DataIngestion()
    data = ingestion.load_data()

    validator = DataValidator(data)
    results = validator.run_all_checks()

    print("\nValidation Results:")
    print(f"Overall Status: {results['overall_status']}")
    print(f"Missing Values: {results['missing_values']['total_missing']}")
    print(f"Duplicates: {results['duplicates']['duplicate_count']}")
    print(f"Business Rule Violations: {len(results['business_rules']['violations'])}")

"""
Unit Tests for Analytics Module
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

from analytics import OperationsAnalytics


class TestOperationsAnalytics(unittest.TestCase):
    """Test cases for OperationsAnalytics class"""

    def setUp(self):
        """Set up test data before each test"""
        self.test_data = pd.DataFrame({
            'date': pd.date_range('2026-02-01', periods=20),
            'shift': ['Morning', 'Afternoon', 'Night'] * 6 + ['Morning', 'Afternoon'],
            'production_line': ['Line_A', 'Line_B', 'Line_C', 'Line_D'] * 5,
            'units_produced': np.random.randint(800, 1200, 20),
            'planned_production': np.random.randint(1000, 1300, 20),
            'defect_count': np.random.randint(10, 50, 20),
            'downtime_minutes': np.random.randint(20, 80, 20),
            'oee': np.random.uniform(75, 95, 20),
            'defect_rate': np.random.uniform(1.0, 3.0, 20),
            'throughput_efficiency': np.random.uniform(80, 110, 20),
            'operator_id': [f'OP{str(i%5).zfill(3)}' for i in range(20)]
        })
        self.analytics = OperationsAnalytics(self.test_data)

    def test_calculate_oee(self):
        """Test OEE calculation"""
        oee = self.analytics.calculate_oee()

        self.assertEqual(len(oee), len(self.test_data))
        self.assertTrue(all(oee >= 0))
        self.assertTrue(all(oee <= 100))

    def test_calculate_defect_rate(self):
        """Test defect rate calculation"""
        defect_rate = self.analytics.calculate_defect_rate()

        self.assertEqual(len(defect_rate), len(self.test_data))
        self.assertTrue(all(defect_rate >= 0))

    def test_calculate_throughput_efficiency(self):
        """Test throughput efficiency calculation"""
        efficiency = self.analytics.calculate_throughput_efficiency()

        self.assertEqual(len(efficiency), len(self.test_data))
        self.assertTrue(all(efficiency >= 0))

    def test_aggregate_by_production_line(self):
        """Test aggregation by production line"""
        line_metrics = self.analytics.aggregate_by_production_line()

        self.assertEqual(len(line_metrics), 4)  # 4 production lines
        self.assertIn('units_produced', line_metrics.columns)
        self.assertIn('oee', line_metrics.columns)
        self.assertIn('total_records', line_metrics.columns)

    def test_aggregate_by_shift(self):
        """Test aggregation by shift"""
        shift_metrics = self.analytics.aggregate_by_shift()

        self.assertEqual(len(shift_metrics), 3)  # 3 shifts
        self.assertIn('units_produced', shift_metrics.columns)
        self.assertIn('defect_count', shift_metrics.columns)

    def test_aggregate_by_date(self):
        """Test aggregation by date"""
        daily_metrics = self.analytics.aggregate_by_date(freq='D')

        self.assertIsInstance(daily_metrics, pd.DataFrame)
        self.assertIn('units_produced', daily_metrics.columns)
        self.assertIn('oee', daily_metrics.columns)

    def test_calculate_downtime_impact(self):
        """Test downtime impact analysis"""
        impact = self.analytics.calculate_downtime_impact()

        self.assertIn('correlation_with_production', impact)
        self.assertIn('correlation_with_defects', impact)
        self.assertIn('total_downtime_hours', impact)
        self.assertIn('avg_downtime_per_shift', impact)

        # Correlations should be between -1 and 1
        self.assertGreaterEqual(impact['correlation_with_production'], -1)
        self.assertLessEqual(impact['correlation_with_production'], 1)

    def test_identify_bottlenecks(self):
        """Test bottleneck identification"""
        bottlenecks = self.analytics.identify_bottlenecks(threshold_oee=85.0)

        self.assertIsInstance(bottlenecks, pd.DataFrame)
        self.assertTrue(all(bottlenecks['oee'] < 85.0))

    def test_calculate_operator_performance(self):
        """Test operator performance calculation"""
        operator_perf = self.analytics.calculate_operator_performance()

        self.assertIsInstance(operator_perf, pd.DataFrame)
        self.assertIn('units_produced', operator_perf.columns)
        self.assertIn('oee', operator_perf.columns)
        self.assertIn('total_shifts', operator_perf.columns)

    def test_calculate_monthly_trends(self):
        """Test monthly trends calculation"""
        monthly = self.analytics.calculate_monthly_trends()

        self.assertIsInstance(monthly, pd.DataFrame)
        self.assertIn('units_produced', monthly.columns)
        self.assertIn('oee', monthly.columns)

    def test_generate_kpi_summary(self):
        """Test KPI summary generation"""
        summary = self.analytics.generate_kpi_summary()

        self.assertIn('total_production', summary)
        self.assertIn('avg_oee', summary)
        self.assertIn('avg_defect_rate', summary)
        self.assertIn('total_downtime_hours', summary)
        self.assertIn('best_production_line', summary)
        self.assertIn('total_records', summary)

        # Verify data types
        self.assertIsInstance(summary['total_production'], (int, np.integer))
        self.assertIsInstance(summary['avg_oee'], (float, np.floating))
        self.assertEqual(summary['total_records'], len(self.test_data))


class TestAnalyticsEdgeCases(unittest.TestCase):
    """Test edge cases for analytics module"""

    def test_empty_dataframe(self):
        """Test analytics with empty dataframe"""
        empty_df = pd.DataFrame()

        with self.assertRaises(Exception):
            analytics = OperationsAnalytics(empty_df)

    def test_single_row(self):
        """Test analytics with single row"""
        single_row = pd.DataFrame({
            'date': [pd.Timestamp('2026-02-01')],
            'shift': ['Morning'],
            'production_line': ['Line_A'],
            'units_produced': [1000],
            'planned_production': [1100],
            'defect_count': [20],
            'downtime_minutes': [30],
            'oee': [85.0],
            'defect_rate': [2.0],
            'throughput_efficiency': [90.9],
            'operator_id': ['OP001']
        })

        analytics = OperationsAnalytics(single_row)
        summary = analytics.generate_kpi_summary()

        self.assertEqual(summary['total_records'], 1)
        self.assertIsInstance(summary['avg_oee'], (float, np.floating))


if __name__ == '__main__':
    unittest.main()

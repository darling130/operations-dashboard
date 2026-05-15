"""
M4: Analytics Module
Purpose: Calculate KPIs, aggregate metrics, and perform operational analytics
Author: Gnanachandu Kalla
Organization: Arrowcosta Technology Pvt Ltd
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OperationsAnalytics:
    """Performs operations analytics and KPI calculations"""

    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.kpis = {}

    def calculate_oee(self) -> pd.Series:
        """
        Calculate Overall Equipment Effectiveness (OEE)
        OEE = Availability × Performance × Quality
        """
        # Availability: (Planned Time - Downtime) / Planned Time
        shift_duration = 480  # minutes (8 hours)
        availability = (shift_duration - self.data['downtime_minutes']) / shift_duration

        # Performance: Actual Output / Planned Output
        performance = self.data['units_produced'] / self.data['planned_production']

        # Quality: (Total Output - Defects) / Total Output
        quality = (self.data['units_produced'] - self.data['defect_count']) / self.data['units_produced']

        # OEE = Availability × Performance × Quality × 100
        oee = (availability * performance * quality * 100).clip(lower=0, upper=100)

        logger.info(f"Calculated OEE: Mean = {oee.mean():.2f}%")
        return oee

    def calculate_defect_rate(self) -> pd.Series:
        """Calculate defect rate as percentage"""
        defect_rate = (self.data['defect_count'] / self.data['units_produced'] * 100)
        logger.info(f"Calculated Defect Rate: Mean = {defect_rate.mean():.2f}%")
        return defect_rate

    def calculate_throughput_efficiency(self) -> pd.Series:
        """Calculate throughput efficiency"""
        efficiency = (self.data['units_produced'] / self.data['planned_production'] * 100)
        logger.info(f"Calculated Throughput Efficiency: Mean = {efficiency.mean():.2f}%")
        return efficiency

    def aggregate_by_production_line(self) -> pd.DataFrame:
        """Aggregate metrics by production line"""
        agg_dict = {
            'units_produced': 'sum',
            'planned_production': 'sum',
            'defect_count': 'sum',
            'downtime_minutes': 'sum',
            'oee': 'mean',
            'defect_rate': 'mean',
            'throughput_efficiency': 'mean'
        }

        line_metrics = self.data.groupby('production_line').agg(agg_dict).round(2)
        line_metrics['total_records'] = self.data.groupby('production_line').size()

        logger.info(f"Aggregated metrics for {len(line_metrics)} production lines")
        return line_metrics

    def aggregate_by_shift(self) -> pd.DataFrame:
        """Aggregate metrics by shift"""
        agg_dict = {
            'units_produced': 'sum',
            'defect_count': 'sum',
            'downtime_minutes': 'sum',
            'oee': 'mean',
            'defect_rate': 'mean',
            'throughput_efficiency': 'mean'
        }

        shift_metrics = self.data.groupby('shift').agg(agg_dict).round(2)
        shift_metrics['total_records'] = self.data.groupby('shift').size()

        logger.info(f"Aggregated metrics for {len(shift_metrics)} shifts")
        return shift_metrics

    def aggregate_by_date(self, freq: str = 'D') -> pd.DataFrame:
        """Aggregate metrics by time period"""
        self.data.set_index('date', inplace=True)

        agg_dict = {
            'units_produced': 'sum',
            'planned_production': 'sum',
            'defect_count': 'sum',
            'downtime_minutes': 'sum',
            'oee': 'mean',
            'defect_rate': 'mean'
        }

        time_metrics = self.data.resample(freq).agg(agg_dict).round(2)

        self.data.reset_index(inplace=True)

        logger.info(f"Aggregated metrics by {freq} frequency")
        return time_metrics

    def calculate_downtime_impact(self) -> Dict:
        """Analyze impact of downtime on production"""
        # Correlation between downtime and production
        corr_production = self.data[['downtime_minutes', 'units_produced']].corr().iloc[0, 1]

        # Correlation between downtime and defects
        corr_defects = self.data[['downtime_minutes', 'defect_count']].corr().iloc[0, 1]

        # Average production loss per minute of downtime
        production_loss = self.data.groupby('downtime_minutes')['units_produced'].mean()

        impact = {
            'correlation_with_production': round(corr_production, 3),
            'correlation_with_defects': round(corr_defects, 3),
            'total_downtime_hours': round(self.data['downtime_minutes'].sum() / 60, 2),
            'avg_downtime_per_shift': round(self.data['downtime_minutes'].mean(), 2)
        }

        logger.info(f"Downtime Impact Analysis: {impact}")
        return impact

    def identify_bottlenecks(self, threshold_oee: float = 70.0) -> pd.DataFrame:
        """Identify production bottlenecks based on OEE threshold"""
        bottlenecks = self.data[self.data['oee'] < threshold_oee].copy()
        bottlenecks = bottlenecks.sort_values('oee')

        logger.info(f"Identified {len(bottlenecks)} bottleneck instances (OEE < {threshold_oee}%)")
        return bottlenecks[['date', 'shift', 'production_line', 'oee', 
                            'downtime_minutes', 'defect_count', 'units_produced']]

    def calculate_operator_performance(self) -> pd.DataFrame:
        """Analyze performance by operator"""
        operator_metrics = self.data.groupby('operator_id').agg({
            'units_produced': 'sum',
            'defect_count': 'sum',
            'downtime_minutes': 'sum',
            'oee': 'mean',
            'defect_rate': 'mean'
        }).round(2)

        operator_metrics['total_shifts'] = self.data.groupby('operator_id').size()
        operator_metrics = operator_metrics.sort_values('oee', ascending=False)

        logger.info(f"Calculated performance for {len(operator_metrics)} operators")
        return operator_metrics

    def calculate_monthly_trends(self) -> pd.DataFrame:
        """Calculate monthly KPI trends"""
        self.data['month'] = pd.to_datetime(self.data['date']).dt.to_period('M')

        monthly = self.data.groupby('month').agg({
            'units_produced': 'sum',
            'planned_production': 'sum',
            'defect_count': 'sum',
            'downtime_minutes': 'sum',
            'oee': 'mean',
            'defect_rate': 'mean',
            'throughput_efficiency': 'mean'
        }).round(2)

        # Calculate month-over-month growth
        monthly['production_growth_%'] = monthly['units_produced'].pct_change() * 100
        monthly['oee_change_%'] = monthly['oee'].pct_change() * 100

        self.data.drop('month', axis=1, inplace=True)

        logger.info(f"Calculated monthly trends for {len(monthly)} months")
        return monthly

    def generate_kpi_summary(self) -> Dict:
        """Generate comprehensive KPI summary"""
        summary = {
            'total_production': int(self.data['units_produced'].sum()),
            'total_planned': int(self.data['planned_production'].sum()),
            'total_defects': int(self.data['defect_count'].sum()),
            'total_downtime_hours': round(self.data['downtime_minutes'].sum() / 60, 2),
            'avg_oee': round(self.data['oee'].mean(), 2),
            'avg_defect_rate': round(self.data['defect_rate'].mean(), 2),
            'avg_throughput_efficiency': round(self.data['throughput_efficiency'].mean(), 2),
            'best_production_line': self.data.groupby('production_line')['oee'].mean().idxmax(),
            'worst_production_line': self.data.groupby('production_line')['oee'].mean().idxmin(),
            'best_shift': self.data.groupby('shift')['oee'].mean().idxmax(),
            'total_records': len(self.data)
        }

        logger.info("Generated comprehensive KPI summary")
        return summary


if __name__ == "__main__":
    from ingestion import DataIngestion
    from cleaning import DataCleaner

    # Load and clean data
    ingestion = DataIngestion()
    data = ingestion.load_data()

    cleaner = DataCleaner(data)
    cleaned_data = cleaner.get_cleaned_data()

    # Perform analytics
    analytics = OperationsAnalytics(cleaned_data)

    print("\n=== KPI Summary ===")
    summary = analytics.generate_kpi_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\n=== Production Line Performance ===")
    print(analytics.aggregate_by_production_line())

    print("\n=== Downtime Impact ===")
    print(analytics.calculate_downtime_impact())

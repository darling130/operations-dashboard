"""
M7: Insights Module
Purpose: Generate actionable insights and recommendations from analytics
Author: Gnanachandu Kalla
Organization: Arrowcosta Technology Pvt Ltd
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InsightsGenerator:
    """Generates actionable insights from production analytics"""

    def __init__(self, data: pd.DataFrame, kpi_targets: Dict = None):
        self.data = data.copy()
        self.kpi_targets = kpi_targets or {
            'oee': 85.0,
            'defect_rate': 2.0,
            'throughput_efficiency': 95.0
        }
        self.insights = []

    def analyze_oee_performance(self) -> List[Dict]:
        """Generate insights on OEE performance"""
        insights = []
        avg_oee = self.data['oee'].mean()
        target_oee = self.kpi_targets['oee']

        if avg_oee < target_oee:
            gap = target_oee - avg_oee
            insights.append({
                'category': 'OEE',
                'severity': 'HIGH' if gap > 10 else 'MEDIUM',
                'insight': f'Average OEE is {avg_oee:.1f}%, which is {gap:.1f}% below target of {target_oee}%',
                'recommendation': 'Focus on reducing downtime and improving quality metrics',
                'metric': 'oee',
                'current': round(avg_oee, 2),
                'target': target_oee
            })
        else:
            insights.append({
                'category': 'OEE',
                'severity': 'LOW',
                'insight': f'Average OEE is {avg_oee:.1f}%, exceeding target of {target_oee}%',
                'recommendation': 'Maintain current operational standards',
                'metric': 'oee',
                'current': round(avg_oee, 2),
                'target': target_oee
            })

        # Identify lines below target
        line_oee = self.data.groupby('production_line')['oee'].mean()
        underperforming_lines = line_oee[line_oee < target_oee]

        if len(underperforming_lines) > 0:
            for line, oee in underperforming_lines.items():
                insights.append({
                    'category': 'OEE',
                    'severity': 'HIGH',
                    'insight': f'{line} has OEE of {oee:.1f}%, below target',
                    'recommendation': f'Investigate root causes in {line} - check maintenance schedules and operator training',
                    'metric': 'oee_by_line',
                    'production_line': line,
                    'current': round(oee, 2),
                    'target': target_oee
                })

        return insights

    def analyze_defect_patterns(self) -> List[Dict]:
        """Generate insights on defect patterns"""
        insights = []
        avg_defect_rate = self.data['defect_rate'].mean()
        target_defect_rate = self.kpi_targets['defect_rate']

        if avg_defect_rate > target_defect_rate:
            excess = avg_defect_rate - target_defect_rate
            insights.append({
                'category': 'Quality',
                'severity': 'HIGH' if excess > 2 else 'MEDIUM',
                'insight': f'Defect rate is {avg_defect_rate:.2f}%, exceeding target of {target_defect_rate}%',
                'recommendation': 'Implement quality control measures and operator training programs',
                'metric': 'defect_rate',
                'current': round(avg_defect_rate, 2),
                'target': target_defect_rate
            })

        # Correlation between downtime and defects
        corr = self.data[['downtime_minutes', 'defect_count']].corr().iloc[0, 1]
        if corr > 0.3:
            insights.append({
                'category': 'Quality',
                'severity': 'MEDIUM',
                'insight': f'Strong correlation ({corr:.2f}) between downtime and defects',
                'recommendation': 'Equipment downtime may be causing quality issues - schedule preventive maintenance',
                'metric': 'downtime_defect_correlation',
                'correlation': round(corr, 3)
            })

        # Identify shifts with high defect rates
        shift_defects = self.data.groupby('shift')['defect_rate'].mean()
        worst_shift = shift_defects.idxmax()
        worst_shift_rate = shift_defects.max()

        if worst_shift_rate > target_defect_rate:
            insights.append({
                'category': 'Quality',
                'severity': 'MEDIUM',
                'insight': f'{worst_shift} shift has highest defect rate at {worst_shift_rate:.2f}%',
                'recommendation': f'Review {worst_shift} shift procedures and operator performance',
                'metric': 'defect_rate_by_shift',
                'shift': worst_shift,
                'current': round(worst_shift_rate, 2)
            })

        return insights

    def analyze_downtime(self) -> List[Dict]:
        """Generate insights on downtime patterns"""
        insights = []
        total_downtime_hours = self.data['downtime_minutes'].sum() / 60
        avg_downtime_per_shift = self.data['downtime_minutes'].mean()

        insights.append({
            'category': 'Downtime',
            'severity': 'HIGH' if avg_downtime_per_shift > 60 else 'MEDIUM',
            'insight': f'Total downtime: {total_downtime_hours:.1f} hours across all shifts',
            'recommendation': 'Implement predictive maintenance to reduce unplanned downtime',
            'metric': 'total_downtime',
            'value': round(total_downtime_hours, 2)
        })

        # Identify lines with highest downtime
        line_downtime = self.data.groupby('production_line')['downtime_minutes'].sum()
        worst_line = line_downtime.idxmax()
        worst_line_hours = line_downtime.max() / 60

        insights.append({
            'category': 'Downtime',
            'severity': 'HIGH',
            'insight': f'{worst_line} has highest downtime at {worst_line_hours:.1f} hours',
            'recommendation': f'Prioritize maintenance and equipment upgrades for {worst_line}',
            'metric': 'downtime_by_line',
            'production_line': worst_line,
            'value': round(worst_line_hours, 2)
        })

        # Maintenance events analysis
        maintenance_records = self.data[self.data['maintenance_flag'] == 1]
        if len(maintenance_records) > 0:
            avg_downtime_maintenance = maintenance_records['downtime_minutes'].mean()
            insights.append({
                'category': 'Maintenance',
                'severity': 'MEDIUM',
                'insight': f'{len(maintenance_records)} maintenance events recorded, avg downtime: {avg_downtime_maintenance:.1f} min',
                'recommendation': 'Optimize maintenance schedules to minimize production impact',
                'metric': 'maintenance_downtime',
                'events': len(maintenance_records),
                'avg_downtime': round(avg_downtime_maintenance, 2)
            })

        return insights

    def analyze_throughput(self) -> List[Dict]:
        """Generate insights on throughput efficiency"""
        insights = []
        avg_efficiency = self.data['throughput_efficiency'].mean()
        target_efficiency = self.kpi_targets['throughput_efficiency']

        if avg_efficiency < target_efficiency:
            gap = target_efficiency - avg_efficiency
            insights.append({
                'category': 'Throughput',
                'severity': 'HIGH' if gap > 10 else 'MEDIUM',
                'insight': f'Average throughput efficiency is {avg_efficiency:.1f}%, below target of {target_efficiency}%',
                'recommendation': 'Review production planning and resource allocation',
                'metric': 'throughput_efficiency',
                'current': round(avg_efficiency, 2),
                'target': target_efficiency
            })

        # Best and worst performing lines
        line_efficiency = self.data.groupby('production_line')['throughput_efficiency'].mean()
        best_line = line_efficiency.idxmax()
        worst_line = line_efficiency.idxmin()

        insights.append({
            'category': 'Throughput',
            'severity': 'LOW',
            'insight': f'{best_line} has best throughput efficiency at {line_efficiency[best_line]:.1f}%',
            'recommendation': f'Study best practices from {best_line} and replicate across other lines',
            'metric': 'best_throughput_line',
            'production_line': best_line,
            'value': round(line_efficiency[best_line], 2)
        })

        if line_efficiency[worst_line] < target_efficiency:
            insights.append({
                'category': 'Throughput',
                'severity': 'MEDIUM',
                'insight': f'{worst_line} has lowest throughput efficiency at {line_efficiency[worst_line]:.1f}%',
                'recommendation': f'Investigate bottlenecks in {worst_line} and optimize workflow',
                'metric': 'worst_throughput_line',
                'production_line': worst_line,
                'value': round(line_efficiency[worst_line], 2)
            })

        return insights

    def analyze_operator_performance(self) -> List[Dict]:
        """Generate insights on operator performance"""
        insights = []
        operator_metrics = self.data.groupby('operator_id').agg({
            'oee': 'mean',
            'defect_rate': 'mean',
            'units_produced': 'sum'
        })

        # Top performers
        top_operators = operator_metrics.nlargest(3, 'oee')
        insights.append({
            'category': 'Operators',
            'severity': 'LOW',
            'insight': f'Top 3 operators: {", ".join(top_operators.index.tolist())} with avg OEE > {top_operators["oee"].min():.1f}%',
            'recommendation': 'Recognize top performers and use as trainers for others',
            'metric': 'top_operators',
            'operators': top_operators.index.tolist()
        })

        # Operators needing improvement
        low_performers = operator_metrics[operator_metrics['oee'] < self.kpi_targets['oee']]
        if len(low_performers) > 0:
            insights.append({
                'category': 'Operators',
                'severity': 'MEDIUM',
                'insight': f'{len(low_performers)} operators below OEE target',
                'recommendation': 'Provide additional training and mentorship for underperforming operators',
                'metric': 'low_performing_operators',
                'count': len(low_performers)
            })

        return insights

    def generate_all_insights(self) -> List[Dict]:
        """Generate comprehensive insights report"""
        logger.info("Generating comprehensive insights...")

        all_insights = []
        all_insights.extend(self.analyze_oee_performance())
        all_insights.extend(self.analyze_defect_patterns())
        all_insights.extend(self.analyze_downtime())
        all_insights.extend(self.analyze_throughput())
        all_insights.extend(self.analyze_operator_performance())

        self.insights = all_insights
        logger.info(f"Generated {len(all_insights)} insights")

        return all_insights

    def get_prioritized_insights(self, severity_filter: str = None) -> List[Dict]:
        """Get insights prioritized by severity"""
        if not self.insights:
            self.generate_all_insights()

        if severity_filter:
            filtered = [i for i in self.insights if i['severity'] == severity_filter]
        else:
            filtered = self.insights

        # Sort by severity: HIGH > MEDIUM > LOW
        severity_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
        sorted_insights = sorted(filtered, key=lambda x: severity_order.get(x['severity'], 3))

        return sorted_insights

    def export_insights_report(self, filename: str = 'insights_report.txt'):
        """Export insights to text report"""
        if not self.insights:
            self.generate_all_insights()

        with open(filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write("OPERATIONS ANALYTICS INSIGHTS REPORT\n")
            f.write("Generated by Arrowcosta Technology Operations Dashboard\n")
            f.write("="*80 + "\n\n")

            for severity in ['HIGH', 'MEDIUM', 'LOW']:
                severity_insights = [i for i in self.insights if i['severity'] == severity]
                if severity_insights:
                    f.write(f"\n{severity} PRIORITY INSIGHTS ({len(severity_insights)})\n")
                    f.write("-"*80 + "\n")

                    for idx, insight in enumerate(severity_insights, 1):
                        f.write(f"\n{idx}. [{insight['category']}]\n")
                        f.write(f"   Insight: {insight['insight']}\n")
                        f.write(f"   Recommendation: {insight['recommendation']}\n")

            f.write("\n" + "="*80 + "\n")

        logger.info(f"Insights report exported to {filename}")


if __name__ == "__main__":
    from ingestion import DataIngestion
    from cleaning import DataCleaner

    # Load and clean data
    ingestion = DataIngestion()
    data = ingestion.load_data()

    cleaner = DataCleaner(data)
    cleaned_data = cleaner.get_cleaned_data()

    # Generate insights
    insights_gen = InsightsGenerator(cleaned_data)
    insights = insights_gen.generate_all_insights()

    print("\n=== PRIORITIZED INSIGHTS ===\n")
    for severity in ['HIGH', 'MEDIUM', 'LOW']:
        severity_insights = insights_gen.get_prioritized_insights(severity)
        if severity_insights:
            print(f"\n{severity} PRIORITY ({len(severity_insights)} insights):")
            for i, insight in enumerate(severity_insights, 1):
                print(f"  {i}. [{insight['category']}] {insight['insight']}")
                print(f"     → {insight['recommendation']}")

    # Export report
    insights_gen.export_insights_report()

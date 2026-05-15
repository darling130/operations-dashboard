# Production Records Data Dictionary

## Overview
This dataset contains production records from industrial manufacturing operations spanning February to July 2026. Each record represents a single shift's production metrics across four production lines.

## Schema

| Column Name | Data Type | Description | Unit | Range/Values |
|------------|-----------|-------------|------|--------------||
| `date` | datetime | Production date | YYYY-MM-DD | 2026-02-01 to 2026-07-31 |
| `shift` | string | Work shift | - | Morning, Afternoon, Night |
| `production_line` | string | Production line identifier | - | Line_A, Line_B, Line_C, Line_D |
| `units_produced` | integer | Actual units manufactured | units | 500-1200 |
| `planned_production` | integer | Targeted production volume | units | 1000-1300 |
| `defect_count` | integer | Number of defective units | units | 0-100+ |
| `downtime_minutes` | integer | Equipment downtime duration | minutes | 0-120 |
| `cycle_time_avg` | float | Average cycle time per unit | minutes | 2.5-4.5 |
| `material_waste_kg` | float | Material wastage | kilograms | 5-25 |
| `energy_consumption_kwh` | float | Energy consumed during shift | kWh | 150-300 |
| `operator_id` | string | Operator identifier | - | OP001 to OP020 |
| `maintenance_flag` | integer | Maintenance event indicator | binary | 0 (no), 1 (yes) |
| `oee` | float | Overall Equipment Effectiveness | percentage | 0-100 |
| `defect_rate` | float | Defect percentage | percentage | 0-10+ |
| `throughput_efficiency` | float | Production vs planned ratio | percentage | 50-120 |

## Key Performance Indicators (KPIs)

### OEE (Overall Equipment Effectiveness)
**Formula**: Availability × Performance × Quality

**Calculation**:
- Availability = (Planned Time - Downtime) / Planned Time
- Performance = Actual Output / Planned Output
- Quality = (Total Output - Defects) / Total Output

**Target**: ≥ 85%

### Defect Rate
**Formula**: (Defect Count / Units Produced) × 100

**Target**: ≤ 2%

### Throughput Efficiency
**Formula**: (Units Produced / Planned Production) × 100

**Target**: ≥ 95%

## Data Quality Notes

1. **Correlations**: Downtime negatively impacts production volume and increases defect rates
2. **Missing Values**: None (synthetic dataset)
3. **Outliers**: Some shifts may exceed 100% throughput efficiency due to operational improvements
4. **Maintenance Events**: 15% of shifts include planned or unplanned maintenance

## Usage Guidelines

- Use for trend analysis across production lines and shifts
- Identify bottlenecks and root causes of downtime
- Perform correlation studies between downtime and defect rates
- Track KPI performance against targets
- Support predictive maintenance modeling

## Data Source
Synthetic dataset generated for Operations Analytics Dashboard project at Arrowcosta Technology Pvt Ltd.

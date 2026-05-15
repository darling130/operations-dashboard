# Operations Analytics Dashboard

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-success.svg)]()

Industrial Operations Analytics Dashboard for monitoring production KPIs, analyzing downtime patterns, and generating actionable insights.

**Organization:** Arrowcosta Technology Private Limited  
**Author:** Gnanachandu Kalla  
**Role:** Operations Data Analyst Intern  
**Period:** February - July 2026

---

## 📊 Overview

This dashboard provides comprehensive analytics for industrial manufacturing operations, including:

- **Real-time KPI Monitoring**: OEE, defect rates, throughput efficiency, and downtime tracking
- **Data Validation**: Automated data quality checks and business rule validation
- **Advanced Analytics**: Correlation studies, trend analysis, and performance benchmarking
- **Interactive Visualizations**: Dark-themed dashboard with Chart.js for production insights
- **Actionable Insights**: AI-generated recommendations based on operational data

---

## 🏗️ Project Structure

```
operations-dashboard/
├── data/
│   ├── production_records.csv     # Synthetic production data (543 records)
│   └── data_dictionary.md         # Data schema and field descriptions
├── notebooks/
│   ├── 01_exploratory.ipynb       # Exploratory Data Analysis
│   ├── 02_kpi_validation.ipynb    # KPI target validation
│   └── 03_correlation_study.ipynb # Downtime vs Defects analysis
├── src/
│   ├── ingestion.py               # M1: Data loading and preparation
│   ├── validation.py              # M2: Data quality validation
│   ├── cleaning.py                # M3: Data preprocessing
│   ├── analytics.py               # M4: KPI calculations and aggregations
│   └── insights.py                # M7: Insights generation
├── dashboard/
│   ├── index.html                 # Main dashboard interface
│   ├── styles.css                 # Dark theme styling
│   ├── app.js                     # M5+M6: Visualization and interactivity
│   └── chart-config.js            # Chart.js configuration
├── docs/
│   ├── README.md                  # Quick-start guide
│   └── user_guide.pdf             # Detailed user documentation
├── tests/
│   ├── test_analytics.py          # Unit tests for analytics module
│   └── test_validation.py         # Unit tests for validation module
└── README.md                      # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Modern web browser (Chrome, Firefox, Edge)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/darling130/operations-dashboard.git
   cd operations-dashboard
   ```

2. **Install Python dependencies**
   ```bash
   pip install pandas numpy matplotlib seaborn scipy scikit-learn jupyter
   ```

3. **Run data ingestion**
   ```bash
   python src/ingestion.py
   ```

4. **Open the dashboard**
   ```bash
   cd dashboard
   python -m http.server 8000
   # Navigate to http://localhost:8000
   ```

### Running Tests

```bash
python -m unittest discover tests
```

---

## 📈 Key Performance Indicators

| KPI | Target | Description |
|-----|--------|-------------|
| **OEE** | ≥ 85% | Overall Equipment Effectiveness (Availability × Performance × Quality) |
| **Defect Rate** | ≤ 2% | Percentage of defective units in production |
| **Throughput Efficiency** | ≥ 95% | Actual production vs. planned production ratio |
| **Downtime** | Minimize | Equipment idle time impacting production |

---

## 🔬 Modules

### M1: Data Ingestion (`ingestion.py`)
- Load production records from CSV
- Date parsing and data type conversion
- Summary statistics generation

### M2: Data Validation (`validation.py`)
- Missing value detection
- Data type verification
- Value range checks
- Business rule validation
- Duplicate record identification

### M3: Data Cleaning (`cleaning.py`)
- Duplicate removal
- Missing value handling (drop/fill strategies)
- Outlier detection and removal (IQR/Z-score methods)
- Text normalization
- Data type fixing

### M4: Analytics (`analytics.py`)
- OEE calculation
- Defect rate computation
- Throughput efficiency analysis
- Production line aggregations
- Shift performance metrics
- Downtime impact analysis
- Bottleneck identification
- Operator performance tracking

### M5+M6: Dashboard (`app.js`)
- Real-time data visualization
- Interactive Chart.js charts
- KPI card updates
- Insight generation
- Performance table rendering

### M7: Insights (`insights.py`)
- Automated insight generation
- Severity-based prioritization
- Recommendation engine
- Report export functionality

---

## 📊 Dashboard Features

### KPI Cards
- Real-time metrics with trend indicators
- Color-coded status (green/amber/red)
- Target comparison

### Charts
1. **OEE Trend Over Time** - Line chart tracking daily OEE performance
2. **Production Volume by Line** - Bar chart comparing production lines
3. **Performance by Shift** - Grouped bar chart for shift analysis
4. **Downtime vs Defects Correlation** - Scatter plot showing relationship
5. **Defect Rate Distribution** - Histogram of defect rate frequency
6. **Monthly Production Trends** - Multi-series line chart with dual Y-axis

### Insights Panel
- High/Medium/Low priority insights
- Category-based organization (OEE, Quality, Downtime, Throughput)
- Actionable recommendations

### Performance Table
- Production line summary
- Status badges (Excellent/Good/Needs Improvement/Poor)
- Sortable columns

---

## 📓 Jupyter Notebooks

### 01_exploratory.ipynb
- Data loading and overview
- Distribution analysis
- Time series visualization
- Categorical analysis
- Correlation matrix

### 02_kpi_validation.ipynb
- Target vs. actual comparison
- Production line validation
- Shift-level validation
- Visual KPI comparison

### 03_correlation_study.ipynb
- Statistical correlation analysis
- Downtime category impact
- Production line-specific correlations
- Linear regression modeling
- Hypothesis testing

---

## 🧪 Testing

Unit tests cover:
- Data validation logic
- Analytics calculations
- KPI formula accuracy
- Edge cases and error handling

Run specific test files:
```bash
python tests/test_validation.py
python tests/test_analytics.py
```

---

## 📦 Data

### Production Records
- **Period**: February 1 - July 31, 2026
- **Records**: 543 production shifts
- **Lines**: 4 (Line_A, Line_B, Line_C, Line_D)
- **Shifts**: 3 per day (Morning, Afternoon, Night)

### Schema
See `data/data_dictionary.md` for complete field definitions.

---

## 🎨 Technology Stack

- **Backend**: Python 3.9+
- **Data Processing**: pandas, NumPy
- **Visualization**: matplotlib, seaborn, Chart.js
- **Analytics**: scipy, scikit-learn
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Testing**: unittest

---

## 📄 License

This project is developed as part of an internship program at Arrowcosta Technology Private Limited.

---

## 👤 Author

**Gnanachandu Kalla**  
Operations Data Analyst Intern  
Arrowcosta Technology Private Limited  
📧 Email: [Contact via organization]  
📍 Location: Gurgaon, Haryana, India

---

## 🙏 Acknowledgments

Special thanks to:
- **Tushar Goyal** (Director, Arrowcosta Technology) for project guidance
- Arrowcosta Technology team for support and mentorship
- Industrial operations domain experts for requirements input

---

## 📞 Support

For questions or issues:
1. Check `docs/user_guide.pdf` for detailed documentation
2. Review notebook examples in `notebooks/`
3. Contact project maintainer through organization channels

---

**Last Updated**: May 2026  
**Version**: 1.0.0  
**Status**: Production Ready

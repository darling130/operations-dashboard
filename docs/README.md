# Quick Start Guide
## Operations Analytics Dashboard

### Getting Started in 5 Minutes

---

## Step 1: Installation

### Clone Repository
```bash
git clone https://github.com/darling130/operations-dashboard.git
cd operations-dashboard
```

### Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn jupyter
```

---

## Step 2: Explore the Data

### View Data Dictionary
```bash
cat data/data_dictionary.md
```

### Load Production Data
```python
from src.ingestion import DataIngestion

ingestion = DataIngestion('data/production_records.csv')
df = ingestion.load_data()
print(df.head())
```

---

## Step 3: Run Analytics

### Calculate KPIs
```python
from src.analytics import OperationsAnalytics

analytics = OperationsAnalytics(df)
summary = analytics.generate_kpi_summary()
print(summary)
```

### Generate Insights
```python
from src.insights import InsightsGenerator

insights_gen = InsightsGenerator(df)
insights = insights_gen.generate_all_insights()

for insight in insights[:5]:
    print(f"[{insight['severity']}] {insight['insight']}")
```

---

## Step 4: Launch Dashboard

### Start Local Server
```bash
cd dashboard
python -m http.server 8000
```

### Open Browser
Navigate to: `http://localhost:8000`

---

## Step 5: Explore Notebooks

### Launch Jupyter
```bash
jupyter notebook notebooks/
```

### Recommended Order
1. `01_exploratory.ipynb` - Data exploration
2. `02_kpi_validation.ipynb` - KPI validation
3. `03_correlation_study.ipynb` - Correlation analysis

---

## Common Tasks

### Validate Data Quality
```python
from src.validation import DataValidator

validator = DataValidator(df)
results = validator.run_all_checks()
print(f"Status: {results['overall_status']}")
```

### Clean Data
```python
from src.cleaning import DataCleaner

cleaner = DataCleaner(df)
cleaner.remove_duplicates()
cleaner.handle_missing_values(strategy='drop')
cleaned_data = cleaner.get_cleaned_data()
```

### Analyze by Production Line
```python
line_metrics = analytics.aggregate_by_production_line()
print(line_metrics)
```

### Identify Bottlenecks
```python
bottlenecks = analytics.identify_bottlenecks(threshold_oee=85.0)
print(f"Found {len(bottlenecks)} bottleneck instances")
```

---

## Running Tests

### All Tests
```bash
python -m unittest discover tests
```

### Specific Module
```bash
python tests/test_analytics.py
python tests/test_validation.py
```

---

## Troubleshooting

### Issue: Import errors
**Solution**: Ensure you're in the project root directory and Python path includes `src/`

### Issue: CSV file not found
**Solution**: Verify data file exists at `data/production_records.csv`

### Issue: Dashboard not loading
**Solution**: Check that you're accessing `http://localhost:8000` (not file://)

### Issue: Charts not rendering
**Solution**: Ensure Chart.js CDN is accessible (requires internet connection)

---

## Key Files Reference

| File | Purpose |
|------|---------||
| `src/ingestion.py` | Load data |
| `src/validation.py` | Validate quality |
| `src/cleaning.py` | Preprocess data |
| `src/analytics.py` | Calculate KPIs |
| `src/insights.py` | Generate insights |
| `dashboard/index.html` | Dashboard UI |
| `dashboard/app.js` | Dashboard logic |

---

## Next Steps

1. **Customize**: Modify KPI targets in `src/insights.py`
2. **Extend**: Add new metrics in `src/analytics.py`
3. **Visualize**: Create additional charts in `dashboard/app.js`
4. **Document**: Add findings to notebooks

---

## Support Resources

- **Full Documentation**: `user_guide.pdf`
- **Data Schema**: `data/data_dictionary.md`
- **Example Code**: Jupyter notebooks in `notebooks/`
- **Main README**: `../README.md`

---

**Quick Reference**: Python Module Flow

```
ingestion.py → validation.py → cleaning.py → analytics.py → insights.py
     ↓              ↓              ↓             ↓             ↓
  Load Data   → Validate    → Clean      → Calculate  → Generate
                Quality        Data         KPIs        Insights
```

---

**Author**: Gnanachandu Kalla  
**Organization**: Arrowcosta Technology Pvt Ltd  
**Date**: May 2026

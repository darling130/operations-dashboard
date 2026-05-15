"""
M1: Data Ingestion Module
Purpose: Load production records from CSV and prepare for processing
Author: Gnanachandu Kalla
Organization: Arrowcosta Technology Pvt Ltd
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataIngestion:
    """Handles data loading and initial preparation"""

    def __init__(self, data_path: str = "../data/production_records.csv"):
        self.data_path = Path(data_path)
        self.raw_data: Optional[pd.DataFrame] = None

    def load_data(self) -> pd.DataFrame:
        """Load production records from CSV file"""
        try:
            logger.info(f"Loading data from {self.data_path}")
            self.raw_data = pd.read_csv(self.data_path)
            self.raw_data['date'] = pd.to_datetime(self.raw_data['date'])
            logger.info(f"Successfully loaded {len(self.raw_data)} records")
            logger.info(f"Date range: {self.raw_data['date'].min()} to {self.raw_data['date'].max()}")
            return self.raw_data
        except FileNotFoundError:
            logger.error(f"File not found: {self.data_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def get_summary(self) -> dict:
        """Get summary statistics of loaded data"""
        if self.raw_data is None:
            raise ValueError("No data loaded. Call load_data() first.")

        summary = {
            'total_records': len(self.raw_data),
            'date_range': {
                'start': str(self.raw_data['date'].min()),
                'end': str(self.raw_data['date'].max())
            },
            'production_lines': self.raw_data['production_line'].unique().tolist(),
            'shifts': self.raw_data['shift'].unique().tolist(),
            'columns': self.raw_data.columns.tolist(),
            'shape': self.raw_data.shape
        }
        return summary

    def filter_by_date(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Filter data by date range"""
        if self.raw_data is None:
            raise ValueError("No data loaded. Call load_data() first.")

        mask = (self.raw_data['date'] >= start_date) & (self.raw_data['date'] <= end_date)
        filtered_data = self.raw_data[mask].copy()
        logger.info(f"Filtered {len(filtered_data)} records between {start_date} and {end_date}")
        return filtered_data


if __name__ == "__main__":
    # Example usage
    ingestion = DataIngestion()
    data = ingestion.load_data()
    print("\nData Summary:")
    print(ingestion.get_summary())
    print("\nFirst 5 records:")
    print(data.head())

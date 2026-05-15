"""
M3: Data Cleaning Module
Purpose: Clean and preprocess production data
Author: Gnanachandu Kalla
Organization: Arrowcosta Technology Pvt Ltd
"""

import pandas as pd
import numpy as np
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataCleaner:
    """Cleans and preprocesses production data"""

    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.original_shape = data.shape
        self.cleaning_log = []

    def remove_duplicates(self) -> pd.DataFrame:
        """Remove duplicate records based on key columns"""
        key_columns = ['date', 'shift', 'production_line']
        initial_count = len(self.data)

        self.data = self.data.drop_duplicates(subset=key_columns, keep='first')

        removed = initial_count - len(self.data)
        if removed > 0:
            self.cleaning_log.append(f"Removed {removed} duplicate records")
            logger.info(f"Removed {removed} duplicates")

        return self.data

    def handle_missing_values(self, strategy: str = 'drop') -> pd.DataFrame:
        """Handle missing values using specified strategy"""
        initial_count = len(self.data)
        missing_before = self.data.isnull().sum().sum()

        if strategy == 'drop':
            self.data = self.data.dropna()
            removed = initial_count - len(self.data)
            if removed > 0:
                self.cleaning_log.append(f"Dropped {removed} rows with missing values")
                logger.info(f"Dropped {removed} rows with missing values")

        elif strategy == 'fill_mean':
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if self.data[col].isnull().any():
                    mean_val = self.data[col].mean()
                    self.data[col].fillna(mean_val, inplace=True)
                    self.cleaning_log.append(f"Filled {col} missing values with mean: {mean_val:.2f}")

        elif strategy == 'fill_median':
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if self.data[col].isnull().any():
                    median_val = self.data[col].median()
                    self.data[col].fillna(median_val, inplace=True)
                    self.cleaning_log.append(f"Filled {col} missing values with median: {median_val:.2f}")

        missing_after = self.data.isnull().sum().sum()
        logger.info(f"Missing values: {missing_before} → {missing_after}")

        return self.data

    def remove_outliers(self, columns: list, method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
        """Remove outliers using IQR or Z-score method"""
        initial_count = len(self.data)

        for col in columns:
            if col not in self.data.columns:
                continue

            if method == 'iqr':
                Q1 = self.data[col].quantile(0.25)
                Q3 = self.data[col].quantile(0.75)
                IQR = Q3 - Q1

                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR

                outlier_mask = (self.data[col] < lower_bound) | (self.data[col] > upper_bound)
                outliers_removed = outlier_mask.sum()

                self.data = self.data[~outlier_mask]

                if outliers_removed > 0:
                    self.cleaning_log.append(f"Removed {outliers_removed} outliers from {col} using IQR method")
                    logger.info(f"Removed {outliers_removed} outliers from {col}")

            elif method == 'zscore':
                z_scores = np.abs((self.data[col] - self.data[col].mean()) / self.data[col].std())
                outlier_mask = z_scores > threshold
                outliers_removed = outlier_mask.sum()

                self.data = self.data[~outlier_mask]

                if outliers_removed > 0:
                    self.cleaning_log.append(f"Removed {outliers_removed} outliers from {col} using Z-score method")
                    logger.info(f"Removed {outliers_removed} outliers from {col}")

        total_removed = initial_count - len(self.data)
        if total_removed > 0:
            logger.info(f"Total outliers removed: {total_removed}")

        return self.data

    def normalize_text_fields(self) -> pd.DataFrame:
        """Normalize text fields to standard format"""
        text_columns = self.data.select_dtypes(include=['object']).columns

        for col in text_columns:
            # Strip whitespace
            self.data[col] = self.data[col].str.strip()

            # Standardize case for specific columns
            if col in ['shift', 'production_line', 'operator_id']:
                unique_before = self.data[col].nunique()
                self.data[col] = self.data[col].str.title()
                unique_after = self.data[col].nunique()

                if unique_before != unique_after:
                    self.cleaning_log.append(f"Normalized {col}: {unique_before} → {unique_after} unique values")

        logger.info("Text normalization complete")
        return self.data

    def fix_data_types(self) -> pd.DataFrame:
        """Ensure correct data types for all columns"""
        # Integer columns
        int_columns = ['units_produced', 'planned_production', 'defect_count', 
                       'downtime_minutes', 'maintenance_flag']
        for col in int_columns:
            if col in self.data.columns:
                self.data[col] = self.data[col].astype(int)

        # Float columns
        float_columns = ['cycle_time_avg', 'material_waste_kg', 'energy_consumption_kwh',
                         'oee', 'defect_rate', 'throughput_efficiency']
        for col in float_columns:
            if col in self.data.columns:
                self.data[col] = self.data[col].astype(float)

        # Datetime columns
        if 'date' in self.data.columns:
            self.data['date'] = pd.to_datetime(self.data['date'])

        self.cleaning_log.append("Fixed data types for all columns")
        logger.info("Data type fixing complete")

        return self.data

    def get_cleaned_data(self) -> pd.DataFrame:
        """Return cleaned dataset"""
        return self.data

    def get_cleaning_summary(self) -> dict:
        """Get summary of cleaning operations"""
        summary = {
            'original_shape': self.original_shape,
            'final_shape': self.data.shape,
            'rows_removed': self.original_shape[0] - self.data.shape[0],
            'cleaning_operations': self.cleaning_log
        }
        return summary


if __name__ == "__main__":
    from ingestion import DataIngestion

    # Load data
    ingestion = DataIngestion()
    data = ingestion.load_data()

    # Clean data
    cleaner = DataCleaner(data)
    cleaner.remove_duplicates()
    cleaner.handle_missing_values(strategy='drop')
    cleaner.normalize_text_fields()
    cleaner.fix_data_types()

    cleaned_data = cleaner.get_cleaned_data()
    summary = cleaner.get_cleaning_summary()

    print("\nCleaning Summary:")
    print(f"Original shape: {summary['original_shape']}")
    print(f"Final shape: {summary['final_shape']}")
    print(f"Rows removed: {summary['rows_removed']}")
    print("\nOperations performed:")
    for op in summary['cleaning_operations']:
        print(f"  - {op}")

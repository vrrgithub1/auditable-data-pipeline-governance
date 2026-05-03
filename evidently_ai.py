import pandas as pd
import os
import warnings
from evidently import Report
from evidently.presets import DataDriftPreset

# Author: Venkat Rajadurai
# Purpose: Generate an Evidently data drift report comparing governed credit data against the reference dataset.

# Suppress SciPy warnings about division by zero for small reference datasets
warnings.filterwarnings('ignore', category=RuntimeWarning)

# 1. Load the data
try:
    reference_df = pd.read_csv("data/silver/reference_data.csv")
    current_df = pd.read_csv("data/silver/credit_data_governed.csv")
except FileNotFoundError as e:
    print(f"Error loading files: {e}. Please ensure both files exist.")
    exit()

# 2. Align the columns for Evidently analysis
features = ['checking_status', 'duration_months', 'credit_amount', 'age']
reference_df = reference_df[features]
current_df = current_df[features]

# 3. Initialize the Report
drift_report = Report(metrics=[
    DataDriftPreset(),
])

# 4. Run the evaluation
print("Analyzing dataset shift...")
# Capture the returned snapshot object
report_result = drift_report.run(reference_data=reference_df, current_data=current_df)

# 5. Save the report from the result object
output_path = "data/silver/data_drift_report.html"
report_result.save_html(output_path)

print(f"Data drift report generated at: {os.path.abspath(output_path)}")
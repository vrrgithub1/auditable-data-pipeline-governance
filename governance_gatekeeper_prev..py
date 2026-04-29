import pandas as pd
import great_expectations as gx
import os

# 1. Load the raw data (Bronze)
# Make sure you have dropped your credit_data.csv into data/bronze/
input_path = "data/bronze/credit_data.csv"
df_raw = pd.read_csv(input_path)

# 2. Convert to a Great Expectations Dataset
df = gx.dataset.PandasDataset(df_raw)

# 3. Apply the Governance Rules (The "Audit Contract")
# Rule: Credit amount must be positive
df.expect_column_values_to_be_between(column="credit_amount", min_value=1)

# Rule: Loan duration must be within policy (72 months)
df.expect_column_values_to_be_between(column="duration_months", min_value=1, max_value=72)

# Rule: No missing IDs or critical fields
df.expect_column_values_to_not_be_null(column="checking_status")

# 4. The "Audit Check"
results = df.validate()

if results["success"]:
    print("✅ All data passed governance checks. Promoting to Silver.")
    df.to_csv("data/silver/credit_data_clean.csv", index=False)
else:
    print("⚠️ Governance violations detected! Identifying bad records...")
    
    # Logic to separate the 'Bad' from 'Good'
    # For now, let's just log the failure for the auditor
    with open("governance_log.txt", "a") as f:
        f.write(f"Batch failed at {pd.Timestamp.now()}: {results['statistics']}\n")
    
    # Still save the full batch to quarantine for investigation
    df.to_csv("data/quarantine/failed_batch.csv", index=False)
    
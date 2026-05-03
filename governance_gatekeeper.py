import pandas as pd
import great_expectations as gx
import os

# Author: Venkat Rajadurai
# Purpose: Governance gatekeeper for credit application data.

# 1. Setup Context
context = gx.get_context()

# 2. Define the Governance Suite (The 'Contract')
suite_name = "credit_governance_suite"
# Check if suite exists, otherwise create it
try:
    suite = context.suites.get(name=suite_name)
except:
    suite = context.suites.add(gx.ExpectationSuite(name=suite_name))

# 3. Add the Rules to the Contract
# Note: We use clear, descriptive names for our Governance Rules
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
    column="credit_amount", min_value=1
))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
    column="duration_months", min_value=1, max_value=72
))

# 4. Create the Data Source and Asset
# In V1.0, we use 'data_sources' instead of 'sources'
source_name = "my_banking_data_source"
try:
    data_source = context.data_sources.get(source_name)
except:
    data_source = context.data_sources.add_pandas(name=source_name)

asset_name = "credit_applications_asset"
try:
    data_asset = data_source.get_asset(asset_name)
except:
    data_asset = data_source.add_dataframe_asset(name=asset_name)

# 5. Load and Validate the "Bronze" Data
df_raw = pd.read_csv("data/bronze/credit_data.csv")

# Create a definition for this specific batch of data
batch_definition_name = "latest_batch_definition"
try:
    batch_definition = data_asset.get_batch_definition(batch_definition_name)
except:
    batch_definition = data_asset.add_batch_definition_whole_dataframe(name=batch_definition_name)

batch = batch_definition.get_batch(batch_parameters={"dataframe": df_raw})

# RUN THE AUDIT
validation_result = batch.validate(suite)

# 6. The Scalpel (Row-Level Governance)
mask_bad_amount = df_raw['credit_amount'] <= 0
mask_bad_duration = df_raw['duration_months'] > 72

df_quarantine = df_raw[mask_bad_amount | mask_bad_duration]
df_silver = df_raw[~(mask_bad_amount | mask_bad_duration)]

# 7. Finalize and Save
os.makedirs("data/silver", exist_ok=True)
os.makedirs("data/quarantine", exist_ok=True)

df_silver.to_csv("data/silver/credit_data_governed.csv", index=False)
df_quarantine.to_csv("data/quarantine/failed_records.csv", index=False)

print(f"✅ Governance Check Complete.")
print(f"Batch Validation Success: {validation_result.success}")
print(f"Promoted to Silver: {len(df_silver)} | Quarantined: {len(df_quarantine)}")

# 8. Generate and Open Data Docs (The Auditor's View)
context.build_data_docs()
context.open_data_docs()

print("🌐 Data Docs generated! Your browser should open to the Governance Report.")

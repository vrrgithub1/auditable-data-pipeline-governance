import pandas as pd
import numpy as np

reference_df = pd.DataFrame({
    'checking_status': ['A11', 'A12', 'A11', 'A14', 'A12'],
    'duration_months': [12, 24, 36, 12, 48],
    'credit_amount': [2000, 4500, 3000, 1500, 5000],
    'age': [35, 42, 28, 51, 39]
})

# Save to your Silver folder
reference_df.to_csv("data/silver/reference_data.csv", index=False)
print("✅ Sample 'Dirty' data generated in data/silver/reference_data.csv")

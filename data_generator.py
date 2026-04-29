import pandas as pd
import numpy as np

# Create a sample of the German Credit data structure
data = {
    'applicant_id': range(1, 11),
    'checking_status': ['A11', 'A12', 'A11', 'A14', 'A12', 'A11', 'A12', 'A14', 'A11', 'A12'],
    'duration_months': [6, 48, 12, 100, 24, 12, 75, 15, 24, 36], # 100 and 75 are "Dirty" (>72)
    'credit_amount': [1169, 5951, 2096, -500, 4870, 9055, 2835, 3103, 1000, 200], # -500 is "Dirty"
    'age': [67, 22, 49, 45, 53, 35, 53, 35, 61, 28]
}

df = pd.DataFrame(data)

# Save to your Bronze folder
df.to_csv("data/bronze/credit_data.csv", index=False)
print("✅ Sample 'Dirty' data generated in data/bronze/credit_data.csv")

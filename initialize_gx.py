import great_expectations as gx
import os

# 1. Create the Data Context (This is the "Brain" of your governance setup)
context = gx.get_context()

# 2. Create the folder structure for our Medallion Architecture
folders = ['data/bronze', 'data/silver', 'data/quarantine']
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"Created: {folder}")

print("\nGovernance Context Initialized successfully!")
print(f"Context project root: {context.root_directory}")

# Auditable Data Pipeline Governance

A comprehensive data governance framework that ensures data quality, traceability, and compliance throughout the data pipeline using Great Expectations and Evidently AI.

## Overview

This project implements an auditable data pipeline governance system with the following capabilities:

- **Data Validation**: Enforce data quality rules using Great Expectations
- **Data Drift Detection**: Monitor for data distribution changes using Evidently AI
- **Medallion Architecture**: Organize data into Bronze (raw), Silver (validated), and Quarantine (failed) layers
- **Governance Gatekeeping**: Automated validation and quarantine of invalid records

## Project Structure

```
auditable-data-pipeline-governance/
├── app.py                      # Main governance application
├── data_generator.py           # Generates sample credit data with intentional issues
├── data_generator_2.py         # Additional data generator
├── governance_gatekeeper.py    # Core governance validation logic
├── initialize_gx.py            # Great Expectations context initialization
├── evidently_ai.py             # Data drift detection and reporting
├── data/
│   ├── bronze/                 # Raw, unvalidated data
│   │   └── credit_data.csv
│   ├── silver/                 # Validated, governed data
│   │   ├── credit_data_governed.csv
│   │   ├── reference_data.csv
│   │   └── data_drift_report.html
│   └── quarantine/            # Failed records isolated for review
│       └── failed_records.csv
├── notebooks/                  # Jupyter notebooks for exploration
└── tests/                      # Test suite
```

## Prerequisites

- Python 3.8+
- Great Expectations
- Evidently AI
- Pandas
- NumPy

## Installation

Install the required dependencies:

```bash
pip install great-expectations evidently pandas numpy
```

## Components

### 1. Data Generation (`data_generator.py`)

Generates sample credit data with intentional data quality issues for testing:
- Invalid duration months (>72)
- Negative credit amounts

### 2. Governance Initialization (`initialize_gx.py`)

Sets up the Great Expectations context and creates the Medallion Architecture folder structure.

### 3. Governance Gatekeeper (`governance_gatekeeper.py`)

Core validation engine that:
- Defines governance rules (expectations)
- Validates data against rules
- Routes clean data to Silver layer
- Quarantines failed records

### 4. Data Drift Detection (`evidently_ai.py`)

Monitors for data distribution changes by comparing:
- Reference dataset (baseline)
- Current dataset (new data)

Generates HTML drift reports for visualization.

### 5. Main Application (`app.py`)

Orchestrates the entire governance workflow:
1. Setup governance suite with rules
2. Create data source and assets
3. Load and validate Bronze data
4. Generate validation results

## Usage

### Step 1: Initialize the Environment

```bash
python initialize_gx.py
```

### Step 2: Generate Sample Data

```bash
python data_generator.py
```

### Step 3: Run Governance Validation

```bash
python app.py
```

### Step 4: Check for Data Drift

```bash
python evidently_ai.py
```

## Governance Rules

The system enforces the following data quality rules:

| Rule | Description | Column |
|------|-------------|--------|
| Positive Values | Credit amount must be greater than 0 | `credit_amount` |
| Valid Duration | Duration in months must be between 1 and 72 | `duration_months` |

## Data Flow

```
Bronze (Raw) → Governance Gatekeeper → Silver (Governed)
                   ↓                      ↓
              Quarantine            Validated Data
```

## Output

- **Validation Results**: Detailed pass/fail status for each record
- **Drift Report**: HTML report showing data distribution changes
- **Audit Trail**: Complete history of data quality checks

## License

MIT License
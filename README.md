# Auditable Data Pipeline Governance

An end-to-end auditable data pipeline designed for credit risk data, featuring data governance controls, model fairness, data quality checks, and drift monitoring.

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

## Architecture & Pipeline Layers

This project implements a production-grade multi-layer data storage architecture following the Medallion Architecture pattern:

### Bronze Layer: Raw Data Ingestion

- **Location**: `data/bronze/credit_data.csv`
- **Purpose**: Landing zone for raw, unvalidated data directly from source systems
- **Characteristics**: 
  - Contains original data as ingested with minimal transformation
  - May contain data quality issues (invalid values, missing fields)
  - Serves as the source of truth for all downstream processing
  - Preserves data lineage and auditability

### Silver Layer: Cleaned & Governed Data

- **Location**: `data/silver/credit_data_governed.csv`
- **Purpose**: Validated, cleaned, and quality-checked data ready for consumption
- **Characteristics**:
  - Passed all governance rules and data quality checks
  - Standardized schema and data types
  - Enriched with governance metadata
  - Ready for analytics, reporting, and model training

### Quarantine Layer: Invalid Records

- **Location**: `data/quarantine/failed_records.csv`
- **Purpose**: Isolation of erroneous or invalid rows for manual inspection
- **Characteristics**:
  - Contains records that failed governance validation
  - Preserved for data engineering review and remediation
  - Includes failure reason and validation details
  - Prevents invalid data from propagating downstream

### Data Flow

```
Source System → Bronze Layer → Governance Gatekeeper → Silver Layer (Valid)
                                           ↓
                                    Quarantine Layer (Invalid)
```

## Compliance Frameworks

This project aligns with major regulatory and standards frameworks for AI and data governance:

### NIST AI Risk Management Framework (AI RMF)

The project implements the following NIST AI RMF functions:

- **Measure**: Great Expectations provides quantitative metrics for data quality, completeness, and validity. Each validation run produces detailed pass/fail statistics and error rates that can be tracked over time.
  
- **Monitor**: Evidently AI enables continuous monitoring for data drift and distribution changes. The system generates automated HTML reports comparing reference baselines against current data, ensuring ongoing model performance and data integrity.

### EU AI Act Alignment

This pipeline addresses EU AI Act requirements through:

- **Data Minimization & PII Protection**: Sensitive consumer attributes and personally identifiable information (PII) are isolated in the Quarantine layer when they fail validation. Only validated, cleaned data proceeds to the Silver layer.
  
- **Auditability**: Complete audit trail of all data quality checks, validation results, and data transformations. Each record's journey from Bronze → Silver → Quarantine is traceable.
  
- **Explainability**: Governance rules are explicitly defined as Great Expectations "expectations" with clear documentation of what constitutes valid vs. invalid data.
  
- **Fairness**: Data quality checks ensure consistent treatment of records, preventing bias from incomplete or erroneous data from entering downstream models.

## Validation Steps

This section documents the key validation and monitoring steps implemented in the pipeline:

### Great Expectations Suite

The `credit_governance_suite` is a comprehensive validation suite that enforces business rules on credit risk data:

- **credit_amount Validation**: Ensures loan amounts are constrained to acceptable business limits (must be positive values greater than 0)
- **duration_months Validation**: Ensures loan duration is within acceptable business limits (must be between 1 and 72 months)
- **Column-level Expectations**: Validates presence and type of all required columns
- **Statistical Checks**: Monitors distribution of values to detect anomalies

Each validation run produces detailed pass/fail statistics, error rates, and actionable failure messages for data engineers.

### Data Drift Analysis

Evidently AI is used to continuously monitor for data distribution changes by comparing:

- **Reference Dataset**: The baseline training data (`data/silver/reference_data.csv`) representing expected data distributions
- **Current Dataset**: Incoming batches from the Bronze layer for validation

The drift analysis monitors the following 4 core features:
- `checking_status`: Distribution of checking account status
- `duration_months`: Distribution of loan duration values
- `credit_amount`: Distribution of credit/loan amounts
- `age`: Distribution of applicant ages

When drift exceeds configured thresholds, the system generates an HTML report (`data/silver/data_drift_report.html`) visualizing the distribution changes, enabling proactive model retraining and data quality intervention.

## Setup & Execution Instructions

### Prerequisites

- Python 3.9+
- Conda environment: `governance_pipeline`
- Dependencies: `pip install -r requirements.txt` (or specify evident/Great Expectations installs)

### Running the Pipeline

1. **Initialize Great Expectations**:
   ```bash
   python initialize_gx.py
   ```

2. **Generate the governed datasets and run validation checks**:
   ```bash
   python data_generator.py
   ```

3. **Generate the Evidently Data Drift Report**:
   ```bash
   python evidently_ai.py
   ```

## Components

### 1. Governance Initialization (`initialize_gx.py`)

Sets up the Great Expectations context and creates the Medallion Architecture folder structure.

### 2. Governance Gatekeeper (`governance_gatekeeper.py`)

Core validation engine that:
- Defines governance rules (expectations)
- Validates data against rules
- Routes clean data to Silver layer
- Quarantines failed records

### 3. Data Drift Detection (`evidently_ai.py`)

Monitors for data distribution changes by comparing:
- Reference dataset (baseline)
- Current dataset (new data)

Generates HTML drift reports for visualization.

### 4. Main Application (`app.py`)

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
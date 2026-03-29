# 🏦 Finance Loan Data Engineering Project

A cloud-based end-to-end data engineering pipeline built on **Azure Databricks** and **Azure Data Lake Storage Gen2 (ADLS)** to process, clean, and calculate loan scores for 2.26 million+ loan records in the finance domain.

---

## 📋 Project Overview

This project ingests a **1.5GB raw finance dataset** (`FinanceProjectData.csv`), splits it into domain-specific datasets, applies multi-stage data cleaning, creates external Parquet tables using **Unity Catalog**, and finally computes a **Loan Score** for each customer based on three weighted criteria.

### Key Objectives
- Ingest raw loan data (2.26M+ records) from CSV stored in Databricks Volumes
- Split raw data into 4 domain datasets: Customers, Loans, Loan Repayments, Loan Defaulters
- Clean and standardize each dataset across 4 dedicated cleaning sessions
- Create permanent external tables on ADLS Gen2 using Unity Catalog
- Build a consolidated view by joining all 5 tables
- Identify and segregate bad/duplicate data
- Calculate final loan scores based on Payment History, Defaulters History & Financial Health

---

## 🏗️ Architecture

```
Raw CSV (1.5GB) in Databricks Volumes
              │
              ▼
    Bronze Layer (Raw Data)
    ┌─────────────────────────────┐
    │  customers_data_csv         │
    │  loans_data_csv             │
    │  loans_repayments_csv       │
    │  loans_defaulters_csv       │
    └─────────────────────────────┘
              │
              ▼
    Silver Layer (Cleaned Data - Parquet)
    ┌─────────────────────────────┐
    │  customers_parquet          │
    │  loans_parquet              │
    │  loans_repayments_parquet   │
    │  loans_defaulters_delinq    │
    │  loans_defaulters_rec_enq   │
    └─────────────────────────────┘
              │
              ▼
    External Tables (Unity Catalog on ADLS Gen2)
    ┌─────────────────────────────┐
    │  customers_external         │
    │  loans_external             │
    │  loans_repayments_external  │
    │  loans_defaulters_delinq    │
    │  loans_defaulters_rec_enq   │
    └─────────────────────────────┘
              │
              ▼
    Gold Layer (Loan Score Output)
    ┌─────────────────────────────┐
    │  loan_score (Parquet)       │
    │  loan_final_grade (A-F)     │
    └─────────────────────────────┘
```

---

## 📁 Project Structure

```
finance-loan-de-project/
│
├── Notebooks/
│   ├── 01_finance_project_setup.ipynb               # Raw data ingestion, SHA-256 hash key generation, dataset splitting
│   ├── 02_data_cleaning_1.ipynb                     # Customers data cleaning
│   ├── 03_data_cleaning_2.ipynb                     # Loans data cleaning
│   ├── 04_data_cleaning_3.ipynb                     # Loan repayments data cleaning
│   ├── 05_data_cleaning_4.ipynb                     # Loan defaulters data cleaning
│   ├── 06_permanent_table_creation.ipynb            # External table creation on ADLS Gen2 via Unity Catalog
│   ├── 07_access_patterns_quick_and_slow.ipynb      # Consolidated view + managed table for quick/slow access
│   ├── 08_identifying_bad_data.ipynb                # Duplicate member_id detection & bad data segregation
│   └── 09_loan_score_processing_and_storing.ipynb   # Loan score calculation & storage
│
├── configs/
│   └── config.yaml                                  # Environment & pipeline configurations
│
├── tests/
│   └── test_data_cleaning.py                        # Unit tests for transformation logic
│
├── requirements.txt                                 # Python dependencies
└── README.md
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Azure Databricks** | Data processing & notebook orchestration |
| **Azure Data Lake Storage Gen2 (ADLS)** | Raw, cleaned & processed data storage |
| **Unity Catalog** | Data governance, external locations & credentials |
| **Parquet** | Efficient columnar storage format |
| **Apache Spark (PySpark)** | Distributed data processing (2.26M+ records) |
| **Spark SQL** | Data querying & transformations |
| **Python** | Pipeline logic & transformations |
| **Azure Managed Identity** | Secure authentication to ADLS |

---

## 🔄 Pipeline Sequence

| Step | Notebook | Description | Layer |
|---|---|---|---|
| 1 | `01_finance_project_setup.ipynb` | Load raw CSV, generate SHA-256 hash keys, split into 4 datasets | 🔵 Bronze |
| 2 | `02_data_cleaning_1.ipynb` | Clean customers data (schema, dedup, nulls, emp_length, address_state) | 🟡 Silver |
| 3 | `03_data_cleaning_2.ipynb` | Clean loans data (schema, nulls, loan_term, loan_purpose standardization) | 🟡 Silver |
| 4 | `04_data_cleaning_3.ipynb` | Clean loan repayments (nulls, zero payments fix, date corrections) | 🟡 Silver |
| 5 | `05_data_cleaning_4.ipynb` | Clean loan defaulters (type casting, split into delinq & records datasets) | 🟡 Silver |
| 6 | `06_permanent_table_creation.ipynb` | Create 5 external tables on ADLS Gen2 via Unity Catalog | 🟠 Silver/Gold |
| 7 | `07_access_patterns_quick_and_slow.ipynb` | Create consolidated view (slow access) & managed table (quick access) | 🟠 Silver/Gold |
| 8 | `08_identifying_bad_data.ipynb` | Detect duplicate member_ids, segregate bad data, create clean new tables | 🟠 Silver/Gold |
| 9 | `09_loan_score_processing_and_storing.ipynb` | Calculate loan scores & grades (A-F), store results in Processed folder | 🟢 Gold |

---

## 📊 Dataset Details

### Raw Data Stats
| Metric | Value |
|---|---|
| Total Records | 2,260,701 |
| Unique Members | 2,257,384 |
| Duplicate Members (multiple loans) | 3,317 |
| Bad Data Records (flagged) | 3,189 |
| Final Scored Records | 1,102,587 |

### Generated Datasets (Bronze Layer)
| Dataset | Key Column | Description |
|---|---|---|
| `customers_data_csv` | `member_id` (SHA-256 hash) | Customer demographic & financial info |
| `loans_data_csv` | `loan_id`, `member_id` | Loan details & status |
| `loans_repayments_csv` | `loan_id` | Loan repayment history |
| `loans_defaulters_csv` | `member_id` | Delinquency & public records |

---

## 🧹 Data Cleaning Summary

### Customers (Notebook 2)
- Defined custom schema with correct data types
- Renamed columns for clarity (e.g. `addr_state` → `address_state`)
- Added `ingest_date` timestamp column
- Removed 63 duplicate rows (2,260,701 → 2,260,638)
- Removed 5 rows with null `annual_income`
- Converted `emp_length` to integer using regex; replaced 146,903 nulls with avg value (6 years)
- Cleaned `address_state` — replaced 254 invalid entries with `NA`

### Loans (Notebook 3)
- Defined custom schema, added `ingest_date`
- Dropped rows with nulls in 8 business-critical columns
- Converted `loan_term_months` to `loan_term_years`
- Standardized `loan_purpose` to 14 valid categories (all others → `other`)

### Loan Repayments (Notebook 4)
- Dropped nulls in 5 numeric payment columns
- Fixed 46 records where `total_payment_received = 0` but principal was received
- Removed 995 rows where `total_payment_received = 0`
- Replaced invalid `0.0` date entries with NULL in `last_payment_date` and `next_payment_date`

### Loan Defaulters (Notebook 5)
- Cast all numeric columns to integer, replaced nulls with 0
- Split into two datasets: `delinq` (delinquency details) and `records_enq` (public records & enquiries)

---

## 🏛️ External Tables (Unity Catalog)

5 external tables created on ADLS Gen2 using Unity Catalog with Azure Managed Identity authentication:

| Table | Description |
|---|---|
| `finance_project.customers_external` | Clean customer data |
| `finance_project.loans_external` | Clean loan data |
| `finance_project.loans_repayments_external` | Clean repayment data |
| `finance_project.loans_defaulters_delinq_external` | Delinquency records |
| `finance_project.loans_defaulters_detail_records_enq_external` | Public records & enquiries |

### Access Patterns
| Type | Object | Use Case |
|---|---|---|
| **Slow Access** (always fresh) | `finance_project.customers_loan_v` (VIEW) | Always up-to-date, refreshes with underlying tables |
| **Quick Access** (pre-joined) | `finance_project.customers_loan_managed` (TABLE) | Fast queries, pre-joined consolidated data |

---

## 🎯 Loan Score Calculation

Loan score is calculated based on **3 weighted criteria**:

### 1️⃣ Payment History — 25% weight
| Condition | Points |
|---|---|
| Last payment > 1.5x monthly installment | 800 (Excellent) |
| Last payment between 1x and 1.5x installment | 650 (Very Good) |
| Last payment = monthly installment | 500 (Good) |
| Last payment between 0.5x and 1x installment | 250 (Bad) |
| Last payment < 0.5x installment | 100 (Very Bad) |

### 2️⃣ Defaulters History — 45% weight
| Column | 0 occurrences | 1-2 | 3-5 | >5 |
|---|---|---|---|---|
| `delinq_2yrs` | 800 | 250 | 100 | 0 |
| `pub_rec` | 800 | 250 | 100 | 100 |
| `pub_rec_bankruptcies` | 800 | 250 | 100 | 100 |
| `inq_last_6mths` | 800 | 250 | 100 | 0 |

### 3️⃣ Financial Health — 30% weight
| Factor | Condition | Points |
|---|---|---|
| Loan Status | Fully Paid | 800 |
| Loan Status | Current | 500 |
| Loan Status | Charged Off | 0 |
| Home Ownership | Own | 800 |
| Home Ownership | Rent | 500 |
| Home Ownership | Mortgage | 250 |
| Credit Utilization | Funded ≤ 10% of credit limit | 800 |
| Grade | A1-A4 | 2500 |
| Grade | B1-B4 | 2000 |
| Grade | C1-C4 | 1500 |

### Final Loan Grade
| Loan Score | Grade |
|---|---|
| > 2500 | A ⭐ |
| 1500 – 2500 | B |
| 1000 – 1500 | C |
| 500 – 1000 | D |
| 0 – 500 | E |
| ≤ 0 | F |

---

## 🚀 Getting Started

### Prerequisites
- Azure Databricks workspace (Unity Catalog enabled)
- Azure Data Lake Storage Gen2 account (`financeprojectdatalake01`)
- Azure Managed Identity with **Storage Blob Data Contributor** role
- Python 3.8+

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/kicker12345/finance-loan-de-project.git
   ```

2. **Upload raw data to Databricks Volumes**
   ```
   /Volumes/finance_domain_project/default/raw_data/FinanceProjectData.csv
   ```

3. **Configure Unity Catalog**
   - Create storage credential: `finance_uc_cred`
   - Create external location: `finance_raw_location`
   - Assign Storage Blob Data Contributor role to Managed Identity

4. **Run notebooks in order**
   ```
   01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09
   ```

---

## 📦 Requirements

```
pyspark
delta-spark
pandas
openpyxl
pytest
chispa
pyyaml
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📈 Future Improvements

- [ ] Merge DataCleaning notebooks into a single unified pipeline
- [ ] Add CI/CD with GitHub Actions
- [ ] Implement Great Expectations for automated data quality checks
- [ ] Add Databricks Workflows for pipeline orchestration
- [ ] Implement incremental data loading (instead of full refresh)
- [ ] Add monitoring & alerting on pipeline failures

---

## 👤 Author

**Himanshu Pal**
- GitHub: [@kicker12345](https://github.com/kicker12345)

---

## 📄 License

This project is for educational and portfolio purposes.

# Credit Card Fraud Detection — End-to-End Data & ML Pipeline in Databricks (Updated)

This repository demonstrates an end-to-end data engineering + ML workflow for detecting fraudulent credit card transactions using Databricks (Community or managed workspace). The project implements a simple Bronze → Silver → Gold pipeline with Delta tables, basic data quality checks, and a scikit-learn model training step.

Why this update
- Align README with the actual notebooks and code in the workspace.
- Provide a concise Quickstart to run notebooks in Databricks.
- Document where audit and model metadata are persisted and note next steps.

Project summary
- Bronze: raw/incoming table stored as a Delta table.
- Silver: cleaned/canonicalized dataset (filtering and null handling).
- Gold: model training on Pandas-converted data and model metadata persisted to a Delta table.

Quickstart (Databricks)
1. Open the repo in Databricks Repos or upload these files into a workspace.
2. Run ingestion (create Bronze table):
   - Open [notebooks/01_ingest_bronze.ipynb](notebooks/01_ingest_bronze.ipynb) and update input_path, then run cells.
3. Create Silver table:
   - Run [notebooks/transform_silver.py](notebooks/transform_silver.py) which uses [`SILVER_TABLE`](notebooks/transform_silver.py).
4. Run data quality checks:
   - Run [notebooks/dq_checks.py](notebooks/dq_checks.py) which writes results to the audit Delta table referenced by [`DQ_AUDIT_TABLE`](notebooks/dq_checks.py).
5. Train model:
   - Run [notebooks/train_model_gold.py](notebooks/train_model_gold.py). This converts the Silver Spark table to Pandas, trains a Logistic Regression model, computes AUC, and writes metadata to `finance_catalog.gold.model_metadata`.

Files of interest
- [notebooks/01_ingest_bronze.ipynb](notebooks/01_ingest_bronze.ipynb) — CSV ingestion and Bronze table creation.
- [notebooks/transform_silver.py](notebooks/transform_silver.py) — Silver transformation and write; defines [`SILVER_TABLE`](notebooks/transform_silver.py).
- [notebooks/dq_checks.py](notebooks/dq_checks.py) — Null-check auditing; uses [`BRONZE_TABLE`](notebooks/dq_checks.py), [`DQ_AUDIT_TABLE`](notebooks/dq_checks.py), and [`RUN_ID`](notebooks/dq_checks.py).
- [notebooks/train_model_gold.py](notebooks/train_model_gold.py) — Converts Silver to Pandas, trains logistic regression (`lr`) and persists metadata.
- [utils/dq_utils.py](utils/dq_utils.py) — placeholder for shared DQ helper functions.
- [config/dq_rules.json](config/dq_rules.json) — configuration for data quality rules (extendable).

How the code currently behaves (accurate to workspace)
- Data quality checks: simple per-column null counts are computed and appended to a Delta audit table. See [`notebooks/dq_checks.py`](notebooks/dq_checks.py).
- Silver transform: filters negative Amount and drops rows with nulls in Time/Amount/Class, then writes to [`SILVER_TABLE`](notebooks/transform_silver.py).
- Model training: converts Silver to Pandas, fits sklearn LogisticRegression (no StandardScaler in current code), computes AUC and writes model metadata to Delta. See [`notebooks/train_model_gold.py`](notebooks/train_model_gold.py).

Recommendations / Next steps
- Implement model serialization (pickle + base64) and persist the serialized model binary alongside metadata in `finance_catalog.gold.model_metadata`. See where metadata is written in [notebooks/train_model_gold.py](notebooks/train_model_gold.py).
- Move DQ logic into [utils/dq_utils.py](utils/dq_utils.py) and drive rules from [config/dq_rules.json](config/dq_rules.json).
- Add unit/integration tests for transformation and DQ checks.
- Consider applying scaling (StandardScaler) and pipeline persistence for production parity.
- Add clear notebook parameterization to allow running in automated jobs.

Contact / contribution
- Open issues or PRs in this repo. Use Databricks Repos for iterative development and running notebooks.

License
- Add a LICENSE file if you intend to open-source or share this project.

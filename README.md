# Credit Card Fraud Detection — End-to-End Data & ML Pipeline in Databricks
### 🧠 Project Overview

This project demonstrates an end-to-end data engineering and machine learning workflow for detecting fraudulent credit card transactions using Databricks Community Edition.

The pipeline simulates a real-world financial data environment, applying Bronze–Silver–Gold data lake architecture, data quality validation, and a fraud classification model built using Python’s scikit-learn.

Unlike traditional Databricks MLlib-based projects, this implementation is fully compatible with Databricks CE, leveraging Spark + Pandas + Delta tables for scalable data prep and persistent model tracking.

#Tech Stack

| Layer                            | Tools / Frameworks                                     |
| -------------------------------- | ------------------------------------------------------ |
| **Data Ingestion (Bronze)**      | Databricks, PySpark, Delta Lake                        |
| **Data Transformation (Silver)** | Spark SQL, PySpark DataFrame APIs                      |
| **Data Quality Validation**      | PySpark (null checks, uniqueness, schema conformance)  |
| **Feature Engineering (Gold)**   | Spark → Pandas                                         |
| **Machine Learning**             | scikit-learn (Logistic Regression, AUC/ROC evaluation) |
| **Model Persistence**            | Delta Table (Base64 serialized model + metadata)       |
| **Orchestration & Versioning**   | Databricks Repos + Git Integration                     |

#Machine Learning Component
After Silver-level cleansing:

Data is converted from Spark to Pandas for local training.
Features are standardized (StandardScaler).
A Logistic Regression model is trained to classify fraudulent vs. legitimate transactions.
Evaluation metrics (AUC, accuracy, recall) are computed and logged.

#📈 Key Features

- End-to-end pipeline using Databricks Delta Lakehouse pattern
- Automated data quality validation using PySpark
- Feature engineering & ML modeling using scikit-learn
- Model version tracking and storage in Delta
- Git-integrated Databricks workflow for code versioning
- 100% Community Edition–compatible, no DBFS or MLflow dependencies

#Learning Highlights

- How to design a Bronze–Silver–Gold data lakehouse
- How to integrate Python ML models into a Spark pipeline
- How to build auditability and traceability in CE
- How to leverage Delta tables for persistence beyond DBFS
- How to work effectively with Git + Databricks notebooks
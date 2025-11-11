# Databricks notebook source
# MAGIC %md
# MAGIC ## Silver Layer usually has the clean data

# COMMAND ----------

SILVER_TABLE="finance_catalog.silver.creditcard_silver"

# COMMAND ----------

df_bronze = spark.table("finance_catalog.bronze.creditcard_bronze")

# COMMAND ----------

print(".............. Silver Table processing Started ...............")

# Filter out rows with negative 'Amount' and drop rows with nulls in 'Time', 'Amount', or 'Class'
df_silver = df_bronze.filter("Amount >= 0").dropna(subset=["Time", "Amount", "Class"])

if spark.catalog.tableExists(SILVER_TABLE):
    df_silver.write.format("delta").mode("append").saveAsTable("finance_catalog.silver.creditcard_silver")
else:
    df_silver.write.format("delta").mode("overwrite").saveAsTable("finance_catalog.silver.creditcard_silver")

print("............... Silver Table Created and Processing Done ..............")

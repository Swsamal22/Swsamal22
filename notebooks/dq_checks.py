# Databricks notebook source
from pyspark.sql import functions as F
from datetime import datetime

# COMMAND ----------

BRONZE_TABLE = "finance_catalog.bronze.creditcard_bronze"
DQ_AUDIT_TABLE = "finance_catalog.bronze.dq_audits"

RUN_ID = datetime.now().strftime("%Y%m%d%H%M%S")

df = spark.table(BRONZE_TABLE)
total_count = df.count()

# COMMAND ----------

######## NULL CHECKS #######
null_summary = []
for c in df.columns:
    null_count = df.filter(F.col(c).isNull()).count()
    null_pct = round((null_count / total_count) * 100, 2)
    null_summary.append((c, null_count, null_pct))

null_df = spark.createDataFrame(data=null_summary, schema=["column_name", "null_count", "null_pct"])
null_df = null_df.withColumn("run_id", F.lit(RUN_ID))
null_df = null_df.withColumn("table_name", F.lit("BRONZE_TABLE"))
null_df = null_df.withColumn("run_timestamp", F.current_timestamp())

# COMMAND ----------

##writing results
if spark.catalog.tableExists(DQ_AUDIT_TABLE):
    null_df.write.format("delta").mode("append").saveAsTable(DQ_AUDIT_TABLE)
else:
    null_df.write.format("delta").mode("overwrite").saveAsTable(DQ_AUDIT_TABLE)

display(null_df.head(5))

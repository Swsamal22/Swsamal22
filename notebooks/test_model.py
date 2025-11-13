# Databricks notebook source
import base64, pickle
import pandas as pd
import numpy as np
from pyspark.sql import functions as F

# COMMAND ----------

model_row =spark.table('finance_catalog.gold.model_metadata').orderBy(F.desc("run_date")).collect()[0]
display(model_row)

coef = np.array(model_row["coefficients"]).flatten()
intercept = np.array(model_row["intercept"]).flatten()

print("Loaded model coefficients and intercept.")

# COMMAND ----------

feature_list = (spark.table("finance_catalog.silver.creditcard_silver"))
display(feature_list.limit(5))

# COMMAND ----------

test_input = pd.DataFrame([{
    [np.random.randn(len(feature_list))],
    columns=feature_list
}])
x=test_input.values

print("Input X shape:", x.shape)
print("Coef shape:", coef.shape)
print("Intercept shape:", intercept.shape)

logit = np.dot(x, coef) + intercept
probability = 1/(1+np.exp(-logit))
label = int(probability>0.5)

print(f"Probability of fraud: {probability[0]:.4f}")
print(f"Predicted Lable: {'Fraud' if label else 'Legit'}")

# COMMAND ----------



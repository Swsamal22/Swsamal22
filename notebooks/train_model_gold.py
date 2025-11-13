# Databricks notebook source
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, classification_report
import pandas as pd
import uuid

# COMMAND ----------

df_silver = spark.table("finance_catalog.silver.creditcard_silver")
pandas_df_silver = df_silver.toPandas()
# display(pandas_df_silver)
X=pandas_df_silver.drop(columns=["Class"])
y=pandas_df_silver["Class"]

print(f" Data Ready for ML: {X.shape[0]} rows, {X.shape[1]} features")

# COMMAND ----------

# Split the dataset into training and test sets with stratified sampling

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Initialize logistic regression model with increased max iterations
lr = LogisticRegression(max_iter=1000)

# Fit the logistic regression model on the training data
lr.fit(X_train, y_train)

# Predict class labels for the test set
y_pred = lr.predict(X_test)

# Predict class probabilities for the test set and select probability for positive class
y_prob = lr.predict_proba(X_test)[:,1]

# Calculate ROC AUC score for the test set predictions
auc = roc_auc_score(y_test, y_prob)

# Print the AUC score
print(f" Logistic Regression AUC: {auc:.4f}")

# Print classification report including precision, recall, f1-score
print(classification_report(y_test, y_pred))
#collect metadata
model_info = pd.DataFrame({
    "run_id": [str(uuid.uuid4())],
    "model_name": ["Logistic Regression"],
    "auc": [auc],
    "coefficients": [lr.coef_.tolist()],
    "intercept": [lr.intercept_.tolist()],
    "run_date": [pd.Timestamp.now()]
})
display(model_info)
spark.createDataFrame(model_info).write.format("delta").option("mergeSchema", "true").mode("append").saveAsTable("finance_catalog.gold.model_metadata")

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 13:10:37 2023

@author: Stenka Vulova
"""
# I am testing 5-fold cross-validation (for accuracy assessment).

#%%  Import libraries

import pandas as pd
import numpy as np

# plotting
import matplotlib.pyplot as plt
import plotly

# ML libraries 

from xgboost import XGBClassifier

from sklearn.metrics import make_scorer, recall_score, precision_score, f1_score, accuracy_score, roc_auc_score
from sklearn.model_selection import cross_validate
from sklearn.preprocessing import LabelEncoder

# Wagner libs
from time import time

import joblib


#%% Import dataset 

df = pd.read_csv("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230623_modeling_df/all/twoclass_subset/modeling_df_2class_2019.csv")

print(df["NDVI_categories"].value_counts())
# large_decrease    2000
# no_change         2000
# Name: NDVI_categories, dtype: int64

#%% Prepare dataframe for modeling

#print(df.columns.tolist()) # print all column names

# remove columns: x, y, NDVI_anomaly, Year_NDVI_anom

# Prepare the data by separating the predictors (X) and the target variable (y)
X = df.drop(["x", "y", "NDVI_categories", "Year_NDVI_anom", "NDVI_anomaly"], axis=1) # predictors 
y = df["NDVI_categories"] # response variable 

print(X.columns.tolist())

#%% Label encoding to target variable

# I got this ValueError: Invalid classes inferred from unique values of `y`.  Expected: [0 1], got ['large_decrease' 'no_change'] 
# The error you encountered suggests that the target variable y contains string labels instead of numerical values (0 and 1) that are expected by the XGBoost classifier.
# To resolve this issue, you need to encode the string labels into numerical values before fitting the XGBoost model.

# Create an instance of LabelEncoder
label_encoder = LabelEncoder()

# Encode the string labels into numerical values
y_encoded = label_encoder.fit_transform(y)

# Verify the encoded labels
print(y)
print(y_encoded)

# 0 = large_decrease
# 1 = no_change


#%% XGB classifier

# Best Parameters found:  {'learning_rate': 0.001, 'max_depth': 10, 'n_estimators': 10000}

# Train the XGBoost classifier

classifier = XGBClassifier(max_depth=10, 
            n_estimators=10000, 
            learning_rate=0.001,
            importance_type = 'total_gain', random_state=19)

#%% scoring 

# scoring
# Make a scorer from a performance metric or loss function.

# This factory function wraps scoring functions for use in GridSearchCV and cross_val_score.
#It takes a score function, such as accuracy_score, mean_squared_error, adjusted_rand_score or average_precision_score and returns a callable that scores an estimator’s output. 

# Define the scoring functions for cross-validation
scoring = {
    'recall': make_scorer(recall_score),
    'precision': make_scorer(precision_score),
    'f1': make_scorer(f1_score),
    'accuracy': make_scorer(accuracy_score),
    'roc_auc': make_scorer(roc_auc_score)
}

#%% 5fold crossvalidation

# Record the start time
start = time()

# Perform 5-fold cross-validation and get the performance metrics for each fold
cv_results = cross_validate(classifier, X, y_encoded, cv=5, scoring = scoring)

# Record the end time
end = time()


# Print the time taken for hyperparameter tuning
print("After {} s".format(end - start))
# After 302.69846367836 s (5 min)

#%% results 

# Print the performance metrics for each fold
print("Recall:", cv_results['test_recall'])
print("Precision:", cv_results['test_precision'])
print("F1:", cv_results['test_f1'])
print("Accuracy:", cv_results['test_accuracy'])
print("ROC AUC:", cv_results['test_roc_auc'])

# Recall: [0.7725 0.7675 0.76   0.74   0.7725]
#Precision: [0.80678851 0.78117048 0.80211082 0.78723404 0.79844961]
#F1: [0.78927203 0.77427491 0.7804878  0.7628866  0.78526048]
#Accuracy: [0.79375 0.77625 0.78625 0.77    0.78875]
#ROC AUC: [0.79375 0.77625 0.78625 0.77    0.78875]

#%%  avg metrics 

# Calculate the average metrics across all folds
average_recall = cv_results['test_recall'].mean()
average_precision = cv_results['test_precision'].mean()
average_f1 = cv_results['test_f1'].mean()
average_accuracy = cv_results['test_accuracy'].mean()
average_roc_auc = cv_results['test_roc_auc'].mean()

# Print the average metrics
print("Average Recall:", average_recall)
print("Average Precision:", average_precision)
print("Average F1:", average_f1)
print("Average Accuracy:", average_accuracy)
print("Average ROC AUC:", average_roc_auc)

# Average Recall: 0.7625
# Average Precision: 0.7951506936216304
# Average F1: 0.7784363643472464
# Average Accuracy: 0.7829999999999999
# Average ROC AUC: 0.783
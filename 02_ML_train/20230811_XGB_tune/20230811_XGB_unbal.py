# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 15:11:56 2023

@author: Stenka Vulova
"""

#%%  Import libraries

import pandas as pd
import numpy as np

# plotting
import matplotlib.pyplot as plt
import plotly

# ML libraries 

from xgboost import XGBClassifier

from sklearn.metrics import recall_score, precision_score, f1_score, accuracy_score, roc_auc_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Wagner libs
from time import time

import joblib

#%% Import dataset 

df = pd.read_csv("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230705_modeling_df_unbalanced/modeling_df_2class_2019_unbal.csv")

print(df["NDVI_categories"].value_counts())
# NDVI_categories
# no_change         5217
#large_decrease    2491
#Name: count, dtype: int64

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

#%% Train/ test split 

# Split the data into training and testing sets using train_test_split
# 'test_size specifies the proportion of the dataset to include in the test split.
# By setting stratify=y, the train_test_split() function will ensure that the class distribution in both the training and testing sets is similar to the original distribution in y.
# This helps maintain the same ratio of the two classes.
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.3, random_state=20, stratify=y)

print('X_train: {}'.format(X_train.shape))
print('y_train: {}'.format(y_train.shape))
print('X_valid: {}'.format(X_test.shape))
print('y_valid: {}'.format(y_test.shape))

# X_train: (5395, 23)
# y_train: (5395,)
# X_valid: (2313, 23)
# y_valid: (2313,)

#%% Train the classifier

# Best Parameters found:  {'learning_rate': 0.001, 'max_depth': 10, 'n_estimators': 10000}

# Train the XGBoost classifier

model = XGBClassifier(max_depth=10, 
            n_estimators=10000, 
            learning_rate=0.001,
            importance_type = 'total_gain', random_state=19)

model.fit(X_train, y_train)

# XGBClassifier(base_score=None, booster=None, callbacks=None,
#              colsample_bylevel=None, colsample_bynode=None,
#              colsample_bytree=None, early_stopping_rounds=None,
#              enable_categorical=False, eval_metric=None, feature_types=None,
 #             gamma=None, gpu_id=None, grow_policy=None,
#              importance_type='total_gain', interaction_constraints=None,
#              learning_rate=0.001, max_bin=None, max_cat_threshold=None,
 #             max_cat_to_onehot=None, max_delta_step=None, max_depth=10,
 #             max_leaves=None, min_child_weight=None, missing=nan,
  #            monotone_constraints=None, n_estimators=10000, n_jobs=None,
 #             num_parallel_tree=None, predictor=None, random_state=19, ...)

#%%  Predict on the test set 

# Use the trained model to make predictions on the test set
y_pred = model.predict(X_test)

#%% Performance metrics

recall = recall_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred)

print("Test Set Metrics:")
print("Recall:", recall)
print("Precision:", precision)
print("F1:", f1)
print("Accuracy:", accuracy)
print("ROC AUC:", roc_auc)

# Test Set Metrics:
#Recall: 0.8722860791826309
#Precision: 0.8293867638129934
#F1: 0.8502956738250856
#Accuracy: 0.7920449632511889
#ROC AUC: 0.7480573635538321

#%% classification report 
report = classification_report(y_test, y_pred)

# The classification_report function provides precision, recall, F1-score, and support for each class.

print("Classification Report:")
print(report)

#Classification Report:
#              precision    recall  f1-score   support

#           0       0.70      0.62      0.66       747
#           1       0.83      0.87      0.85      1566

#    accuracy                           0.79      2313
#   macro avg       0.76      0.75      0.75      2313
#weighted avg       0.79      0.79      0.79      2313

#%% Save the model

# You can save a scikit-learn model as a .pkl file using the joblib library
# which is recommended for efficiently storing large NumPy arrays. 
# Note: The joblib library is preferred over the pickle module for saving scikit-learn models due to its improved performance with large data.

# This code will save the trained model to a file named 'model.pkl' and then load it back using the same file.

# Save the model to a .pkl file
joblib.dump(model, 'D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230811_XGB_tune/xgb_unbal_model.pkl')
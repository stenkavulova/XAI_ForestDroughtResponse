# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 14:08:48 2023

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

from collections import Counter

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

#%% scale_pos_weight 

# summarize class distribution
counter = Counter(y_encoded)
print(counter)

# Counter({1: 5217, 0: 2491})

# estimate scale_pos_weight value
estimate = counter[0] / counter[1]
print('Estimate: %.3f' % estimate)
# 0.477


#%%  Model with scale_pos_weight set

# Set parameter max_delta_step to a finite number (say 1) to help convergence
# xgboost with imbalanced data:
# https://xgboost.readthedocs.io/en/stable/tutorials/param_tuning.html

# define model
model2 = XGBClassifier(scale_pos_weight= estimate , 
        max_depth=10, 
            n_estimators=10000, 
            learning_rate=0.001,
            importance_type = 'total_gain', random_state=19)

model2.fit(X_train, y_train)

# Use the trained model2 to make predictions on the test set
y_pred2 = model2.predict(X_test)

report = classification_report(y_test, y_pred2)

# The classification_report function provides precision, recall, F1-score, and support for each class.

print("Classification Report:")
print(report)

#Classification Report:
 #             precision    recall  f1-score   support
#
 #          0       0.68      0.72      0.70       747
 #          1       0.86      0.84      0.85      1566

 #   accuracy                           0.80      2313
#   macro avg       0.77      0.78      0.77      2313
#weighted avg       0.80      0.80      0.80      2313


# Old result BELOW:
    
#              precision    recall  f1-score   support

#           0       0.70      0.62      0.66       747
#           1       0.83      0.87      0.85      1566

#    accuracy                           0.79      2313
#   macro avg       0.76      0.75      0.75      2313
#weighted avg       0.79      0.79      0.79      2313


# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 17:43:20 2023

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

#%%  Make y into 0 and 1

# Note that when working with binary classification problems, especially imbalanced problems,
# it is important that the majority class is assigned to class 0 and the minority class is assigned to class 1.
# This is because many evaluation metrics will assume this relationship.

# imbalanced classification book is the source. 

# I did the opposite until now unfortunately* 

# Create a mapping dictionary
category_mapping = {"no_change": 0, "large_decrease": 1}

# Create a new Series by mapping the values
y_encoded = y.map(category_mapping)

# Print the resulting encoded Series
print(y_encoded)

y_encoded.value_counts()

# NDVI_categories
# 0    5217
# 1    2491
# Name: count, dtype: int64


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

# Estimate the scale_pos_weight value
est_scale_pos_weight = counter[0] / counter[1]
print('Estimate of scale_pos_weight: %.3f' % est_scale_pos_weight)

#Counter({0: 5217, 1: 2491})
#Estimate of scale_pos_weight: 2.094

#%%  Model with NO scale_pos_weight set

# Set parameter max_delta_step to a finite number (say 1) to help convergence
# xgboost with imbalanced data:
# https://xgboost.readthedocs.io/en/stable/tutorials/param_tuning.html

# define model
model = XGBClassifier(objective = "binary:logistic",
        max_depth=10, 
            n_estimators=10000, 
            learning_rate=0.001,
            importance_type = 'total_gain', random_state=19)

model.fit(X_train, y_train)

# Use the trained model to make predictions on the test set
y_pred = model.predict(X_test)

report = classification_report(y_test, y_pred)

# The classification_report function provides precision, recall, F1-score, and support for each class.

print("Classification Report:")
print(report)

# Classification Report:
#              precision    recall  f1-score   support

#           0       0.83      0.87      0.85      1566
#           1       0.70      0.62      0.66       747

#    accuracy                           0.79      2313
#   macro avg       0.76      0.75      0.75      2313
#weighted avg       0.79      0.79      0.79      2313

#%%  Model with scale_pos_weight set

# define model
model = XGBClassifier(objective = "binary:logistic",
        scale_pos_weight = est_scale_pos_weight,
        max_delta_step = 1, 
        max_depth=10, 
            n_estimators=10000, 
            learning_rate=0.001,
            importance_type = 'total_gain', random_state=19)

model.fit(X_train, y_train)

# Use the trained model to make predictions on the test set
y_pred = model.predict(X_test)

report = classification_report(y_test, y_pred)

# The classification_report function provides precision, recall, F1-score, and support for each class.

print("Classification Report:")
print(report)

# Classification Report:
#              precision    recall  f1-score   support

#           0       0.85      0.84      0.85      1566
#           1       0.68      0.70      0.69       747

#    accuracy                           0.80      2313
#   macro avg       0.77      0.77      0.77      2313
#weighted avg       0.80      0.80      0.80      2313

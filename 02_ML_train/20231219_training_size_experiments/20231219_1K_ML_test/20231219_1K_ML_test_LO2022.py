# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 14:43:47 2023

@author: Stenka Vulova
"""

# I will randomly downsample all years to be the same size (in this example: 1000/ year). That means 500 of each class per year. 
# I will leave out 2022 in all cases and compare the accuracy. 


#%%  Import libraries

import pandas as pd
import numpy as np

# plotting
import matplotlib.pyplot as plt
import plotly

# ML libraries 

from xgboost import XGBClassifier

from sklearn.metrics import recall_score, precision_score, f1_score, accuracy_score, roc_auc_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Wagner libs
import time 
from sklearn.model_selection import GridSearchCV

import joblib # save the trained model 

#%% Import all dfs 

df_2018 = pd.read_csv("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20231219_mod_dfs_reduced/1K/subset_df_2018.csv")
print(df_2018["NDMI_classes"].value_counts())

df_2019 = pd.read_csv("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20231219_mod_dfs_reduced/1K/subset_df_2019.csv")
print(df_2019["NDMI_classes"].value_counts())

df_2020 = pd.read_csv("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20231219_mod_dfs_reduced/1K/subset_df_2020.csv")
print(df_2020["NDMI_classes"].value_counts())

df_2021 = pd.read_csv("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20231219_mod_dfs_reduced/1K/subset_df_2021.csv")
print(df_2021["NDMI_classes"].value_counts())

df_2022 = pd.read_csv("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20231219_mod_dfs_reduced/1K/subset_df_2022.csv")
print(df_2022["NDMI_classes"].value_counts())

#%% make training dfs

# all dfs except 2022 (used for testing)

# List of DataFrames
dfs = [df_2018, df_2019, df_2020, df_2021]

# Concatenate DataFrames vertically
stacked_df = pd.concat(dfs, axis=0, ignore_index=True)

stacked_df.shape
# (4000, 46)

#print(stacked_df.columns.tolist()) # print all column names

# remove columns not used as predictors

# Prepare the data by separating the predictors (X) and the target variable (y)
X_train = stacked_df.drop(["x", "y", "NDMI_classes", "Year_NDMI_anom", "NDMI_anomaly"], axis=1) # predictors 
# X has 41 columns (exactly correct - 41 predictors)

y_train_raw = stacked_df["NDMI_classes"] # response variable 

print(X_train.columns.tolist())

#%% Make testing df 

# 2022 is left out and used for testing 

# Prepare the data by separating the predictors (X) and the target variable (y)
X_test = df_2022.drop(["x", "y", "NDMI_classes", "Year_NDMI_anom", "NDMI_anomaly"], axis=1) # predictors 
# X has 41 columns (exactly correct - 41 predictors)

y_test_raw = df_2022["NDMI_classes"] # response variable 

#%%  Make y into 0 and 1

# Note that when working with binary classification problems, especially imbalanced problems,
# it is important that the majority class is assigned to class 0 and the minority class is assigned to class 1.
# This is because many evaluation metrics will assume this relationship.

# imbalanced classification book is the source. 

# I did the opposite until now unfortunately* 

# Create a mapping dictionary
category_mapping = {"no_change": 0, "damaged": 1}

# Create a new Series by mapping the values
y_train = y_train_raw.map(category_mapping)
y_test = y_test_raw.map(category_mapping)

# Print the resulting encoded Series
print(y_train)
print(y_train_raw)

print(y_test)
print(y_test_raw)

print('X_train: {}'.format(X_train.shape))
print('y_train: {}'.format(y_train.shape))
print('X_valid: {}'.format(X_test.shape))
print('y_valid: {}'.format(y_test.shape))

# X_train: (4000, 41)
# y_train: (4000,)
# X_valid: (1000, 41)
# y_valid: (1000,)

#%% Train 

# Start the timer
start_time = time.time()

# Train the XGBoost classifier
# use the default hyperparameters

model = XGBClassifier(random_state=19)

model.fit(X_train, y_train)

# Use the trained model to make predictions on the test set
y_pred = model.predict(X_test)

# Calculate the elapsed time
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time:.2f} seconds")

# Execution time: 0.58 seconds

report = classification_report(y_test, y_pred)

# The classification_report function provides precision, recall, F1-score, and support for each class.

print("Classification Report:")
print(report)

# Execution time: 0.58 seconds
#Classification Report:
#              precision    recall  f1-score   support

#           0       0.63      0.47      0.54       500
#           1       0.58      0.72      0.64       500

#    accuracy                           0.59      1000
#   macro avg       0.60      0.59      0.59      1000
#weighted avg       0.60      0.59      0.59      1000
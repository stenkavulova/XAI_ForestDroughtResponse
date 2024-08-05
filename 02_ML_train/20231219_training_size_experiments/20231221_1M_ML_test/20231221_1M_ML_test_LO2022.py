# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 14:43:47 2023

@author: Stenka Vulova
"""

# I will randomly downsample all years to be the same size (in this example: 1M/ year). That means 5K of each class per year. 
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

df_2018 = pd.read_csv("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20231219_mod_dfs_reduced/1M/sub_df_1M_2018.csv")
print(df_2018["NDMI_classes"].value_counts())

df_2019 = pd.read_csv("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20231219_mod_dfs_reduced/1M/sub_df_1M_2019.csv")
print(df_2019["NDMI_classes"].value_counts())

df_2020 = pd.read_csv("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20231219_mod_dfs_reduced/1M/sub_df_1M_2020.csv")
print(df_2020["NDMI_classes"].value_counts())

df_2021 = pd.read_csv("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20231219_mod_dfs_reduced/1M/sub_df_1M_2021.csv")
print(df_2021["NDMI_classes"].value_counts())

df_2022 = pd.read_csv("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20231219_mod_dfs_reduced/1M/sub_df_1M_2022.csv")
print(df_2022["NDMI_classes"].value_counts())

#%% make training dfs

# all dfs except 2022 (used for testing)

# List of DataFrames
dfs = [df_2018, df_2019, df_2020, df_2021]

# Concatenate DataFrames vertically
stacked_df = pd.concat(dfs, axis=0, ignore_index=True)

stacked_df.shape
# (400000, 46)

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

# X_train: (400000, 41)
# y_train: (400000,)
# X_valid: (100000, 41)
# y_valid: (100000,)

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

# Execution time: 561.21 seconds (9 min. 21 seconds)

report = classification_report(y_test, y_pred)

# The classification_report function provides precision, recall, F1-score, and support for each class.

print("Classification Report:")
print(report)

# Classification Report:
#              precision    recall  f1-score   support

#           0       0.60      0.57      0.58    500000
#           1       0.59      0.61      0.60    500000

#    accuracy                           0.59   1000000
#   macro avg       0.59      0.59      0.59   1000000
#weighted avg       0.59      0.59      0.59   1000000

#%% Save the model 

# Save the trained model to a file
joblib.dump(model, 'D:/Stenka_Cliwac/Topic_1/12_PYTHON/20231221_1M_ML_test/model_1M_LO2022.pkl')

# To load the model later
loaded_model = joblib.load('D:/Stenka_Cliwac/Topic_1/12_PYTHON/20231221_1M_ML_test/model_1M_LO2022.pkl')

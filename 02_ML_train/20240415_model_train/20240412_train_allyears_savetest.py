# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 14:43:47 2023

@author: Stenka Vulova
"""

# I will randomly downsample all years to be the same size (in this example: 100K/ year). That means 5K of each class per year. 
# I will leave out 2021 in all cases and compare the accuracy. 


#%%  Import libraries

import pandas as pd
import numpy as np

# plotting
import matplotlib.pyplot as plt
import plotly

# ML libraries 

from xgboost import XGBClassifier
import xgboost as xgb

from sklearn.metrics import recall_score, precision_score, f1_score, accuracy_score, roc_auc_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Wagner libs
import time 
from sklearn.model_selection import GridSearchCV

import joblib # save the trained model 

#%% Import all dfs 

df_2018 = pd.read_csv("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_mod_dfs_100K_new/sub_df_100K_2018_new.csv")
print(df_2018["true_class"].value_counts())

df_2019 = pd.read_csv("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_mod_dfs_100K_new/sub_df_100K_2019_new_KH.csv")
print(df_2019["true_class"].value_counts())

df_2020 = pd.read_csv("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_mod_dfs_100K_new/sub_df_100K_2020_new.csv")
print(df_2020["true_class"].value_counts())

df_2021 = pd.read_csv("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_mod_dfs_100K_new/sub_df_100K_2021_new.csv")
print(df_2021["true_class"].value_counts())

df_2022 = pd.read_csv("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_mod_dfs_100K_new/sub_df_100K_2022_new.csv")
print(df_2022["true_class"].value_counts())

#%% make training dfs

# List of DataFrames
dfs = [df_2018, df_2019, df_2020, df_2021, df_2022]

# Concatenate DataFrames vertically
stacked_df = pd.concat(dfs, axis=0, ignore_index=True)

stacked_df.shape
# (500000, 46)

#print(stacked_df.columns.tolist()) # print all column names

# remove columns not used as predictors

# Prepare the data by separating the predictors (X) and the target variable (y)

X_train = stacked_df.drop(["x", "y", "true_class", "coord_code", "Year_NDMI_anom", "NDMI_anomaly"], axis=1) # predictors 
# X has 41 columns (exactly correct - 41 predictors)

y_train = stacked_df["true_class"] # response variable 

print(X_train.columns.tolist())

#%% Make testing df 

# 2021 is left out and used for testing 

# Prepare the data by separating the predictors (X) and the target variable (y)
X_test = df_2021.drop(["x", "y", "true_class", "coord_code", "Year_NDMI_anom", "NDMI_anomaly"], axis=1) # predictors 
# X has 41 columns (exactly correct - 41 predictors)

y_test = df_2021["true_class"] # response variable 

#%%  Make y into 0 and 1

# Comment Katharina: I skipped this part, since the newly created 100k subsets are already
# coded with 0 and 1 within the column "true_class" (which is the new version of "NDMI_classes")

# Note that when working with binary classification problems, especially imbalanced problems,
# it is important that the majority class is assigned to class 0 and the minority class is assigned to class 1.
# This is because many evaluation metrics will assume this relationship.

# imbalanced classification book is the source. 

# I did the opposite until now unfortunately* 

# Create a mapping dictionary
#category_mapping = {"no_change": 0, "damaged": 1}

# Create a new Series by mapping the values
#y_train = y_train_raw.map(category_mapping)
#y_test = y_test_raw.map(category_mapping)

# Print the resulting encoded Series
print(y_train)
#print(y_train_raw)

print(y_test)
#print(y_test_raw)

print('X_train: {}'.format(X_train.shape))
print('y_train: {}'.format(y_train.shape))
print('X_valid: {}'.format(X_test.shape))
print('y_valid: {}'.format(y_test.shape))

# X_train: (500000, 41)
#y_train: (500000,)
#X_valid: (100000, 41)
#y_valid: (100000,)

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

# Execution time: 58.15 seconds (04/12/2024)

report = classification_report(y_test, y_pred)

# The classification_report function provides precision, recall, F1-score, and support for each class.

print("Classification Report:")
print(report)

# Classification Report (04/12/2024):
#               precision    recall  f1-score   support
# 
#            0       0.72      0.73      0.72     50000
#            1       0.72      0.71      0.72     50000
# 
#     accuracy                           0.72    100000
#    macro avg       0.72      0.72      0.72    100000
# weighted avg       0.72      0.72      0.72    100000
#%% Save the model 
# old way

# Save the trained model to a file
joblib.dump(model, 'D:/Vulova/Topic_1/12_PYTHON/20240415_model_allyears/model_100K_allyears_20240415.pkl')

# To load the model later
loaded_model = joblib.load('D:/Vulova/Topic_1/12_PYTHON/20240415_model_allyears/model_100K_allyears_20240415.pkl')

#%% Save the model the new way 

# https://xgboost.readthedocs.io/en/latest/tutorials/saving_model.html 

# WARNING: D:/bld/xgboost-split_1700181111005/work/src/learner.cc:553: 
#  If you are loading a serialized model (like pickle in Python, RDS in R) generated by
 # older XGBoost, please export the model by calling `Booster.save_model` from that version
#  first, then load it back in current version. See:
 
#	https://xgboost.readthedocs.io/en/latest/tutorials/saving_model.html
 
 # for more details about differences between saving model and serializing.

model.save_model("D:/Vulova/Topic_1/12_PYTHON/20240415_model_allyears/model_allyears_20240415.json")

# Load the model from the JSON file
loaded_model = xgb.Booster()
loaded_model.load_model("D:/Vulova/Topic_1/12_PYTHON/20240415_model_allyears/model_allyears_20240415.json")
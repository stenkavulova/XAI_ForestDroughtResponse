# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:21:15 2023

@author: Stenka Vulova
"""

#Use just one year (e.g. 2019)
#Random forests (classification)

#two classes
#decrease class means > -10%
#no change class is between -5 and 5 %

# Anaconda environment shapenv

#### Import libraries ####

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV, cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score, precision_score, f1_score, accuracy_score, roc_auc_score

# my addition
from sklearn.preprocessing import LabelEncoder

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

# X_train: (2800, 23)
# y_train: (2800,)
# X_valid: (1200, 23)
# y_valid: (1200,)


#%% Train the classifier

# Train the RF classifier

model = RandomForestClassifier(random_state=19)
model.fit(X_train, y_train)

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
#Recall: 0.7116666666666667
#Precision: 0.8180076628352491
#F1: 0.7611408199643495
#Accuracy: 0.7766666666666666
#ROC AUC: 0.7766666666666666

#%% Save the model

# You can save a scikit-learn model as a .pkl file using the joblib library
# which is recommended for efficiently storing large NumPy arrays. 
# Note: The joblib library is preferred over the pickle module for saving scikit-learn models due to its improved performance with large data.

# This code will save the trained model to a file named 'model.pkl' and then load it back using the same file.

# Save the model to a .pkl file
joblib.dump(model, 'D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230810_Hanyu_codes/model.pkl')

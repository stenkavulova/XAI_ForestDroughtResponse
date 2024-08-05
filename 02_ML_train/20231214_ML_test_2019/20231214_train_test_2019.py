# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 09:03:23 2023

@author: Stenka Vulova
"""

# This is the first test modeling with the new S2 and Landsat data.


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

#%% Import dataset 

df = pd.read_csv("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230927_modeling_df/balanced/balanced_df_2019.csv")

print(df["NDMI_classes"].value_counts())
# NDMI_classes
#damaged      5128392
#no_change    5128392
#Name: count, dtype: int64

# Classes are balanced 

# Rows: 10,256,784
# Columns: 46

#%% Prepare dataframe for modeling

print(df.columns.tolist()) # print all column names

# remove columns not used as predictors

# Prepare the data by separating the predictors (X) and the target variable (y)
X = df.drop(["x", "y", "NDMI_classes", "Year_NDMI_anom", "NDMI_anomaly"], axis=1) # predictors 
# X has 41 columns (exactly correct - 41 predictors)

y = df["NDMI_classes"] # response variable 

print(X.columns.tolist())


#%%  Make y into 0 and 1

# Note that when working with binary classification problems, especially imbalanced problems,
# it is important that the majority class is assigned to class 0 and the minority class is assigned to class 1.
# This is because many evaluation metrics will assume this relationship.

# imbalanced classification book is the source. 

# I did the opposite until now unfortunately* 

# Create a mapping dictionary
category_mapping = {"no_change": 0, "damaged": 1}

# Create a new Series by mapping the values
y_encoded = y.map(category_mapping)

# Print the resulting encoded Series
print(y_encoded)
print(y)

#y_encoded.value_counts()

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

# X_train: (7179748, 41)
# y_train: (7179748,)
# X_valid: (3077036, 41)
# y_valid: (3077036,)


#%% Train 

# Start the timer
start_time = time.time()

# Train the XGBoost classifier

model = XGBClassifier(max_depth=10, 
            n_estimators=5000, 
            learning_rate=0.001,
            importance_type = 'total_gain', random_state=19)

model.fit(X_train, y_train)

# Use the trained model to make predictions on the test set
y_pred = model.predict(X_test)

# Calculate the elapsed time
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time:.2f} seconds")

# Execution time: 23447.61 seconds (6 hours 30 min.)

report = classification_report(y_test, y_pred)

# The classification_report function provides precision, recall, F1-score, and support for each class.

print("Classification Report:")
print(report)

# Classification Report:
#              precision    recall  f1-score   support

#           0       0.76      0.77      0.77   1538518
#           1       0.77      0.75      0.76   1538518

#    accuracy                           0.76   3077036
#   macro avg       0.76      0.76      0.76   3077036
#weighted avg       0.76      0.76      0.76   3077036



#%% Confusion matrix

# A confusion matrix is a way to visualize the performance of a model. And more importantly, we can easily see where the model fails exactly.

class_names = model.classes_
print(class_names)

# Compute the confusion matrix
cm = confusion_matrix(y_true = y_test, y_pred = y_pred)

# Create the ConfusionMatrixDisplay
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels = class_names)

# Plot the confusion matrix
disp.plot()

# Save the plot as a PNG file
plt.savefig('D:/Stenka_Cliwac/Topic_1/12_PYTHON/20231214_ML_test_2019/20231214_confusion_matrix.png', dpi=300, bbox_inches='tight')

#%% Save the model 

# Save the trained model to a file
#joblib.dump(model, 'D:/Stenka_Cliwac/Topic_1/12_PYTHON/20231214_ML_test_2019/xgb_model_2019.pkl')

# To load the model later
loaded_model = joblib.load('D:/Stenka_Cliwac/Topic_1/12_PYTHON/20231214_ML_test_2019/xgb_model_2019.pkl')

#%% test loaded model

# should give the same results 

# Use the trained loaded_model to make predictions on the test set
y_pred_l = loaded_model.predict(X_test)

report_l = classification_report(y_test, y_pred_l)

# The classification_report_l function provides precision, recall, F1-score, and support for each class.

print("Classification Report (loaded model):")
print(report_l)

# Classification Report (loaded model):
#              precision    recall  f1-score   support

#           0       0.76      0.77      0.77   1538518
#           1       0.77      0.75      0.76   1538518

#    accuracy                           0.76   3077036
#   macro avg       0.76      0.76      0.76   3077036
#weighted avg       0.76      0.76      0.76   3077036
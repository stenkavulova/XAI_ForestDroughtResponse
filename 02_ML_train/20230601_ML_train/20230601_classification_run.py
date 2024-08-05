# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 11:40:42 2023

@author: Stenka Vulova
"""

# Try classification


#%% Libraries

import pandas as pd
import numpy as np

# Machine learning libraries
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

#%% modeling df 

# Load the dataframe from a file (assuming it's a CSV file)
df = pd.read_csv('D:/Stenka_Cliwac/Topic_1/05_RESULTS/20230525_modeling_df/all/modeling_df.csv')

# Delete the columns named "x" and "y"
columns_to_delete = ['x', 'y']
df = df.drop(columns=columns_to_delete)

# Print the modified dataframe
print(df)

#%% new categories

# Define the thresholds and corresponding categories
thresholds = [-np.inf, -10, -5, 5, 10, np.inf]
categories = ["large_decrease", "small_decrease", "no_change", "small_increase", "large_increase"]

# Create a new column "NDVI_categories" based on the classification
df["NDVI_categories"] = pd.cut(df["NDVI_anomaly"], bins=thresholds, labels=categories, right=False)

#%% number per category

category_counts = df["NDVI_categories"].value_counts()
print(category_counts)

#no_change         29350
#small_decrease    13157
#large_decrease     7205
#small_increase     2201
#large_increase      763
#Name: NDVI_categories, dtype: int64

#%% number per category 2019

df_2019 = df[df["Year_NDVI_anom"] == 2019]

cat_counts_2019 = df_2019["NDVI_categories"].value_counts()
print(cat_counts_2019)

#no_change         5392
#small_decrease    4603
#large_decrease    2573
#small_increase      82
#large_increase      26

#%% number per category 2022

df_2022 = df[df["Year_NDVI_anom"] == 2022]

cat_counts_2022 = df_2022["NDVI_categories"].value_counts()
print(cat_counts_2022)

#no_change         5194
#small_decrease    4722
#large_decrease    3369
#small_increase     152
#large_increase      47
#Name: NDVI_categories, dtype: int64

#%% Prepare data for modeling

# Split the data into training and testing sets
train_df = df[df["Year_NDVI_anom"] == 2019]
test_df = df[df["Year_NDVI_anom"] == 2022]

# Select predictors (features) and target variable
predictors = train_df.drop(["NDVI_categories", "Year_NDVI_anom", "NDVI_anomaly"], axis=1)
target = train_df["NDVI_categories"]

#%% Run classifier 

# Train the GBM classifier
gbm = GradientBoostingClassifier()
gbm.fit(predictors, target)

# Make predictions on the testing set
test_predictors = test_df.drop(["NDVI_categories", "Year_NDVI_anom", "NDVI_anomaly"], axis=1)
predictions = gbm.predict(test_predictors)

# Evaluate the performance
test_target = test_df["NDVI_categories"]
accuracy = accuracy_score(test_target, predictions)
confusion_matrix = confusion_matrix(test_target, predictions)
classification_report = classification_report(test_target, predictions)

# Print the performance metrics
print("Accuracy:", accuracy) # Accuracy: 0.3728122218926135
print("Confusion Matrix:\n", confusion_matrix)
# Confusion Matrix:
 #[[1275   91  255 1696   52]
# [  24    7    2   11    3]
 #[ 863   87  628 3452  164]
 #[1002   77  421 3108  114]
# [  59    2   12   70    9]]

print("Classification Report:\n", classification_report)

#Classification Report:
 #                precision    recall  f1-score   support
#
#large_decrease       0.40      0.38      0.39      3369
#large_increase       0.03      0.15      0.05        47
 #    no_change       0.48      0.12      0.19      5194
#small_decrease       0.37      0.66      0.48      4722
#small_increase       0.03      0.06      0.04       152

 #     accuracy                           0.37     13484
 #    macro avg       0.26      0.27      0.23     13484
#  weighted avg       0.41      0.37      0.34     13484
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 11:40:42 2023

@author: Stenka Vulova
"""

# Try classification
# Now I will delete the "positive increase" category - too few samples.

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

#%% remove increase categories

# too few samples in the % increase categories
# plus, my study is about why the forest suffers...

# Create a boolean mask for rows to be removed
mask = (df["NDVI_categories"] == "small_increase") | (df["NDVI_categories"] == "large_increase")

# Apply the mask to the dataframe to remove the rows
df_filtered = df[~mask]

# categories
print(df_filtered["NDVI_categories"].unique())


#%% number per category 2019

df_2019 = df_filtered[df_filtered["Year_NDVI_anom"] == 2019]

cat_counts_2019 = df_2019["NDVI_categories"].value_counts()
print(cat_counts_2019)

#no_change         5392
#small_decrease    4603
#large_decrease    2573
#small_increase      82
#large_increase      26

#%% Balance the training and testing data

# classes should be balanced in training/testing

# Group the dataframe by "NDVI_categories" and "Year_NDVI_anom", get the minimum count per group
min_count = df_filtered.groupby(["NDVI_categories", "Year_NDVI_anom"]).size().min()

# Create an empty list to store sampled dataframes
sampled_dfs = []

# Iterate over each group, sample the minimum number of rows, and append to the list
for group, data in df_filtered.groupby(["NDVI_categories", "Year_NDVI_anom"]):
    sampled_data = data.sample(n=min_count, random_state=42)  # Set random_state for reproducibility
    sampled_dfs.append(sampled_data)

# Concatenate the sampled dataframes into a new dataframe
downsampled_df = pd.concat(sampled_dfs)

# Print the unique values in the "NDVI_categories" column of the downsampled dataframe
print(downsampled_df["NDVI_categories"].unique())


#%% Prepare data for modeling

# Split the data into training and testing sets
train_df = df_filtered[df_filtered["Year_NDVI_anom"] == 2019]
test_df = df_filtered[df_filtered["Year_NDVI_anom"] == 2022]

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
print("Accuracy:", accuracy) # Accuracy: 0.36921339856981555
print("Confusion Matrix:\n", confusion_matrix)
# Confusion Matrix:
 #[[1353  114 1902]
 #[1125  303 3766]
# [1273  200 3249]]

print("Classification Report:\n", classification_report)

#Classification Report:
#                 precision    recall  f1-score   support

#large_decrease       0.35      0.27      0.31      2573
#     no_change       0.45      0.59      0.51      5392
#small_decrease       0.39      0.28      0.33      4603

 #     accuracy                           0.41     12568
#     macro avg       0.39      0.38      0.38     12568
#  weighted avg       0.40      0.41      0.40     12568
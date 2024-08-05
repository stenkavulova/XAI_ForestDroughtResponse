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

# plot variable importance 
import matplotlib.pyplot as plt

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
#small_increase       0
#large_increase       0

#%% resample  2019

# less samples per category

# 2000 to start with
# Set the desired number of samples per category
num_samples = 2000

# Group the dataframe by the "NDVI_categories" column
grouped = df_2019.groupby("NDVI_categories")

# Create an empty list to store the sampled dataframes
sampled_dfs = []

# Iterate over each group
for category, group in grouped:
    # Check if the number of samples in the group is greater than the desired number
    if len(group) > num_samples:
        # Randomly sample the desired number of rows from the group
        sampled_group = group.sample(n=num_samples, random_state=42)
        # Add the sampled group to the list
        sampled_dfs.append(sampled_group)
    else:
        # If the group has fewer samples than the desired number, add all rows to the list
        sampled_dfs.append(group)

# Concatenate the sampled dataframes back into a single dataframe
df_sub_2019 = pd.concat(sampled_dfs)

# Optional: Reset the index of the resulting dataframe
df_sub_2019 = df_sub_2019.reset_index(drop=True)

print(df_sub_2019["NDVI_categories"].value_counts())
# large_decrease    2000
#small_decrease    2000
#no_change         2000
#small_increase       0
#large_increase       0
#Name: NDVI_categories, dtype: int64


#%% number per category 2022

df_2022 = df_filtered[df_filtered["Year_NDVI_anom"] == 2022]

cat_counts_2022 = df_2022["NDVI_categories"].value_counts()
print(cat_counts_2022)

#no_change         5194
#small_decrease    4722
#large_decrease    3369
#small_increase       0
#large_increase       0
#Name: NDVI_categories, dtype: int64

#%% resample 2022

# less samples per category

# 2000 to start with
# Set the desired number of samples per category
#num_samples = 2000

# Group the dataframe by the "NDVI_categories" column
grouped_22 = df_2022.groupby("NDVI_categories")

# Create an empty list to store the sampled dataframes
sampled_dfs_22 = []

# Iterate over each group
for category, group in grouped_22:
    # Check if the number of samples in the group is greater than the desired number
    if len(group) > num_samples:
        # Randomly sample the desired number of rows from the group
        sampled_group = group.sample(n=num_samples, random_state=42)
        # Add the sampled group to the list
        sampled_dfs_22.append(sampled_group)
    else:
        # If the group has fewer samples than the desired number, add all rows to the list
        sampled_dfs_22.append(group)

# Concatenate the sampled dataframes back into a single dataframe
df_sub_2022 = pd.concat(sampled_dfs_22)

# Optional: Reset the index of the resulting dataframe
df_sub_2022 = df_sub_2022.reset_index(drop=True)

print(df_sub_2022["NDVI_categories"].value_counts())
#large_decrease    2000
#small_decrease    2000
#no_change         2000
#small_increase       0
#large_increase       0
#Name: NDVI_categories, dtype: int64

#%% Prepare data for modeling

# Split the data into training and testing sets
train_df = df_sub_2019
test_df = df_sub_2022

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
print("Accuracy:", accuracy) # Accuracy: 0.4241666666666667
print("Confusion Matrix:\n", confusion_matrix)
# Confusion Matrix:
# [[1037  607  356]
# [ 534 1014  452]
# [ 642  864  494]]

print("Classification Report:\n", classification_report)

#Classification Report:
#                 precision    recall  f1-score   support

#large_decrease       0.47      0.52      0.49      2000
#     no_change       0.41      0.51      0.45      2000
#small_decrease       0.38      0.25      0.30      2000

 #     accuracy                           0.42      6000
 #    macro avg       0.42      0.42      0.41      6000
 # weighted avg       0.42      0.42      0.41      6000
 
#%%  Variable importance

# Get feature importance
importance = gbm.feature_importances_

# Get feature names
feature_names = predictors.columns

# Sort indices in descending order of importance
indices = np.argsort(importance)[::-1]

# Plot variable importance
plt.figure(figsize=(10, 6))
plt.title("Variable Importance")
plt.bar(range(len(feature_names)), importance[indices], align="center")
plt.xticks(range(len(feature_names)), feature_names[indices], rotation=90)
plt.xlabel("Features")
plt.ylabel("Importance")
plt.tight_layout()
plt.show()

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 14:39:02 2023

@author: Stenka Vulova
"""

# Use just one year (e.g. 2019)
# Train on 70 %, test on 30 % of the data 
# Random forests (classification)

# two classes
# decrease class means > -10%
# no change class is between -5 and 5 %

#%% Libraries

import pandas as pd
import numpy as np

# plot variable importance 
import matplotlib.pyplot as plt

# ML libraries 
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

#%% modeling df 

# Load the dataframe from a file (assuming it's a CSV file)
df = pd.read_csv('D:/Stenka_Cliwac/Topic_1/05_RESULTS/20230525_modeling_df/all/modeling_df.csv')

# Delete the columns named "x" and "y"
columns_to_delete = ['x', 'y']
df = df.drop(columns=columns_to_delete)

# Print the modified dataframe
print(df)

# Subset to year 2019 

df_2019 = df[df["Year_NDVI_anom"] == 2019] # 12676 rows, 20 columns 

# Get the unique values in the "Year_NDVI_anom" column
unique_years = df_2019['Year_NDVI_anom'].unique()

# Print the unique years
print(unique_years) # [2019]

#%% new categories

# Define the thresholds and corresponding categories
thresholds = [-np.inf, -10, -5, 5, 10, np.inf]
categories = ["large_decrease", "small_decrease", "no_change", "small_increase", "large_increase"]

# Create a new column "NDVI_categories" based on the classification
df_2019["NDVI_categories"] = pd.cut(df_2019["NDVI_anomaly"], bins=thresholds, labels=categories, right=False)

# number per category

category_counts = df_2019["NDVI_categories"].value_counts()
print(category_counts)

#no_change         5392
#small_decrease    4603
#large_decrease    2573
#small_increase      82
#large_increase      26
#Name: NDVI_categories, dtype: int64

#%% remove increase categories

# too few samples in the % increase categories
# plus, my study is about why the forest suffers...
# I am also removing the "small_decrease" class now.

# Create a boolean mask for rows to be removed
mask = (df_2019["NDVI_categories"] == "small_increase") | (df_2019["NDVI_categories"] == "large_increase") | (df_2019["NDVI_categories"] == "small_decrease")

# Apply the mask to the dataframe to remove the rows
df_filtered = df_2019[~mask]

# categories
print(df_filtered["NDVI_categories"].unique())

print(df_filtered["NDVI_categories"].value_counts())
#no_change         5392
#large_decrease    2573
#small_decrease       0
#small_increase       0
#large_increase       0
#Name: NDVI_categories, dtype: int64

#%% make equal sample sizes per class

# less samples per category

# 2500 to start with
# Set the desired number of samples per category
num_samples = 2500

# Group the dataframe by the "NDVI_categories" column
grouped = df_filtered.groupby("NDVI_categories")

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
# large_decrease    2500
#no_change         2500
#small_decrease       0
#small_increase       0
#large_increase       0
#Name: NDVI_categories, dtype: int64

#%% Prepare training and testing datasets

# Prepare the data by separating the predictors (X) and the target variable (y)
X = df_sub_2019.drop(["NDVI_categories", "Year_NDVI_anom", "NDVI_anomaly"], axis=1)
y = df_sub_2019["NDVI_categories"]

# Split the data into training and testing sets using train_test_split
# 'test_size specifies the proportion of the dataset to include in the test split.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)

#%% Train RF

# Train the Random Forest classifier
rf = RandomForestClassifier()
rf.fit(X_train, y_train)

#%% Predict

y_train_pred = rf.predict(X_train)
y_test_pred = rf.predict(X_test)

#%% Performance metrics

# Compute the accuracy and classification report

train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)
classification_report = classification_report(y_test, y_test_pred)

# The accuracy_score function is used to compute the accuracy, which is the proportion of correctly classified samples.
# The classification_report function provides precision, recall, F1-score, and support for each class.

#%% Print the metrics 

print("Training Accuracy:", train_accuracy)
print("Testing Accuracy:", test_accuracy)
print("Classification Report:")
print(classification_report)
# Classification Report:
#                precision    recall  f1-score   support
#
#large_decrease       0.76      0.80      0.78       762
#     no_change       0.78      0.74      0.76       738
#
#     accuracy                           0.77      1500
#     macro avg       0.77      0.77      0.77      1500
#  weighted avg       0.77      0.77      0.77      1500

# Testing Accuracy: 0.7713333333333333

#%%  Variable importance

# Get feature importance
importances = rf.feature_importances_

# Create a pandas DataFrame with the feature importances
feature_importances = pd.DataFrame({'Feature': X.columns, 'Importance': importances})

# Sort the DataFrame in ascending order of importance
feature_importances = feature_importances.sort_values('Importance', ascending=True).reset_index(drop=True)

# Plot the variable importance using a bar plot

plt.figure(figsize=(8, 6))
plt.barh(feature_importances['Feature'], feature_importances['Importance'])
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Variable Importance')

# save plot 

plt.savefig("D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230612_regression/varImp_classi_exp_300dpi.png", dpi=300, bbox_inches='tight')
plt.show()

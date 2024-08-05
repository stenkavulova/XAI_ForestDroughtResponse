# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 10:27:00 2023

@author: Stenka Vulova
"""

# Goal: prepare the dataframe for modeling

#%% functions

import pandas as pd

# Machine learning libraries
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

#%% modeling df 

# Load the dataframe from a file (assuming it's a CSV file)
df = pd.read_csv('D:/Stenka_Cliwac/Topic_1/05_RESULTS/20230525_modeling_df/all/modeling_df.csv')

# Delete the columns named "x" and "y"
columns_to_delete = ['x', 'y']
df = df.drop(columns=columns_to_delete)

# Print the modified dataframe
print(df)

#%% subset years

# the most drought-affected years: 2018, 2019, 2022
# this dataset doesn't have 2018, anyway

# Define the years to subset
years_to_subset = [2019, 2022]

# Subset the dataframe based on the specified years
subset_df = df[df['Year_NDVI_anom'].isin(years_to_subset)]

# Print the subsetted dataframe
print(subset_df)

# check if subsetting worked
# Get the unique values in the "Year_NDVI_anom" column
unique_years = subset_df['Year_NDVI_anom'].unique()

# Print the unique years
print(unique_years)

#%% Prepare training and testing datasets

# Separate the predictors and response variable
X_train = df.loc[df['Year_NDVI_anom'] == 2019].drop(columns=['NDVI_anomaly', 'Year_NDVI_anom'])
y_train = df.loc[df['Year_NDVI_anom'] == 2019, 'NDVI_anomaly']

X_test = df.loc[df['Year_NDVI_anom'] == 2022].drop(columns=['NDVI_anomaly', 'Year_NDVI_anom'])
y_test = df.loc[df['Year_NDVI_anom'] == 2022, 'NDVI_anomaly']

#%% Run GBM regression

# Initialize the Gradient Boosted Machines regressor
gbm = GradientBoostingRegressor()

# Train the model
gbm.fit(X_train, y_train)

# Make predictions on the test set
y_pred = gbm.predict(X_test)

# Compute RMSE and R2
rmse = mean_squared_error(y_test, y_pred, squared=False)
r2 = r2_score(y_test, y_pred)

# Print the performance metrics
print("RMSE:", rmse) # RMSE: 7.01741703451025
print("R2:", r2) # R2: -0.14851262826901857

# This model is performing REALLY badly. 
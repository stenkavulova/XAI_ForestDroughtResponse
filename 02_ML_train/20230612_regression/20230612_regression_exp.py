# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 14:01:42 2023

@author: Stenka Vulova
"""

# Use just one year (e.g. 2019)
# Train on 70 %, test on 30 % of the data 
# Random forests

#%% functions

# standard libraries 
import numpy as np
import pandas as pd

# ML libraries 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

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

#%% Train and test split

# Define the predictors and response variables:
predictors = df_2019.drop(["Year_NDVI_anom", "NDVI_anomaly"], axis=1)
response = df_2019["NDVI_anomaly"]

# Split the data into training and testing sets:
X_train, X_test, y_train, y_test = train_test_split(predictors, response, test_size=0.3, random_state=2020)

# X_train and X_test are the training and testing predictors, respectively
# y_train and y_test are the corresponding response variables
# The test_size parameter is set to 0.3, indicating that 30% of the data will be used for testing
# the random_state parameter ensures reproducibility of the split.

#%% Train Random Forests (RF)

#Train the Random Forest regression model
rf = RandomForestRegressor()
rf.fit(X_train, y_train)

#%% Predict on testing data

y_train_pred = rf.predict(X_train)
y_test_pred = rf.predict(X_test) # this is the one that matters 

#%% Performance metrics

train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
print(train_rmse) # 1.8355143677502779

test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
print(test_rmse) # 4.775985164093345

train_r2 = r2_score(y_train, y_train_pred)
print(train_r2) # 0.8990430860959335

test_r2 = r2_score(y_test, y_test_pred)
print(test_r2) # 0.2741579634725597

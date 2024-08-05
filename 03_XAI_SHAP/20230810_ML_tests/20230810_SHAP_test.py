# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 16:13:23 2023

@author: Stenka Vulova
"""

import pandas as pd
import joblib
import matplotlib.pyplot as plt
import shap
from datetime import datetime
import fasttreeshap

# my addition
from sklearn.preprocessing import LabelEncoder

#%% Load model 

with open('D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230810_Hanyu_codes/model.pkl', 'rb') as file:
    model = joblib.load(file)
    
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

#%%  Run SHAP

# Get the current time before starting the process
current_time = datetime.now()
print('Read over', current_time)

# XAI
# Initialize a TreeExplainer using the FastTreeSHAP algorithm
# This algorithm is faster for large datasets
explainer = fasttreeshap.TreeExplainer(model, algorithm='v2', n_jobs=-1, memory_tolerance=30)

# Compute Shapley values for the ALL training data (before train/ test split) using the explainer
# 4000 values total
shap_values = explainer.shap_values(X)

# Get the current time after the process is complete
current_time = datetime.now()
print('shap over', current_time)

#Read over 2023-08-10 16:42:30.515944
#There may exist memory issue for algorithm v2. Switched to algorithm v1.
#shap over 2023-08-10 16:43:09.860189

#%% Extract SHAP values 

# I assume index 0 -> large_decrease class

# Get Shapley values for the "large_decrease" class
shap_values_dec = shap_values[1]

# Create a DataFrame from the Shapley values
shap_values_dec_df = pd.DataFrame(shap_values_dec)
print(shap_values_dec_df.shape)
# 4000, 23

# Make predictions on the test data using the trained model
y_pred = model.predict(X) # 4000 values

# Create a DataFrame for the predicted labels
y_pred_df = pd.DataFrame(y_pred)

# Concatenate the predicted labels and Shapley values DataFrames
merged_df = pd.concat([y_pred_df, shap_values_dec_df], axis=1)

# Save the merged DataFrame to a CSV file named 'SHAP_train.csv'
#merged_df.to_csv('D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230810_Hanyu_codes/SHAP_train.csv', index=False)

#%% SHAP Summary Plot

summary_fig = plt.figure()

shap.summary_plot(shap_values[1], X)

# Save the plot as a PNG file
summary_fig.savefig('D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230810_Hanyu_codes/20230810_shap_summary_plot.png', dpi=300, bbox_inches='tight')
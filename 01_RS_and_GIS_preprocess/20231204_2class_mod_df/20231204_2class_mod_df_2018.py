# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 16:53:30 2023

@author: Stenka Vulova
"""

#%% Libraries

# shapenv Anaconda environment
import pandas as pd
import numpy as np

# plotting
import matplotlib.pyplot as plt
import plotly

# ML libraries 
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split

# SHAP values
#import shap
#shap.initjs()

#%% Load the modeling dataframe

# Load the dataframe from a file 
df = pd.read_csv("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230927_modeling_df/all/mod_df_2018.csv")
#Rows: 10,406,171
#Columns: 45

# Keep the columns named "x" and "y" this time

# Print the dataframe
print(df)
# [50968 rows x 27 columns]

# Get the unique values in the "Year_NDVI_anom" column
unique_years = df['Year_NDMI_anom'].unique()

# Print the unique years
print(unique_years) # [2018]

#%% Create new classes

# Will do 2 classes:  “damaged” (< -10 % change) and  “stable/ no change” (> -10 % change) class 

# Define the thresholds and corresponding categories
thresholds = [-np.inf, -10, np.inf]
categories = ["damaged", "no_change"]

# Create a new column "NDMI_categories" based on the classification
df["NDMI_categories"] = pd.cut(df["NDMI_anomaly"], bins=thresholds, labels=categories, right=False)

# number per category

category_counts = df["NDMI_categories"].value_counts()
print(category_counts)

#NDMI_categories
#no_change         5217
#small_decrease    4470
#large_decrease    2491
#small_increase      80
#large_increase      23
#Name: count, dtype: int64
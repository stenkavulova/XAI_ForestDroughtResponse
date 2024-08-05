# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 16:46:35 2024

@author: Stenka Vulova
"""

# Anaconda environment shapenv

# inspiration
# https://github.com/wagnerfe/xml4urbanformanalysis/blob/main/urbanformvmt/a_test_runs/2_run/03_aggregate_parts_ml/ml.py 

import pandas as pd
import numpy as np
print(np.__version__) # 1.23.0

# plotting
import matplotlib.pyplot as plt
import plotly

# ML libraries 

import xgboost as xgb
from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# SHAP values
import shap
#shap.initjs()

#%% Import datasets

# SHAP df for all years
df_2018 = pd.read_csv("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_SHAP_2018_new/X_all_2018_SHAP.csv")
df_2019 = pd.read_csv("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_SHAP_2019_new/X_all_2019_SHAP.csv")
df_2020 = pd.read_csv("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_SHAP_2020_new/X_all_2020_SHAP.csv")
df_2021 = pd.read_csv("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_SHAP_2021_new/X_all_2021_SHAP.csv")
df_2022 = pd.read_csv("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_SHAP_2022_new/X_all_2022_SHAP.csv")

df_2018.head

# first column is the predicted classes, not SHAP values
# drop first column 
df_2018 = df_2018.drop(columns=df_2018.columns[0], axis=1)
df_2019 = df_2019.drop(columns=df_2019.columns[0], axis=1)
df_2020 = df_2020.drop(columns=df_2020.columns[0], axis=1)
df_2021 = df_2021.drop(columns=df_2021.columns[0], axis=1)
df_2022 = df_2022.drop(columns=df_2022.columns[0], axis=1)

#%% Import column names

# these column names are nonsense 
# lets add the real column names 

df_colnames_2018 = pd.read_csv("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_SHAP_2018_new/X_all_2018.csv")
df_colnames_2019 = pd.read_csv("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_SHAP_2019_new/X_all_2019.csv")
df_colnames_2020 = pd.read_csv("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_SHAP_2020_new/X_all_2020.csv")
df_colnames_2021 = pd.read_csv("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_SHAP_2021_new/X_all_2021.csv")
df_colnames_2022 = pd.read_csv("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_SHAP_2022_new/X_all_2022.csv")

# 41 columns for all 

# Get the column names from df_colnames
new_colnames_2018 = df_colnames_2018.columns.tolist()
new_colnames_2019 = df_colnames_2019.columns.tolist()
new_colnames_2020 = df_colnames_2020.columns.tolist()
new_colnames_2021 = df_colnames_2021.columns.tolist()
new_colnames_2022 = df_colnames_2022.columns.tolist()

# Assign the column names to df's
df_2018.columns = new_colnames_2018
df_2019.columns = new_colnames_2019
df_2020.columns = new_colnames_2020
df_2021.columns = new_colnames_2021
df_2022.columns = new_colnames_2022

#%%
df_colnames = pd.concat([df_colnames_2018, df_colnames_2019, df_colnames_2020, df_colnames_2021, df_colnames_2022])

df_colnames.head
#%% Combine all df's to a single df

df = pd.concat([df_2018, df_2019, df_2020, df_2021, df_2022])

# convert df to array 
array = df.values

df.head
# looks fine! 
#%% (A) SHAP Summary Plot — Global Interpretability

# A variable importance plot lists the most significant variables in descending order.
# The top variables contribute more to the model than the bottom ones and thus have high predictive power.

#print(shap_values[1])
# second row

summary_bar_plot = plt.figure()

shap.summary_plot(shap_values = array, feature_names = new_colnames_2018, plot_type="bar")

# save plot
summary_bar_plot.savefig('D:/Vulova/Topic_1/12_PYTHON/20240415_SHAP_plots/Barplots/shap_summary_barplot_all_years.png', dpi=300)

#%% SHAP Summary Plot

summary_fig = plt.figure()

shap.summary_plot(shap_values = array, features = df_colnames, feature_names = new_colnames_2018)

# Save the plot as a PNG file
summary_fig.savefig('D:/Vulova/Topic_1/12_PYTHON/20240415_SHAP_plots/summary_plots/shap_summary_plot_all_years.png', dpi=300, bbox_inches='tight')

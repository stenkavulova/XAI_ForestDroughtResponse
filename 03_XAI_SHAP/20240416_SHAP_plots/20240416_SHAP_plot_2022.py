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

#%% Import dataset 

# SHAP df for 2022

df = pd.read_csv("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_SHAP_2022_new/X_all_2022_SHAP.csv")

df.head

# first column is the predicted classes, not SHAP values
# drop first column 
df = df.drop(columns=df.columns[0], axis=1)

#%% Import column names

# these column names are nonsense 
# lets add the real column names 

df_colnames = pd.read_csv("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_SHAP_2022_new/X_all_2022.csv")

# 41 columns for both 

# Get the column names from df_colnames
new_colnames = df_colnames.columns.tolist()

# Assign the column names to df
df.columns = new_colnames

# convert to array 
array = df.values


#%% (A) SHAP Summary Plot — Global Interpretability

# A variable importance plot lists the most significant variables in descending order.
# The top variables contribute more to the model than the bottom ones and thus have high predictive power.

#print(shap_values[1])
# second row

summary_bar_plot = plt.figure()

shap.summary_plot(shap_values = array, feature_names= new_colnames, plot_type="bar")

# save plot
summary_bar_plot.savefig('D:/Vulova/Topic_1/12_PYTHON/20240415_SHAP_plots/Barplots/shap_summary_barplot_2022.png', dpi=300)

#%% SHAP Summary Plot

summary_fig = plt.figure()

shap.summary_plot(shap_values = array, features =df_colnames, feature_names= new_colnames)

# Save the plot as a PNG file
summary_fig.savefig('D:/Vulova/Topic_1/12_PYTHON/20240415_SHAP_plots/Summary_plots/shap_summary_plot_2022.png', dpi=300, bbox_inches='tight')

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 11:19:08 2023

@author: Stenka Vulova
"""

# Import libraries

#Use just one year (e.g. 2019)
#Train on 70 %, test on 30 % of the data 
#Random forests (classification)

#two classes
#decrease class means > -10%
#no change class is between -5 and 5 %

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

#%% Train/ test split 

# Split the data into training and testing sets using train_test_split
# 'test_size specifies the proportion of the dataset to include in the test split.
# By setting stratify=y, the train_test_split() function will ensure that the class distribution in both the training and testing sets is similar to the original distribution in y.
# This helps maintain the same ratio of the two classes.
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=20, stratify=y)

print('X_train: {}'.format(X_train.shape))
print('y_train: {}'.format(y_train.shape))
print('X_valid: {}'.format(X_test.shape))
print('y_valid: {}'.format(y_test.shape))

# X_train: (3200, 23)
# y_train: (3200,)
# X_valid: (800, 23)
# y_valid: (800,)

#%% Train the classifier

# Train the XGBoost classifier

model = XGBClassifier(random_state=19)
model.fit(X_train, y_train)

# ValueError: Invalid classes inferred from unique values of `y`.  Expected: [0 1], got ['large_decrease' 'no_change']
# fixed it :)

#%% Predict 

y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

#print(y_test_pred)

#%% Performance metrics

# Compute the accuracy and classification report

train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)
#classification_report = classification_report(y_test, y_test_pred)
# classification_repond mysteriously stopped working after I gave the model a random_state

# The accuracy_score function is used to compute the accuracy, which is the proportion of correctly classified samples.
# The classification_report function provides precision, recall, F1-score, and support for each class.

## Print the metrics

print("Training Accuracy:", train_accuracy)
print("Testing Accuracy:", test_accuracy) # 0.7575

#%% classification report 
report = classification_report(y_test, y_test_pred)

# The classification_report function provides precision, recall, F1-score, and support for each class.

print("Classification Report:")
print(report)

#Classification Report:
#              precision    recall  f1-score   support

#           0       0.75      0.78      0.76       400
#           1       0.77      0.74      0.75       400

#    accuracy                           0.76       800
#   macro avg       0.76      0.76      0.76       800
#weighted avg       0.76      0.76      0.76       800

#%% Confusion matrix

# A confusion matrix is a way to visualize the performance of a model. And more importantly, we can easily see where the model fails exactly.

class_names = model.classes_
print(class_names)

# Compute the confusion matrix
cm = confusion_matrix(y_true = y_test, y_pred = y_test_pred)

# Create the ConfusionMatrixDisplay
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels = class_names)

# Plot the confusion matrix
disp.plot()

# Save the plot as a PNG file
#plt.savefig('D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230627_XGB/20230627_confusion_matrix.png', dpi=300, bbox_inches='tight')

#%% Conventional variable importance 

# Get feature importance
importances = model.feature_importances_

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

#plt.savefig("D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230627_XGB/20230627_varImp_classi_exp.png", dpi=300, bbox_inches='tight')
plt.show()

#%% SHAP values 

explainer = shap.TreeExplainer(model) 
# This line creates a TreeExplainer object from the shap package,
# which is used to explain the predictions of tree-based models.
# It takes the trained model (model) as input.

shap_values = explainer.shap_values(X) #X are all predictors (before the train/ test split)
# This line computes the Shapley values for the given predictors X.
# The shap_values variable will contain the Shapley values for each predictor variable in X.
# The X should contain all the predictors before the train/test split, as you correctly mentioned.

#print(shap_values)

#%% Most important predictor based on Shapley values 

print(shap_values.shape) # (4000, 23)
# 4000 rows, 23 columns 
# 23 predictors (each predictor has a column)
# 4000 rows => 4000 data points

# Get the index of the most important predictor for each row
# find the index of the predictor with the highest absolute Shapley value for each row in shap_values.
most_important_predictor_index = np.argmax(np.abs(shap_values), axis=1)

# Get the corresponding predictor names
predictor_names = X.columns

# Get the most important predictor for each row
most_important_predictor_per_row = predictor_names[most_important_predictor_index]

#%% (A) SHAP Summary Plot — Global Interpretability

# A variable importance plot lists the most significant variables in descending order.
# The top variables contribute more to the model than the bottom ones and thus have high predictive power.

#print(shap_values[1])
# second row

summary_bar_plot = plt.figure()

shap.summary_plot(shap_values, X, plot_type="bar")

# save plot
#summary_bar_plot.savefig('D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230627_XGB/20230627_shap_summary_barplot.png', dpi=300)

#%% SHAP Summary Plot

summary_fig = plt.figure()

shap.summary_plot(shap_values, X)

# Save the plot as a PNG file
#summary_fig.savefig('D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230627_XGB/20230627_shap_summary_plot.png', dpi=300, bbox_inches='tight')

#%% SHAP dependence plot var1

# Create the dependence plot
fig, ax = plt.subplots()

# highest-ranked feature (SHAP)
shap.dependence_plot("agriculture_proximity",  shap_values = shap_values, features = X, interaction_index = None, ax = ax, show = False)

fig.savefig('D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230627_XGB/20230627_ag_dependence_fig2.png', dpi=300, bbox_inches='tight')

# now it worked!!

#%% SHAP dependence plot SPEI_1year

# Create the dependence plot
fig2, ax2 = plt.subplots()

# highest-ranked feature (SHAP)
shap.dependence_plot("SPEI_1year",  shap_values = shap_values, features = X, interaction_index = None, ax = ax2, show = False)

fig2.savefig('D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230627_XGB/20230627_SPEI_1year_dependence_fig.png', dpi=300, bbox_inches='tight')

#%% SHAP dependence plot SSM_sameyear

# Create the dependence plot
fig3, ax3 = plt.subplots()

# highest-ranked feature (SHAP)
shap.dependence_plot("SSM_sameyear",  shap_values = shap_values, features = X, interaction_index = None, ax = ax3, show = False)

fig3.savefig('D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230627_XGB/20230627_SSM_sameyear_dependence_fig.png', dpi=300, bbox_inches='tight')

#%% SHAP dependence plot TCD

# Create the dependence plot
fig3, ax4 = plt.subplots()

# highest-ranked feature (SHAP)
shap.dependence_plot("TCD",  shap_values = shap_values, features = X, interaction_index = None, ax = ax4, show = False)

fig3.savefig('D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230627_XGB/20230627_TCD_dependence_fig.png', dpi=300, bbox_inches='tight')

#%% SHAP dependence plot canopyheight

# Create the dependence plot
fig3, ax5 = plt.subplots()

# highest-ranked feature (SHAP)
shap.dependence_plot("canopyheight",  shap_values = shap_values, features = X, interaction_index = None, ax = ax5, show = False)

fig3.savefig('D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230627_XGB/20230627_canopyheight_dependence_fig.png', dpi=300, bbox_inches='tight')
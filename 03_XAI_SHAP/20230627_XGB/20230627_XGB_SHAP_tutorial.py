# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 14:47:58 2023

@author: Stenka Vulova
"""

# Census income classification with XGBoost
# https://shap.readthedocs.io/en/latest/example_notebooks/tabular_examples/tree_based_models/Census%20income%20classification%20with%20XGBoost.html
# going through this example to better understand Shapley values 

#%% Libraries 

from sklearn.model_selection import train_test_split
import xgboost
import shap
import numpy as np
import matplotlib.pylab as pl

# print the JS visualization code to the notebook
shap.initjs()

#%% Load dataset 

X,y = shap.datasets.adult()
X_display,y_display = shap.datasets.adult(display=True)

# create a train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)
d_train = xgboost.DMatrix(X_train, label=y_train)
d_test = xgboost.DMatrix(X_test, label=y_test)

#%% Train the model 

params = {
    "eta": 0.01,
    "objective": "binary:logistic",
    "subsample": 0.5,
    "base_score": np.mean(y_train),
    "eval_metric": "logloss"
}
model = xgboost.train(params, d_train, 5000, evals = [(d_test, "test")], verbose_eval=100, early_stopping_rounds=20)

#%% Classic feature attributions 

# Here we try out the global feature importance calcuations that come with XGBoost.
# Note that they all contradict each other, which motivates the use of SHAP values
# since they come with consistency gaurentees (meaning they will order the features correctly).

xgboost.plot_importance(model)
pl.title("xgboost.plot_importance(model)")
pl.show()

xgboost.plot_importance(model, importance_type="cover")
pl.title('xgboost.plot_importance(model, importance_type="cover")')
pl.show()

xgboost.plot_importance(model, importance_type="gain")
pl.title('xgboost.plot_importance(model, importance_type="gain")')
pl.show()

#%% Explain predictions

# Here we use the Tree SHAP implementation integrated into XGBoost to explain the entire dataset (32561 samples).
# For training, only 26048 samples were used. 

# this takes a minute or two since we are explaining over 30 thousand samples in a model with over a thousand trees
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

#%% Visualize a single prediction

#Note that we use the “display values” data frame so we get nice strings instead of category codes.

shap_values[0,:] # first tow 

shap.force_plot(explainer.expected_value, shap_values[0,:], X_display.iloc[0,:], matplotlib= True)

#%% Visualize many predictions

# Try 10 

shap.force_plot(explainer.expected_value, shap_values[:1000,:], X_display.iloc[:1000,:], show = True)
# does NOT work

#%% Bar chart of mean importance 

#This takes the average of the SHAP value magnitudes across the dataset and plots it as a simple bar chart.

shap.summary_plot(shap_values, X_display, plot_type="bar")

#%% SHAP Summary Plot

shap.summary_plot(shap_values, X)

#%% SHAP Dependence plots 

for name in X_train.columns:
    shap.dependence_plot(name, shap_values, X, display_features=X_display)



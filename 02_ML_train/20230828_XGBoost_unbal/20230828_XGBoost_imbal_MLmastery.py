# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 11:06:50 2023

@author: Stenka Vulova

Testing this code:
https://machinelearningmastery.com/xgboost-for-imbalanced-classification/ 

"""


#%% Import libraries

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

# ML libraries 

from xgboost import XGBClassifier

from sklearn.metrics import recall_score, precision_score, f1_score, accuracy_score, roc_auc_score, classification_report, make_scorer
from sklearn.model_selection import train_test_split, cross_validate, cross_val_predict
from sklearn.preprocessing import LabelEncoder

# for this tutorial
from sklearn.datasets import make_classification
from collections import Counter

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold

#%% Imbalanced Classification Dataset

# first define an imbalanced classification dataset.
# can use the make_classification() scikit-learn function to define a synthetic imbalanced two-class classification dataset. 
# We will generate 10,000 examples with an approximate 1:100 minority to majority class ratio.

# define dataset
X, y = make_classification(n_samples=10000, n_features=2, n_redundant=0,
	n_clusters_per_class=2, weights=[0.99], flip_y=0, random_state=7)

#%% Explore dataset 

# summarize class distribution
counter = Counter(y)
print(counter)

# Counter({0: 9900, 1: 100})

# Scatter plot of examples by class label
for label, _ in counter.items():
    row_ix = np.where(y == label)[0]
    plt.scatter(X[row_ix, 0], X[row_ix, 1], label=str(label))
plt.legend()
plt.show()

#%% Define model 

# define model
model = XGBClassifier()

# define evaluation procedure
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)

#%% Evaluate model 

# evaluate model
scores = cross_val_score(model, X, y, scoring='roc_auc', cv=cv, n_jobs=-1)
# summarize performance
print('Mean ROC AUC: %.5f' % np.mean(scores))

# Mean ROC AUC: 0.96052


#%% Get accuracy per class

# Split the data into training and testing sets using train_test_split
# 'test_size specifies the proportion of the dataset to include in the test split.
# By setting stratify=y, the train_test_split() function will ensure that the class distribution in both the training and testing sets is similar to the original distribution in y.
# This helps maintain the same ratio of the two classes.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20, stratify=y)

model.fit(X_train, y_train)

# Use the trained model to make predictions on the test set
y_pred = model.predict(X_test)

report = classification_report(y_test, y_pred)

# The classification_report function provides precision, recall, F1-score, and support for each class.

print("Classification Report:")
print(report)

#               precision    recall  f1-score   support

 #          0       0.99      1.00      1.00      2970
#           1       0.73      0.27      0.39        30

#    accuracy                           0.99      3000
 #  macro avg       0.86      0.63      0.69      3000
#weighted avg       0.99      0.99      0.99      3000

# 1 is the minority class. 

#%% Estimate scale_post_weight 

# estimate a value for the scale_pos_weight xgboost hyperparameter

# count examples in each class

# estimate scale_pos_weight value
estimate = counter[0] / counter[1]
print('Estimate: %.3f' % estimate)
# Estimate: 99.000

#%%  Model with scale_pos_weight set

# Set parameter max_delta_step to a finite number (say 1) to help convergence
# xgboost with imbalanced data:
# https://xgboost.readthedocs.io/en/stable/tutorials/param_tuning.html

# define model
model2 = XGBClassifier(scale_pos_weight=99, max_delta_step = 1)


# define evaluation procedure
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)

# evaluate model
scores = cross_val_score(model2, X, y, scoring='roc_auc', cv=cv, n_jobs=-1)
# summarize performance
print('Mean ROC AUC: %.5f' % np.mean(scores))
# Mean ROC AUC: 0.95532

#%% Get accuracy per class pt. 2

model2.fit(X_train, y_train)

# Use the trained model2 to make predictions on the test set
y_pred2 = model2.predict(X_test)

report = classification_report(y_test, y_pred2)

# The classification_report function provides precision, recall, F1-score, and support for each class.

print("Classification Report:")
print(report)

#Classification Report:
#              precision    recall  f1-score   support

#           0       0.99      1.00      1.00      2970
#           1       0.52      0.37      0.43        30

#    accuracy                           0.99      3000
#   macro avg       0.76      0.68      0.71      3000
#weighted avg       0.99      0.99      0.99      3000
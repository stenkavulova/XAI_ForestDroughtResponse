# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 10:30:38 2023

@author: Stenka Vulova
"""

# This is more understandable.
# I will first write out the code here; but I will actually run it on the HPC> 

#%% Libraries

import pandas as pd  
import math  
import os  
import multiprocessing
from itertools import repeat

#import shap
from datetime import datetime
import fasttreeshap

from xgboost import XGBClassifier

import joblib # save/load the trained model 
# import pickle (Hanyu used it instead of joblib)

#%% Prepare larger dataset for Shapley values

# I want to map Shap values
# They should be mapped for all coordinates with these 2 classes
# Not just the reduced dataset used for training

#df_all = pd.read_csv("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240216_HPC_test2_Katharina/X_top10_2019_onefourth.csv")

#df_all.shape
# Number of rows: 2609361
# Number of columns: 41

# (2609361, 41)

#%% Hanyu way of importing

    # Read the data from a CSV file into a pandas DataFrame
#name = 'X_train'  # Define the name of the data file to be processed
#df = pd.read_csv(name + '.csv')

os.getcwd()
# 'C:\\Users\\Stenka Vulova'

os.chdir("E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_SHAP_2020_new")

os.getcwd()

name = 'X_all_2020'  # Define the name of the data file to be processed
df = pd.read_csv(name + '.csv') # it works!

#%% test model import

#model = joblib.load('model_100K_all_years.pkl')
# no need for this, model loaded in a later step

#%% Function divide_data

def divide_data(df, name, num_parts):
    # Function definition begins. This function divides a DataFrame into multiple parts.

    num_rows = len(df)  # Number of rows in the DataFrame
    rows_per_part = math.ceil(num_rows / num_parts)  # Calculate rows per part, rounding up if needed

    # Divide the DataFrame into parts based on the specified number of parts
    df_parts = [df[i * rows_per_part : (i + 1) * rows_per_part] for i in range(num_parts - 1)]
    df_parts.append(df[(num_parts - 1) * rows_per_part:])  # Add the remaining rows to the last part

    # Save each divided part of the DataFrame to separate CSV files
    for i, df_part in enumerate(df_parts):
        df_part_name = name + f"_part_{i+1}"  # Construct the name for each part
        df_part.to_csv(f"{df_part_name}.csv", index=False)  # Save the part to a CSV file without the index

#%% Function combine_data

def combine_data(name):
    # Function definition to combine multiple CSV files into one DataFrame and save it as a CSV file.

    folder_path = os.getcwd()  # Get the current working directory
    csv_files = [file for file in os.listdir(folder_path) if file.startswith(name) and file.endswith('.csv')]
    csv_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))  # Sorting CSV files numerically by their indices

    concatenated_df = pd.DataFrame()  # Initialize an empty DataFrame to concatenate individual DataFrames

    # Iterate through CSV files, read each one, and concatenate its content to the main DataFrame
    for file in csv_files:
        file_path = os.path.join(folder_path, file)  # Get the full path of the CSV file
        df = pd.read_csv(file_path)  # Read the CSV file into a DataFrame
        concatenated_df = pd.concat([concatenated_df, df])  # Concatenate the DataFrame content

    file_name = name + '.csv'  # Set the name for the combined CSV file
    file_path = os.path.join(folder_path, file_name)  # Get the full path for the combined CSV file

    # Save the concatenated DataFrame to a new CSV file without including the index
    concatenated_df.to_csv(file_path, index=False)

# The commented-out section runs the 'combine_data' function when the script is executed as the main program
# Uncomment the lines to enable direct execution of the 'combine_data' function

# if __name__ == '__main__':
#     combine_data('train_df_part')

#%% Function process_data

# Define a function named process_data that takes 'name' and 'i' as parameters
def process_data(name, i):
    # Read the input data from a CSV file based on 'name' and 'i'
    X_input = pd.read_csv(name + '_part_{}.csv'.format(i))

    model = joblib.load('E:/Data/Vulova/Topic_1/04_PROCESSED_DATA/20240415_SHAP_2020_new/model_100K_allyears_20240415.pkl')
    # Load the trained model from a pickle file
#    with open('model.pkl', 'rb') as file:
 #       model = pickle.load(file)

    # Initialize a TreeExplainer object for computing SHAP values using a fast implementation
    explainer = fasttreeshap.TreeExplainer(model, algorithm='v2', n_jobs=-1, memory_tolerance=30)

    # Compute SHAP values for the input data
    shap_values = explainer.shap_values(X_input, check_additivity = False)

    # Extract SHAP values related to the 'fire' class (assuming a binary classification)
    shap_values_fire = shap_values

    # Create a DataFrame from the SHAP values related to the 'fire' class
    shap_values_fire_df = pd.DataFrame(shap_values_fire)

    # Make predictions using the input data
    Y_pred = model.predict(X_input)

    # Create a DataFrame containing the model predictions
    Y_pred_df = pd.DataFrame(Y_pred)

    # Concatenate the prediction DataFrame and SHAP values DataFrame
    merged_df = pd.concat([Y_pred_df, shap_values_fire_df], axis=1)

    # Save the merged DataFrame to a CSV file
    filename = name + '_SHAP_{}.csv'.format(i)
    merged_df.to_csv(filename, index=False)

#%% check the number of cores

# Get the number of CPU cores
#num_cores = multiprocessing.cpu_count()
#print("Number of CPU cores:", num_cores)
# Number of CPU cores: 256

# Don't use the total number of CPU cores.
# Python cannot handle it.

# https://github.com/pycaret/pycaret/issues/38
# Multiprocessing-pool-pool-on-windows-cpu-limit-of-63

# from concurrent.futures import ProcessPoolExecutor

#def f(x):
#    return x

#if __name__ == '__main__':
#    with ProcessPoolExecutor(max_workers=70) as executor:
#        a = list(executor.map(f, range(70)))
#        print(a)

#%% Run the entire script

if __name__ == '__main__':
   
    # Print current time to mark the start of data processing
    current_time = datetime.now()
    print('Start time', current_time)
    
    # Define the number of CPU cores to be used in parallel processing
    num_cores = 60  # Number of CPU cores to utilize
    
    # Display the number of cores
    print("Number of CPU cores:", num_cores)
    
    # # Read the data from a CSV file into a pandas DataFrame
    name = 'X_all_2020'  # Define the name of the data file to be processed
    df = pd.read_csv(name + '.csv')
    
    # # Divide the data into multiple parts for parallel processing
    divide_data(df, name, num_cores)
    del df  # Delete the DataFrame to free up memory
    print('Division completed')
    
    # # Run the 'process_data' function in parallel using multiprocessing Pool
    pool = multiprocessing.Pool(processes=num_cores)  # Create a multiprocessing Pool
    inputs = zip(repeat(name), range(1, num_cores + 1))  # Create input arguments for each process
    pool.starmap(process_data, inputs)  # Execute 'process_data' function in parallel
    pool.close()  # Close the Pool to prevent further tasks
    pool.join()  # Wait for all processes to complete

    # Combine the processed data parts into a single result
    combine_data(name + '_SHAP')  # Combine the processed data files
    print('Combination completed')

    current_time = datetime.now()
    print('shap over', current_time)

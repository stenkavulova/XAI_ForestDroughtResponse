# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 16:42:32 2023

@author: Stenka Vulova
"""

# Now I will re-run the conversion from .xyz files to .tif files for the entire archive.
# The problem with the gaps between tiles is fixed now. 

# I am taking into account that the x and y coordinates of the .xyz files
# are in the center of the pixel of the resulting raster:

#%% Libraries 

import os
import glob
import pandas as pd
import numpy as np
import rasterio as rio
import rasterio.transform as riotrans
import multiprocessing
import time

#%% Load a list of xyz files 

# Each file is in its own folder. 

# You can use the os module to traverse the directory tree and find all the .xyz files in the subfolders.

# set the top-level directory to search in
top_dir = 'D:/Stenka_Cliwac/Topic_1/03_RAW_DATA/20230303_DGM_zip_files'

# define a list to hold the file paths
file_list = []

# This code will search through all the subfolders of top_dir and find all the files that end with .xyz.
# For each file, it will create the full file path by joining the root directory path and the file name,
# and then append that path to the file_list.

# https://stackoverflow.com/questions/16333569/mixed-slashes-with-os-path-join-on-windows

# traverse the directory tree
for root, dirs, files in os.walk(top_dir):
    for file in files:
        if file.endswith('.xyz'):
            # create the full file path and add it to the list
            file_path = os.path.join(root, file).replace("\\","/")
            file_list.append(file_path)
            
print(len(file_list)) # 30520


#%% new functions

# https://geobasis-bb.de/lgb/de/geodaten/3d-produkte/laserscandaten/ 
# EPSG: 25833
CRS='EPSG:25833'

def load_xyz(fn: str) -> pd.DataFrame:
    """
    Loads a xyz data table from disk
    
    Parameters
    ----------
    fn : str
        File name
    """
    #print(f"Loading file: {fn}")
    xyz = pd.read_csv(filepath_or_buffer= fn, delimiter=',', names=['x', 'y', 'z'], index_col=False)
    #print(f"Loaded {len(xyz)} rows from file")
    # To return the xyz variable as a pandas DataFrame, add return xyz at the end of the function.
    return xyz

def xyz2matrix(xyz: pd.DataFrame, cell_size: float) -> (np.ndarray, float, float, float, float):
    """
    Converts the xyz dataframe to a 2d numpy array with origin and bounding box
    """
    # Get grid boundaries
    xmin = np.floor(xyz['x'].min() / cell_size) * cell_size
    xmax = np.ceil(xyz['x'].max() / cell_size) * cell_size
    ymin = np.floor(xyz['y'].min() / cell_size) * cell_size
    ymax = np.ceil(xyz['y'].max() / cell_size) * cell_size
    
    # Create 2D numpy array
    nrows = int((ymax - ymin) / cell_size)
    ncols = int((xmax - xmin) / cell_size)
    mat = np.zeros((nrows, ncols), dtype=np.float32)
    
    # Fill array with values from xyz
    col_idx = ((xyz['x'] - xmin) / cell_size).astype(int)
    row_idx = ((ymax - xyz['y']) / cell_size).astype(int)
    mat[row_idx, col_idx] = xyz['z']
    
    # Get origin (upper left corner)
    west = xmin + cell_size / 2
    north = ymax - cell_size / 2
    
    # Calculate other coordinates
    south = north - nrows * cell_size
    east = west + ncols * cell_size
    
    return mat, west, south, east, north

def matrix2raster(fn_out:str, arr: np.ndarray, west: float, south: float, east: float, north: float, cell_size: float):

    transform = riotrans.from_bounds(
        west=west - cell_size / 2, south=south - cell_size / 2,
        east=east + cell_size / 2, north=north + cell_size / 2,
        width=arr.shape[1] + 1,
        height=arr.shape[0] + 1
    )
    
    with rio.open(
        fn_out, 'w', 
        driver='GTiff',
        height= arr.shape[0] + 1, width = arr.shape[1] + 1,
        count=1, dtype=str(arr.dtype),
        crs=CRS, transform=transform, compress='lzw'
    ) as raster:
        raster.write(arr, 1)

def process(file_path:str, output_dir:str, cell_size:float):
    print(f'Processing {file_path}')
    file_name = os.path.basename(file_path)
    output_path = os.path.join(output_dir, file_name.replace('.xyz', '.tif'))
    xyz = load_xyz(file_path)
    mat, west, south, east, north = xyz2matrix(xyz, cell_size)
    matrix2raster(output_path, mat, west, south, east, north, cell_size)
    print(f'Finished processing {file_path}')
    

#%%  Loop 

for file_name in file_list:
    process(file_name, output_dir = "D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230304_DEM_raster_tiles", cell_size = 1.0)

# It worked! And now there is no gap between the tiles : ) 
# Now they overlap with 1 pixel (1 m). Interesting! 
# I hope this is correct. Certainly looks good on QGIS ; ) 
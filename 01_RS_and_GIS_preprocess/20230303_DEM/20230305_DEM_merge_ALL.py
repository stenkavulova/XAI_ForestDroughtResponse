# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 12:40:40 2023

@author: Stenka Vulova
"""


#%% Libraries

import sys
import os
import multiprocessing
import time
import pandas as pd
import numpy as np
import rasterio as rio
from rasterio import transform as riotrans

from pathlib import Path
from rasterio.plot import show

#%% Merge function 

# https://geobasis-bb.de/lgb/de/geodaten/3d-produkte/laserscandaten/ 
# EPSG: 25833
CRS='EPSG:25833'

def merge(outfile, *in_files):
    """
    Merges in_files (*.tif) to outfile
    """
    from rasterio.merge import merge as rmerge
    t0 = time.time()
    rasters = [rio.open(fn) for fn in in_files]
    t1 = time.time() -t0
    print(f'{t1:0.1f}s : Merging {len(rasters)} rasters')
    arr, transform = rmerge(rasters)
    t2 = time.time() - t0
    print(f'{t2:0.1f}s : Save {arr.shape[1]} x {arr.shape[2]} raster to {outfile}')
    with rio.open(
        outfile, 'w', 
        driver='GTiff',
        height= arr.shape[1], width = arr.shape[2],
        count=arr.shape[0], dtype=str(arr.dtype),
        crs=CRS, transform=transform, 
        compress='lzw', num_threads=os.cpu_count()
    ) as raster:
        raster.write(arr)
    t3 = time.time() - t0
    print(f'{t3:0.1f}s : Done')
    
    
#%% Iterate over tif files 
#import os

# Set the folder path
folder_path = 'D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230304_DEM_raster_tiles/'

# Get a list of all .tif files in the folder
tif_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.tif')]

print(len(tif_files)) # 30520

#%% Merge
# Call the merge function

merge('D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230304_DEM_raster_tiles/DEM_mosaic/DEM_mosaic_Brandenburg.tif', *tif_files)

# MemoryError: Unable to allocate 214. GiB for an array with shape (1, 246001, 234001) and data type float32
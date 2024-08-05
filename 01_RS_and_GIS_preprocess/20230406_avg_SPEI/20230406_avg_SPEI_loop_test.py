# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 22:20:31 2023

@author: Stenka Vulova
"""

# Annual means of SPEI (over each pixel)
# looping over several years

#%% Libraries

import rasterio
import glob
import numpy as np

#%% Loop

# loop over a list of years
for year in range(1991, 2023): # the latter number in range() is not included

    # the f before the string indicates that it is a formatted string
    # the variable name is enclosed in curly braces {}.
    tif_files = glob.glob(f'D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230405_SPEI/SPEI_{year}*.tif')

    def read_file(file):
        with rasterio.open(file) as src:
            return(src.read(1, masked = True))

    # Read all data as a list of numpy arrays 
    array_list = [read_file(x) for x in tif_files]
    print(array_list)

    # Compute the arithmetic mean along the specified axis
    array_out = np.mean(array_list, axis=0)

    # Get metadata from one of the input files
    with rasterio.open(tif_files[0]) as src:
        meta = src.meta

    with rasterio.open(f'D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230406_SPEI_annual_avg/SPEI_mean_{year}.tif', 'w', **meta) as dst:
        dst.write(array_out.astype(rasterio.float32), 1)

# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 22:25:21 2023

@author: Stenka Vulova
"""


#%% Libraries

import rasterio
import numpy as np
import glob

#%% Input and output directories

# Define input and output directories
input_dir = 'D:/Stenka_Cliwac/Topic_1/03_RAW_DATA/20230316_MODIS_NDVI_cloudmasked'
output_dir = 'D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230319_scaled_MODIS_NDVI'

# Load list of tif files
tif_files = glob.glob(input_dir + '/*.tif')
print(len(tif_files))

#%%  Loop

# Loop through each file and multiply by 0.0001
for tif_file in tif_files:
    # Open raster and read as numpy array
    with rasterio.open(tif_file) as src:
        data = src.read(1)

        # Multiply by 0.0001
        data_scaled = data * 0.0001

        # Update the profile to set the new data type and nodata value
        profile = src.profile.copy()
        profile.update(dtype=rasterio.float32, nodata=-0.9999)

        # Save the new raster to file
        output_file = output_dir + '/' + tif_file.split('\\')[-1].split('.')[0] + '_scale.tif'
        with rasterio.open(output_file, 'w', **profile) as dst:
            dst.write(data_scaled, 1)

# it worked! All the files are saved and successfully re-scaled. 

# loop through each .tif file in the input directory
# multiply it by 0.0001
# set the nodata value to -0.9999
# save the new raster to the output directory with '_scale.tif' appended to the original file name.
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 15:48:46 2023

@author: Stenka Vulova
"""

# I am using tree cover density (TCD) > 50% as my forest mask
# Now I want to test assigning NAN to a NDVI raster based on the TCD > 50 %.
# The rasters are already coregistered.
# If one raster ("TCD") has "nan", the other raster ("NDVI") should also be assigned "nan" at that pixel. 

#%% Libraries

import os
import glob
import rasterio
import numpy as np

import earthpy as et
import earthpy.plot as ep

#%% Open TCD raster

# Open the TCD raster and read its data
with rasterio.open('D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230327_TCD_1km/TCD_1km_over50.tif') as src_tcd:
    tcd = src_tcd.read(1)
    
ep.plot_bands(tcd)

#%% List of NDVI anomaly files 

# Get a list of all NDVI files in the folder
ndvi_files = glob.glob('D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230321_MODIS_NDVI_anomaly/*.tif')

print(ndvi_files)
print(len(ndvi_files)) # 6

ndvi_test = ndvi_files[0]
file_base = os.path.splitext(os.path.basename(ndvi_test))[0]
print(file_base)
out_path = os.path.join("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230327_MODIS_NDVI_anom_forest/", file_base + '_forest.tif')
print(out_path)

#%% Loop 

output_dir = "D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230327_MODIS_NDVI_anom_forest/"

for ndvi_file in ndvi_files:
    # Open the NDVI raster and read its data
    with rasterio.open(ndvi_file) as src_ndvi:
        ndvi = src_ndvi.read(1)
        profile = src_ndvi.profile.copy()

    # Set the NaN values in ndvi to NaN where tcd is NaN
    ndvi[np.isnan(tcd)] = np.nan
    
    file_base = os.path.splitext(os.path.basename(ndvi_file))[0]
    out_path = os.path.join(output_dir, file_base + '_forest.tif')

    # Save the new raster to file
    with rasterio.open(out_path, 'w', **profile) as dst:
        dst.write(ndvi, 1)
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 12:07:48 2023

@author: Stenka Vulova
"""

# Load the raster
# 10-m resolution. I will resample the DEM to it.

#%% Libraries

import rasterio
import glob
import os
from rasterio.warp import reproject, Resampling

#%% Load TCD

# Load the raster 
# 10-m resolution. I will resample the DEM to it. 
TCD = rasterio.open("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_TCD_mosaic/TCD_EPSG4326.tif")

# Check the CRS
print(TCD.crs) # EPSG:4326

# Now I will read in DEM tiles (1-m resolution and different CRS from TCD).
# The goal is to project them to the resolution and CRS of TCD.

#%% DEM tiles 

# specify the directory where your .tif files are located
dir_path = "D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230305_DEM_mosaic_1K"

# use glob to get a list of all .tif files in the directory
tif_files = glob.glob(dir_path + "/*.tif")

# initialize an empty list to store the raster data
raster_list = []

# use a loop to read each file and store it in the list

for file in tif_files:
    with rasterio.open(file) as src:
        raster_list.append(src)
        
#%% Function to reproject 

# function to reproject and save raster
def reproject_and_save(x, y, output_dir):
    
    # project the raster based on another raster
    with y as tcd:
        transform, width, height = reproject(
            x, 
            dst_crs=tcd.crs,
            dst_transform=tcd.transform,
            dst_resolution=tcd.res[0],
            resampling=Resampling.bilinear # Better suited to continuous data (bilinear resampling)
        )
    
    # extract the file name without extension
    name = os.path.splitext(os.path.basename(x.name))[0]
    
    # save the projected raster to the output directory with the original file name
    with rasterio.open(
        output_dir + '/' + name + '.tif', 
        'w', 
        driver='GTiff', 
        height=height, 
        width=width, 
        count=1, 
        dtype=x.dtypes[0], 
        crs=tcd.crs, 
        transform=transform
    ) as dst:
        dst.write(x.read(1), 1)
        
#%% Test for 1 raster 

# example usage of the function for the first raster in the list
reproject_and_save(raster_list[0], TCD, "D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230306_DEM_bigtiles_10m")

#%% Loop

# Now I will run the function for a list of rasters.
# Each raster is reprojected to TCD, and then saved.

for raster in raster_list:
    reproject_and_save(raster, TCD, "D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230306_DEM_bigtiles_10m")

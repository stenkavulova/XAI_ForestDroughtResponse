# -*- coding: utf-8 -*-
"""
Created on Mon 7 March 2023

@author: Stenka Vulova
"""

# I generated DEMs downscaled to 10-m (matching tree canopy cover resolution and CRS) using R>
# Now I will test mosaicing them. 

# Reference code: the older code "20230305_merge_1K_to_2K.py" 


#%% Libraries

import os
import time
import glob
import rasterio as rio
from rasterio.merge import merge as rmerge


#%% Input and output directories

# List all .tif files in the folder
tif_files = glob.glob("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230307_DEM_bigtiles_10m/*.tif")

# Subset which of the tiles to merge
#tif_files = tif_files[0:2]
# Not needed, only 2 files

print(len(tif_files)) # 30

# Define the output file name
out_file = "D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230307_DEM_10m_mosaic/DEM_mosaic_10m_Brandenburg.tif"


#%% Check NA value 

print(tif_files[1])

with rio.open(tif_files[1]) as src:
    nodata = src.nodata
    print(f"Nodata value: {nodata}") 

# This will print out the nodata value of the raster. If the nodata value is not set, nodata will be None.
# Nodata value: nan
# That's good. 

#%% Merge with timer 

# Time how long it takes to merge the files
start_time = time.time()

# Open all the files and add them to a list of rasterio datasets
rasters = [rio.open(fn) for fn in tif_files]

# Merge the rasters using rasterio's merge function
arr, transform = rmerge(rasters, nodata = float('nan') )

# Write the output raster to disk
with rio.open(out_file, 'w', 
              driver='GTiff',
              height=arr.shape[1], width=arr.shape[2],
              count=arr.shape[0], dtype=str(arr.dtype),
              crs=rasters[0].crs, transform=transform, nodata = float('nan'), 
              compress='lzw', num_threads=os.cpu_count()) as dst:
    dst.write(arr)

# Time how long it took to merge the files
end_time = time.time()

elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds") 
# This code will print the elapsed time in seconds to the console after the merge operation is completed.


# 30 tiles
# 1 GB
# Elapsed time: 531.68 seconds (~9 minutes)
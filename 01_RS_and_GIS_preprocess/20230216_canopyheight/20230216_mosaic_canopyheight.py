# -*- coding: utf-8 -*-
"""
Mosaic canopy height 

Created on Thu Feb 16 14:46:18 2023

@author: Stenka Vulova
"""

# https://automating-gis-processes.github.io/CSC18/lessons/L6/raster-mosaic.html

#%% Libraries

# Let’s start by importing required modules and functions.

import rasterio
from rasterio.merge import merge
from rasterio.plot import show 
import glob 
import os 

#%% import tif files 

# As there are many tif files in our folder, it is not really pracical to start listing them manually.
# Luckily, we have a module and function called glob that can be used to create a list of those files that we are interested in based on search criteria.

# File and folder paths

dirpath = r"D:\Stenka_Cliwac\Topic_1\03_RAW_DATA\canopyheight_10m"

out_fp = r"D:\Stenka_Cliwac\Topic_1\04_PROCESSED_DATA\20230216_canopyheight\canopyheight_mosaic.tif"

# Make a search criteria to select the files

search_criteria = "*.tif"

q = os.path.join(dirpath, search_criteria)

print(q)

#%% files in a list 

# Now we can see that we have a search criteria (q) that we can pass to glob function.

# List all dem files with glob() function

dem_fps = glob.glob(q)

dem_fps

# Great! Now we have the 2 files in a list and we can start to make a mosaic out of them.

# Let’s first create an empty list for the datafiles that will be part of the mosaic.

src_files_to_mosaic = [] # empty list 

# Now we open all those files in read mode with rasterio
# and add those files into a our source file list.

for fp in dem_fps:
    src = rasterio.open(fp)
    src_files_to_mosaic.append(src)
    
src_files_to_mosaic

# Okey, now we can see that we have a list full of open raster objects.

#%% Merge

# Now it is really easy to merge those together and create a mosaic with rasterio’s merge function.

# Merge function returns a single mosaic array and the transformation info

mosaic, out_trans = merge(src_files_to_mosaic)

# Let’s check that it looks okey.

show(mosaic, cmap="terrain")

type(mosaic) # numpy.ndarray

mosaic.crs
# AttributeError: 'numpy.ndarray' object has no attribute 'crs'

#%% Copy metadata 

# Great, it looks correct! Now we are ready to save our mosaic to disk.
# Let’s first update the metadata with our new dimensions, transform and CRS

# original metadata
src.meta 
#{'driver': 'GTiff',
 #'dtype': 'uint8',
# 'nodata': 255.0,
# 'width': 36000,
 #'height': 36000,
 #'count': 1,
 #'crs': CRS.from_epsg(4326),
# 'transform': Affine(8.333333333333333e-05, 0.0, 12.0,
 #       0.0, -8.333333333333333e-05, 54.0)}

# Copy the metadata

out_meta = src.meta.copy()
out_meta

# Update the metadata
out_meta.update( { "driver": "GTiff",
                  "height": mosaic.shape[1],
                  "width": mosaic.shape[2],
                  "transform": out_trans
    })

out_meta
# width changed compared to src.meta 

#%% Save mosaic 

# Finally we can write our mosaic to our computer

# Write the mosaic raster to disk

#with rasterio.open(out_fp, "w", **out_meta) as dest:
#    dest.write(mosaic)
    
# it worked!

src.crs
# CRS.from_epsg(4326)
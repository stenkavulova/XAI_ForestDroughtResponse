# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 14:18:21 2023

@author: Stenka Vulova
"""

# I want to mask all of the P rasters to the Brandenburg with a 5 km buffer now.  

# https://rasterio.readthedocs.io/en/latest/topics/masking-by-shapefile.html 

#%% Libraries

#Using rasterio with fiona, it is simple to open a shapefile,
# read geometries, and mask out regions of a raster
# that are outside the polygons defined in the shapefile.

import fiona
import rasterio
import rasterio.mask

import rasterio.plot
import matplotlib as mpl
from descartes import PolygonPatch

# import multiple tif files 
import os 
import glob

#%% Open Brandenburg shapefile 

with fiona.open("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_Brandenburg_border/5km_buffer/BB_5km_buffer_EPSG31467.shp", "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

#type(shapes) # list
print(len(shapes)) # 1

# shapes is 1 element long

#%% List of P files 

# Get a list of all .asc files in the folder
P_files = glob.glob('D:/Stenka_Cliwac/Topic_1/03_RAW_DATA/20230330_P_DWD_grids/*.asc')

print(P_files)
print(len(P_files)) # 384


#%% Test name for saving

# I am trying to create a file name for saving the cropped raster
# _BB refers to Brandenburg. 

P_test = P_files[0]
file_base = os.path.splitext(os.path.basename(P_test))[0]
print(file_base)
# grids_germany_monthly_evapo_p_201808

out_path = os.path.join("D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230330_crop_P/loop_test/", file_base + '_BB.tif')
print(out_path)
# Looks good! 


#%% Check out metadata

# Why is the CRS not being saved?

with rasterio.open(P_test) as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True) # mask 
    out_meta = src.meta
    
print(out_meta)
# 'crs': None
# it wasn't defined in the .asc files originally.


#%% Loop 

output_dir = "D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230330_P_DWD_grids_cropped/"

for P_file in P_files:
    # Open the P raster and read its data
    
    with rasterio.open(P_file) as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True) # mask / crop
        out_meta = src.meta

# update the medata before saving the cropped raster
    out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform,
                 "crs": "EPSG:31467"}) # add the CRS 
    
    file_base = os.path.splitext(os.path.basename(P_file))[0]
    out_path = os.path.join(output_dir, file_base + '_BB.tif')

    with rasterio.open(out_path, "w", **out_meta) as dest:
        dest.write(out_image)


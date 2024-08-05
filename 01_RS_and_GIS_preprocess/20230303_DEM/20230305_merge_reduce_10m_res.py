# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 18:51:53 2023

@author: Stenka Vulova
"""

# To mosaic 1000 tiles and then reduce the resolution to 10-m before saving them.
    
#%% Libraries

import os
import glob
import rasterio as rio
from rasterio.merge import merge
from rasterio.warp import calculate_default_transform, reproject, Resampling

#%% Directories

# Set the output filename and directory
out_dir = 'D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230305_DEM_mosaic'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
out_file = os.path.join(out_dir, 'mosaic.tif')

# Get a list of all .tif files in the input directory
in_dir = 'D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230304_DEM_raster_tiles'
tif_files = glob.glob(os.path.join(in_dir, '*.tif'))

#%% Loop 

# Mosaic 1000 tiles at a time
batch_size = 1000

# try with 2 first
for i in range(0, 2, batch_size):
    # Get the current batch of files
    current_files = tif_files[i:i+batch_size]
    
    # Open the current batch of files
    src_files_to_mosaic = [rio.open(src_file) for src_file in current_files]
    
    # Merge the current batch of files
    mosaic, out_trans = merge(src_files_to_mosaic)
    
    # Calculate the new resolution and shape for the output mosaic
    out_res = (out_trans[0], out_trans[4])
    out_width = int((mosaic.shape[2] * out_trans[0]) / 10)
    out_height = int((mosaic.shape[1] * abs(out_trans[4])) / 10)
    out_shape = (mosaic.shape[0], out_height, out_width)
    
    # Reproject the mosaic to the new resolution and shape
    out_data = rio.zeros(out_shape, dtype=mosaic.dtype)
    out_trans = rio.transform.from_bounds(*out_trans[0:4], out_width, out_height)
    reproject(
        mosaic,
        out_data,
        src_transform=out_trans,
        src_crs='EPSG:4326',
        dst_transform=out_trans,
        dst_crs='EPSG:4326',
        resampling=Resampling.bilinear)
    
    # Save the output mosaic to a new file
    out_file_i = os.path.join(out_dir, f'mosaic_{i//batch_size}.tif')
    with rio.open(out_file_i, 'w', driver='GTiff',
                  width=out_width, height=out_height,
                  count=out_shape[0], dtype=out_data.dtype,
                  crs='EPSG:4326', transform=out_trans) as dst:
        dst.write(out_data)

# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 21:01:44 2023

@author: Stenka Vulova
"""

#%% Libraries

import rasterio
import numpy as np
import matplotlib.pyplot as plt

#%% Open raster file 

# https://pygis.io/docs/e_raster_math.html

# Open raster and plot
raster_a = rasterio.open('D:/Stenka_Cliwac/Topic_1/03_RAW_DATA/20230316_MODIS_NDVI_cloudmasked/2022-08-13_MODIS_NDVI.tif').read(1)
plt.imshow(raster_a, cmap = "BrBG")
plt.title("MODIS NDVI (original)")
plt.show()

#with rasterio.open('D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230319_preproc_MODIS/20220813_NDVI_NAN.tif', 'w', **profile) as dst:
 #   dst.write(data, 1)

# View raster values
print(raster_a)

#%% Multiply raster by a constant 

# Get product
product_a = raster_a * 0.0001

# Plot raster
plt.imshow(product_a, cmap = "BrBG")
plt.title("Re-scaled NDVI")
plt.show()

#%% Save result

# Open the original raster to use its metadata
with rasterio.open('D:/Stenka_Cliwac/Topic_1/03_RAW_DATA/20230316_MODIS_NDVI_cloudmasked/2022-08-13_MODIS_NDVI.tif') as src:
    profile = src.profile.copy()

# Update the profile to set the new data type
profile.update(dtype=rasterio.float32)

# Save the new raster to file
with rasterio.open('D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230319_preproc_MODIS/20220813_NDVI_scale1.tif', 'w', **profile) as dst:
    dst.write(product_a, 1)
    dst.nodata = -0.9999

# it worked! 

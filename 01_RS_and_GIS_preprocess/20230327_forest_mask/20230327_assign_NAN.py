# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 15:01:58 2023

@author: Stenka Vulova
"""

# I am using tree cover density (TCD) > 50% as my forest mask
# Now I want to test assigning NAN to a NDVI raster based on the TCD > 50 %.
# The rasters are already coregistered.
# If one raster ("TCD") has "nan", the other raster ("NDVI") should also be assigned "nan" at that pixel. 

import rasterio
import numpy as np

import earthpy as et
import earthpy.plot as ep

#%% Open rasters 

# Open the TCD raster and read its data
with rasterio.open('D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230327_TCD_1km/TCD_1km_over50.tif') as src:
    tcd = src.read(1)

ep.plot_bands(tcd)

# Open the NDVI raster and read its data
with rasterio.open("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230321_MODIS_NDVI_anomaly/NDVI_anomaly_2022.tif") as src:
    ndvi = src.read(1)
    profile = src.profile.copy()

print(profile)

#%%  Set NAN based on TCD

# Set the NaN values in ndvi to NaN where tcd is NaN
ndvi[np.isnan(tcd)] = np.nan

ep.plot_bands(ndvi)

#%%  Save the new raster to file

# Save the new raster to file
with rasterio.open('D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230327_TCD_1km/NDVI_forest_mask/NDVI_anomaly_2022_forest.tif', 'w', **profile) as dst:
    dst.write(ndvi, 1)

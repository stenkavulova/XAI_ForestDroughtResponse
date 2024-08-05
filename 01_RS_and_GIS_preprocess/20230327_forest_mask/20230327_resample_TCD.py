# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 12:02:04 2023

@author: Stenka Vulova
"""

# resample tree cover density (TCD) from 10-m to 1 km

#%% Libraries 

# https://pygis.io/docs/e_raster_resample.html

#Co-registering data is a bit complicated with rasterio
# you need to choose an “reference image” to match the bounds, CRS, and cell size.

from rasterio.warp import reproject, Resampling, calculate_default_transform
import rasterio
from rasterio.plot import show

import geowombat as gw
print(gw.__version__)

import matplotlib.pyplot as plt
fig, ax = plt.subplots(dpi=200)

#%% import TCD raster

TCD = rasterio.open("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_TCD_mosaic/TCD_EPSG4326.tif")

show(TCD)

print(TCD.crs) #  EPSG:4326
print(TCD.nodata)

#%% import MODIS NDVI

#I will resample to it. 

NDVI = rasterio.open("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230321_MODIS_NDVI_anomaly/NDVI_anomaly_2022.tif")

show(NDVI)

print(NDVI.crs) # EPSG:4326

#%%  function to resample 

NDVI = "D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230321_MODIS_NDVI_anomaly/NDVI_anomaly_2022.tif"
TCD = "D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_TCD_mosaic/TCD_EPSG4326.tif"

with gw.config.update(ref_image=NDVI):
    with gw.open(TCD, resampling="bilinear") as src:
        print(src)
        ax.imshow(src.data[0])

        # to write out simply:
        src.gw.to_raster(
             "D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230327_TCD_1km/TCD_1km.tif",
             overwrite=True,
         ) 

# This is taking forever. 
# I have to stop it... Terra R was so much faster. 
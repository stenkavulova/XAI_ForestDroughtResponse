# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 15:40:14 2023

@author: Stenka Vulova
"""

# Crop TCD to include just Berlin & Brandenburg 

# FIRST, I need to change CRS to match.

#%% Libraries 

import os

import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from rasterio.crs import CRS
import rioxarray as rxr
import earthpy as et

from rasterio.plot import show

import rasterio as rio

#%% Import Brandenburg shapefile 

brandenburg = geopandas.read_file("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_Brandenburg_border/20230214_Brandenburg_border.shp")

brandenburg.head()

brandenburg.plot()

brandenburg.crs
# <Geographic 2D CRS: EPSG:4326>

#%% import TCD raster

TCD = rasterio.open("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_TCD_mosaic/TCD_mosaic_Brandenburg.tif")

show(TCD)

print(TCD.crs) # EPSG:3035 


#%% import TCD raster with rxr

# Try rioxarray package 
# https://www.earthdatascience.org/courses/use-data-open-source-python/intro-raster-data-python/raster-data-processing/reproject-raster/

TCD_rxr = rxr.open_rasterio("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_TCD_mosaic/TCD_mosaic_Brandenburg.tif").squeeze()

# Check the CRS
TCD_rxr.rio.crs
# CRS.from_epsg(3035)

#%% Reproject to another CRS

# Create a rasterio crs object for wgs 84 crs - lat / lon
crs_brand = CRS.from_string('EPSG:4326')

# Reproject the data using the crs object

TCD_EPSG4326 = TCD_rxr.rio.reproject(crs_brand)

TCD_EPSG4326.rio.crs
# CRS.from_epsg(4326)

#%% Plot

# Plot your newly converted data
f, ax = plt.subplots(figsize=(10, 4))

TCD_EPSG4326.plot.imshow(ax=ax,
                            cmap='Greys')
brandenburg.plot(ax=ax)
ax.set(title="Brandenburg border and TCD")
ax.set_axis_off()
plt.show()

# Looks good! 

#%% Save reprojected raster 

type(TCD_EPSG4326)
# xarray.core.dataarray.DataArray

TCD_EPSG4326.rio.to_raster("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_TCD_mosaic/TCD_EPSG4326.tif")

#%% Check if saved raster has correct projection

TCD_TEST = rxr.open_rasterio("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_TCD_mosaic/TCD_EPSG4326.tif").squeeze()

TCD_TEST.rio.crs
# CRS.from_epsg(4326)
# Cool, it worked 
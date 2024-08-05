# -*- coding: utf-8 -*-
"""
Reproject the canopy height data 

Created on Thu Feb 16 17:16:34 2023

@author: Stenka Vulova
"""

# Reproject canopy height data so CRS matches the Berlin-Brandenburg polygon 

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

brandenburg = gpd.read_file("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_Brandenburg_border/20230214_Brandenburg_border.shp")

brandenburg.head()

brandenburg.plot()

brandenburg.crs
# <Geographic 2D CRS: EPSG:4326>

#%% import canopyheight raster

canopyheight = rio.open("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230216_canopyheight/canopyheight_mosaic.tif")

show(canopyheight)

#%% check CRS 

print(canopyheight.crs) # EPSG:4326
print(brandenburg.crs)

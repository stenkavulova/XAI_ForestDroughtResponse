# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 14:29:56 2023

@author: Stenka Vulova
"""

# Exclude areas with a TCD value < 50 %

# Tree cover density (TCD) High Resolution Layer (HRL; EEA, 2017) provided through the Copernicus land monitoring service
# and exclude areas with a TCD value < 50 % (Lukas Blickensdörfer)
# (10-m resolution; reference year 2018)

# https://stackoverflow.com/questions/75072241/replace-negative-values-by-nan-on-a-raster-without-converting-it-into-an-array 

import xarray
import rasterio as rio
from matplotlib import pyplot


#%% Open file 

# Open the file with xarray
raster_file = xarray.open_dataarray("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230327_TCD_1km/TCD_1km_R.tif", engine="rasterio")
print(raster_file.min().data)
# 0.0


#%% Assign NaN when less than 50

raster_file = raster_file.where(raster_file > 50)
print(raster_file.min().data)
# 50.00199508666992 is the minimum now. 


#%% Save the raster

raster_file.rio.to_raster("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230327_TCD_1km/TCD_1km_over50.tif")


#%% Check if saved raster has correct projection

TEST = rio.open('D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230327_TCD_1km/TCD_1km_over50.tif')

TEST.crs
# CRS.from_epsg(4326) 

TEST
print(TEST.nodata) # None

# first band

TEST1 = TEST.read(1)

pyplot.imshow(TEST1)
pyplot.show()  

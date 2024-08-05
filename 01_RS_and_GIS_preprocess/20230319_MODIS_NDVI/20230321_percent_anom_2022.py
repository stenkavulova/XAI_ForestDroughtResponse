# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 18:01:45 2023

@author: Stenka Vulova
"""


# I would like to adjust my original NDVI anomaly calculation.
# https://en.unesco.org/sites/default/files/ukzn-practical-_calculating_change_in_indices_over_time.pdf
# https://gis.stackexchange.com/questions/415177/calculating-ndvi-percentage-change-in-qgis

#%% Libraries

import rasterio
import numpy as np
from rasterio.plot import show

import earthpy as et
import earthpy.plot as ep

#%% Import rasters 

# August 2022 monthly averaged NDVI 
src_2022 = rasterio.open('D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230320_monthly_MODIS_NDVI/2022_08_MODIS_NDVI_avg.tif')
r_2022 = src_2022.read()

show(src_2022)

# Historical reference period (2013-2017)
# Pixel average for August 2013 - 2017

# 'D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230320_monthly_MODIS_NDVI/2013_to_2017_reference_period/08_2013_to_2017_NDVI_avg.tif'

src_ref = rasterio.open('D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230320_monthly_MODIS_NDVI/2013_to_2017_reference_period/08_2013_to_2017_NDVI_avg.tif')
r_ref = src_ref.read()

show(src_ref)

#%% Calculate the percent change 

# However, we will have to implement a variation that allows for the fact that the NDVI ranges across
# both negative and positive values. 

# % change of NDVI from reference period (2013 - 2017)

#First: work out the difference (increase) between the two numbers you are comparing.
#Increase = New Number - Original Number

#Then:  divide the increase by the original number and multiply the answer by 100.
#% increase = Increase ÷ Original Number × 100.

#If your answer is a negative number, then this is a percentage decrease.

# % increase = ( (New Number - Original Number) ÷ Original Number ) × 100.

mask = np.where(r_ref < 0, -1, 1)
# The np.where() function creates a mask array based on the condition reference NDVI < 0. If the condition is true, it sets the value to -1, otherwise, it sets the value to 1.

diff = ((r_2022 - r_ref) / r_ref) * 100
result = mask * diff

ep.plot_bands(result)
ep.plot_bands(mask) # a much nicer plot! cool!
# Thanks Earthpy

#%% Replace 0 with NA value
# I think the masked mean makes NA to be 0.diff

# Replace 0 values with -0.9999
result = np.where(result == 0, -0.9999, result)

result = np.where(result == 0.0, -0.9999, result)

ep.plot_bands(result)

#%% Save result

# Open the original raster to use its metadata
profile = src_ref.profile.copy()
print(profile)

# Save the new raster to file
with rasterio.open('D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230321_MODIS_NDVI_anomaly/NDVI_anomaly_2022.tif', 'w', **profile) as dst:
    dst.write(result)
    
# save the mask 

with rasterio.open('D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230321_MODIS_NDVI_anomaly/NDVI_anomaly_2022_mask.tif', 'w', **profile) as dst:
    dst.write(mask)


#%% Histogram of values 

ep.hist(result, bins = 100)

#%% Load data 
# Loading the saved raster

# August 2022anom monthly averaged NDVI 
src_2022anom = rasterio.open('D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230321_MODIS_NDVI_anomaly/NDVI_anomaly_2022.tif')
r_2022anom = src_2022anom.read()

print(src_2022anom.profile)

#%%  Explore 2022 anomaly

ep.hist(r_2022anom, bins = 100)

print("the minimum raster value is: ", r_2022anom.min())
print("the maximum raster value is: ", r_2022anom.max())

ep.plot_bands(r_2022anom)

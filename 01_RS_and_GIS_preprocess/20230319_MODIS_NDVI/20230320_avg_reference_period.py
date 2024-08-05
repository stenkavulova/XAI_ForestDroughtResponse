# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 13:27:59 2023

@author: Stenka Vulova
"""

# avg the reference period 
# The baseline NDVI was computed by calculating the mean for each pixel
# from 2013 until 2017 (5 years).


#%% Libraries

import rasterio
from rasterio.plot import show
import numpy as np
import glob

# You can instead use np.ma.mean() from the NumPy masked array module, which calculates the mean ignoring masked values.
# Import NumPy masked array module
import numpy.ma as ma

#%% Load the files 

# Load list of tif files
# August 2022 MODIS NDVI (already scaled)

# search the files according to a patrticular pattern inside a given directory. 
tif_files = glob.glob('D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230319_scaled_MODIS_NDVI/reference_period/*.tif')
print(len(tif_files))
print(tif_files)


#%%  Check out first file 

# A raster data source, such as a GeoTIFF file, can be accessed using the rasterio.open function.
# This creates a connection to the raster data.
# The raster properties are imported instantly.
# The raster data, however, are not automatically imported, as they are potentially very large and memory-consuming.
src = rasterio.open(tif_files[0])

src 
# <open DatasetReader name='D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230319_scaled_MODIS_NDVI/2022-08-13_MODIS_NDVI_scale.tif' mode='r'>
# Note that the printout includes the mode='r' part, which indicates the dataset is opened in reading mode.
# This is the default mode of rasterio.open.

# print the metadata of the first raster file 
print(src.meta)

# {'driver': 'GTiff', 'dtype': 'float32', 'nodata': -0.9999, 'width': 407, 'height': 256, 'count': 1, 'crs': CRS.from_epsg(4326), 'transform': Affine(0.008983152841195215, 0.0, 11.184025287288042,
#       0.0, -0.008983152841195215, 53.61145615625305)}

show(src)

print(src.nodata)
# -0.9999

#%% Read all data from tif files list

# https://gis.stackexchange.com/questions/244376/computing-mean-of-all-rasters-in-a-directory-using-python
# https://gis.stackexchange.com/questions/224043/excluding-nodata-value-in-band-calculation-with-rasterio
# You can get a Numpy masked array that covers up nodata values from Rasterio by adding a keyword argument: src.read(1, masked=True). 
# Operations on a masked array do not use the covered up elements.
def read_file(file):
    with rasterio.open(file) as src:
        return(src.read(1, masked = True))

# Read all data as a list of numpy arrays 
array_list = [read_file(x) for x in tif_files]
print(array_list)

#%% Average 

# Perform averaging
# Compute the arithmetic mean along the specified axis, ignoring NaNs.
# You can instead use np.ma.mean() from the NumPy masked array module, which calculates the mean ignoring masked values.
array_out = ma.mean(ma.masked_array(array_list), axis=0)

# Get metadata from one of the input files
with rasterio.open(tif_files[0]) as src:
    meta = src.meta

print(meta)

#%% Replace 0 with NA value
# I think the masked mean makes NA to be 0. 

# Replace 0 values in array_out with -0.9999
array_out = np.where(array_out == 0, -0.9999, array_out)

array_out = np.where(array_out == 0.0, -0.9999, array_out)

#%%  Write the output file 

# Write output file
with rasterio.open('D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230320_monthly_MODIS_NDVI/2013_to_2017_reference_period/08_2013_to_2017_NDVI_avg.tif', 'w', **meta) as dst:
    dst.write(array_out.astype(rasterio.float32), 1)
    
#%% Number of pixels used for averaging 

# You can use the numpy.ma.count function to count the number of non-NA pixels used for averaging.
# This function returns a new masked array that contains the number of non-masked elements along the specified axis.
# It counts the number of non-NA pixels along the 0th axis (i.e., the list of arrays)
count = np.ma.count(ma.masked_array(array_list), axis=0)

# This will give you a new masked array called count that contains the number of non-NA pixels used for averaging at each pixel location.
#You can then save this masked array to a new raster file using the same metadata as the array_out raster:

with rasterio.open('D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230320_monthly_MODIS_NDVI/2013_to_2017_reference_period/nonNA_pixels.tif', 'w', **meta) as dst:
    dst.write(count.astype(rasterio.float32), 1)

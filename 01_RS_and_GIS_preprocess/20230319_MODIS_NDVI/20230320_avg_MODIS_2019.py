# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 10:44:57 2023

@author: Stenka Vulova
"""

# https://geobgu.xyz/py/rasterio.html
# Rasters with rasterio 

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
# August 2019 MODIS NDVI (already scaled)

# search the files according to a patrticular pattern inside a given directory. 
tif_files = glob.glob('D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230319_scaled_MODIS_NDVI/2019-08*.tif')
print(len(tif_files))
print(tif_files)

#%%  Check out first file 

# A raster data source, such as a GeoTIFF file, can be accessed using the rasterio.open function.
# This creates a connection to the raster data.
# The raster properties are imported instantly.
# The raster data, however, are not automatically imported, as they are potentially very large and memory-consuming.
src = rasterio.open(tif_files[0])

src 
# <open DatasetReader name='D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230319_scaled_MODIS_NDVI/2019-08-13_MODIS_NDVI_scale.tif' mode='r'>
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
with rasterio.open('D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230320_monthly_MODIS_NDVI/2019_08_MODIS_NDVI_avg.tif', 'w', **meta) as dst:
    dst.write(array_out.astype(rasterio.float32), 1)
    
# Now it works! 

#%% Check loading file

# Check how saved file loads 

# A raster data source, such as a GeoTIFF file, can be accessed using the rasterio.open function.
# This creates a connection to the raster data.
# The raster properties are imported instantly.
# The raster data, however, are not automatically imported, as they are potentially very large and memory-consuming.
src = rasterio.open('D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230320_monthly_MODIS_NDVI/2019_08_MODIS_NDVI_avg.tif')

src 
# <open DatasetReader name='D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230319_scaled_MODIS_NDVI/2019-08-13_MODIS_NDVI_scale.tif' mode='r'>
# Note that the printout includes the mode='r' part, which indicates the dataset is opened in reading mode.
# This is the default mode of rasterio.open.

# print the metadata of the first raster file 
print(src.meta)

# {'driver': 'GTiff', 'dtype': 'float32', 'nodata': -0.9999, 'width': 407, 'height': 256, 'count': 1, 'crs': CRS.from_epsg(4326), 'transform': Affine(0.008983152841195215, 0.0, 11.184025287288042,
#       0.0, -0.008983152841195215, 53.61145615625305)}

show(src)

print(src.nodata)
# -0.9999

# Looks good. 
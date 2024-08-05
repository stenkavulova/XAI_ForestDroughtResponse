# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 19:47:23 2023

@author: Stenka Vulova
"""

# First, average SPEI for a single year as a test 
# We see how to loop it in a future script.

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
# A test year

# search the files according to a particular pattern inside a given directory. 
year = 2019
print(year)
# the f before the string indicates that it is a formatted string
# the variable name is enclosed in curly braces {}.
tif_files = glob.glob(f'D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230405_SPEI/SPEI_{year}*.tif')

print(len(tif_files)) # 12 
print(tif_files)


#%%  Check out first file 

# A raster data source, such as a GeoTIFF file, can be accessed using the rasterio.open function.
# This creates a connection to the raster data.
# The raster properties are imported instantly.
# The raster data, however, are not automatically imported, as they are potentially very large and memory-consuming.
src = rasterio.open(tif_files[0])

src 
# <open DatasetReader name='D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230405_SPEI/SPEI_2019-01.tif' mode='r'>
# Note that the printout includes the mode='r' part, which indicates the dataset is opened in reading mode.
# This is the default mode of rasterio.open.

# print the metadata of the first raster file 
print(src.meta)

#{'driver': 'GTiff', 'dtype': 'float32', 'nodata': nan, 'width': 253, 'height': 255, 'count': 1, 'crs': CRS.from_wkt('PROJCS["DHDN / 3-degree Gauss-Kruger zone 3",GEOGCS["DHDN",DATUM["Deutsches_Hauptdreiecksnetz",SPHEROID["Bessel 1841",6377397.155,299.152812800003,AUTHORITY["EPSG","7004"]],AUTHORITY["EPSG","6314"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4314"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",9],PARAMETER["scale_factor",1],PARAMETER["false_easting",3500000],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]'), 'transform': Affine(1000.0, 0.0, 3646414.71163347,
#       0.0, -1000.0, 5952500.62890625)}

show(src)

print(src.nodata)
# nan


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

# Notice:
 #     fill_value=nan,
 #     dtype=float32)]
 
#%% Average 

# Compute the arithmetic mean along the specified axis
array_out = np.mean(array_list, axis=0)

# Get metadata from one of the input files
with rasterio.open(tif_files[0]) as src:
    meta = src.meta

print(meta)


#%%  Write the output file 

with rasterio.open(f'D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230406_avg_SPEI/SPEI_avg2_{year}.tif', 'w', **meta) as dst:
    dst.write(array_out.astype(rasterio.float32), 1)
    
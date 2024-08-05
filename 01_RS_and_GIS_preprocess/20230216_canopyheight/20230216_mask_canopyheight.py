# -*- coding: utf-8 -*-
"""
Mask canopy height to Brandenburg 

Created on Thu Feb 16 16:01:36 2023

@author: Stenka Vulova
"""

# Masking / clipping raster
# https://automating-gis-processes.github.io/CSC18/lessons/L6/clipping-raster.html

# One common task in raster processing is to clip raster files based on a Polygon. 


#%% Libraries

# Let’s start by importing required modules and functions.

import rasterio
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
from fiona.crs import from_epsg
import pycrs

import fiona

#%% Filepaths

# Filepaths
fp = r"D:\Stenka_Cliwac\Topic_1\04_PROCESSED_DATA\20230216_canopyheight\canopyheight_mosaic.tif"

out_tif = r"D:\Stenka_Cliwac\Topic_1\04_PROCESSED_DATA\20230216_canopyheight\canopyheight_mask.tif"

#%% Open raster 

# Open the raster in read mode

data = rasterio.open(fp)

# Plot the data

show(data, cmap='terrain')
data.crs # CRS.from_epsg(4326)


#%% Open Brandenburg shapefile 

with fiona.open("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_Brandenburg_border/20230214_Brandenburg_border.shp", "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

# shapes is two elements long (Berlin & Brandenburg)
type(shapefile) # fiona.collection.Collection
type(shapes) # list

print(shapes)

#%% Mask the raster 

# Now we are ready to clip the raster with the polygon using the shapes variable that we just created.
# Clipping the raster can be done easily with the mask function that we imported in the beginning from rasterio, and specifying clip=True.

out_img, out_transform = rasterio.mask.mask(dataset=data, shapes=shapes, crop=True)

#%% Modify the metadata

# Next, we need to modify the metadata.
# Let’s start by copying the metadata from the original data file.

# Copy the metadata
out_meta = data.meta.copy()

print(out_meta)

# {'driver': 'GTiff', 'dtype': 'uint8', 'nodata': 255.0, 'width': 72000, 'height': 36000, 'count': 1, 'crs': CRS.from_epsg(4326), 'transform': Affine(8.333333333333333e-05, 0.0, 9.0,
#       0.0, -8.333333333333333e-05, 54.0)}

#%% EPSG CRS code 

# Next we need to parse the EPSG value from the CRS so that we can create a Proj4 string using PyCRS library
# (to ensure that the projection information is saved correctly).

# Parse EPSG code
epsg_code = int(data.crs.data['init'][5:])
print(epsg_code)

# Now we need to update the metadata with new dimensions, transform (affine) and CRS (as Proj4 text)
out_meta.update({"driver": "GTiff",
                 "height": out_img.shape[1],
                 "width": out_img.shape[2],
                 "transform": out_transform,
                 "crs": pycrs.parse.from_epsg_code(epsg_code).to_proj4()}
                )

print(out_meta)

#%% Save raster

# Finally, we can save the clipped raster to disk with following command.

with rasterio.open(out_tif, "w", **out_meta) as dest:
    dest.write(out_img)
    
#%% Plot the result 

# Let’s still check that the result is correct by plotting our new clipped raster.

clipped = rasterio.open(out_tif)
show(clipped, cmap = "terrain") # Looks good! 

clipped.crs

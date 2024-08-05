# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 10:52:56 2023

@author: Stenka Vulova
"""

# I want to mask TCD to the Brandenburg raster now. 

# https://rasterio.readthedocs.io/en/latest/topics/masking-by-shapefile.html 

#%% Libraries

#Using rasterio with fiona, it is simple to open a shapefile,
# read geometries, and mask out regions of a raster
# that are outside the polygons defined in the shapefile.

import fiona
import rasterio
import rasterio.mask

import numpy as np

#%% Open Brandenburg shapefile 

with fiona.open("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_Brandenburg_border/20230214_Brandenburg_border.shp", "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

# shapes is two elements long (Berlin & Brandenburg)
type(shapefile) # fiona.collection.Collection
type(shapes) # list

#%% Open raster

with rasterio.open("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_TCD_mosaic/TCD_over50_EPSG4326.tif") as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True, nodata = np.nan)
    out_meta = src.meta

#%% Save

out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

with rasterio.open("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_TCD_mosaic/TCD_masked_over50.tif", "w", **out_meta) as dest:
    dest.write(out_image)
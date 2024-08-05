# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 10:09:32 2023

@author: Stenka Vulova
"""

# I want to mask PET to the Brandenburg with a 5 km buffer now. 

# https://rasterio.readthedocs.io/en/latest/topics/masking-by-shapefile.html 

#%% Libraries

#Using rasterio with fiona, it is simple to open a shapefile,
# read geometries, and mask out regions of a raster
# that are outside the polygons defined in the shapefile.

import fiona
import rasterio
import rasterio.mask

import rasterio.plot
import matplotlib as mpl
from descartes import PolygonPatch


#%% Open Brandenburg shapefile 

with fiona.open("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_Brandenburg_border/5km_buffer/BB_5km_buffer_EPSG31467.shp", "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

# shapes is 1 element long 
type(shapefile) # fiona.collection.Collection
type(shapes) # list


#%% Open raster

with rasterio.open("D:/Stenka_Cliwac/Topic_1/03_RAW_DATA/20230328_PET_DWD_grids/grids_germany_monthly_evapo_p_202206.asc/grids_germany_monthly_evapo_p_202206.asc") as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True) # mask 
    out_meta = src.meta
    
print(out_meta)

# plot the raster
src2 = rasterio.open("D:/Stenka_Cliwac/Topic_1/03_RAW_DATA/20230328_PET_DWD_grids/grids_germany_monthly_evapo_p_202206.asc/grids_germany_monthly_evapo_p_202206.asc")
rasterio.plot.show((src2, 1))

#%% Save

out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

with rasterio.open("D:/Stenka_Cliwac/Topic_1/12_PYTHON/20230330_crop_PET/PET_crop_Python.tif", "w", **out_meta) as dest:
    dest.write(out_image)
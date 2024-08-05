# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 15:05:56 2023

@author: Stenka Vulova
"""

# Mask TCD data to Brandenburg
# Here, I will first import the Germany shapefile & subset to Berlin and Brandenburg. 

#%% Libraries 

import geopandas

import fiona
fiona.supported_drivers

#%% Import Germany shapefile 

germany = geopandas.read_file("D:/Stenka_Cliwac/Topic_1/03_RAW_DATA/gadm41_DEU_shp/gadm41_DEU_1.shp")

germany.head()

germany.plot()

type(germany) # D:/Stenka_Cliwac/Topic_1/03_RAW_DATA/gadm41_DEU_shp/gadm41_DEU_1.shp


#%% Filter data

# test - Brandeburg only 

brand_only = germany[germany['NAME_1'] == "Brandenburg"]
brand_only.plot()

brandenburg_berlin_outline = germany[ (germany['NAME_1'] == "Brandenburg") | (germany['NAME_1'] == "Berlin") ] 
brandenburg_berlin_outline.plot()

type(brandenburg_berlin_outline)
# geopandas.geodataframe.GeoDataFrame

# check CRS
brandenburg_berlin_outline.crs

#<Geographic 2D CRS: EPSG:4326>
#Name: WGS 84
#Axis Info [ellipsoidal]:
#- Lat[north]: Geodetic latitude (degree)
#- Lon[east]: Geodetic longitude (degree)
#Area of Use:
#- name: World
#- bounds: (-180.0, -90.0, 180.0, 90.0)
#Datum: World Geodetic System 1984
#- Ellipsoid: WGS 84
#- Prime Meridian: Greenwich

#%% Save data 

brandenburg_berlin_outline.to_file("D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_Brandenburg_border/20230214_Brandenburg_border.shp")

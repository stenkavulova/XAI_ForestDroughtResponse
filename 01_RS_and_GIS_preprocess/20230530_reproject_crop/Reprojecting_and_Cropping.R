### Clear memory
rm(list=ls())

### Install packages 
# maybe some of those won't be needed in the end
install.packages("sp")
install.packages("raster")
install.packages("ncdf4")
install.packages("terra")
install.packages("geodata")
install.packages("sf")
install.packages("rgdal")

# Load packages
library("sp")
library("raster")
library("ncdf4")
library("terra")
library("geodata")
library("sf")
library("rgdal")

setwd("D:\\CliWaC")

# Read in Brandenburg Borders
brandenburg <- terra::vect("D:\\CliWaC\\02_RAW DATA\\Brandenburg Border\\Brandenburg Border Polygon\\BB_10km_4326.shp")
plot(brandenburg)

SMI_germany <- terra::rast("D:\\Nextcloud\\Documents\\CliWaC\\03_RAW DATA\\SMI_Drought_Monitor\\SM_Lall_2021_2022.nc")
template <- SMI_germany
plot(SMI_germany)
plot(template)

# Reproject SMI
gc()
SMI_reproject <- terra::project(SMI_germany, brandenburg, method="bilinear", mask=TRUE)
plot(SMI_reproject)
terra::writeRaster(SMI_reproject, filename="D:\\CliWaC\\03_PROCESSED DATA\\SMI_reprojected\\SMI_Germany.tif")

bb_raster <- terra::rasterize(brandenburg, SMI_germany)
plot(bb_raster)

# Crop SMI_reproject to Brandenburg extent
SMI_Brandenburg <- terra::crop(SMI_reproject, bb_raster, mask=TRUE)
plot(SMI_Brandenburg)

terra::writeRaster(SMI_Brandenburg, filename="D:\\CliWaC\\03_PROCESSED DATA\\SMI_reprojected\\SMI_reproj.tif")

########################################################################
### Project       : CliWaC                                           ###
### Description   : SSM and SWI Data Preprocessing                   ###
### Date          : 24/05/2023                                       ###
########################################################################


### Clear memory
rm(list=ls())

# Load packages----
library("sp")
library("ncdf4")
library("terra")
library("geodata")
library("sf")
library("rgdal")

setwd("D:\\CliWaC\\02_RAW DATA\\")


# SSM----

# Set the path to the folder containing the subfolders for each year
folder_path <- "D:\\CliWaC\\02_RAW DATA\\SSM"

# Get a list of all the files in the subfolders
file_list <- list.files(path = folder_path, pattern = ".nc$", recursive = TRUE, full.names = TRUE)

#open one file to test and see variables
nc_test <- nc_open("D:\\CliWaC\\02_RAW DATA\\SSM\\SSM_20160101_356.nc")
names(nc_open("D:\\CliWaC\\02_RAW DATA\\SSM\\SSM_20160101_356.nc")$var)
# variables "ssm" and "ssm_noise"

# Create a RasterStack from the file list
SSM_2016 <- terra::rast(file_list, "ssm")

# Import a shapefile with Brandenburg extent (+ 10km Buffer)
bb_border_10km <- terra::vect("D:\\Katharina\\CliWaC\\02_RAW DATA\\Brandenburg Border\\Brandenburg Border Polygon\\BB_10km_4326.shp")
plot(bb_border_10km)

# Crop SSM to the extent of Brandenburg (+ 10km Buffer)
SSM_bb <- terra::crop(SSM_2016, bb_border_10km, mask = TRUE)
plot(SSM_bb)
SSM_bb

# Save cropped SSM dataset
gc()
terra::writeRaster(SSM_bb,"C:\\Users\\Katharina_Horn\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\SSM\\SSM_bb.tif", overwrite=TRUE)


# SWI----
##  Calculate averages for the years of 2017 to 2022----

# Set the path to the folder containing the subfolders for each year
folder_path_SWI_2017 <- "F:\\Katharinas Local Data\\SWI\\2017"
folder_path_SWI_2018 <- "F:\\Katharinas Local Data\\SWI\\2018"
folder_path_SWI_2019 <- "F:\\Katharinas Local Data\\SWI\\2019"
folder_path_SWI_2020 <- "F:\\Katharinas Local Data\\SWI\\2020"
folder_path_SWI_2021 <- "F:\\Katharinas Local Data\\SWI\\2021"
folder_path_SWI_2022 <- "F:\\Katharinas Local Data\\SWI\\2022"

# Get a list of all the files in the subfolders
file_list_SWI_2017 <- list.files(path = folder_path_SWI_2017, pattern = ".nc$", recursive = TRUE, full.names = TRUE)
file_list_SWI_2018 <- list.files(path = folder_path_SWI_2018, pattern = ".nc$", recursive = TRUE, full.names = TRUE)
file_list_SWI_2019 <- list.files(path = folder_path_SWI_2019, pattern = ".nc$", recursive = TRUE, full.names = TRUE)
file_list_SWI_2020 <- list.files(path = folder_path_SWI_2020, pattern = ".nc$", recursive = TRUE, full.names = TRUE)
file_list_SWI_2021 <- list.files(path = folder_path_SWI_2021, pattern = ".nc$", recursive = TRUE, full.names = TRUE)
file_list_SWI_2022 <- list.files(path = folder_path_SWI_2022, pattern = ".nc$", recursive = TRUE, full.names = TRUE)

# Open one file to test and see variables
nc_test_SWI <- nc_open("F:\\Katharinas Local Data\\SWI\\2017\\SWI_20170102.nc")
names(nc_open("F:\\Katharinas Local Data\\SWI\\2017\\SWI_20170102.nc")$var)
#variables "crs"       "SSF"       "SWI_002"   "QFLAG_002" "SWI_005"   "QFLAG_005" "SWI_010"   "QFLAG_010" "SWI_015"   "QFLAG_015" "SWI_020"   "QFLAG_020" "SWI_040"   "QFLAG_040" "SWI_060"   "QFLAG_060" "SWI_100"   "QFLAG_100"
# SWI_015 is needed 

# Create a RasterStack for each year from the file list
SWI_2017 <- terra::rast(file_list_SWI_2017, "SWI_015")
SWI_2018 <- terra::rast(file_list_SWI_2018, "SWI_015")
SWI_2019 <- terra::rast(file_list_SWI_2019, "SWI_015")
SWI_2020 <- terra::rast(file_list_SWI_2020, "SWI_015")
SWI_2021 <- terra::rast(file_list_SWI_2021, "SWI_015")
SWI_2022 <- terra::rast(file_list_SWI_2022, "SWI_015")

# Import a shapefile with the Brandenburg extent
bb_border_10km <- terra::vect("D:\\Katharina\\CliWaC\\02_RAW DATA\\Brandenburg Border\\Brandenburg Border Polygon\\BB_10km_4326.shp")
plot(bb_border_10km)
bb_border_10km

# Calculate the mean raster for each year (2017 to 2022)
mean_swi_2017 <- terra::app(SWI_2017, mean, na.rm = TRUE)
mean_swi_2018 <- terra::app(SWI_2018, mean, na.rm = TRUE)
mean_swi_2019 <- terra::app(SWI_2019, mean, na.rm = TRUE)
mean_swi_2020 <- terra::app(SWI_2020, mean, na.rm = TRUE)
mean_swi_2021 <- terra::app(SWI_2021, mean, na.rm = TRUE)
mean_swi_2022 <- terra::app(SWI_2022, mean, na.rm = TRUE)

# Crop Dataset to the size of Brandenburg
par(mfrow=c(2,3))
SWI_bb_2017 <- terra::crop(mean_swi_2017, bb_border_10km, mask = TRUE)
plot(SWI_bb_2017)
SWI_bb_2017

SWI_bb_2018 <- terra::crop(mean_swi_2018, bb_border_10km, mask = TRUE)
plot(SWI_bb_2018)
SWI_bb_2018

SWI_bb_2019 <- terra::crop(mean_swi_2019, bb_border_10km, mask = TRUE)
plot(SWI_bb_2019)
SWI_bb_2019

SWI_bb_2020 <- terra::crop(mean_swi_2020, bb_border_10km, mask = TRUE)
plot(SWI_bb_2020)
SWI_bb_2020

SWI_bb_2021 <- terra::crop(mean_swi_2021, bb_border_10km, mask = TRUE)
plot(SWI_bb_2021)
SWI_bb_2021

SWI_bb_2022 <- terra::crop(mean_swi_2022, bb_border_10km, mask = TRUE)
plot(SWI_bb_2022)
SWI_bb_2022

# Stack for years of 2017 to 2022
SWI_bb_annual_all <- c(SWI_bb_2017, SWI_bb_2018, SWI_bb_2019, SWI_bb_2020, SWI_bb_2021, SWI_bb_2022)

# Change names of the layers
names(SWI_bb_annual_all) <- c("SWI_2017_avg", "SWI_2018_avg", "SWI_2019_avg", "SWI_2020_avg", "SWI_2021_avg", "SWI_2022_avg")
SWI_bb_annual_all
plot(SWI_bb_annual_all)

# Save annual mean raster stack for SWI for 2017 to 2022
gc()
terra::writeRaster(SWI_bb_annual_all, "D:\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\Soil Moisture Data\\SWI\\2017 to 2022\\SWI_bb_15cm_annual_mean_2017_to_2022.tif", overwrite=TRUE)



## Calculate averages for January to July of each year (2017 to 2022) ----

# Create new file lists that contain only January to July of each year
file_list_SWI_2017_jj <- file_list_SWI_2017[1:212] # 07/31 is DOY 212
file_list_SWI_2017_jj

file_list_SWI_2018_jj <- file_list_SWI_2018[1:212]
file_list_SWI_2018_jj

file_list_SWI_2019_jj <- file_list_SWI_2019[1:212]
file_list_SWI_2019_jj

file_list_SWI_2020_jj <- file_list_SWI_2020[1:213] # leap year, 07/31 is DOY 213
file_list_SWI_2020_jj

file_list_SWI_2021_jj <- file_list_SWI_2021[1:212]
file_list_SWI_2021_jj

file_list_SWI_2022_jj <- file_list_SWI_2022[1:212]
file_list_SWI_2022_jj

# Create a raster stack for each year from the file list
SWI_2017_jj <- terra::rast(file_list_SWI_2017_jj, "SWI_015")
SWI_2018_jj <- terra::rast(file_list_SWI_2018_jj, "SWI_015")
SWI_2019_jj <- terra::rast(file_list_SWI_2019_jj, "SWI_015")
SWI_2020_jj <- terra::rast(file_list_SWI_2020_jj, "SWI_015")
SWI_2021_jj <- terra::rast(file_list_SWI_2021_jj, "SWI_015")
SWI_2022_jj <- terra::rast(file_list_SWI_2022_jj, "SWI_015")

# Calculate the mean raster for each year (2017 to 2022) from January to July
mean_swi_2017_jj <- terra::app(SWI_2017_jj, mean, na.rm = TRUE)
mean_swi_2018_jj <- terra::app(SWI_2018_jj, mean, na.rm = TRUE)
mean_swi_2019_jj <- terra::app(SWI_2019_jj, mean, na.rm = TRUE)
mean_swi_2020_jj <- terra::app(SWI_2020_jj, mean, na.rm = TRUE)
mean_swi_2021_jj <- terra::app(SWI_2021_jj, mean, na.rm = TRUE)
mean_swi_2022_jj <- terra::app(SWI_2022_jj, mean, na.rm = TRUE)

# Crop to Brandenburg
par(mfrow=c(2,3))
SWI_bb_2017_jj <- terra::crop(mean_swi_2017_jj, bb_border_10km, mask = TRUE)
plot(SWI_bb_2017_jj)
SWI_bb_2017_jj

SWI_bb_2018_jj <- terra::crop(mean_swi_2018_jj, bb_border_10km, mask = TRUE)
plot(SWI_bb_2018_jj)
SWI_bb_2018_jj

SWI_bb_2019_jj <- terra::crop(mean_swi_2019_jj, bb_border_10km, mask = TRUE)
plot(SWI_bb_2019_jj)
SWI_bb_2019_jj

SWI_bb_2020_jj <- terra::crop(mean_swi_2020_jj, bb_border_10km, mask = TRUE)
plot(SWI_bb_2020_jj)
SWI_bb_2020_jj

SWI_bb_2021_jj <- terra::crop(mean_swi_2021_jj, bb_border_10km, mask = TRUE)
plot(SWI_bb_2021_jj)
SWI_bb_2021_jj

SWI_bb_2022_jj <- terra::crop(mean_swi_2022_jj, bb_border_10km, mask = TRUE)
plot(SWI_bb_2022_jj)
SWI_bb_2022_jj

# Stack for years of 2017 to 2022
SWI_bb_jj_all <- c(SWI_bb_2017_jj, SWI_bb_2018_jj, SWI_bb_2019_jj, SWI_bb_2020_jj, SWI_bb_2021_jj, SWI_bb_2022_jj)

# Change names of the layers
names(SWI_bb_jj_all) <- c("SWI_2017_avg_jul", "SWI_2018_avg_jul", "SWI_2019_avg_jul", "SWI_2020_avg_jul", "SWI_2021_avg_jul", "SWI_2022_avg_jul")
SWI_bb_jj_all

# Save annual mean raster stack for SWI for 2017 to 2022
gc()
terra::writeRaster(SWI_bb_jj_all, "D:\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\Soil Moisture Data\\SWI\\2017 to 2022\\SWI_bb_15cm_jan_jul_mean_2017_to_2022.tif", overwrite=TRUE)

# Check resulting file
result_avg2 <- terra::rast("D:\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\Soil Moisture Data\\SWI\\2017 to 2022\\SWI_bb_15cm_jan_jul_mean_2017_to_2022.tif")
plot(result_avg2)
result_avg2




## End of script
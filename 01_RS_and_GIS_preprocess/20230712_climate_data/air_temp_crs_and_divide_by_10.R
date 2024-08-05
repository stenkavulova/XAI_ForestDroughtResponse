##############################################################
##############################################################

##### Assign CRS to Mean AIR TEMPERATURE and DIVDE by 10 #####

##############################################################
##############################################################


library("sp")
library("ncdf4")
library("terra")
library("geodata")
library("sf")
library("rgdal")

## Assign CRS to air temperature files
path <- "D:\\CliWaC\\03_PROCESSED DATA\\DWD Data\\Air Temperature Mean\\final"
output_folder <- "D:\\CliWaC\\03_PROCESSED DATA\\DWD Data\\Air Temperature Mean\\final_crs"

## List all the .tif files in the directory
temp_files <- list.files(path = path, pattern = "\\.tif$", full.names = TRUE)

print(temp_files)

## Assign new coordinate system
crs <- "EPSG:31467"

library(terra)
## Loop through each file and assign the CRS
for (temp_file in temp_files) {
  # Read the raster
  r <- rast(temp_file)
  
  # Assign the CRS
  crs(r) <- crs
  
  # Divide the values by 10 because the DWD data is provided in 1/10 °C
  r <- r / 10 
  
  # Create the output file path with the suffix "_crs"
  output_file <- file.path(output_folder, paste0(basename(temp_file)))
  
  # Save the updated raster with the new CRS
  writeRaster(r, filename = output_file, overwrite = TRUE)
}

test <- terra::rast("D:\\CliWaC\\03_PROCESSED DATA\\DWD Data\\Air Temperature Mean\\final_crs\\grids_germany_monthly_air_temp_mean_200002_BB.tif")

print(test)
plot(test)


##############################################################
##############################################################

#####               Assign CRS to Radiation Direct       #####

##############################################################
##############################################################


library("sp")
library("ncdf4")
library("terra")
library("geodata")
library("sf")
library("rgdal")

## Assign CRS to radiation_direct files
path <- "D:\\CliWaC\\03_PROCESSED DATA\\DWD Data\\Radiation_direct\\final"
output_folder <- "D:\\CliWaC\\03_PROCESSED DATA\\DWD Data\\Radiation_direct\\final_crs"

## List all the .tif files in the directory
rad_files <- list.files(path = path, pattern = "\\.tif$", full.names = TRUE)

print(rad_files)

## Assign new coordinate system
crs <- "EPSG:31467"

library(terra)
## Loop through each file and assign the CRS
for (rad_file in rad_files) {
  # Read the raster
  r <- rast(rad_file)
  
  # Assign the CRS
  crs(r) <- crs
  
  # Create the output file path with the suffix "_crs"
  output_file <- file.path(output_folder, paste0(basename(rad_file)))
  
  # Save the updated raster with the new CRS
  writeRaster(r, filename = output_file, overwrite = TRUE)
}

test <- terra::rast("D:\\CliWaC\\03_PROCESSED DATA\\DWD Data\\Radiation_direct\\final_crs\\grids_germany_monthly_radiation_direct_201501_BB.tif")

print(test)
plot(test)


test_temp <- terra::rast("D:\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\DWD Data\\Air Temperature Mean\\final_BB\\grids_germany_monthly_air_temp_mean_200002_BB.tif")
print(test_temp)
plot(test_temp)


test_evapo <- terra::rast("D:\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\DWD Data\\Evapotranspiration\\final_BB\\grids_germany_monthly_evapo_r_200001_BB.tif")
print(test_evapo)
plot(test_evapo)

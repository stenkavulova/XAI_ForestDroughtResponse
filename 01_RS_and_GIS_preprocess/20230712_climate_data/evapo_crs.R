##############################################################
##############################################################

#####        Assign CRS to Evapotranspiration Data       #####

##############################################################
##############################################################


library("sp")
library("ncdf4")
library("terra")
library("geodata")
library("sf")
library("rgdal")

## Assign CRS to air temperature files
path <- "D:\\CliWaC\\03_PROCESSED DATA\\DWD Data\\Evapo_r\\final"
output_folder <- "D:\\CliWaC\\03_PROCESSED DATA\\DWD Data\\Evapo_r\\final_crs"

## List all the .tif files in the directory
evapo_files <- list.files(path = path, pattern = "\\.tif$", full.names = TRUE)

print(evapo_files)

## Assign new coordinate system
crs <- "EPSG:31467"

library(terra)
## Loop through each file and assign the CRS
for (evapo_file in evapo_files) {
  # Read the raster
  r <- rast(evapo_file)
  
  # Assign the CRS
  crs(r) <- crs
  
  # Create the output file path with the suffix "_crs"
  output_file <- file.path(output_folder, paste0(basename(evapo_file)))
  
  # Save the updated raster with the new CRS
  writeRaster(r, filename = output_file, overwrite = TRUE)
}

test <- terra::rast("D:\\CliWaC\\03_PROCESSED DATA\\DWD Data\\Evapo_r\\final_crs\\grids_germany_monthly_evapo_r_200001_BB.tif")

print(test)
plot(test)

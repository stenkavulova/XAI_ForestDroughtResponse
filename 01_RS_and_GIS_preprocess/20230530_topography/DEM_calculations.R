########################################################################
### Project       : CliWaC                                           ###
### Description   : Digital Elevation Model                          ###
### Date          : 05/04/2023                                       ###
########################################################################

#=======================================================================
# Calculate Slope, Sun exposure, Topographic Wetness Index
#=======================================================================

### Clear memory
rm(list=ls())

### Install packages 
# maybe some of those won't be needed in the end
install.packages("sp")
install.packages("ncdf4")
install.packages("terra")
install.packages("geodata")
install.packages("sf")
install.packages("rgdal")

# Load packages
library("sp")
library("ncdf4")
library("terra")
library("geodata")
library("sf")
library("rgdal")

setwd("C:\\Users\\Katharina_Horn\\Nextcloud\\Documents\\CliWaC")

# Load in DEM
bb_dem <- terra::rast("D:\\CliWaC\\02_RAW DATA\\DEM\\DEM_mosaic_10m_Brandenburg.tif")

# Calculate slope from DEM
# Slope (in degrees)
bb_slope_deg <- terrain(bb_dem, v="slope", neighbors=8, unit="degrees")

output_path <- ("C:\\Users\\Katharina_Horn\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\Topography\\Slope in degrees\\slope_bb.tif")
terra::writeRaster(bb_slope, filename=output_path)

# Slope (in radians)
bb_slope_r <- terrain(bb_dem, v="slope", neighbors=8, unit="radians")
output_path_r <- ("C:\\Users\\Katharina_Horn\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\Topography\\Slope in radians\\slope_bb_r.tif")
terra::writeRaster(bb_slope_r, filename=output_path_r)


# Calculate folded aspect / sun exposure
# Aspect (in degrees)
bb_aspect <- terrain(bb_dem, v="aspect", neighbors=8, unit="degrees")
output_path_aspect <- ("C:\\Users\\Katharina_Horn\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\Topography\\Aspect in degrees\\aspect_bb.tif")
terra::writeRaster(bb_aspect, filename=output_path_aspect)

# Aspect (in radians)
bb_aspect_r <- terrain(bb_dem, v="aspect", neighbors=8, unit="radians")
output_path_r2 <- ("C:\\Users\\Katharina_Horn\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\Topography\\Aspect in radians\\aspect_bb_r.tif")
terra::writeRaster(bb_aspect_r, filename=output_path_r2)


###### Calculate TWI #########
install.packages("whitebox")
install.packages("RSAGA")
library(RSAGA)

## TWI formula: TWI = Ln(As/tan(Slope))
# As = specific contributing area
# Slope = slope at the cell

# Set up RSAGA Environment
env <- RSAGA::rsaga.env(
  path = "D:\\05_PACKAGES FOR R\\SAGA\\saga-9.0.1_x64\\saga-9.0.1_x64\\",
  modules = "D:\\05_PACKAGES FOR R\\SAGA\\saga-9.0.1_x64\\saga-9.0.1_x64\\tools",
  workspace = "D:\\05_PACKAGES FOR R\\SAGA",
  cmd = ifelse(Sys.info()["sysname"] == "Windows", "saga_cmd.exe", "saga_cmd"),
  version = rsaga.get.version(),
  cores,
  parallel = FALSE,
  root = NULL,
  lib.prefix
)

dem_sgrd <- RSAGA::rsaga.import.gdal(in.grid = "C:\\Users\\Katharina_Horn\\Nextcloud\\Documents\\CliWaC\\03_RAW DATA\\DEM\\DEM_mosaic_10m_Brandenburg.tif", env = env)

RSAGA::rsaga.wetness.index()

rsaga.geoprocessor(lib = "ta_morphometry", module = "Slope, Aspect, Curvature",
                   param = list(ELEVATION = paste(getwd("C:\\Users\\Katharina_Horn\\Nextcloud\\Documents\\CliWaC\\03_RAW DATA\\DEM\\"),"DEM_mosaic_10m_Brandenburg.tif", sep = ""), 
                                SLOPE = paste(getwd("C:\\Users\\Katharina_Horn\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\Topography\\Slope\\Slope in radians"),"slope_bb_r.tif", sep = "")),
                   env = env)

# rsaga.wetness.index("dem.sgrd","swi.sgrd")
RSAGA::rsaga.env()
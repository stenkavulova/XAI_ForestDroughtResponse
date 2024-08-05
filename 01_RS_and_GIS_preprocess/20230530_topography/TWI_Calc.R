########################################################################
### Project       : CliWaC                                           ###
### Description   : Topographic Wetness Index                        ###
### Date          : 05/04/2023                                       ###
########################################################################

#=======================================================================
# Calculate Topographic Wetness Index using 'whitebox' package
#=======================================================================

### Clear memory
rm(list=ls())

### Install packages 
install.packages("tidyverse")
install.packages("raster")
install.packages("sf")
install.packages("whitebox")
install.packages("tmap")

library(tidyverse)
library(raster)
library(sf)
library(whitebox)
library(tmap)

install_whitebox()
whitebox::wbt_init()

## Read in four Subsets of DEM
dem <- raster("D:/CliWaC/02_RAW DATA/DEM/DEM_mosaic_10m_Brandenburg.tif", crs = '+init=EPSG:4326')
dem1 <- raster("D:/CliWaC/02_RAW DATA/DEM/DEM_subset_1_1.tif", crs = '+init=EPSG:4326')
dem2 <- raster("D:/CliWaC/02_RAW DATA/DEM/DEM_subset_1_2.tif", crs = '+init=EPSG:4326')
dem3 <- raster("D:/CliWaC/02_RAW DATA/DEM/DEM_subset_2_1.tif", crs = '+init=EPSG:4326')
dem4 <- raster("D:/CliWaC/02_RAW DATA/DEM/DEM_subset_2_2.tif", crs = '+init=EPSG:4326')

writeRaster(dem, "D:/CliWaC/03_PROCESSED DATA/DEM/DEM_new.tif", overwrite = TRUE)
writeRaster(dem1, "D:/CliWaC/03_PROCESSED DATA/DEM/DEM1_crs.tif", overwrite = TRUE)
writeRaster(dem2, "D:/CliWaC/03_PROCESSED DATA/DEM/DEM2_crs.tif", overwrite = TRUE)
writeRaster(dem3, "D:/CliWaC/03_PROCESSED DATA/DEM/DEM3_crs.tif", overwrite = TRUE)
writeRaster(dem4, "D:/CliWaC/03_PROCESSED DATA/DEM/DEM4_crs.tif", overwrite = TRUE)

dem_new <- raster("D:/CliWaC/03_PROCESSED DATA/DEM/DEM_new.tif")

# Plot DEM
plot(dem_new)
plot(dem1)
plot(dem2)
plot(dem3)
plot(dem4)


# Breach depressions and fill sinks for the entire DEM
gc()
wbt_breach_depressions_least_cost(
  dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM_crs.tif",
  output = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM_breached.tif",
  dist = 5,
  fill = TRUE)

gc()
wbt_fill_depressions_wang_and_liu(
  dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM_breached.tif",
  output = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM_filled_breached.tif"
)

#### Breach depressions and fill sinks with subsets
# Subset 1
gc()
wbt_breach_depressions_least_cost(
  dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM1_crs.tif",
  output = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM1_breached.tif",
  dist = 5,
  fill = TRUE)

gc()
wbt_fill_depressions_wang_and_liu(
  dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM1_breached.tif",
  output = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM1_filled_breached.tif"
)

# Subset 2
gc()
wbt_breach_depressions_least_cost(
  dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM2_crs.tif",
  output = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM2_breached.tif",
  dist = 5,
  fill = TRUE)

gc()
wbt_fill_depressions_wang_and_liu(
  dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM2_breached.tif",
  output = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM2_filled_breached.tif"
)

# Subset 3
gc()
wbt_breach_depressions_least_cost(
  dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM3_crs.tif",
  output = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM3_breached.tif",
  dist = 5,
  fill = TRUE)

gc()
wbt_fill_depressions_wang_and_liu(
  dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM3_breached.tif",
  output = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM3_filled_breached.tif"
)

# Subset 4
gc()
wbt_breach_depressions_least_cost(
  dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM4_crs.tif",
  output = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM4_breached.tif",
  dist = 5,
  fill = TRUE)

gc()
wbt_fill_depressions_wang_and_liu(
  dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM4_breached.tif",
  output = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM4_filled_breached.tif"
)


# Calculate "Specific Contributing Area" (SCA) needed for TWI calculation
gc()
wbt_d_inf_flow_accumulation(input = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM_filled_breached.tif",
                            output = "D:/CliWaC/03_PROCESSED DATA/DEM/DinfFAsca_test.tif",
                            out_type = "Specific Contributing Area")
gc()
wbt_d_inf_flow_accumulation(input = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM1_filled_breached.tif",
                            output = "D:/CliWaC/03_PROCESSED DATA/DEM/DinfFAsca_subset1.tif",
                            out_type = "Specific Contributing Area")
gc()
wbt_d_inf_flow_accumulation(input = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM2_filled_breached.tif",
                            output = "D:/CliWaC/03_PROCESSED DATA/DEM/DinfFAsca_subset2.tif",
                            out_type = "Specific Contributing Area")
gc()
wbt_d_inf_flow_accumulation(input = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM3_filled_breached.tif",
                            output = "D:/CliWaC/03_PROCESSED DATA/DEM/DinfFAsca_subset3.tif",
                            out_type = "Specific Contributing Area")
gc()
wbt_d_inf_flow_accumulation(input = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM4_filled_breached.tif",
                            output = "D:/CliWaC/03_PROCESSED DATA/DEM/DinfFAsca_subset4.tif",
                            out_type = "Specific Contributing Area")

# Calculate Slope needed for TWI calculation
wbt_slope(dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM_filled_breached.tif",
          output = "D:/CliWaC/03_PROCESSED DATA/DEM/demslope_test.tif",
          units = "degrees")

# Calculate Slope for Subsets needed for TWI Calculation
gc()
wbt_slope(dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM1_filled_breached.tif",
          output = "D:/CliWaC/03_PROCESSED DATA/DEM/demslope_subset1.tif",
          units = "degrees")
gc()
wbt_slope(dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM2_filled_breached.tif",
          output = "D:/CliWaC/03_PROCESSED DATA/DEM/demslope_subset2.tif",
          units = "degrees")
gc()
wbt_slope(dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM3_filled_breached.tif",
          output = "D:/CliWaC/03_PROCESSED DATA/DEM/demslope_subset3.tif",
          units = "degrees")
gc()
wbt_slope(dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM4_filled_breached.tif",
          output = "D:/CliWaC/03_PROCESSED DATA/DEM/demslope_subset4.tif",
          units = "degrees")

# Calculate Topographic Wetness Index (TWI)
gc()
wbt_wetness_index(sca = "D:/CliWaC/03_PROCESSED DATA/DEM/DinfFAsca_test.tif", 
                  slope = "D:/CliWaC/03_PROCESSED DATA/DEM/demslope_test.tif",
                  output = "D:/CliWaC/03_PROCESSED DATA/DEM/TWI_test.tif")

# Calculate Topographic Wetness Index (TWI) with subsets
gc()
wbt_wetness_index(sca = "D:/CliWaC/03_PROCESSED DATA/DEM/DinfFAsca_subset1.tif", 
                  slope = "D:/CliWaC/03_PROCESSED DATA/DEM/demslope_subset1.tif",
                  output = "D:/CliWaC/03_PROCESSED DATA/DEM/TWI_subset1.tif")
gc()
wbt_wetness_index(sca = "D:/CliWaC/03_PROCESSED DATA/DEM/DinfFAsca_subset2.tif", 
                  slope = "D:/CliWaC/03_PROCESSED DATA/DEM/demslope_subset2.tif",
                  output = "D:/CliWaC/03_PROCESSED DATA/DEM/TWI_subset2.tif")
gc()
wbt_wetness_index(sca = "D:/CliWaC/03_PROCESSED DATA/DEM/DinfFAsca_subset3.tif", 
                  slope = "D:/CliWaC/03_PROCESSED DATA/DEM/demslope_subset3.tif",
                  output = "D:/CliWaC/03_PROCESSED DATA/DEM/TWI_subset3.tif")
gc()
wbt_wetness_index(sca = "D:/CliWaC/03_PROCESSED DATA/DEM/DinfFAsca_subset4.tif", 
                  slope = "D:/CliWaC/03_PROCESSED DATA/DEM/demslope_subset4.tif",
                  output = "D:/CliWaC/03_PROCESSED DATA/DEM/TWI_subset4.tif")


# Load results for check-up
twi <- raster("D:/CliWaC/03_PROCESSED DATA/DEM/TWI_test.tif")
twi[twi > 0] <- NA
plot(twi)


# Load subset results for check-up
twi_s1 <- raster("D:/CliWaC/03_PROCESSED DATA/DEM/TWI_subset1.tif")
twi_s2 <- raster("D:/CliWaC/03_PROCESSED DATA/DEM/TWI_subset2.tif")
twi_s3 <- raster("D:/CliWaC/03_PROCESSED DATA/DEM/TWI_subset3.tif")
twi_s4 <- raster("D:/CliWaC/03_PROCESSED DATA/DEM/TWI_subset4.tif")

plot(twi_s1)
plot(twi_s2)
plot(twi_s3)
plot(twi_s4)

# Create a raster stack with the four rasters
raster_stack <- stack(twi_s1, twi_s2, twi_s3, twi_s4)

# Merge the rasters into a single raster
merged_raster <- merge(raster_stack)


twi_all <- c(twi_s1, twi_s2, twi_s3, twi_s4)


## Calculate slope from DEM
gc()
slope <- wbt_slope(dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM_new.tif", 
          output = "D:/CliWaC/03_PROCESSED DATA/DEM/dem_slope_wbt.tif",
          units = "degrees")
plot(slope)

## Calculate aspect from DEM
gc()
aspect <- wbt_aspect(dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM_new.tif", 
                     output = "D:/CliWaC/03_PROCESSED DATA/Topography/dem_aspect_wbt.tif")

####################
# Calculate hillshade from DEM
#gc()
#wbt_hillshade(dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM_crs.tif",
#output = "D:/CliWaC/03_PROCESSED DATA/DEM/hillshade.tif",
#azimuth = 115)

#wbt_hillshade(dem = "D:/CliWaC/03_PROCESSED DATA/DEM/DEM_test_crs.tif",
#output = "D:/CliWaC/03_PROCESSED DATA/DEM/hillshade_small.tif",
#azimuth = 115)


#hillshade <- raster("D:/CliWaC/03_PROCESSED DATA/DEM/hillshade.tif")
#plot(hillshade)

#hillshade_small <- raster("D:/CliWaC/03_PROCESSED DATA/DEM/hillshade_small.tif")
#plot(hillshade_small)
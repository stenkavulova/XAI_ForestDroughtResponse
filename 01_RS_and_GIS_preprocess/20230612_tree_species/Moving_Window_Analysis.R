#############################################################
#############################################################
#############################################################
#######                   CLIWAC                     ########
#############################################################
        #############################################
              ###################################


### Clear memory
rm(list=ls())

#############################################################
## Calculation of Moving Window for Forest Type Percentage ##
#############################################################

library("sp")
library("ncdf4")
library("terra")
library("geodata")
library("sf")
library("rgdal")

setwd("D:/CliWaC")

bb <- terra::vect("D:\\CliWaC\\03_PROCESSED DATA\\Brandenburg\\BB_10km_3035.shp")
fty1 <- terra::rast("D:\\CliWaC\\02_RAW DATA\\CORINE Forest Type Germany 10m\\81048aa9a161f7881afe19b16519e8e7849dd415\\FTY_2018_010m_de_03035_v010\\FTY_2018_010m_de_03035_v010\\DATA\\FTY_2018_010m_E46N33_03035_v010.tif")
fty2 <- terra::rast("D:\\CliWaC\\02_RAW DATA\\CORINE Forest Type Germany 10m\\81048aa9a161f7881afe19b16519e8e7849dd415\\FTY_2018_010m_de_03035_v010\\FTY_2018_010m_de_03035_v010\\DATA\\FTY_2018_010m_E46N32_03035_v010.tif")
fty3 <- terra::rast("D:\\CliWaC\\02_RAW DATA\\CORINE Forest Type Germany 10m\\81048aa9a161f7881afe19b16519e8e7849dd415\\FTY_2018_010m_de_03035_v010\\FTY_2018_010m_de_03035_v010\\DATA\\FTY_2018_010m_E46N31_03035_v010.tif")
fty4 <- terra::rast("D:\\CliWaC\\02_RAW DATA\\CORINE Forest Type Germany 10m\\81048aa9a161f7881afe19b16519e8e7849dd415\\FTY_2018_010m_de_03035_v010\\FTY_2018_010m_de_03035_v010\\DATA\\FTY_2018_010m_E45N34_03035_v010.tif")
fty5 <- terra::rast("D:\\CliWaC\\02_RAW DATA\\CORINE Forest Type Germany 10m\\81048aa9a161f7881afe19b16519e8e7849dd415\\FTY_2018_010m_de_03035_v010\\FTY_2018_010m_de_03035_v010\\DATA\\FTY_2018_010m_E45N33_03035_v010.tif")
fty6 <- terra::rast("D:\\CliWaC\\02_RAW DATA\\CORINE Forest Type Germany 10m\\81048aa9a161f7881afe19b16519e8e7849dd415\\FTY_2018_010m_de_03035_v010\\FTY_2018_010m_de_03035_v010\\DATA\\FTY_2018_010m_E45N32_03035_v010.tif")
fty7 <- terra::rast("D:\\CliWaC\\02_RAW DATA\\CORINE Forest Type Germany 10m\\81048aa9a161f7881afe19b16519e8e7849dd415\\FTY_2018_010m_de_03035_v010\\FTY_2018_010m_de_03035_v010\\DATA\\FTY_2018_010m_E45N31_03035_v010.tif")
fty8 <- terra::rast("D:\\CliWaC\\02_RAW DATA\\CORINE Forest Type Germany 10m\\81048aa9a161f7881afe19b16519e8e7849dd415\\FTY_2018_010m_de_03035_v010\\FTY_2018_010m_de_03035_v010\\DATA\\FTY_2018_010m_E44N33_03035_v010.tif")
fty9 <- terra::rast("D:\\CliWaC\\02_RAW DATA\\CORINE Forest Type Germany 10m\\81048aa9a161f7881afe19b16519e8e7849dd415\\FTY_2018_010m_de_03035_v010\\FTY_2018_010m_de_03035_v010\\DATA\\FTY_2018_010m_E44N32_03035_v010.tif")
fty10 <- terra::rast("D:\\CliWaC\\02_RAW DATA\\CORINE Forest Type Germany 10m\\81048aa9a161f7881afe19b16519e8e7849dd415\\FTY_2018_010m_de_03035_v010\\FTY_2018_010m_de_03035_v010\\DATA\\FTY_2018_010m_E44N31_03035_v010.tif")
fty11 <- terra::rast("D:\\CliWaC\\02_RAW DATA\\CORINE Forest Type Germany 10m\\81048aa9a161f7881afe19b16519e8e7849dd415\\FTY_2018_010m_de_03035_v010\\FTY_2018_010m_de_03035_v010\\DATA\\FTY_2018_010m_E43N33_03035_v010.tif")

# Create a SpatRasterCollection for merging datasets
raster_list <- list(fty1, fty2, fty3, fty4, fty5, fty6, fty7, fty8, fty9, fty10, fty11)
raster_sprc <- sprc(raster_list)

forest_type <- merge(raster_sprc)

forest_type
plot(forest_type)

# Rasterize vector layer (Brandenburg)
bb_raster <- terra::rasterize(bb, forest_type)
bb_raster
plot(bb_raster)

# Crop forest layer to the extent of bb_raster
forest_type_bb <- terra::crop(forest_type, bb_raster, mask=TRUE)
plot(forest_type_bb)
forest_type_bb

# Write Raster from created forest type layer
gc()
writeRaster(forest_type_bb, filename="D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\fty_bb.tif")

# Create Raster from forest type layer defining the data type to ease processing
gc()
writeRaster(forest_type_bb, filename="D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\fty_bb2.tif", datatype = "INT4U")

fty2_bb <- terra::rast("D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\fty_bb2.tif")
fty2_bb
plot(fty2_bb)

test_fty <- terra::rast("D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\fty_sub.tif")
test_fty
plot(test_fty)


## Create subsets from fty2_bb

# load fty2_bb as raster file from raster package
fty2_bb_ras <- raster::raster("D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\fty_bb2.tif")

# Set the number of rows and columns for subsets
num_rows <- 2
num_cols <- 2

# Calculate the size of each subset
subset_width <- ceiling(ncol(fty2_bb_ras) / num_cols)
subset_height <- ceiling(nrow(fty2_bb_ras) / num_rows)

# Loop through the subsets and create separate raster files
library(raster)
gc()
for (row in 1:num_rows) {
  for (col in 1:num_cols) {
    # Calculate the subset's bounding box
    xmin <- extent(fty2_bb_ras)[1] + (col - 1) * subset_width * res(fty2_bb_ras)[1]
    xmax <- xmin + subset_width * res(fty2_bb_ras)[1]
    ymin <- extent(fty2_bb_ras)[3] + (row - 1) * subset_height * res(fty2_bb_ras)[2]
    ymax <- ymin + subset_height * res(fty2_bb_ras)[2]
    
    # Create the subset raster
    subset_extent <- raster::extent(xmin, xmax, ymin, ymax)
    subset <- crop(fty2_bb_ras, subset_extent)
    
    # Set the output file path
    output_file <- paste0("D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\Subsets\\fty2_bb_subset_", row, "_", col, ".tif")
    
    # Write the subset raster to a new file
    writeRaster(subset, output_file, format = "GTiff", overwrite = TRUE)
  }
}

subset1 <- rast("D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\Subsets\\fty2_bb_subset_1_1.tif")
subset2 <- rast("D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\Subsets\\fty2_bb_subset_1_2.tif")
subset3 <- rast("D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\Subsets\\fty2_bb_subset_2_1.tif")
subset4 <- rast("D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\Subsets\\fty2_bb_subset_2_2.tif")

plot(subset1)
plot(subset2)
plot(subset3)
plot(subset4)



# Create an example 3 class raster
library (terra)
#r <- rast(nrow=40000, ncol=40000)
#r[] <- sample(1:3, ncell(r), replace=TRUE)

raster <- test_fty
gc()
raster[] <- sample(1:3, ncell(raster), replace=TRUE)

# Create an example 3 class raster
sub_raster1 <- subset1
sub_raster2 <- subset2
sub_raster3 <- subset3
sub_raster4 <- subset4
plot(sub_raster1)


# Create subsets for coniferous and for broadleaf forests separately
# Broadleaf
broadleaf_1 <- rast(sub_raster1)
broadleaf_2 <- rast(sub_raster2)
broadleaf_3 <- rast(sub_raster3)
broadleaf_4 <- rast(sub_raster4)

# Set all pixels that are not equal to 1 to 0
broadleaf_1 <- ifel(sub_raster1 == 1,1,0)
broadleaf_2 <- ifel(sub_raster2 == 1,1,0)
broadleaf_3 <- ifel(sub_raster3 == 1,1,0)
broadleaf_4 <- ifel(sub_raster4 == 1,1,0)

# Plot the results (broadleaf)
plot(broadleaf_1)
plot(broadleaf_2)
plot(broadleaf_3)
plot(broadleaf_4)

writeRaster(broadleaf_1, filename = "D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\Subsets\\Broadleaf Forests\\broadleaf_1.tif")
writeRaster(broadleaf_2, filename = "D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\Subsets\\Broadleaf Forests\\broadleaf_2.tif")
writeRaster(broadleaf_3, filename = "D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\Subsets\\Broadleaf Forests\\broadleaf_3.tif")
writeRaster(broadleaf_4, filename = "D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\Subsets\\Broadleaf Forests\\broadleaf_4.tif")

broadleaf_list <- list(broadleaf_1, broadleaf_2, broadleaf_3, broadleaf_4)
broadleaf_merge <- sprc(broadleaf_list)
broadleaf_merged <- merge(broadleaf_merge)
writeRaster(broadleaf_merged, filename = "D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\Subsets\\Broadleaf Forests\\broadleaf_merge.tif")


# Coniferous forest
# Set all pixels that are not equal to 1 to 0
conif_1 <- ifel(sub_raster1 == 2,2,0)
conif_2 <- ifel(sub_raster2 == 2,2,0)
conif_3 <- ifel(sub_raster3 == 2,2,0)
conif_4 <- ifel(sub_raster4 == 2,2,0)

# Plot the results (Coniferous)
plot(conif_1)
plot(conif_2)
plot(conif_3)
plot(conif_4)

writeRaster(conif_1, filename = "D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\Subsets\\Coniferous Forests\\conif_1.tif")
writeRaster(conif_2, filename = "D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\Subsets\\Coniferous Forests\\conif_2.tif")
writeRaster(conif_3, filename = "D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\Subsets\\Coniferous Forests\\conif_3.tif")
writeRaster(conif_4, filename = "D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\Subsets\\Coniferous Forests\\conif_4.tif")


conif_list <- list(conif_1, conif_2, conif_3, conif_4)
conif_merge <- sprc(conif_list)
conif_merged <- merge(conif_merge)
writeRaster(conif_merged, filename = "D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\Subsets\\Coniferous Forests\\conif_merge.tif")


par(mfrow=c(2,1))
plot(broadleaf_merged)
plot(conif_merged)



# Write function that returns percent of class(s). We set the default to 2,3 as to illustrate that there may be more than one class of interest 
# (eg., 2 forest classes). You can simply change the default value(s) to suit your data. 
pclass <- function(x, y=c(0,1)) {
  return( length(which(x %in% y)) / length(x) )
}

# Pass pclass function to focal function thus, returning class percent with a 
# 9x9 window
gc()
( pf <- terra::focal(raster, w=matrix(1, 9, 9), pclass) )
par(mfrow=c(2,1))

plot(raster)
plot(pf)
pf

gc()
( pf <- terra::focal(sub_raster1, w=matrix(1, 9, 9), pclass) )
par(mfrow=c(2,2))
gc()
( pf_subset2 <- terra::focal(sub_raster2, w=matrix(1, 9, 9), pclass) )
gc()
( pf_subset3 <- terra::focal(sub_raster3, w=matrix(1, 9, 9), pclass) )
gc()
( pf_subset4 <- terra::focal(sub_raster4, w=matrix(1, 9, 9), pclass) )


# Plot the resulting subsets
plot(pf)
plot(pf_subset2)
plot(pf_subset3)
plot(pf_subset4)

# Write raster for resulting subsets
library(terra)

terra::writeRaster(pf, filename = "D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\pf_subset1.tif")
terra::writeRaster(pf_subset2, filename = "D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\pf_subset2.tif")
terra::writeRaster(pf_subset3, filename = "D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\pf_subset3.tif")
terra::writeRaster(pf_subset4, filename = "D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\pf_subset4.tif")

gc()
writeRaster(pf, filename = "D:\\CliWaC\\03_PROCESSED DATA\\Forest Type Data\\mvngb_pf.tif", overwrite=TRUE)
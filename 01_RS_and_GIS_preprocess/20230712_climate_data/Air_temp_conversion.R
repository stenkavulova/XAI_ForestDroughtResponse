---
  title: "PET DWD gridded - test"
author: "Stenka Vulova"
date: '2023-03-29'
output:
  pdf_document: default
html_document: default
---
  
  # Libraries 
  
  ```{r libs, include = FALSE }

library(sp)
library(raster)
library(rgdal)
library(lubridate)
library(maptools)
library(ggplot2)
library(tidyr)
library(plyr)
library(dplyr)
library(RColorBrewer)
library(reshape2)
library(scales)
library(readr)
library(rgeos)

library(grid)
library(spatstat)
library(sf)

library(zoo)
library(tictoc) # benchmarking

library(terra)

library(ggspatial)
#library(geobuffer)
library(rgeos)

library(SPEI)

```

# Open the ascii file 

# First I needed to unzip the file. 

# ```{r open the ascii file }

#PET = terra::rast("D:/Stenka_Cliwac/Topic_1/03_RAW_DATA/20230328_PET_DWD_grids/grids_germany_monthly_evapo_p_202206.asc/grids_germany_monthly_evapo_p_202206.asc")

## Load Air Temperature Data as lists
# Specify the directory path
dir_path_01 <- "D:\\CliWaC\\02_RAW DATA\\DWD Data\\Air_temp_mean\\01_JAN"
dir_path_02 <- "D:\\CliWaC\\02_RAW DATA\\DWD Data\\Air_temp_mean\\02_FEB"
dir_path_03 <- "D:\\CliWaC\\02_RAW DATA\\DWD Data\\Air_temp_mean\\03_MAR"
dir_path_04 <- "D:\\CliWaC\\02_RAW DATA\\DWD Data\\Air_temp_mean\\04_APR"
dir_path_05 <- "D:\\CliWaC\\02_RAW DATA\\DWD Data\\Air_temp_mean\\05_MAY"
dir_path_06 <- "D:\\CliWaC\\02_RAW DATA\\DWD Data\\Air_temp_mean\\06_JUN"
dir_path_07 <- "D:\\CliWaC\\02_RAW DATA\\DWD Data\\Air_temp_mean\\07_JUL"
dir_path_08 <- "D:\\CliWaC\\02_RAW DATA\\DWD Data\\Air_temp_mean\\08_AUG"
dir_path_09 <- "D:\\CliWaC\\02_RAW DATA\\DWD Data\\Air_temp_mean\\09_SEP"
dir_path_10 <- "D:\\CliWaC\\02_RAW DATA\\DWD Data\\Air_temp_mean\\10_OCT"
dir_path_11 <- "D:\\CliWaC\\02_RAW DATA\\DWD Data\\Air_temp_mean\\11_NOV"
dir_path_12 <- "D:\\CliWaC\\02_RAW DATA\\DWD Data\\Air_temp_mean\\12_DEC"


## List all the .gz files in the directory
gz_files_01 <- list.files(path = dir_path_01, pattern = "\\.gz$", full.names = TRUE)
gz_files_02 <- list.files(path = dir_path_02, pattern = "\\.gz$", full.names = TRUE)
gz_files_03 <- list.files(path = dir_path_03, pattern = "\\.gz$", full.names = TRUE)
gz_files_04 <- list.files(path = dir_path_04, pattern = "\\.gz$", full.names = TRUE)
gz_files_05 <- list.files(path = dir_path_05, pattern = "\\.gz$", full.names = TRUE)
gz_files_06 <- list.files(path = dir_path_06, pattern = "\\.gz$", full.names = TRUE)
gz_files_07 <- list.files(path = dir_path_07, pattern = "\\.gz$", full.names = TRUE)
gz_files_08 <- list.files(path = dir_path_08, pattern = "\\.gz$", full.names = TRUE)
gz_files_09 <- list.files(path = dir_path_09, pattern = "\\.gz$", full.names = TRUE)
gz_files_10 <- list.files(path = dir_path_10, pattern = "\\.gz$", full.names = TRUE)
gz_files_11 <- list.files(path = dir_path_11, pattern = "\\.gz$", full.names = TRUE)
gz_files_12 <- list.files(path = dir_path_12, pattern = "\\.gz$", full.names = TRUE)

# Unzip .gz files
#test <- lapply(X = files_01, FUN = "gunzip")


## Load Radiation_direct as list
dir_path_radiation <- "D:\\CliWaC\\02_RAW DATA\\DWD Data\\Radiation_direct"

radiation <- list.files(path = dir_path_radiation, pattern = "\\.zip$", full.names = TRUE)
as.list(radiation)

# Define destination file
dest_dir <- "D:\\CliWaC\\02_RAW DATA\\DWD Data\\Radiation_direct\\unzipped"

# Unzip .zip datasets
unzip <- lapply(X = radiation, FUN = unzip, exdir = dest_dir)

for (a in length(radiation[]) {
  unzip(a, overwrite = FALSE, unzip = "internal")
})


print(class(gz_files_01))

install.packages("purr")
library(purr)
walk(gz_files_01, gunzip, destname = "D:\\CliWaC\\03_PROCESSED DATA\\Air Temp Mean\\01_JAN\\test")


install.packages("R.utils")
library(R.utils)

for (f in 1:length(gz_files_01)) {
  gunzip f -a "$f" > "D:\\CliWaC\\03_PROCESSED DATA\\Air Temp Mean\\01_JAN\\${f%.*}" ; done
  } 

for (i in 1:length(tiff_files_2018_1)) {
  eco_raster <- terra::rast(tiff_files_2018_1[i])
  eco_resample <- resample(eco_raster, bb_resample, method = "bilinear")
  eco_stack_2018_1[[i]] <- eco_resample
}

files_01 <- gunzip(dir_path_01, destname = "D:\\CliWaC\\03_PROCESSED DATA\\Air Temp Mean\\01_JAN\\", ext="gz", FUN=gzfile, full.names = TRUE)




terra::plot(PET)

PET # no CRS 

# Values in the grid must be divided by 10 to get correct unit of mm. 
PET1 = PET / 10

terra::plot(PET1)

# Set the CRS
# Gauss Kr̈uger 3. meridian strip.
# 3-degree Gauss-Kruger zone 3, Ellipsoid Bessel, Datum Potsdam (central point Rauenberg), EPSG:31467 (precipitation, but I think they're the same)

terra::crs(PET1) = "epsg:31467"

terra::plot(PET1)

PET1

#class       : SpatRaster 
#dimensions  : 866, 654, 1  (nrow, ncol, nlyr)
#resolution  : 1000, 1000  (x, y)
#extent      : 3280414, 3934414, 5237501, 6103501  (xmin, xmax, ymin, ymax)
#coord. ref. : DHDN / 3-degree Gauss-Kruger zone 3 (EPSG:31467) 
#source      : memory 
#name        : grids_germany_monthly_evapo_p_202206 
#min value   :                                 84.8 
#max value   :                                150.8 

```

# Crop to Brandenburg 

## Import Brandenburg border

```{r import border }

BB_border = readOGR(dsn = "D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_Brandenburg_border",
                    layer = "BB_border_merged")

crs(BB_border)
# CRS arguments: +proj=longlat +datum=WGS84 +no_defs 

plot(BB_border)

crs(PET1)

# reproject the border 
BB_EPSG31467 = spTransform(BB_border, crs(PET1))
# Warning: Discarded datum Deutsches Hauptdreiecksnetz in Proj4 definition

plot(BB_EPSG31467)
crs(BB_EPSG31467)

# save the new shapefile
#writeOGR(BB_EPSG31467, dsn = "D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_Brandenburg_border", 
#         layer = "BB_border_EPSG31467", driver = "ESRI Shapefile")

```

```{r raster plot }

#png("D:/Stenka_Cliwac/Topic_1/06_R_SCRIPTS/20230215_TCD/TCD_over50.png",width = 7, height = 7, units = "in", res = 300)

plot(PET1,
     col=colorRampPalette(c("dark red", "red3", "orange1", 'lightgoldenrod1', "seagreen1", "dodgerblue4", "blue4"))(255), 
     legend.args = list(text = "PET (mm)", line = 0.5, cex = 1, adj = 0.25))
plot(BB_EPSG31467, add = TRUE)

#dev.off()

```

## Crop 

```{r crop }

PET_r = raster::raster(PET1)
plot(PET_r)
PET_r
#class      : RasterLayer 
#dimensions : 866, 654, 566364  (nrow, ncol, ncell)
#resolution : 1000, 1000  (x, y)
#extent     : 3280414, 3934414, 5237501, 6103501  (xmin, xmax, ymin, ymax)
#crs        : +proj=tmerc +lat_0=0 +lon_0=9 +k=1 +x_0=3500000 +y_0=0 +ellps=bessel +units=m +no_defs 
#source     : memory
#names      : grids_germany_monthly_evapo_p_202206 
#values     : 84.8, 150.8  (min, max)


PET_crop = raster::crop(PET_r, BB_EPSG31467)
raster::plot(PET_crop)

PET_mask = raster::mask(PET_crop, BB_EPSG31467)
raster::plot(PET_mask)

PET_mask

#raster::writeRaster(PET_mask, "D:/Stenka_Cliwac/Topic_1/06_R_SCRIPTS/20230329_DWD_gridded_test/PET_mask.tif", options='COMPRESS=LZW')

```

# 5 km buffer

Similar to Christian's Google Earth Engine code, I will buffer the Brandenburg shapefile by 5 km. (Better not to have weird missing pixels near the border)

```{r 5 km buffer }
# Load required libraries
#library(rgdal)
#library(rgeos)

# Create a buffer of 5 km
BB_5km_buffer <- gBuffer(BB_EPSG31467, byid = TRUE, width = 5000)

plot(BB_5km_buffer)

# save the new shapefile
#writeOGR(BB_5km_buffer, dsn = "D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230214_Brandenburg_border/5km_buffer", 
#         layer = "BB_5km_buffer_EPSG31467", driver = "ESRI Shapefile")

# Looks good in QGIS

```

## Crop with 5 km buffer 

```{r crop with 5km buffer }

PET_5km_crop = raster::crop(PET_r, BB_5km_buffer)
raster::plot(PET_5km_crop)

PET_5km_mask = raster::mask(PET_5km_crop, BB_5km_buffer)
raster::plot(PET_5km_mask)

PET_5km_mask

#class      : RasterLayer 
#dimensions : 255, 258, 65790  (nrow, ncol, ncell)
#resolution : 1000, 1000  (x, y)
##extent     : 3646414, 3904414, 5697501, 5952501  (xmin, xmax, ymin, ymax)
#crs        : +proj=tmerc +lat_0=0 +lon_0=9 +k=1 +x_0=3500000 +y_0=0 +ellps=bessel +units=m +no_defs 
#source     : memory
#names      : grids_germany_monthly_evapo_p_202206 
#values     : 122.9, 150.5  (min, max)

#raster::writeRaster(PET_5km_mask, "D:/Stenka_Cliwac/Topic_1/06_R_SCRIPTS/20230329_DWD_gridded_test/PET_5km_mask.asc", format = "ascii") 
# 380 KB
# Germany-wide asc file was 3.24 MB. 

# test saving as a .tif
#raster::writeRaster(PET_5km_mask, "D:/Stenka_Cliwac/Topic_1/06_R_SCRIPTS/20230329_DWD_gridded_test/PET_5km_mask.tif", options='COMPRESS=LZW') 
# 56 KB! wow, it's smaller.
# tif has the smallest data size...

```


```{r 5km raster plot }

#png("D:/Stenka_Cliwac/Topic_1/06_R_SCRIPTS/20230215_TCD/TCD_over50.png",width = 7, height = 7, units = "in", res = 300)

plot(PET_5km_mask,
     col=colorRampPalette(c("dark red", "red3", "orange1", 'lightgoldenrod1', "seagreen1", "dodgerblue4", "blue4"))(255), 
     legend.args = list(text = "PET (mm)", line = 0.5, cex = 1, adj = 0.25))
plot(BB_5km_buffer, add = TRUE)

#dev.off()

# The right buffer side is missing because it's the border of Germany! 

```
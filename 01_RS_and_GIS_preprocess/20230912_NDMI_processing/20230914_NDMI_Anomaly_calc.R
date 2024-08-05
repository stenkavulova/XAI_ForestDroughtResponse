
# Calculation of NDMI Anomaly Rasters (in %) ----
# Katharina Horn
# Date: 12/09/2023

## Prepare Workspace and load files ----
# Load packages
library(terra)

# Set working directory
setwd("C:\\Users\\ka_horn\\Nextcloud\\Documents\\CliWaC")

# Load NDMI files
NDMI_2013 <- terra::rast(".\\04_PROCESSED DATA\\NDMI\\BB_NDMI_2013.tif")
NDMI_2014 <- terra::rast(".\\04_PROCESSED DATA\\NDMI\\BB_NDMI_2014.tif")
NDMI_2015 <- terra::rast(".\\04_PROCESSED DATA\\NDMI\\BB_NDMI_2015.tif")
NDMI_2016 <- terra::rast(".\\04_PROCESSED DATA\\NDMI\\BB_NDMI_2016.tif")
NDMI_2017 <- terra::rast(".\\04_PROCESSED DATA\\NDMI\\BB_NDMI_2017.tif")


###########################################################################################################################
## Step 1: Calculate NDMI Mean for 2013 to 2017-----

# Create average for NDMI_2013 to NDMI_2017 to create a reference .tif file for further processing
# Calculate the mean of the stacked rasters
mean_raster <- terra::mean(NDMI_2013, NDMI_2014, NDMI_2015, NDMI_2016, NDMI_2017, na.rm = TRUE)
plot(mean_raster)

# Save the mean raster to a file if needed
writeRaster(mean_raster, filename = ".\\04_PROCESSED DATA\\NDMI\\mean_NDMI_2013_to_2017.tif", overwrite = TRUE)

# Read resulting file to check
mean_result <- terra::rast(".\\04_PROCESSED DATA\\NDMI\\mean_NDMI_2013_to_2017.tif")

# Optional: Plot the mean raster
par(mfrow=c(1,1))
plot(mean_result, main = "Mean NDMI for 2013 to 2017")
summary(mean_result)
# 56042 NA values

###########################################################################################################################
## Step 2: Calculate NDMI Anomaly (in %) for each year from 2018 to 2022-----
# Load NDMI files
NDMI_2018 <- terra::rast(".\\04_PROCESSED DATA\\NDMI\\BB_NDMI_2018.tif")
NDMI_2018 <- mask(NDMI_2018, is.na(NDMI_2018))
NDMI_2019 <- terra::rast(".\\04_PROCESSED DATA\\NDMI\\BB_NDMI_2019.tif")
NDMI_2019 <- mask(NDMI_2019, is.na(NDMI_2019))
NDMI_2020 <- terra::rast(".\\04_PROCESSED DATA\\NDMI\\BB_NDMI_2020.tif")
NDMI_2020 <- mask(NDMI_2020, is.na(NDMI_2020))
NDMI_2021 <- terra::rast(".\\04_PROCESSED DATA\\NDMI\\BB_NDMI_2021.tif")
NDMI_2021 <- mask(NDMI_2021, is.na(NDMI_2021))
NDMI_2022 <- terra::rast(".\\04_PROCESSED DATA\\NDMI\\BB_NDMI_2022.tif")
NDMI_2022 <- mask(NDMI_2022, is.na(NDMI_2022))

# Create a new mean_result raster that contains -1 for all negative values and +1 for all positive values
# Step 1: Assign -1 to all raster cells that contain a negative value
mean_result_invert <- ifel(mean_result < 0, -1, mean_result)
plot(mean_result_invert)

# Step 2: Assign +1 to all raster cells that contain a positive value
mean_result_inverted <- ifel(mean_result_invert > 0, 1, mean_result_invert)
mean_result_inverted <- mask(mean_result_inverted, is.na(mean_result_inverted))

# Display or save the resulting raster as needed
par(mfrow=c(1,2))
plot(mean_result_inverted)
hist(mean_result_inverted)

# Save inverted raster 
writeRaster(mean_result_inverted, ".\\04_PROCESSED DATA\\NDMI\\mask_raster_NDMI.tif", overwrite = TRUE)

# First: Work out the difference (increase) between the two numbers you are comparing.
# Increase = New Number - Original Number
# Then: Multiply resulting difference layer by 100 for %
NDMI_2018_anom <- ((NDMI_2018 - mean_result) / mean_result) * 100
NDMI_2019_anom <- ((NDMI_2019 - mean_result) / mean_result) * 100
NDMI_2020_anom <- ((NDMI_2020 - mean_result) / mean_result) * 100
NDMI_2021_anom <- ((NDMI_2021 - mean_result) / mean_result) * 100
NDMI_2022_anom <- ((NDMI_2022 - mean_result) / mean_result) * 100

NDMI_2018_anom_final <- mean_result_inverted*NDMI_2018_anom
NDMI_2019_anom_final <- mean_result_inverted*NDMI_2019_anom
NDMI_2020_anom_final <- mean_result_inverted*NDMI_2020_anom
NDMI_2021_anom_final <- mean_result_inverted*NDMI_2021_anom
NDMI_2022_anom_final <- mean_result_inverted*NDMI_2022_anom

par(mfrow=c(1,2))
plot(NDMI_2018_anom, main = "NDMI anomaly for 2018 without mask")
plot(NDMI_2018_anom_final, main = "NDMI anomaly for 2018 with mask")

plot(NDMI_2019_anom, main = "NDMI anomaly for 2019 without mask")
plot(NDMI_2019_anom_final, main = "NDMI anomaly for 2019 with mask")

plot(NDMI_2020_anom, main = "NDMI anomaly for 2020 without mask")
plot(NDMI_2020_anom_final, main = "NDMI anomaly for 2020 with mask")

plot(NDMI_2021_anom, main = "NDMI anomaly for 2021 without mask")
plot(NDMI_2021_anom_final, main = "NDMI anomaly for 2021 with mask")

plot(NDMI_2022_anom, main = "NDMI anomaly for 2022 without mask")
plot(NDMI_2022_anom_final, main = "NDMI anomaly for 2022 with mask")

par(mfrow=c(2,3))
plot(NDMI_2018_anom_final, main = "NDMI Anomaly for 2018")
plot(NDMI_2019_anom_final, main = "NDMI Anomaly for 2019")
plot(NDMI_2020_anom_final, main = "NDMI Anomaly for 2020")
plot(NDMI_2021_anom_final, main = "NDMI Anomaly for 2021")
plot(NDMI_2022_anom_final, main = "NDMI Anomaly for 2022")


# Check number of NA values
summary(mean_result)
# mean_raster has 56042 NA's 
summary(NDMI_2018_anom_final)
# NDMI_2018_anom has 56212 NA's (170 additional NA's)
summary(NDMI_2019_anom_final)
# NDMI_2019_anom has 56059 NA's (17 additional NA's)
summary(NDMI_2020_anom_final)
# NDMI_2020_anom has 56060 NA's (18 additional NA's)
summary(NDMI_2021_anom_final)
# NDMI_2021_anom has 60074 NA's (4032 additional NA's)
summary(NDMI_2022_anom_final)
# NDMI_2022_anom has 56064 NA's (22 additional NA's)


# Write Rasters with anomalies for each year
writeRaster(NDMI_2018_anom_final, ".\\04_PROCESSED DATA\\NDMI\\Anomaly Rasters wo TCD\\NDMI_2018_anom.tif", overwrite = TRUE)
writeRaster(NDMI_2019_anom_final, ".\\04_PROCESSED DATA\\NDMI\\Anomaly Rasters wo TCD\\NDMI_2019_anom.tif", overwrite = TRUE)
writeRaster(NDMI_2020_anom_final, ".\\04_PROCESSED DATA\\NDMI\\Anomaly Rasters wo TCD\\NDMI_2020_anom.tif", overwrite = TRUE)
writeRaster(NDMI_2021_anom_final, ".\\04_PROCESSED DATA\\NDMI\\Anomaly Rasters wo TCD\\NDMI_2021_anom.tif", overwrite = TRUE)
writeRaster(NDMI_2022_anom_final, ".\\04_PROCESSED DATA\\NDMI\\Anomaly Rasters wo TCD\\NDMI_2022_anom.tif", overwrite = TRUE)


###########################################################################################################################
## Step 3: Include TCD Raster file to exclude non-forest areas from the anomaly rasters-----

# Load TCD raster
tcd <- terra::rast(".\\04_PROCESSED DATA\\TCD\\TCD_over50_resampNDMI.tif")

# Assign all values above 50% as 1 and all below to NA
tcd_modif <- ifel(tcd <= 50, NA, 1)
plot(tcd_modif)

# Resample tcd_modif to the anomaly rasters
tcd_final <- terra::resample(tcd_modif, NDMI_2018_anom, method = "bilinear")

# Extract only forested areas from anomaly rasters using tcd_modif as a masking file
# Extract by Mask (tcd_modif)
anom_2018_tcd <- mask(NDMI_2018_anom_final, mask = tcd_final)
anom_2019_tcd <- mask(NDMI_2019_anom_final, mask = tcd_final)
anom_2020_tcd <- mask(NDMI_2020_anom_final, mask = tcd_final)
anom_2021_tcd <- mask(NDMI_2021_anom_final, mask = tcd_final)
anom_2022_tcd <- mask(NDMI_2022_anom_final, mask = tcd_final)

par(mfrow=c(2,3))
plot(anom_2018_tcd, main = "NDMI Anomaly 2018 in forested areas in %")
plot(anom_2019_tcd, main = "NDMI Anomaly 2019 in forested areas in %")
plot(anom_2020_tcd, main = "NDMI Anomaly 2020 in forested areas in %")
plot(anom_2021_tcd, main = "NDMI Anomaly 2021 in forested areas in %")
plot(anom_2022_tcd, main = "NDMI Anomaly 2022 in forested areas in %")

# Check out histograms for the anomaly rasters
terra::hist(anom_2018_tcd, main = "Anomaly Values for 2018", xlim = range(-1000,1000), breaks = "Sturges")
terra::hist(anom_2019_tcd, main = "Anomaly Values for 2019", xlim = range(-1000,1000), breaks = "Sturges")
terra::hist(anom_2020_tcd, main = "Anomaly Values for 2020", xlim = range(-1000,1000), breaks = "Sturges")
terra::hist(anom_2021_tcd, main = "Anomaly Values for 2021", xlim = range(-1000,1000), breaks = "Sturges")
terra::hist(anom_2022_tcd, main = "Anomaly Values for 2022", xlim = range(-1000,1000), breaks = "Sturges")

# Write Rasters with anomalies in forested areas
writeRaster(anom_2018_tcd, ".\\04_PROCESSED DATA\\NDMI\\Anomaly Rasters with TCD\\NDMI_2018_anom_forest.tif", overwrite = TRUE)
writeRaster(anom_2019_tcd, ".\\04_PROCESSED DATA\\NDMI\\Anomaly Rasters with TCD\\NDMI_2019_anom_forest.tif", overwrite = TRUE)
writeRaster(anom_2020_tcd, ".\\04_PROCESSED DATA\\NDMI\\Anomaly Rasters with TCD\\NDMI_2020_anom_forest.tif", overwrite = TRUE)
writeRaster(anom_2021_tcd, ".\\04_PROCESSED DATA\\NDMI\\Anomaly Rasters with TCD\\NDMI_2021_anom_forest.tif", overwrite = TRUE)
writeRaster(anom_2022_tcd, ".\\04_PROCESSED DATA\\NDMI\\Anomaly Rasters with TCD\\NDMI_2022_anom_forest.tif", overwrite = TRUE)

# Create a raster stack with the anomaly rasters for 2018 to 2022
anomaly_stack <- c(anom_2018_tcd, anom_2019_tcd, anom_2020_tcd, anom_2021_tcd, anom_2022_tcd)

# Change names so that the layers are assigned with the correct year
names(anomaly_stack) <- c("anomaly_2018", "anomaly_2019", "anomaly_2020", "anomaly_2021", "anomaly_2022")
print(anomaly_stack)

# Write Raster for anomaly raster stack
writeRaster(anom_2022_tcd, ".\\04_PROCESSED DATA\\NDMI\\Anomaly Rasters with TCD\\NDMI_anomaly_forest_stack.tif", overwrite = TRUE)
plot(anomaly_stack)

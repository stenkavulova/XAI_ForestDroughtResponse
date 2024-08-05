#### LST MODIS Data Postprocessing
# Katharina Horn
# 08th September, 2023

library(terra)

# Load raster
LST_2017 <- rast("D:\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\LST\\all_without_NA\\HighestMeanLST_2017_06_18.tif")
LST_2018 <- rast("D:\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\LST\\all_without_NA\\HighestMeanLST_2018_07_28.tif")
LST_2019 <- rast("D:\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\LST\\all_without_NA\\HighestMeanLST_2019_06_26.tif")
LST_2020 <- rast("D:\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\LST\\all_without_NA\\HighestMeanLST_2020_08_04.tif")
LST_2021 <- rast("D:\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\LST\\all_without_NA\\HighestMeanLST_2021_06_18.tif")
LST_2022 <- rast("D:\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\LST\\all_without_NA\\HighestMeanLST_2022_07_20.tif")

# Assigning NA values to cells with a value of 0
LST_2017_NA <- ifel(LST_2017 == 0, NA, LST_2017)
LST_2018_NA <- ifel(LST_2018 == 0, NA, LST_2018)
LST_2019_NA <- ifel(LST_2019 == 0, NA, LST_2019)
LST_2020_NA <- ifel(LST_2020 == 0, NA, LST_2020)
LST_2021_NA <- ifel(LST_2021 == 0, NA, LST_2021)
LST_2022_NA <- ifel(LST_2022 == 0, NA, LST_2022)

# Plot results
plot(LST_2017_NA)

# Add scaling factor of 0.02
LST_2017_sf <- LST_2017_NA*0.02
LST_2018_sf <- LST_2018_NA*0.02
LST_2019_sf <- LST_2019_NA*0.02
LST_2020_sf <- LST_2020_NA*0.02
LST_2021_sf <- LST_2021_NA*0.02
LST_2022_sf <- LST_2022_NA*0.02

# Convert values from Kelvin to Celsius
LST_2017_Celsius <- LST_2017_sf-273.15
LST_2018_Celsius <- LST_2018_sf-273.15
LST_2019_Celsius <- LST_2019_sf-273.15
LST_2020_Celsius <- LST_2020_sf-273.15
LST_2021_Celsius <- LST_2021_sf-273.15
LST_2022_Celsius <- LST_2022_sf-273.15


# Change name of the layers
names(LST_2017_Celsius) <- "LST_2017_06_18" 
names(LST_2018_Celsius) <- "LST_2018_07_28" 
names(LST_2019_Celsius) <- "LST_2019_06_26" 
names(LST_2020_Celsius) <- "LST_2020_08_04" 
names(LST_2021_Celsius) <- "LST_2021_06_18" 
names(LST_2022_Celsius) <- "LST_2022_07_20" 

# Stack LST images
LST_BB <- c(LST_2017_Celsius, LST_2018_Celsius, LST_2019_Celsius, LST_2020_Celsius, LST_2021_Celsius, LST_2022_Celsius)
plot(LST_BB)

# write new raster files
writeRaster(LST_BB, "D:\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\LST\\LST_BB_stack.tif")

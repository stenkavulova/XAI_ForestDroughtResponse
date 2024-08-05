
############################################################################################################
################                                Processing NDMI data                        ################
############################################################################################################


#### Move files to one single folder
# Load the terra library
library(terra)

# Define the source folder path
parent_folder_2022 <- "D:\\Docker\\force\\processed_data\\Cliwac_NDMI\\Cliwac_NDMI_2022"

# Define the destination folder path
destination_folder <- "D:/Docker/force/processed_data/cliwac_NDMI/cliwac_all/2022"

# List all subdirectories in the parent folder
subdirs_2022 <- list.dirs(parent_folder_2022, full.names = TRUE, recursive = FALSE)

# Filter subdirectories that start with "X00"
x00_subdirs_2022 <- subdirs_2022[grep("^X00", basename(subdirs_2022))]
tif_files_list <- list()

# Loop through the x00_subdirs and list .tif files
for (x00_dir in x00_subdirs_2022) {
  tif_files <- list.files(x00_dir, pattern = "\\.tif$", full.names = TRUE)
  tif_files_list <- append(tif_files_list, tif_files)
}

# Loop through the tif_files_list and move each .tif file to the destination folder
for (tif_file in tif_files_list) {
  # Construct the destination file path in the destination folder
  destination_file <- file.path(destination_folder, basename(tif_file))
  
  # Ensure the destination file doesn't already exist; if it does, add a numerical suffix
  if (file.exists(destination_file)) {
    i <- 1
    while (file.exists(destination_file)) {
      i <- i + 1
      destination_file <- gsub(".tif$", paste0("_", i, ".tif"), destination_file)
    }
  }
  
  # Copy the .tif file to the destination folder
  file.copy(tif_file, destination_file)
}

# Read in Raster files
raster_files <- lapply(tif_files_list, terra::rast)
spatrastcoll <- sprc(raster_files)
merged_raster <- terra::merge(spatrastcoll)

# Correct the scaling factor
new_raster <- merged_raster/10000
plot(new_raster)

# Define the output file path and name
output_path <- "D:\\Docker\\force\\processed_data\\cliwac_NDMI\\cliwac_all\\BB_NDMI_2022.tif"

# Save the 'new_raster' as a .tif file
terra::writeRaster(new_raster, filename = output_path, overwrite = TRUE)

# Define the folder path containing "BB_NDMI_" tif files
folder_path <- "D:/Docker/force/processed_data/cliwac_NDMI/cliwac_all"

# List all the "BB_NDMI_" tif files in the folder
tif_files_list <- list.files(folder_path, pattern = "^BB_NDMI_", full.names = TRUE)

# Create a list of raster objects from the tif files
raster_list <- lapply(tif_files_list, function(file) terra::rast(file))

r_2013 <- rast(raster_list[1])
r_2014 <- rast(raster_list[2])
r_2015 <- rast(raster_list[3])
r_2016 <- rast(raster_list[4])
r_2017 <- rast(raster_list[5])
r_2018 <- rast(raster_list[6])
r_2019 <- rast(raster_list[7])
r_2020 <- rast(raster_list[8])
r_2021 <- rast(raster_list[9])
r_2022 <- rast(raster_list[10])


par(mfrow = c(2,5))
plot(r_2013)  
plot(r_2014)  
plot(r_2015)  
plot(r_2016)  
plot(r_2017)  
plot(r_2018)  
plot(r_2019)  
plot(r_2020)  
plot(r_2021)  
plot(r_2022)

  
# Stack the raster objects into a single raster
stacked_raster <- c(r_2013,r_2014,r_2015,r_2016,r_2017,r_2018,r_2019,r_2020,r_2021,r_2022)

# Print information about the stacked raster
print(stacked_raster)

# Get the number of layers in the stacked raster
num_layers <- nlyr(stacked_raster)

# Generate new layer names based on your desired naming convention
new_layer_names <- paste0("BB_NDMI_", 2013:(2013 + num_layers - 1), ".tif")

# Assign the new layer names to the stacked raster
names(stacked_raster) <- new_layer_names

# Print the updated stacked raster with new names
print(stacked_raster)

# Define the output file path and name
output_path_final <- "D:\\Docker\\force\\processed_data\\cliwac_NDMI\\cliwac_all\\BB_NDMI_stack.tif"

# Export the stacked raster to a multi-layer GeoTIFF file
terra::writeRaster(stacked_raster, filename = output_path_final, overwrite = TRUE)

test <- terra::rast("D:\\Docker\\force\\processed_data\\cliwac_NDMI\\cliwac_all\\BB_NDMI_stack.tif")
plot(test)
test


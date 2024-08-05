

############################################################
#####          Processing Sentinel-2 Data          #########
############################################################

# Katharina Horn
# 09th August 2023

# Load packages
library("sp")
library("terra")
library("geodata")
library("sf")
library("rgdal")
library("dplyr")
library("purrr")
library("tidyr")


# Set working directory
setwd("D:\\Docker\\force\\processed_data\\cliwac_ndvi\\")

## Load data
# Set the path to the parent folder containing the X00 folders
parent_folder <- "D:/Docker/force/processed_data/cliwac_ndvi"

# Load Brandenburg as mask for the stacking and mosaicking of the Sentinel-2 .tif files
bb_5km_3035 <- terra::rast("D:\\CliWaC\\03_PROCESSED DATA\\Brandenburg\\BB_5km_10m_res_3035.tif")
test_file_1 <- terra::rast("D:\\Docker\\force\\processed_data\\cliwac_ndvi\\X0065_Y0041\\2017-2022_182-243_HL_TSA_SEN2L_NDV_TSS.tif")
nlyr(test_file_1)

bb_5km_3035

bbmask <- terra::rast("D:\\CliWaC\\03_PROCESSED DATA\\Brandenburg\\BB_mask.tif")
bbmask

test_file_2 <- terra::rast("D:\\Docker\\force\\processed_data\\cliwac_ndvi\\X0067_Y0043\\2017-2022_182-243_HL_TSA_SEN2L_NDV_TSS.tif")
nlyr(test_file_2)
list(names(test_file_2))

# List all subdirectories in the parent folder
subdirs <- list.dirs(parent_folder, full.names = TRUE, recursive = FALSE)

# Filter subdirectories that start with "X00"
x00_subdirs <- subdirs[grep("^X00", basename(subdirs))]

tif_files_list <- list()

# Loop through the x00_subdirs and list .tif files
for (x00_dir in x00_subdirs) {
  tif_files <- list.files(x00_dir, pattern = "\\.tif$", full.names = TRUE)
  tif_files_list <- append(tif_files_list, tif_files)
}

# Resample the first tif file from the list of tif files
file1 <- rast(tif_files_list[[1]])
file2 <- rast(tif_files_list[[2]])
file3 <- rast(tif_files_list[[3]])
file4 <- rast(tif_files_list[[4]])
file5 <- rast(tif_files_list[[5]])
file6 <- rast(tif_files_list[[6]])
file7 <- rast(tif_files_list[[7]])
file8 <- rast(tif_files_list[[8]])
file9 <- rast(tif_files_list[[9]])
file10 <- rast(tif_files_list[[10]])

nlyr(file1) #62
nlyr(file2) #65
nlyr(file3) #65
nlyr(file4) #71
nlyr(file5) #69
nlyr(file6) #66
nlyr(file7) #64
nlyr(file8) #63
nlyr(file9) #88
nlyr(file10) #64


# Resample file1 to match the grid of bb_5km_3035
gc()
resampled_file1 <- resample(file1, bb_5km_3035, method = "bilinear")

gc()
resampled_file2 <- resample(file2, bb_5km_3035, method = "bilinear")

gc()
resampled_file3 <- resample(file3, bb_5km_3035, method = "bilinear")

gc()
resampled_file4 <- resample(file4, bb_5km_3035, method = "bilinear")

gc()
resampled_file5 <- resample(file5, bb_5km_3035, method = "bilinear")

gc()
resampled_file6 <- resample(file6, bb_5km_3035, method = "bilinear")

gc()
resampled_file7 <- resample(file7, bb_5km_3035, method = "bilinear")

gc()
resampled_file8 <- resample(file8, bb_5km_3035, method = "bilinear")

gc()
resampled_file9 <- resample(file9, bb_5km_3035, method = "bilinear")

gc()
resampled_file10 <- resample(file10, bb_5km_3035, method = "bilinear")


# Print the number of layers in the resampled raster
nlyr(resampled_file1)
nlyr(resampled_file2)
nlyr(resampled_file3) #65
nlyr(resampled_file4)
nlyr(resampled_file5)
nlyr(resampled_file6)
nlyr(resampled_file7)
nlyr(resampled_file8)
nlyr(resampled_file9)
nlyr(resampled_file10)

plot(resampled_file1)

# Save the resampled raster to a new file
output_file_1 <- "D:\\CliWaC\\03_PROCESSED DATA\\Sentinel_NDVI_resampled\\tile1_resample.tif"
writeRaster(resampled_file1, output_file_1)
output_file_2 <- "D:\\CliWaC\\03_PROCESSED DATA\\Sentinel_NDVI_resampled\\tile2_resample.tif"
writeRaster(resampled_file2, output_file_2)
output_file_3 <- "D:\\CliWaC\\03_PROCESSED DATA\\Sentinel_NDVI_resampled\\tile3_resample.tif"
writeRaster(resampled_file3, output_file_3)
output_file_4 <- "D:\\CliWaC\\03_PROCESSED DATA\\Sentinel_NDVI_resampled\\tile4_resample.tif"
writeRaster(resampled_file4, output_file_4)
output_file_5 <- "D:\\CliWaC\\03_PROCESSED DATA\\Sentinel_NDVI_resampled\\tile5_resample.tif"
writeRaster(resampled_file5, output_file_5)
output_file_6 <- "D:\\CliWaC\\03_PROCESSED DATA\\Sentinel_NDVI_resampled\\tile6_resample.tif"
writeRaster(resampled_file6, output_file_6)
output_file_7 <- "D:\\CliWaC\\03_PROCESSED DATA\\Sentinel_NDVI_resampled\\tile7_resample.tif"
writeRaster(resampled_file7, output_file_7)
output_file_8 <- "D:\\CliWaC\\03_PROCESSED DATA\\Sentinel_NDVI_resampled\\tile8_resample.tif"
writeRaster(resampled_file8, output_file_8)
output_file_9 <- "D:\\CliWaC\\03_PROCESSED DATA\\Sentinel_NDVI_resampled\\tile9_resample.tif"
writeRaster(resampled_file9, output_file_9)
output_file_10 <- "D:\\CliWaC\\03_PROCESSED DATA\\Sentinel_NDVI_resampled\\tile10_resample.tif"
writeRaster(resampled_file10, output_file_10)

test2 <- terra::rast("D:\\CliWaC\\03_PROCESSED DATA\\Sentinel_NDVI_resampled\\tile2_resample.tif")
print(test2)
plot(test)

# Combine the file paths into a single vector
all_tif_files <- unlist(tif_files_list)
all_tif_files

# Divide files into batches of 5
file_batches <- split(all_tif_files, ceiling(seq_along(all_tif_files)/5))

# Initialize an empty list to store mosaics
all_final_mosaics <- list()

library(terra)

gc()
# Loop through batches of files
for (batch_idx in seq_along(file_batches)) {
  file_batch <- file_batches[[batch_idx]]
  
  # Initialize an empty list to store resampled stacks for this batch
  resampled_stacks <- list()
  
  # Loop through files in the batch
  for (file_path in file_batch) {
    raster_stack <- rast(file_path)
    
    # Resample each layer in the stack and store in a list
    resampled_layers <- list()
    for (layer_idx in 1:nlyr(raster_stack)) {
      layer <- raster_stack[[layer_idx]]
      resampled_layer <- resample(layer, bb_5km_3035, method = "bilinear")
      resampled_layers[[layer_idx]] <- resampled_layer
    }
    
    # Create a raster stack from the resampled layers
    resampled_stack <- rast(resampled_layers)
    
    # Store the resampled stack for this file
    resampled_stacks <- append(resampled_stacks, list(resampled_stack))
  }
  
  # Merge all resampled stacks of this batch
  batch_final_mosaic <- terra::merge(resampled_stacks)
  
  # Add the batch mosaic to the list of all final mosaics
  all_final_mosaics <- append(all_final_mosaics, list(batch_final_mosaic))
}

# Merge all final mosaics together
final_mosaic <- terra::merge(all_final_mosaics)

# Save the final mosaic to disk
writeRaster(final_mosaic, filename = "path/to/output/mosaic.tif", overwrite = TRUE)


-------------
# Initialize lists to store directory and filename data
directories <- character(0)
filenames <- list()

# List .tif files within each X00 subdirectory and store data
for (x00_dir in x00_subdirs) {
  files <- list.files(x00_dir, pattern = "\\.tif$", full.names = TRUE)
  directories <- c(directories, basename(x00_dir))
  filenames[[basename(x00_dir)]] <- files
}

# Create a dataframe from the collected data
df <- data.frame(Directory = directories, stringsAsFactors = FALSE) %>%
  mutate(Files = map_chr(Directory, ~ paste(filenames[[.x]], collapse = ", ")))


# Print the resulting dataframe
print(df)
---------------------
  
# Iterate through the .tif files and print coordinate system information
#for (file_path in unlist(strsplit(df$Files, ", "))) {
#  cat("File:", file_path, "\n")
#  raster_obj <- rast(file_path)
#  crs_info <- crs(raster_obj)
#  cat("Coordinate System:\n", crs_info, "\n\n")
#}

# CRS is 3035

# Print the coordinate system information from the Brandenburg mask .tif
print(crs(bb_5km_3035))
# crs is indeed 3035

print(res(bb_5km_3035))
# resolution is 10x10m


### Create empty stack with Brandenburg as mask file
bb_mask_stack <- terra::rast(nrow=nrow(bb_5km_3035), 
                              ncol=ncol(bb_5km_3035),
                              extent=ext(bb_5km_3035),
                              resolution=res(bb_5km_3035),
                              nl=length(all_tif_files),
                              crs=crs(bb_5km_3035))
bb_mask_stack


# Loop through each raster file and resample it to the template raster
gc()
for (i in 1:length(all_tif_files)) {
  sentinel_ndvi_raster <- terra::rast(all_tif_files[i])
  sentinel_ndvi_resample <- resample(sentinel_ndvi_raster, bb_5km_3035, method = "bilinear")
  bb_mask_stack[[i]] <- sentinel_ndvi_resample
}

bb_mask_stack

# Create output paths for saving the raster stacks
output_path <- "D:\\CliWaC\\03_PROCESSED DATA\\Docker Processed Data\\result_mosaic_ndvi"
output_file_ndvi <- file.path(output_path, "ndvi_sentinel_stack.tif")

# Write rasters out of the stacked raster files for each year and then combined
gc()
raster::writeRaster(bb_mask_stack, filename=output_file_2018)
result_check_2018 <- terra::rast("C:\\Users\\ka_horn\\tubCloud\\Documents\\CliWaC\\Data\\R-Scripts\\Results\\ndvi_sentinel_stack.tif")
plot(result_check_2018)
print(result_check_2018)












##### Mosaicking the .tif files together
library(terra)

# List of file paths from the dataframe
file_paths <- df$Files  

# Set the desired CRS
desired_crs <-  crs("+init=EPSG:3035")

# Set output directory for intermediate results
output_dir <- "D:\\CliWaC\\03_PROCESSED DATA\\NDVI_S2_2017-to-2022"

# Create the output directory if it doesn't exist
#dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

# Batch size (number of files to process in each iteration)
batch_size <- 5

gc()
# Process the files in batches
for (i in seq(1, length(file_paths), by = batch_size)) {
  batch_paths <- file_paths[i:min(i + batch_size - 1, length(file_paths))]
  
  # Open all raster files in the batch using rast() and set the desired CRS
  raster_list <- lapply(batch_paths, function(path) {
    r <- rast(path)
    crs(r) <- desired_crs
    return(r)
  })
  
  # Merge the raster files
  merged_raster <- terra::merge(raster_list)
  
  # Generate a unique name for the intermediate mosaic
  mosaic_name <- paste0("mosaic_", i, ".tif")
  
  # Save the intermediate mosaic to disk
  writeRaster(merged_raster, filename = file.path(output_dir, mosaic_name), overwrite = FALSE)
}

# After processing all batches, merge the intermediate mosaics
intermediate_mosaics <- list.files(output_dir, pattern = "mosaic_", full.names = TRUE)
final_merged_raster <- terra::merge(intermediate_mosaics)

# Output file path for the final merged raster
final_merged_file_path <- "path_to_output/final_merged.tif"  # Replace with your desired output file path

# Save the final merged raster to a file
writeRaster(final_merged_raster, filename = final_merged_file_path, overwrite = TRUE)

# Clean up intermediate files if needed
# file.remove(intermediate_mosaics)

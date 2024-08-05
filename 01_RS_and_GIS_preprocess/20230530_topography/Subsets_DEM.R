########################################################
## Calculate Subsets from DEM to ease data processing ##
########################################################

library(raster)

# Set the number of rows and columns for subsets
num_rows <- 2
num_cols <- 2

# Read the raster data
raster_data <- raster("D:/CliWaC/02_RAW DATA/DEM/DEM_mosaic_10m_Brandenburg.tif")

# Calculate the size of each subset
subset_width <- ceiling(ncol(raster_data) / num_cols)
subset_height <- ceiling(nrow(raster_data) / num_rows)

# Loop through the subsets and create separate raster files
for (row in 1:num_rows) {
  for (col in 1:num_cols) {
    # Calculate the subset's bounding box
    xmin <- extent(raster_data)[1] + (col - 1) * subset_width * res(raster_data)[1]
    xmax <- xmin + subset_width * res(raster_data)[1]
    ymin <- extent(raster_data)[3] + (row - 1) * subset_height * res(raster_data)[2]
    ymax <- ymin + subset_height * res(raster_data)[2]
    
    # Create the subset raster
    subset_extent <- extent(xmin, xmax, ymin, ymax)
    subset <- crop(raster_data, subset_extent)
    
    # Set the output file path
    output_file <- paste0("D:/CliWaC/02_RAW DATA/DEM/DEM_subset_", row, "_", col, ".tif")
    
    # Write the subset raster to a new file
    writeRaster(subset, output_file, format = "GTiff", overwrite = TRUE)
  }
}

subset1 <- rast("D:/CliWaC/02_RAW DATA/DEM/DEM_subset_1_1.tif")
subset2 <- rast("D:/CliWaC/02_RAW DATA/DEM/DEM_subset_1_2.tif")
subset3 <- rast("D:/CliWaC/02_RAW DATA/DEM/DEM_subset_2_1.tif")
subset4 <- rast("D:/CliWaC/02_RAW DATA/DEM/DEM_subset_2_2.tif")

plot(subset1)
plot(subset2)
plot(subset3)
plot(subset4)

# Compute weather data averages for Potsdam (Brandenburg)

# Load data
airtemp <- read.table("C:\\Users\\User\\Nextcloud\\Documents\\CliWaC\\03_RAW DATA\\Potsdam_weather_station\\temp\\stundenwerte_TU_03987_18930101_20231231_hist\\produkt_tu_stunde_18930101_20231231_03987.txt", 
                      header = TRUE, sep = ";")
prec <- read.table("C:\\Users\\User\\Nextcloud\\Documents\\CliWaC\\03_RAW DATA\\Potsdam_weather_station\\prec\\stundenwerte_RR_03987_19950901_20231231_hist\\produkt_rr_stunde_19950901_20231231_03987.txt",
                   header = TRUE, sep = ";", dec = ".")


# Convert data columns in date format
airtemp$MESS_DATUM <- as.POSIXct(as.character(airtemp$MESS_DATUM), format = "%Y%m%d%H", tz = "UTC")
prec$MESS_DATUM <- as.POSIXct(as.character(prec$MESS_DATUM), format = "%Y%m%d%H", tz = "UTC")


# Filter years (2017 to 2022)
# Define the start and end date for the subset
start_date <- as.POSIXct("2017-01-01 00:00", tz = "UTC")
end_date <- as.POSIXct("2022-12-31 23:59", tz = "UTC")

# Filter the dataset for the specified date range
airtemp_subset <- subset(airtemp, MESS_DATUM >= start_date & MESS_DATUM <= end_date)
prec_subset <- subset(prec, MESS_DATUM >= start_date & MESS_DATUM <= end_date)

# Extract the year from the date-time column
airtemp_subset$year <- as.integer(format(airtemp_subset$MESS_DATUM, "%Y"))
prec_subset$year <- as.integer(format(prec_subset$MESS_DATUM, "%Y"))


# Exclude -999 from prec_subset dataset
prec_subset_modif <- prec_subset
prec_subset_modif$R1[prec_subset_modif$R1 == -999.0000] <- 0


# Compute the mean temperature per year and the precipitation sum per year
mean_per_year_temp <- aggregate(TT_TU ~ year, data = airtemp_subset, FUN = mean, na.rm = TRUE)
sum_per_year_prec <- aggregate(R1 ~ year, data = prec_subset_modif, FUN = sum, na.rm = TRUE)


# Rename the columns for clarity
colnames(mean_per_year_temp) <- c("Year", "Mean_Temperature")
colnames(sum_per_year_prec) <- c("Year", "Total_Precipitation")

# Save both air temperature and precipitation in one table
weather_data <- mean_per_year_temp
weather_data$Total_Precipitation <- sum_per_year_prec$Total_Precipitation

# Show resulting data table
weather_data

# Save data table 
write.table(weather_data, "C:\\Users\\User\\Nextcloud\\Documents\\CliWaC\\04_PROCESSED DATA\\weather_data\\weather_data.txt",
            col.names = TRUE, row.names = FALSE, dec = ".", sep = ";")

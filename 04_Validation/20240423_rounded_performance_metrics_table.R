### Performance metrics .csv table rounding to three decimals

# Load training df
perf_table <- read.csv("D:\\Nextcloud\\Documents\\CliWaC\\05_RESULTS\\20240415_Validation_metrics\\20240415_Validation_metrics.csv", 
                       header = TRUE, sep = ";", dec = ",")

# Round the relevant columns (except the first column and header)
rounded_table <- perf_table
rounded_table[, -1] <- round(as.data.frame(lapply(perf_table[, -1], as.numeric)), 3)

# Save the rounded table to a new CSV file
write.csv(rounded_table, file = "D:\\Nextcloud\\Documents\\CliWaC\\05_RESULTS\\20240415_Validation_metrics\\20240415_Validation_metrics_rounded.csv",
          row.names = FALSE, sep = ",", dec = ".")

# Load saved .csv to check
check_table <- read.csv("D:\\Nextcloud\\Documents\\CliWaC\\05_RESULTS\\20240415_Validation_metrics\\20240415_Validation_metrics_rounded.csv", 
                        sep = ",", dec = ".")

head(check_table)

# Year Accuracy Precision Recall F1.Score   AUC
# 1    2018    0.777     0.676  0.799    0.732 0.781
# 2    2019    0.716     0.717  0.697    0.707 0.716
# 3    2020    0.726     0.713  0.736    0.724 0.726
# 4    2021    0.701     0.258  0.689    0.376 0.696
# 5    2022    0.701     0.614  0.713    0.660 0.703
# 6 Average    0.724     0.596  0.727    0.640 0.724

## Looks fine! 
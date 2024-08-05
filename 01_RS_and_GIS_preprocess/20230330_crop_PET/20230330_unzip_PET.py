# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 11:15:01 2023

@author: Stenka Vulova
"""

# I want to unzip all the .asc files (Potential ET) from DWD.
# Example file name: grids_germany_monthly_evapo_p_199103.asc.gz

# To extract .gz files, you can use the gzip module.
    
#%% Libraries 

import os
import glob
import gzip

#%% Folder with zip files 

# Set the path to the folder containing the .gz files
folder_path = 'D:/Stenka_Cliwac/Topic_1/03_RAW_DATA/20230329_PET_DWD_grids'

# Get a list of all .gz files in the folder
gz_files = glob.glob(os.path.join(folder_path, '*.gz'))

print(len(gz_files)) # 386

gz_file = gz_files[2]
# Set the output file name by removing the .gz extension and adding .asc
out_file = os.path.splitext(gz_file)[0] 
print(out_file)

#%% Loop over the files

# Loop over all .gz files in the folder
for gz_file in gz_files:
    # Set the output file name by removing the .gz extension and adding .asc
    out_file = os.path.splitext(gz_file)[0] # .asc is already in the file name 

    # Open the .gz file and the output file, and decompress the data
    with gzip.open(gz_file, 'rb') as f_in:
        with open(out_file, 'wb') as f_out:
            f_out.write(f_in.read())

    # Print the name of the output file
    print(f'Extracted {out_file}')
    
# Cool, it worked! 
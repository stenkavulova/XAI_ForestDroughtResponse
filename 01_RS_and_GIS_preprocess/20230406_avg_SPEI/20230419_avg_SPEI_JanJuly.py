# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 11:07:56 2023

@author: Stenka Vulova
"""

# Annual means of SPEI (over each pixel)
# looping over several years

#%% Libraries

import rasterio
import glob
import numpy as np
import os

#%% check 

tif_files = glob.glob(f'D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230405_SPEI/SPEI_{1991}-*.tif')
print(tif_files)

# os.path.basename(file) extracts the filename from the full file path
# .split('-') splits the filename at the hyphen, resulting in a list with two elements:
# the prefix (SPEI_year) and the month (01, 02, etc.).
#We then use int() to convert the month string to an integer so that we can compare it with the range of integers 1 to 7.

file = tif_files[0]
print(file) # D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230405_SPEI\SPEI_1991-01.tif

os.path.basename(file) # 'SPEI_1991-01.tif'

os.path.basename(file).split('-') # ['SPEI_1991', '01.tif']

os.path.basename(file).split('-')[1] # 01.tif'

# The os.path.splitext() method splits the file name into a tuple of the file name and the extension
# so os.path.splitext(os.path.basename(file)) would return ('SPEI_1991-01', '.tif').
os.path.splitext(os.path.basename(file)) # ('SPEI_1991-01', '.tif')

# The [0] at the end selects just the file name without the extension
os.path.splitext(os.path.basename(file))[0] # SPEI_1991-01

# then split('-')[1] splits the file name on the hyphen and selects the second element (index 1) of the resulting list.
os.path.splitext(os.path.basename(file))[0].split('-')[1] # 01

#int(os.path.basename(file).split('-')[1] # SyntaxError: unexpected EOF while parsing

#%% Loop

# loop over a list of years
for year in range(1991, 2023):
    # Get a list of all files for the current year
    tif_files = glob.glob(f'D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230405_SPEI/SPEI_{year}-*.tif')

    # Filter the list to only include files with month between 01 and 07
    tif_files_filtered = [file for file in tif_files if int( os.path.splitext(os.path.basename(file))[0].split('-')[1] ) in range(1, 8)] # means months 1-7 

    def read_file(file):
        with rasterio.open(file) as src:
            return(src.read(1, masked = True))

    # Read all data as a list of numpy arrays 
    array_list = [read_file(x) for x in tif_files_filtered]
    print(array_list)

    # Compute the arithmetic mean along the specified axis
    array_out = np.mean(array_list, axis=0)

    # Get metadata from one of the input files
    with rasterio.open(tif_files_filtered[0]) as src:
        meta = src.meta

    # Write the output to a new file
    year_str = str(year)
    out_filename = f'D:/Stenka_Cliwac/Topic_1/04_PROCESSED_DATA/20230406_SPEI_annual_avg/Jan_to_July/SPEI_JanJuly_mean_{year_str}.tif'
    with rasterio.open(out_filename, 'w', **meta) as dst:
        dst.write(array_out.astype(rasterio.float32), 1)

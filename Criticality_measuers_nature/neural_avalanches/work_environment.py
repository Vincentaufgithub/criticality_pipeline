# %%

# %%
import sys
import os
import numpy as np
import pandas as pd

import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import Criticality_measuers_nature as cr

def bin_data_to_50ms(data: np.ndarray) -> np.ndarray:
    num_bins, num_neurons = data.shape
    
    # if necessary, trim data so it will be divisible by 10
    excess_rows = num_bins % 10
    if excess_rows != 0:
        data = data[:-excess_rows]
    
    # Reshape the trimmed data so that each 10 rows (50ms) is grouped together
    reshaped_data = data.reshape(-1, 10, num_neurons)
    
    # Sum across the second dimension (axis 1) to get the 50ms binned data
    binned_data = reshaped_data.sum(axis=1)
    return binned_data


####################
# Accessing previously stored spike trains
####################
# /local2/Vincent/neuro_pixels_binned_spiking_data/819701982_CA1_124.npy
# Define the directory containing the .npy files
directory = '/local2/Vincent/binned_spiking_data/'

# Get a list of all .npy files in the directory
npy_files = [f for f in os.listdir(directory)]

# Group files by their base name (excluding the last 6 characters)
# so spike trains will be grouped by session and area
# e.g. 'mil_CA1_sleep_02_03_', 'fra_CA2_sleep_03_05_', 'bon_CA3_sleep_05_01_'

file_groups = {}
for file in npy_files:
    base_name = file[:-6] # -6 for loren frank
    if base_name not in file_groups:
        file_groups[base_name] = []
    file_groups[base_name].append(os.path.join(directory, file))



for base_name, file_list in file_groups.items():
    arrays = [np.load(file).reshape(-1, 1) for file in file_list]
    data = np.concatenate(arrays, axis=1)
    data = bin_data_to_50ms(data) # originally in 5ms bins, but Habibollahi et al. used larger ones
    
    try:
        r = cr.AV_analysis_BurstT(data, perc = 0.25)
        x = r['S'] # x is AVsize
        y = r['T'] # y is AVdura

        burstM = 10
        tM = 3

        result, fit_sigma = cr.AV_analysis_ExponentErrorComments(x, y, burstM, tM, flag = 1)
        
        data_to_store = pd.DataFrame([result])             
        filename = f"/local2/Vincent/power_laws/loren_frank/{base_name}.parquet"
                        
        data_to_store.to_parquet(filename, index = True)
        print("stored succesfully:", base_name)
    except Exception as e:
        print(e)
        continue
 

# %%
import os
import pandas as pd
import statsmodels.formula.api as smf

# File path and file reading
filepath = "/local2/Vincent/power_laws/loren_frank/"
results = [f for f in os.listdir(filepath) if f.endswith(".parquet")]

big_df = []
 
for result in results:
    # Create a new DataFrame for each result file
    df = pd.DataFrame()

    # Extract the area (e.g., "CA1") from the filename
    area = result.split("_")[1] #.split(".")[0] # for neuropixels

    # Read the "beta" column from the parquet file
    df["beta"] = pd.read_parquet(f"{filepath}{result}")["beta"][0]

    # Add the 'area' as a new column
    df["area"] = str(area)
    
    # Append this DataFrame to the list
    big_df.append(df)

# Combine all DataFrames in the list into one DataFrame
combined_df = pd.concat(big_df, ignore_index = True)

# Set the 'area' column as the index (optional, based on your need)
# combined_df.set_index('area', inplace=True)

combined_df = combined_df.dropna()
print(combined_df)
# Define the formula for the linear model
formula = "beta ~ area"

# Fit the linear model using Ordinary Least Squares (OLS)
model = smf.ols(formula=formula, data=combined_df).fit()

# Print the summary of the model
print(model.summary())
# %%
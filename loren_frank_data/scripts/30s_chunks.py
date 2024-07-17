# %%

import os
import numpy as np
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))
sys.path.append(parent_dir)
import tools


# The code below will load all spiking arrays and corresponding tau values
# Can then be used either to run new analysises or to create graphs.

# Define the directory containing the .npy files
directory = '/local2/Vincent/binned_spiking_data/'


# Get a list of all .npy files in the directory
npy_files = [f for f in os.listdir(directory)]


# Group files by their base name (excluding the last 6 characters)
# so spike trains will be grouped by session and area

file_groups = {}
for file in npy_files:
    base_name = file[:-6]
    if base_name not in file_groups:
        file_groups[base_name] = []
    file_groups[base_name].append(os.path.join(directory, file))


for base_name, file_list in file_groups.items():
    arrays = [np.load(file).reshape(-1, 1) for file in file_list]
    
    data = np.concatenate(arrays, axis=1)

    tools.mr_estimator_for_prepared_epoch_data(data, 
                                               window_size= 30,
                                               bin_size= 5,
                                               fit_func = "f_complex",
                                               filename = f'/local2/Vincent/loren_frank_MR_30s//{base_name}',
                                               )

# %%
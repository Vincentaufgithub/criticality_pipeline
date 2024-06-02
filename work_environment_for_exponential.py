# %%

import os
import numpy as np
import tools

# basically, this script does the same as the other work_environment
# except that we can now rely on the previously stored numpy arrays, which will come in extremely handy.


# Define the directory containing the .npy files
directory = '/local2/Vincent/binned_spiking_data/'


# Get a list of all .npy files in the directory
npy_files = [f for f in os.listdir(directory)]


# Group files by their base name (excluding the last 6 characters)
file_groups = {}
for file in npy_files:
    base_name = file[:-6]
    if base_name not in file_groups:
        file_groups[base_name] = []
    file_groups[base_name].append(os.path.join(directory, file))



# Load and concatenate arrays for each group
for base_name, file_list in file_groups.items():
    arrays = [np.load(file).reshape(-1, 1) for file in file_list]
    
    data = np.concatenate(arrays, axis=1)

  
    tools.mr_estimator_for_prepared_epoch_data(data, window_size= 90,
                                               bin_size= 5,
                                               fit_func = "f_exponential_offset",
                                               filename = f'/local2/Vincent/mr_analysis_with_exponential/{base_name}.parquet',
                                               )

# %%
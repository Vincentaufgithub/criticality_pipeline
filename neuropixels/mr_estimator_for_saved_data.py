# %%

import os
import sys
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tools



# The code below will load all spiking arrays and corresponding tau values
# Can then be used either to run new analysises or to create graphs.

# Define the directory containing the .npy files
directory = '/local2/Vincent/neuro_pixels_binned_spiking_data/'


# Get a list of all .npy files in the directory
npy_files = [f for f in os.listdir(directory)]


# Group files by their base name (excluding the last 6 characters)
file_groups = {}
for file in npy_files:
    base_name = file[:-7]
    if base_name not in file_groups:
        file_groups[base_name] = []
    file_groups[base_name].append(os.path.join(directory, file))
    



# Load and concatenate arrays for each group
for base_name, file_list in file_groups.items():
    arrays = [np.load(file).reshape(-1, 1) for file in file_list]
    
    data = np.concatenate(arrays, axis=1)
   
    tools.mr_estimator_for_prepared_epoch_data(data, 
                                                window_size= 90,
                                                bin_size= 5,
                                                fit_func = "f_complex",
                                                filename = f'/local2/Vincent/neuro_pixels_output_f_complex/{base_name}'
                                                )
    
    
# %%

from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache


cache = EcephysProjectCache.from_warehouse(manifest = '/local2/Vincent/neuro_pixels_sessions/manifest.json')
session_table = cache.get_session_table()

index_to_specimen_id = dict(zip(session_table.index, session_table['specimen_id']))

# %%
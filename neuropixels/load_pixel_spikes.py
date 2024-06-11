# %%
import sys
import os

# Add the parent directory to the system path
# somehow necessary for import of tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tools

import glob
import pynapple as nap
from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache
import tools
import numpy as np
import math



def find_nwb_files(root_dir):
    # the neuropixel files are stacked in subfolders
    # this function will return a list of the filepaths for all .nwb files
    pattern = os.path.join(root_dir, '**', '*.nwb')
    nwb_files = glob.glob(pattern, recursive=True)
    return nwb_files



def get_binned_activity(spike_dict, id_list, bin_size, file_key = None):
    '''
    parameters
    
    spike_dict : dictionary
        contains all spiking timestamps for one session (unit = seconds). Keys are unique neuron ids
    
    id_list : list
        contains all neuron ids of interest (e.g. all neuron ids belonging to one area)
    
    bin_size : int
        bin size in ms. Will be converted to seconds
    
    file_key : str
        optional. If given, all single binned spike trains will be saved to disk.
        base name where to store results
    
    '''
    bin_size = bin_size / 1000
    
    time_series_list = [spike_dict[id] for id in id_list]
 
    end_time = max(time_series[-1] for time_series in time_series_list)
    
    bin_edges = np.arange(0, end_time + bin_size, bin_size) # create grid to bin time series onto
    
    # create empty 2-d array. The binned time series will be integrated into the return_array
    return_array = np.zeros((len(bin_edges)-1, len(id_list)), dtype=int)
    
    # Bin the spike arrays and save each one to disk
    for i, timestamps in enumerate(time_series_list):
        # Create histogram (binned array)
        binned_array, _ = np.histogram(timestamps, bins=bin_edges)
        
        if file_key:
            # Save the binned array to disk
            file_path = f'{file_key}_{i:03d}.npy' # e.g. /local2/Vincent/neuro_pixels_binned_spiking_data/715093703_CA1_004.npy
            np.save(file_path, binned_array)
        
        # Collect binned arrays
        return_array[:, i] = binned_array
    
    
    return return_array








cache = EcephysProjectCache.from_warehouse(manifest = '/local2/Jan/ecephys_data/manifest.json')
bin_size = 5
window_size = 90
area_list = ["CA1"]
target_dir_between = "/local2/Vincent/neuro_pixels_binned_spiking_data/"
target_dir_final = ""

session_id = 715093703
session = cache.get_session_data(session_id)


for area in area_list:
    unit_ids = session.units[session.units["ecephys_structure_acronym"] == area]
    unit_ids = unit_ids.index.values

    file_base_name = f"{target_dir_between}{session_id}_{area}"

    data = session.spike_times

    binned_activity = get_binned_activity(data, unit_ids, bin_size, file_base_name)
    
    tools.mr_estimator_for_prepared_epoch_data(data = binned_activity,
                                               window_size = window_size,
                                               bin_size = bin_size,
                                               fit_func = "f_complex",
                                               filename = target_dir_final)


# %%

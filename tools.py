import pandas as pd
import numpy as np
from glob import glob
from scipy.io import loadmat

import loren_frank_data_processing.neurons as lf_neurons 

import utilities.load_recording_information as rec_info
import utilities.load_spiking_times as spikes




def create_sorted_dict_with_cellinfos(animal):
    '''
    loads the cellino file for the animal
    creates a pandas dataframe with relevant information
    sorts the dataframe according to recording area
    returns a dictionary. In the dictionary is one cellinfo_dataframe for each recorded area
    ------------------
    parameters:
    
    animal : named tuple
        containing 'short_name' and 'filepath' to animal folder
    ------------------
    returns:
    
    neuron_info_dict : dictionary
        one pd.Dataframe for each recorded epoch
        containing usually the following columns:
            ['spikewidth', 'meanrate', 'numspikes', 'area', 'tetnum', 'neuron_id']
        also contains unique keys to identify each neuron
    
    '''
    
    cellinfo_filename = f"{animal.directory}{animal.short_name}cellinfo.mat"
    neuron_cellinfo = loadmat(cellinfo_filename)
    
    
    # using loren frank lab, we create a dataframe containing all neuron info for a given animal
    # also creates a unique neuron key for each recorded unit - pretty cool!
    neuron_info_dataframe = pd.concat([
        lf_neurons.convert_neuron_epoch_to_dataframe(epoch, animal.short_name, day_ind + 1, epoch_ind + 1)
        for day_ind, day in enumerate(neuron_cellinfo['cellinfo'].T)
        for epoch_ind, epoch in enumerate(day[0].T)
        ]).sort_index()
    
    # print all the areas that were recorded
    # print(neuron_info_dataframe.columns.names)
    
    # sort the information according to recording area into a dict
    neuron_info_dict = rec_info.group_df_to_dict(neuron_info_dataframe, "area")
    
    return neuron_info_dict




def create_sorted_dict_with_tasks(animal):
    '''
    there is a task-file for each recording day 
    describing every epoch, like the environment, the animal state, ...
    Relying on the loren frank package, this function loads all task-files and sorts them according to animal state
    So we'll know what state the animal was in for each epoch
    -----------------
    parameters:
    
    animal : named tuple
        containing 'short_name' and 'filepath' to animal folder
        
    -----------------
    returns:
    
    task_files_dict_sorted : dictionary
        sorts all epochs according to the state the animal was in
        format: {state: {day: [list of epochs]}}
        
        states are usually "run" and "sleep"
        sometimes, we'll get something like sleep_failed - ignoring that so far
    
    '''
    # find the names of all task files
    task_files = glob(f"{animal.directory}{animal.short_name}task*.mat"  )
    
    # gives us the information of all recording epochs in one df
    task_file_df = pd.concat( rec_info.load_task_file(task_file, animal) for task_file in task_files)

    # sort the information into a dict, according to the state the animal was in
    task_files_dict_sorted = rec_info.group_df_to_dict(task_file_df, "type")
    
    # print all the different states that were defined by the lab
    # print(task_files_dict_sorted.keys())
    
    return task_files_dict_sorted




def create_neuron_dicts_for_each_state(cellinfo_df, taskinfo_dict):
    '''
    Creates nested dict for a given brain area, allowing to access the neuron_keys via state, day and epoch
    ---------------
    parameters:
    
    cellinfo_df : dataframe
        containing all the neuron_keys for specific area
    
    taskinfo_dict : keys: ("state",)           
        contains all days and epochs where the animal was in specified state
    ----------------
    returns:
    
    state_day_epoch_neuron_dict : dictionary
        a nested dictionary specific to animal, and recording area.
        With the following structure:
        
        {state:
            {day:
                {epoch:
                    [list of neuron_keys]
        }}}
        
        (state will either be "wake" or "sleep".)
    
    '''
    # in this list, we'll store the df for wake and sleep state
    dict_list = []
    
    for state in ["run", "sleep"]:
        
        # selects all the neurons out of cellinfo_df which belong to state x
        neuron_keys_for_state_df = rec_info.match_neuron_key_to_state(cellinfo_df, taskinfo_dict[state,].index)

        # dict containing all the epochs that were in state x
        # {day_n: [epochs]}
        day_epoch_dict = rec_info.get_epochs_by_day(neuron_keys_for_state_df.index)
        
        # adds all the neuron keys of neuron_keys_for_state_df to day_epoch_dict
        day_epoch_neuron_dict = rec_info.add_neuron_keys_to_state_dict(
            day_epoch_dict, 
            neuron_keys_for_state_df['neuron_id'].tolist())
        
        dict_list.append(day_epoch_neuron_dict)
   
    # merge both dicts
    state_day_epoch_neuron_dict = {"wake": dict_list[0],
                "sleep": dict_list[1]}
    
    return state_day_epoch_neuron_dict





def load_spikes(neuron_dict, animal, bin_size = 5):
    '''
    given a dict with neuron_keys, this function will load all the spiking times of one epoch into a grouped pynapple time series.
    It will then bin the data and finally sum up the bins of all neurons.
    Returns a dict with the same structure as the input.
    ---------------------
    parameters
    
    
    neuron_dict : dictionary
        a nested dictionary specific to animal, and recording area.
        With the following structure:
        (state will either be "wake" or "sleep".)
        
            {state:
                {day:
                    {epoch:
                        [list of neuron_keys]
            }}}
        
    
    animal : named tuple
        containing 'short_name' and 'filepath' to animal folder
    
    
    bin_size : int
        optional
        size to bin spiking series in, in ms
    
    ------------------
    returns
    
    
    neuron_dict : dictionary
        Same dict structure as input dict.
        However, neuron_dict[state][day][epoch] will give a one-dimensional np.ndarray of the summed activity.
        Each item being the total number of recorded spikes in the corresponding bin.
        The length of each np.ndarray will be:
            (last_recorded_spike_in_epoch_in_ms - first_recorded_spike_in_epoch_in_ms) / bin_size
    '''

    for state_index in neuron_dict:
        for day_index in neuron_dict[state_index]:
            for epoch_index in neuron_dict[state_index][day_index]:
                
                grouped_time_series = spikes.grouped_time_series(neuron_dict[state_index][day_index][epoch_index], animal)
                
                binned_ts_group = grouped_time_series.count(bin_size = bin_size, time_units = "ms")
                summed_activity = np.sum(binned_ts_group.values, axis=1)
                
                neuron_dict[state_index][day_index][epoch_index] = summed_activity
    
    return neuron_dict
    # return spikes.load_and_bin_spike_data(neuron_dict, animal)





def run_mr_estimator_on_summed_activity(neuron_dict, bin_size, window_size):
    # here, we'll iterate over activity array
    # ... using np.array_split()
    
    # number of elements in each slice
    slice_size = (window_size * 1000) / bin_size
    
    for state_index in neuron_dict:
        for day_index in neuron_dict[state_index]:
            for epoch_index in neuron_dict[state_index][day_index]:
                slices = np.array_split(neuron_dict[state_index][day_index][epoch_index], slice_size)
                
                # delete last element if it is smaller than the other ones
                # haven't found a more elegent solution yet
                if len(slices[-1]) < slice_size:
                    slices = slices[:-1] 
    
    # after sclicing it, we can already run the estimator
    return








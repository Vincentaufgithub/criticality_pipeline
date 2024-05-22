import pandas as pd
import numpy as np
from glob import glob
from scipy.io import loadmat
import pynapple as nap

import loren_frank_data_processing.neurons as lf_neurons 



# The following functions are specific to the dataset from the loren frank lab
# it will probably be unavoidable to create a script like this for each dataset,
# since naming conventions and such always differ.



###############################################################
# FUNCTIONS INTENDED FOR BEING CALLED IN THE WORK ENVIRONMENT #
###############################################################


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
    neuron_info_dict = group_df_to_dict(neuron_info_dataframe, "area")
    
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
    task_file_df = pd.concat( load_task_file(task_file, animal) for task_file in task_files)

    # sort the information into a dict, according to the state the animal was in
    task_files_dict_sorted = group_df_to_dict(task_file_df, "type")
    
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
        neuron_keys_for_state_df = match_neuron_key_to_state(cellinfo_df, taskinfo_dict[state,].index)

        # dict containing all the epochs that were in state x
        # {day_n: [epochs]}
        day_epoch_dict = get_epochs_by_day(neuron_keys_for_state_df.index)
        
        # adds all the neuron keys of neuron_keys_for_state_df to day_epoch_dict
        day_epoch_neuron_dict = add_neuron_keys_to_state_dict(
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

    return_dict = neuron_dict.copy()
    
    for state_index in neuron_dict:
        for day_index in neuron_dict[state_index]:
            
            # there's a spiking file for each recording day.
            neuron_file = loadmat(f"{animal.directory}{animal.short_name}spikes{day_index:02d}.mat")
            
            
            for epoch_index in neuron_dict[state_index][day_index]:
                
                
                epoch = neuron_file['spikes'][0, -1][0, epoch_index-1][0, 0][0, 0]["timerange"][0][0][0]
                epoch = nap.IntervalSet(start = epoch[0] /1000, end = epoch[1] /1000, time_units='s')
                
                grouped_epoch_time_series = grouped_time_series(neuron_dict[state_index][day_index][epoch_index], animal)
        
                
                if np.any(grouped_epoch_time_series):
                    
                    binned_ts_group = grouped_epoch_time_series.count(bin_size = bin_size, time_units = "ms", ep = epoch)
                    
                    #with np.printoptions(threshold=np.inf):
                     #  print(binned_ts_group)
                        
                        
                    summed_activity = np.sum(binned_ts_group.values, axis=1)

                    
                    
                    #with np.printoptions(threshold=np.inf):
                     #  print(summed_activity)

                    
                    return_dict[state_index][day_index][epoch_index] = summed_activity
                
                else:
                    print(f"no spiking data for: {state_index}, day {day_index}, epoch {epoch_index}")
                    return_dict[state_index][day_index][epoch_index] = None

    
    return return_dict



























####################
# HELPER FUNCTIONS #
####################



def group_df_to_dict(df, label):
    dfs = {}
    for idx, group in df.groupby([label]):
        dfs[idx] = group.copy()
    return dfs




def load_task_file(file_name, animal):
    '''
    This function is mostly taken from loren frank lab.
    '''
    
    data = loadmat(file_name, variable_names=('task'))['task']
    #print(data.dtype.names)
    
    # data.shape returns a tuple (a,b), b being the number of days in the array
    n_days = data.shape[-1]
    
    epochs = data[0, -1][0]
    n_epochs = len(epochs)
    
    index = pd.MultiIndex.from_product(
        ([animal.short_name], [n_days], np.arange(n_epochs) + 1),
        names=['animal', 'day', 'epoch'])
    

    # Create a DataFrame from a list of dictionaries
    df_list = [
        {name: epoch[name].item().squeeze() 
         for name in epoch.dtype.names if name =='type'}
        for epoch in epochs]
    
    
    df = pd.DataFrame(df_list)

    # Set index and convert data types
    df = df.set_index(index).assign(
        type=lambda df: df.type.astype(str)
    )

    return df



def match_neuron_key_to_state(dataframe, multiindex):
    
    # bc first element in each index is the animal name
    valid_entries = [row_index[1:] for row_index in multiindex]
    
    df_entries = [(row_index[2],row_index[4]) for row_index in dataframe.index]
    
    matching_entries = [entry for entry in valid_entries if entry in df_entries]
    filtered_dataframe = pd.DataFrame()
    
    for matching_entry in matching_entries:
        temp_dataframe = dataframe.loc[(dataframe.index.get_level_values('day') == matching_entry[0]) & (dataframe.index.get_level_values('epoch') == matching_entry[1])]
        filtered_dataframe = pd.concat([filtered_dataframe, temp_dataframe])

    return filtered_dataframe




def get_epochs_by_day(multi_index):
    '''
    Returns: A dict with keys days, and values lists of epochs per day
    '''
    epochs_by_day = {}
    
    for index in multi_index:
        day = index[1]
        epoch = index[2]
        
        if day in epochs_by_day:
            if epoch not in epochs_by_day[day]:
                epochs_by_day[day].append(epoch)    
        else:
            epochs_by_day[day] = [epoch]
    
    return epochs_by_day



def add_neuron_keys_to_state_dict(get_epochs_per_day_dict, neuron_id_list):
    '''
    Input: epochs_per_day_dict with days as keys and lists of epochs per day as values
    
    Returns: embedded dict of dicts, where the outer dict contains the days as keys and the epoch dicts as (values/sub-keys).
             The inner values are the neuron ids per epoch (inner dict) per day (outer dict)
    '''
    epochs_per_day_dict = {}
    neuron_id_component_list = []
    
    for neuron_key_str in neuron_id_list:
        animal_short_name, day_number, epoch_number, tetrode_number, neuron_number = neuron_key_str.split("_")
        neuron_id_component_list.append((animal_short_name, day_number, epoch_number, tetrode_number, neuron_number))
    
    for key in get_epochs_per_day_dict:
        inner_dict = {}
        for value in get_epochs_per_day_dict[key]:
            inner_dict[value] = []
            for neuron_id in neuron_id_component_list:
                if neuron_id[1] == '0'+str(key) and neuron_id[2] == '0'+str(value):
                    inner_dict[value].append('_'.join(neuron_id))
        epochs_per_day_dict[key] = inner_dict
    return epochs_per_day_dict









def grouped_time_series(epoch_neuron_keys, animal):
    epoch_dict = {}
                
    for neuron_key_index, neuron_key_str in enumerate(epoch_neuron_keys):
        try:
            # unpack the neuron key from string to tuple
            animal_short_name, day_number, epoch_number, tetrode_number, neuron_number = neuron_key_str.split("_")
            neuron_key = (animal_short_name, int(day_number), int(epoch_number), int(tetrode_number), int(neuron_number))  
                
                          
            epoch_dict[neuron_key_index] = get_spikes_series(neuron_key, animal) # experimental
            #time_series = nap.TsGroup(epoch_dict)

                    
        except Exception as e:
            print(e, neuron_key)

                        
            ## neuron_dict[state_index][day_index][epoch_index][neuron_key_index] = spike_time_array 

            # create time Series group for each epoch
    if not epoch_dict:
        return None
    
    
    sorted_epoch_dict = {i: epoch_dict[key] for i, key in enumerate(epoch_dict)}
    
    return nap.TsGroup(sorted_epoch_dict)



# this an attempt to load the spiking data into pynapple instead of pandas Time Series
# the original function can be found below
def get_spikes_series(neuron_key, animal):
    '''Spike times for a particular neuron.

    Parameters
    ----------
    neuron_key : tuple
        Unique key identifying that neuron. Elements of the tuple are
        (animal_short_name, day, epoch, tetrode_number, neuron_number).
        Key can be retrieved from `make_neuron_dataframe` function.
    animals : dict of named-tuples
        Dictionary containing information about the directory for each
        animal. The key is the animal_short_name.

    Returns
    -------
    spikes_dataframe : pandas.DataFrame
        np.ones array, indexed with spiking times
    '''
    
    animal_short_name, day, epoch, tetrode_number, neuron_number = neuron_key
    filename = f"{animal.directory}{animal.short_name}spikes{day:02d}.mat"

    neuron_file = loadmat(filename)
    
    
    if not neuron_file['spikes'][0, -1][0, epoch - 1][0, tetrode_number - 1][0, neuron_number - 1][0]['data'][0].any():
        raise Exception("No spiking times")
    
    
    spike_time = neuron_file['spikes'][0, -1][0, epoch - 1][0, tetrode_number - 1][0, neuron_number - 1][0]['data'][0][:, 0]
    ts = nap.Ts(t = spike_time, time_units= "s")
    



    return ts
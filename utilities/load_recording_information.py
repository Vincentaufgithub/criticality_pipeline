from scipy.io import loadmat
import pandas as pd
import numpy as np



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









####################################################################
# Functions I'm not using 
# But keeping them here just in case
####################################################################




# this one would be called in tools.create_neuron_dicts_for_each_state
# and is supposed to combine the state dicts combining neuron_keys for each day and epoch
# However, it checks for every neuron key if it also exists in the other dict
# and if so, the neuron key will be added to neither dict
# not using this for two reasons:
# 1. looping costs time and so far, it never detected any overlaps
# 2. if any overlaps should exist, that would mean that something is wrong with the way we generate the neuron_keys
# and this wouldn't be the rifht place to fix it.
def conjoined_dict_with_overlap_checked(wake_day_epoch_dict, sleep_day_epoch_dict):
    '''Input: wake_day_epoch_dict, sleep_day_epoch_dict -- Behav State specific (relative to epoch categorization) day epoch combinations'
    Returns: embedded dict with outher keys behav state, inner keys day, and double inner keys epoch, with overlapping combinations deleted'
    '''
    final_dict = {'wake': {}, 'sleep': {}}
    overlap_counter = 0
    
    for i in wake_day_epoch_dict.keys():
        for j in wake_day_epoch_dict[i].keys():
            if i in sleep_day_epoch_dict and j in sleep_day_epoch_dict[i]:
                if wake_day_epoch_dict[i][j] == sleep_day_epoch_dict[i][j]:
                    overlap_counter += 1
            else:
                final_dict['wake'].setdefault(i, {})[j] = wake_day_epoch_dict[i][j]
    
    for i in sleep_day_epoch_dict.keys():
        for j in sleep_day_epoch_dict[i].keys():
            if i in wake_day_epoch_dict and j in wake_day_epoch_dict[i]:
                if wake_day_epoch_dict[i][j] == sleep_day_epoch_dict[i][j]:
                    overlap_counter += 1
            else:
                final_dict['sleep'].setdefault(i, {})[j] = sleep_day_epoch_dict[i][j]
    
    #print("overlap counter:", overlap_counter)
                
    return final_dict 




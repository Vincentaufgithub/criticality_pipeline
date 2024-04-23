from scipy.io import loadmat
import loren_frank_data_processing.neurons as lf_neurons 
import pandas as pd
from glob import glob
import utilities.data_preparation as prep



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
    
    # load the cellinfo file of the animal
    cellinfo_filename = f"{animal.directory}{animal.short_name}cellinfo.mat"
    neuron_cellinfo = loadmat(cellinfo_filename)
    
    
    # using loren frank lab, we create a dataframe containing all neuron info for a given animal
    # please don't ask me how it works. It just does, somehow.
    # the function from loren frank lab also creates a unique neuron key for each recorded unit - pretty cool!
    neuron_info_dataframe = pd.concat([
        lf_neurons.convert_neuron_epoch_to_dataframe(epoch, animal.short_name, day_ind + 1, epoch_ind + 1)
        for day_ind, day in enumerate(neuron_cellinfo['cellinfo'].T)
        for epoch_ind, epoch in enumerate(day[0].T)
        ]).sort_index()
    
    # print all the areas that were recorded
    # print(neuron_info_dataframe.columns.names)
    neuron_info_dict = prep.group_df_to_dict(neuron_info_dataframe, "area")
    
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
        keys: ("area",)           - don't know why the weird format, I'll try fixing that
        contains all days and epochs where the animal was in specified state
    
    '''
    # find the names of all task files
    task_files = glob(f"{animal.directory}{animal.short_name}task*.mat"  )
    
    task_file_df = pd.concat( prep.load_task_file(task_file, animal) for task_file in task_files)

    task_files_dict_sorted = prep.group_df_to_dict(task_file_df, "type")
    
    # print all the different states that were defined
    #print(task_files_dict_sorted.keys())
    
    return task_files_dict_sorted



def create_neuron_dicts_for_each_state(cellinfo_df, taskinfo_dict):
    '''
    Creates two nested dictionarys for a given brain area, allowing to access the neuron_keys via day and epoch
    ---------------
    parameters:
    
    cellinfo_df : dataframe
        containing all the neuron_keys for specific area
    
    taskinfo_dict : keys: ("state",)           
        contains all days and epochs where the animal was in specified state
    ----------------
    returns:
    
    day_epoch_neuron_state_dict : dictionary
        returns one for each state: "run" and "sleep".
        a nested dictionary specific to animal, recording area and animal state (run or sleep).
        With the folloeing structure:
        
        {day:
            {epoch:
                [list of neuron_keys]
        }}
    
    '''
    # in this list, we'll store the df for run and sleep state
    dict_list = []
    
    for state in ["run", "sleep"]:
        
        # selects all the neurons out of cellinfo_df which belong to state x
        neuron_keys_for_state_df = prep.match_neuron_key_to_state(cellinfo_df, taskinfo_dict[state,].index)

        
        # the index being apparently just the neuron keys
        # returns a dictionary
        # key : day (int)
        # values: list of epochs (int)
        # so this gives us all the epochs that were in given state
        state_day_epoch_dict = prep.get_epochs_by_day(neuron_keys_for_state_df.index)
        
        
        
        # adds all the neuron keys of state_df to state_day_epoch_dict
        day_epoch_neuron_state_dict = prep.add_neuron_keys_to_state_dict(
            state_day_epoch_dict, 
            neuron_keys_for_state_df['neuron_id'].tolist())
        
        
        dict_list.append(day_epoch_neuron_state_dict)
    
    return dict_list[0], dict_list[1]
   


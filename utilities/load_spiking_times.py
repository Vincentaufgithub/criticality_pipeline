import numpy as np
from scipy.io import loadmat
import pynapple as nap
from collections import namedtuple
import pandas as pd



def grouped_time_series(epoch_neuron_keys, animal):
    epoch_dict = {}
                
    for neuron_key_index, neuron_key_str in enumerate(epoch_neuron_keys):
        try:
            # unpack the neuron key from string to tuple
            animal_short_name, day_number, epoch_number, tetrode_number, neuron_number = neuron_key_str.split("_")
            neuron_key = (animal_short_name, int(day_number), int(epoch_number), int(tetrode_number), int(neuron_number))  
                
                          
            epoch_dict[neuron_key_index] = get_spikes_series(neuron_key, animal) # experimental
            time_series = nap.TsGroup(epoch_dict)
            
                    
        except Exception as e:
            print(e, neuron_key)

                        
            ## neuron_dict[state_index][day_index][epoch_index][neuron_key_index] = spike_time_array 

            # create time Series group for each epoch
    return time_series



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
    
    neuron_file = []
    spike_time = []

    neuron_file = loadmat(filename)
    
    
    if not neuron_file['spikes'][0, -1][0, epoch - 1][0, tetrode_number - 1][0, neuron_number - 1][0]['data'][0].any():
        raise Exception("No spiking times")
    
    
    spike_time = neuron_file['spikes'][0, -1][0, epoch - 1][0, tetrode_number - 1][0, neuron_number - 1][0]['data'][0][:, 0]
    ts = nap.Ts(t = spike_time, time_units= "s")
    #print(ts)


    return ts




def activity_series_to_time_chunks(summed_epoch_activity, slice_size):
    chunk_list = []
                
    for i in range(0, len(summed_epoch_activity), slice_size):
        chunk_list.append(summed_epoch_activity[i:(i+slice_size)])
                
                
        # delete last element if it is smaller than the other ones
        # haven't found a more elegent solution yet
        if len(chunk_list[-1]) < slice_size:
            chunk_list = chunk_list[:-1] 

    return chunk_list






####################################################################
# Functions I'm not using 
# But keeping them here just in case
####################################################################


def load_and_bin_spike_data(neuron_dict, animal):
    '''Input: neuron_dict: embedded state_day_epoch_neuron_key dict
        Returns: spike indicator dict of spike trains per day epoch combination
    ''' 
    
    # iterate ocer every neuron_key in neuron_dict
    for state_index in neuron_dict:
        for day_index in neuron_dict[state_index]:
            for epoch_index in neuron_dict[state_index][day_index]:
                
                epoch_dict = {} # experimental
                
                for neuron_key_index, neuron_key_str in enumerate(neuron_dict[state_index][day_index][epoch_index]):
                    # we are now inside a list of neuron key. I would prefer a dict structure
 
                    if type(neuron_key_str) == str:
                        
                        # unpack the neuron key from string to tuple
                        animal_short_name, day_number, epoch_number, tetrode_number, neuron_number = neuron_key_str.split("_")
                        neuron_key = (animal_short_name, int(day_number), int(epoch_number), int(tetrode_number), int(neuron_number))
                        
                        # if possible, replace neuron_key with time series
                        ## spike_time_array = None
                        try:
                            ## spike_time_array = spike_time_index_association(neuron_key, animal)
                            
                            epoch_dict[neuron_key_index] = spike_time_index_association(neuron_key, animal) # experimental
                            
                        except:
                            print("failed to load", neuron_key)
                        
                        ## neuron_dict[state_index][day_index][epoch_index][neuron_key_index] = spike_time_array 

                # create time Series group for each epoch
                time_series = nap.TsGroup(epoch_dict)
                
                # bin the spikes for each neuron into 5ms
                count = time_series.count(bin_size = 5, time_units = "ms")
                

                neuron_dict[state_index][day_index][epoch_index] = count # experimental

    return neuron_dict
import numpy as np
from scipy.io import loadmat
import pynapple as nap
from collections import namedtuple

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



# by using pynapple, we'll now definitely derive from Jans original code
# I just want to try leaving the time series the way they are. And seeing if we can get any results already
# finetuning can be done later
def spike_time_index_association(neuron_key, animal):
    ''' Calls get_trial_time for reference of dataframe size.
    Fits recorded data of neuron into the time bins.
    Parameters
    --------
    neuron_key : tuple
        key for specific neuron
    animals : dict
        file paths to all animal directories
    time_function : function
        optional
        by default get_trial_time
        determine size of dataframe (total recording time, recording frequency, ...)
    returns
    ---------
    spikes_df : dataframe
        number of spikes summed up for each time bin (-> activity)
    '''
    #print("neuron_key:", neuron_key)
    #time = time_function(neuron_key[:3], animal)
    #print("sdd: creating spikes_df")
    
    
    spikes_df = get_spikes_series(neuron_key, animal)
    return spikes_df
    

    
    '''
    time_index = None
    
    try:
        time_index = np.digitize(spikes_df.index.total_seconds(),
                             time.total_seconds())
 
        time_index[time_index >= len(time)] = len(time) -1
        return (spikes_df.groupby(time[time_index]).sum().reindex(index=time, fill_value=0))
    
    except AttributeError: 
        print('No spikes here; data is emtpy')
        return None
    '''
    

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

    try:
        neuron_file = loadmat(filename)
        spike_time = neuron_file['spikes'][0, -1][0, epoch - 1][0, tetrode_number - 1][0, neuron_number - 1][0]['data'][0][:, 0]
        ts = nap.Ts(t=spike_time, time_units= "s")
    
    except (FileNotFoundError, TypeError, IndexError):
        spike_time = []


    return ts


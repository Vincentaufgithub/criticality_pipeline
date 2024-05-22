import pandas as pd
import numpy as np
from math import ceil
import pynapple as nap
import utilities.load_spiking_times as spikes




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
            for epoch_index in neuron_dict[state_index][day_index]:
                

                grouped_time_series = spikes.grouped_time_series(neuron_dict[state_index][day_index][epoch_index], animal)
        
                
                if np.any(grouped_time_series):
                    
                
                    #with np.printoptions(threshold=np.inf):
                     #   for i in range(len(grouped_time_series)):
                      #      print(grouped_time_series[i])


                    # count() sometimes cuts off values, so we first have to define an epoch
                    # where the starting time will be the first recorded spike and the end time the last recorded spike

                    first_spikes = [grouped_time_series[i].start_time() for i in range(len(grouped_time_series))]
                    last_spikes = [grouped_time_series[i].end_time() for i in range(len(grouped_time_series))]
                    
                    # creating an epoch with first and last recorded spike time
                    # I rounded up the last spiking thime to the next highest number, making sure it still gets included
                    epoch = nap.IntervalSet(start = min(first_spikes), end = float(ceil(max(last_spikes))), time_units='s')
                    
                    
                    binned_ts_group = grouped_time_series.count(bin_size = bin_size, time_units = "ms", ep = epoch)
                    
                    with np.printoptions(threshold=np.inf):
                       print(binned_ts_group)
                        
                        
                    summed_activity = np.sum(binned_ts_group.values, axis=1)

                    
                    
                    with np.printoptions(threshold=np.inf):
                       print(summed_activity)

                    
                    return_dict[state_index][day_index][epoch_index] = summed_activity
                
                else:
                    print(f"no spiking data for: {state_index}, day {day_index}, epoch {epoch_index}")
                    return_dict[state_index][day_index][epoch_index] = None

    
    return return_dict
    # return spikes.load_and_bin_spike_data(neuron_dict, animal)





def run_mr_estimator_on_summed_activity(neuron_dict, bin_size, window_size):
    # here, we'll iterate over activity array
    # ... using np.array_split()
    
    # number of elements in each slice
    slice_size = int((window_size * 1000) / bin_size)
    
    for state_index in neuron_dict:
        for day_index in neuron_dict[state_index]:
            for epoch_index in neuron_dict[state_index][day_index]:
                
                if np.any(neuron_dict[state_index][day_index][epoch_index]):
                    time_chunks = spikes.activity_series_to_time_chunks(
                        neuron_dict[state_index][day_index][epoch_index],
                        slice_size)

                
                neuron_dict[state_index][day_index][epoch_index] = time_chunks
                
                
               
                    

            
    # after sclicing it, we can already run the estimator
    return neuron_dict








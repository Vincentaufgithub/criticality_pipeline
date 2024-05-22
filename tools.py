import pandas as pd
import numpy as np
from math import ceil
import pynapple as nap
import utilities.load_spiking_times as spikes


def save_binned_spike_trains(neuron_dict, destination_folder):
    for state_index in neuron_dict:
        for day_index in neuron_dict[state_index]:
            for epoch_index in neuron_dict[state_index][day_index]:
                thing = neuron_dict[state_index][day_index][epoch_index]
                # WILL CONTINUE HERE
    
    return



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








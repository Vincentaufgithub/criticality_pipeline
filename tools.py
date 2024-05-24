import pandas as pd
import numpy as np
import utilities.load_spiking_times as spikes

import mrestimator as mre


def save_binned_spike_trains(neuron_dict, destination_folder, key):
    for state_index in neuron_dict:
        for day_index in neuron_dict[state_index]:
            for epoch_index in neuron_dict[state_index][day_index]:
                
                epoch_data = neuron_dict[state_index][day_index][epoch_index]
                
                if not np.any(epoch_data):
                    continue
                
                for neuron in range (epoch_data.shape[1]):
                    filename = f"{destination_folder}{key[0]}_{key[1]}_{state_index}_{day_index:02d}_{epoch_index:02d}_{neuron:02d}.npy"
                    np.save(filename, epoch_data[:,neuron])
                    
                    # print(len(epoch_data[:,neuron]))
                 

    
    return



def run_mr_estimator_on_summed_activity(neuron_dict, bin_size, window_size, dest_folder, key):
    # here, we'll iterate over activity array
    # ... using np.array_split()
    
    # number of elements in each slice
    slice_size = int((window_size * 1000) / bin_size)
    
    for state_index in neuron_dict:
        for day_index in neuron_dict[state_index]:
            for epoch_index in neuron_dict[state_index][day_index]:
                
                data = neuron_dict[state_index][day_index][epoch_index]
                
                if not np.any(data):
                    continue
                
                
                # I find this important to estimate the quality of the analysis result
                num_neurons = data.shape[1]
                
                # sum up all spike occurrences for one epoch
                data = np.sum(data, axis=1)
                    
                # slicing
                time_chunks = spikes.activity_series_to_time_chunks(
                    data,slice_size)
                    
                    
                for n_chunk, chunk in enumerate(time_chunks):
    
                    print(len(chunk))
                    
                    if np.all(chunk == 0):
                        print("chunk empty")
                        continue
                    
                    try:
                        coefficients = mre.coefficients(chunk, dtunit='ms', dt = bin_size, method = 'ts')    
                            
                        output = mre.fit(coefficients.coefficients, fitfunc='f_complex')
                            
                        data_to_store = {
                                'popt': output.popt,
                                'ssres': output.ssres,
                                'steps': output.steps,
                                'dt': output.dt,
                                'dtunit': output.dtunit,
                                'quantiles': output.quantiles,
                                'mrequantiles': output.mrequantiles,
                                'tauquantiles': output.tauquantiles,
                                'description': output.description,
                                'tau': output.tau,
                                'branching_factor': output.mre,
                                'num_neurons': num_neurons
                            }

                            
                        data_to_store = pd.DataFrame([data_to_store])
                        filename = f"{dest_folder}{key[0]}_{key[1]}_{state_index}_{day_index:02d}_{epoch_index:02d}_{n_chunk:02d}.parquet"
                        data_to_store.to_parquet(filename, index = True)
                        
                        print("analysed and saved", filename)
                        print("tau =", output.tau, "branching_factor =", output.mre)
                    
                    
                    except Exception as e:
                        print(e, "; no Analysis possible")
    
    print("DONE for", key[0], key[1])
    return

                







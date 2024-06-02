import pandas as pd
import numpy as np
import utilities.load_spiking_times as spikes
import matplotlib.pyplot as plt
import mrestimator as mre


def save_binned_spike_trains(neuron_dict, destination_folder, key):
    '''
    The binned spike trains are intermediary results and exist for neuron in a recording epoch.
    They might look like: np.ndarray[0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0]
    Where each element represents a time bin (usually of 5ms) and the value represents the number of spikes that were registered in that bin (usually not exceeding 1)
    
    Will save the binned spike trains to given folder, so they might be used later / for different analysis methods.
    -----------------------
    parameters
    
    neuron_dict : dictionary
        nested dictionary with the structure {state:    {day:   {epoch: {2-D numpy array of binned spike trains }}}}
        ... as returned by lf_helper.load_spikes()
    
    destination_folder : str
        folder where to store the arrays in
    
    key : tuple
        (animal short name, area)
        used for naming the stored arrays
        
    ----------------------
    returns
    
    Will store the binned spike arrays in the .npy - format to disk.
    '''
    for state_index in neuron_dict:
        for day_index in neuron_dict[state_index]:
            for epoch_index in neuron_dict[state_index][day_index]:
                
                epoch_data = neuron_dict[state_index][day_index][epoch_index]
                
                if not np.any(epoch_data):
                    continue
                
                for neuron in range (epoch_data.shape[1]):
                    filename = f"{destination_folder}{key[0]}_{key[1]}_{state_index}_{day_index:02d}_{epoch_index:02d}_{neuron:02d}.npy"
                    np.save(filename, epoch_data[:,neuron])
                    
    return




# might consider breaking chunking and summing into a separate function
def run_mr_estimator_on_summed_activity(neuron_dict, bin_size, window_size, dest_folder, key):
    '''
    The spike_train_arrays for each epoch will be summed up to get the overall epoch activity.
    The activity will be sliced into chunks of window_size.
    MR Estimator will be run on the chunks.
    Results will be stored as parquet files to disk.
    
    ----------------------
    parameters
    
    neuron_dict : dictionary
        nested dictionary with the structure {state:    {day:   {epoch: {2-D numpy array of binned spike trains }}}}
        ... as returned by lf_helper.load_spikes()
    
    bin_size : int
        size that the neuron data was binned into, in ms
        for reference, we are currently using 5ms
    
    window_size : int
        size for chunks that will be analyzed separately, in s
        for reference, we are currently usind 90s
    
    dest_folder : str
        folder where to store the analysis results into
        
    key : tuple
        (animal short name, area)
        used for naming the stored files
        
    ----------------------------    
    returns
    
    Will store important values of the mr.estimator analysis result as parquet files to disk.
    Most importantly, tau_value and branching factor.
    File will be named like: "animalname_area_day_epoch_timechunk.parquet"
    '''
    
    # number of bins in each slice
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

                




def create_and_save_graph(coefficients, output_handler):
    plt.plot(coefficients.steps, coefficients.coefficients, label='data')
            
    plt.plot(coefficients.steps, mre.f_complex(coefficients.steps, *output_handler.popt),
                label='complex m={:.5f}'.format(output_handler.mre))

    plt.legend()
    plt.savefig(f"/local2/Vincent/graphs/example_graphic.png")
    print("SAVED FIG")






def mr_estimator_for_prepared_epoch_data(data, window_size, bin_size, fit_func, filename):
    
    if not np.any(data):
        return
    
    
    slice_size = slice_size = int((window_size * 1000) / bin_size)
    
    
    # I find this important to estimate the quality of the analysis result
    num_neurons = data.shape[1]
                
    # sum up all spike occurrences for one epoch
    data = np.sum(data, axis=1)
                    
    # slicing
    time_chunks = spikes.activity_series_to_time_chunks(
        data,slice_size)
                    
                    
    for n_chunk, chunk in enumerate(time_chunks):
                    
        if np.all(chunk == 0):
            print("chunk empty")
            continue
                    
        try:
            coefficients = mre.coefficients(chunk, dtunit='ms', dt = bin_size, method = 'ts')    
                        
                        
                        
            output = mre.fit(coefficients.coefficients, fitfunc = fit_func)

                        
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
                        
            data_to_store.to_parquet(f'{filename}{n_chunk:02d}', index = True)
                        
            print("analysed and saved", filename)
            print("tau =", output.tau, "branching_factor =", output.mre)
                    
                    
        except Exception as e:
            print(e, "; no Analysis possible")
            
    return
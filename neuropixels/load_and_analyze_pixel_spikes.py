import numpy as np
import pandas as pd
from pynwb import NWBHDF5IO
import os


def bin_spike_times_incrementally(nwb_file_path, output_dir, bin_size=0.001, chunk_size=90):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    with NWBHDF5IO(nwb_file_path, 'r') as io:
        nwbfile = io.read()

        if not nwbfile.units:
            raise ValueError("No units found in the NWB file.")
        
        units = nwbfile.units
        spike_times_dict = {unit_id: units['spike_times'][i] for i, unit_id in enumerate(units.id)}
        
        session_duration = max(max(times) for times in spike_times_dict.values())
        chunk_count = int(np.ceil(session_duration / chunk_size))
        
        for chunk_idx in range(chunk_count):
            start_time = chunk_idx * chunk_size
            end_time = start_time + chunk_size
            bins = np.arange(start_time, end_time + bin_size, bin_size)
            binned_data = {}
            timestamps = []

            for bin_idx in range(len(bins) - 1):
                bin_time = start_time + bin_idx * bin_size
                timestamps.append(bin_time)

            for unit_id, spike_times in spike_times_dict.items():
                # Select spikes within the current chunk
                chunk_spikes = spike_times[(spike_times >= start_time) & (spike_times < end_time)]
                binned_spikes, _ = np.histogram(chunk_spikes, bins)
                binned_data[unit_id] = binned_spikes

            # Convert the current chunk to DataFrame
            chunk_df = pd.DataFrame(binned_data, index=timestamps)
            chunk_df.index.name = 'Time'

            # Save the chunk DataFrame to disk
            chunk_df.to_csv(os.path.join(output_dir, f'chunk_{chunk_idx}.csv'))

# Example usage
nwb_file_path = '/local2/Jan/ecephys_data/session_715093703/session_715093703.nwb'
output_dir = '/local2/Jan/ecephys_data/processed_chunks_testing_22_05'
bin_spike_times_incrementally(nwb_file_path, output_dir, bin_size=0.005, chunk_size=90)

import os
import pandas as pd

def retrieve_single_chunk(output_dir, chunk_index=0):
    # List all chunk files in the directory
    chunk_files = sorted([f for f in os.listdir(output_dir) if f.startswith('chunk_') and f.endswith('.csv')])
    
    # Check if the specified chunk index is within the range of available chunks
    if chunk_index < 0 or chunk_index >= len(chunk_files):
        raise IndexError("Chunk index out of range.")
    
    # Retrieve the specified chunk file
    chunk_file = chunk_files[chunk_index]
    chunk_df = pd.read_csv(os.path.join(output_dir, chunk_file), index_col=0)
    
    # Return the single chunk DataFrame
    return chunk_df

# Example usage
output_dir = '/local2/Jan/ecephys_data/processed_chunks_testing_22_05'
chunk_index = 0  # Change this to retrieve a different chunk
single_chunk_df = retrieve_single_chunk(output_dir, chunk_index)
display(single_chunk_df)
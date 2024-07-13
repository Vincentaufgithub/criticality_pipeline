# script in order to get an overview of the number of results, trials, animals, ... tht we analyzed

# %%
############################
# get number of individual trials

import os
from collections import defaultdict

def count_combinations(folder_path: str) -> dict:
    # Get list of all files in the folder
    files = os.listdir(folder_path)
    
    # Dictionary to store the count of each letter combination
    combination_counts = defaultdict(int)
    
    for file in files:
        # Extract the letter combination before the underscore
        if "_" in file:
            combination = f'{file.split("_")[1]}'
            combination_counts[combination] += 1
    
    return dict(combination_counts)

# Example usage
folder_path = '/local2/Vincent/neuro_pixels_output_f_complex/'  # Replace with the path to your folder
unique_count = count_combinations(folder_path)
print(unique_count)
print(len(unique_count))



# %%
################################
# get average number of neurons per time chunk

import os
import pandas as pd
import statistics

def compute_average_n_neurons(folder_path: str) -> float:
    # List of n_neurons values
    n_neurons_list = []

    # Iterate over all files in the folder
    for file in os.listdir(folder_path):

        file_path = os.path.join(folder_path, file)
            # Read the parquet file
        df = pd.read_parquet(file_path)
            # Extract the n_neurons value and append to the list
        
        n_neurons_list.append(df['num_neurons'].iloc[0])
        

    # Compute the average of n_neurons values
    average_n_neurons = sum(n_neurons_list) / len(n_neurons_list)
    std_dev = statistics.stdev(n_neurons_list)
    
    return average_n_neurons, std_dev
   

folder_path = '/local2/Vincent/neuro_pixels_output_f_complex/'  
average_n_neurons, stdev = compute_average_n_neurons(folder_path)
print(f"Average n_neurons: {average_n_neurons}; stdev: {stdev}")






# %%
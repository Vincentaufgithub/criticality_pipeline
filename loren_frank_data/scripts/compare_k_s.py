###################
# this file will compute tau values for a specific animal, but with different ks
#  so we can correlate the results
###################



# %%

import os
import numpy as np
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))
sys.path.append(parent_dir)
import tools


# The code below will load all spiking arrays and corresponding tau values
# Can then be used either to run new analysises or to create graphs.

# Define the directory containing the .npy files
directory = '/local2/Vincent/binned_spiking_data/'

# Define the prefix to search for
prefix = 'bon_CA1_sleep'

# Get a list of all .npy files in the directory
npy_files = [f for f in os.listdir(directory) if f.startswith(prefix)]

steps_list = [1000, 2000]



# Group files by their base name (excluding the last 6 characters)
# so spike trains will be grouped by session and area

file_groups = {}
for file in npy_files:
    base_name = file[:-6]
    if base_name not in file_groups:
        file_groups[base_name] = []
    file_groups[base_name].append(os.path.join(directory, file))

for step in steps_list:
    
    for base_name, file_list in file_groups.items():
        arrays = [np.load(file).reshape(-1, 1) for file in file_list]
        
        data = np.concatenate(arrays, axis=1)

        tools.mr_estimator_for_prepared_epoch_data(data, 
                                                window_size= 30,
                                                bin_size= 5,
                                                fit_func = "f_complex",
                                                filename = f'/local2/Vincent/loren_frank/MR_comparing_ks/k_{str(step)}/{base_name}',
                                                input_steps = (1, step)
                                                )



# %%





#######################
# Creating plot to compare analysis results
#######################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mode


def extract_taus(directory: str, files: list) -> list :
    taus : list = []
    
    for file in files:
        taus.append(pd.read_parquet(f'{directory}{file}')["tau"][0])
        
    return taus



# k 1000
directory_k_1000 = '/local2/Vincent/loren_frank/MR_comparing_ks/k_1000/'
files_k_1000 = [f for f in os.listdir(directory_k_1000)]
taus_1 = extract_taus(directory_k_1000, files_k_1000)

# k 2000
directory_k_2000 = '/local2/Vincent/loren_frank/MR_comparing_ks/k_2000/'
files_k_2000 = [f for f in os.listdir(directory_k_2000)]
taus_2 = extract_taus(directory_k_2000, files_k_2000)

# k 3000
directory_k_3000 = '/local2/Vincent/loren_frank/MR_30s_revised/'
files_k_3000 = [f for f in os.listdir(directory_k_3000) if f.startswith('bon_CA1_sleep')]
taus_3 = extract_taus(directory_k_3000, files_k_3000)



# Create a DataFrame from the lists
data = pd.DataFrame({
    'k = 1000': pd.Series(taus_1),
    'k = 2000': pd.Series(taus_2),
    'k = 3000': pd.Series(taus_3)
})

# Melt the DataFrame to long format for easier plotting
melted_data = pd.melt(data, var_name='Analysis', value_name='tau values')

# Plotting
plt.figure(figsize=(14, 7))

# Use seaborn to create violin plots
sns.violinplot(data=melted_data, x='Analysis', y='tau values', inner=None, bw=0.05)

# Calculate and plot mean, std, and mode for each analysis
for i, analysis in enumerate(['k = 1000', 'k = 2000', 'k = 3000']):
    results = data[analysis].dropna()
    mean_result = results.mean()
    std_result = results.std()
    median_result = np.median(results)

     # Annotate the values on the plot
    plt.text(i, results.max(), f'Mean: {mean_result:.2f}', horizontalalignment='center', size='medium', color='red', weight='semibold')
    plt.text(i, results.max() - (results.max() - results.min()) * 0.05, f'Std: {std_result:.2f}', horizontalalignment='center', size='medium', color='black', weight='semibold')
    plt.text(i, results.max() - (results.max() - results.min()) * 0.10, f'Median: {median_result:.2f}', horizontalalignment='center', size='medium', color='blue', weight='semibold')

# Enhance the plot
plt.title('Comparing Parameter k for bon_CA1_sleep: ca. 890 chunks')
plt.xlabel('k Parameter')
plt.ylabel('tau (ms)')
plt.legend(title='Statistics', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

# Save the plot to disk
plt.savefig('/local2/Vincent/loren_frank/MR_comparing_ks/neural_data_analysis_comparison_with_violin.png', bbox_inches='tight')

# Display the plot
plt.show()




# %%





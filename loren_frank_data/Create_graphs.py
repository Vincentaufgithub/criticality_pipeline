# %%

import os
import numpy as np
import tools
import glob
import pandas as pd
import utilities.load_spiking_times as spikes
import matplotlib.pyplot as plt
import seaborn as sns

# %%
# The code below will load all spiking arrays and corresponding tau values
# Can then be used either to run new analysises or to create graphs.

# Define the directory containing the .npy files
directory = '/local2/Vincent/binned_spiking_data/'


# Get a list of all .npy files in the directory
npy_files = [f for f in os.listdir(directory)]


# %%


# Group files by their base name (excluding the last 6 characters)
file_groups = {}
for file in npy_files:
    base_name = file[:-6]
    if base_name not in file_groups:
        file_groups[base_name] = []
    file_groups[base_name].append(os.path.join(directory, file))



# %%
tau_values = []
total_activity = []
n_neurons = []

# Load and concatenate arrays for each group
for base_name, file_list in file_groups.items():
    arrays = [np.load(file).reshape(-1, 1) for file in file_list]
    
    data = np.concatenate(arrays, axis=1)
    chunk_list = spikes.activity_series_to_time_chunks(data, 18000)
    
    for n, element in enumerate(chunk_list):
        
        try:
            loaded_file = pd.read_parquet(f"/local2/Vincent/mr_analysis_with_new_pipeline/{base_name}{n:02d}.parquet")
    
            tau_values.append(loaded_file["tau"][0])
            # total_activity.append(np.sum(element))
            n_neurons.append(loaded_file["num_neurons"][0])
            
        except:
            print("failed to load", f"{base_name}{n:02d}")
            continue
        
    

# %%
# Calculate the correlation coefficient
correlation_matrix = np.corrcoef(n_neurons, tau_values)
correlation_coefficient = correlation_matrix[0, 1]

x_values_scattered = n_neurons + np.random.normal(0, 0.1, size=np.array(n_neurons).shape)

plt.scatter(x_values_scattered, tau_values, color='blue', marker='o', s=20, alpha = 0.25, edgecolors="none")

sns.regplot(x= n_neurons, y= tau_values, scatter=False, color='red')

plt.xlabel("Number of recorded units")
plt.ylabel("tau value in ms")

plt.suptitle("Plotting tau relative to number of units")
plt.title(f'r = {correlation_coefficient:.2f}', fontsize = 10)
plt.show()
    
plt.savefig('/local2/Vincent/graphs/scatter_plot_1.png')



    
# %%
# runs mr.estimator again, with f_exponential_offset, to compare.
tools.mr_estimator_for_prepared_epoch_data(data, window_size= 90,
                                               bin_size= 5,
                                               fit_func = "f_exponential_offset",
                                               filename = f'/local2/Vincent/mr_analysis_with_exponential/{base_name}',
                                               )

# %%


# correlate f_complex and f_exponential_offset

import os
import numpy as np
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# COMPLEX
directory_complex = '/local2/Vincent/mr_analysis_with_new_pipeline/'
file_list_complex = sorted([file for file in os.listdir(directory_complex)])


# EXPONENTIAL_OFFSET 
directory_expo = '/local2/Vincent/mr_analysis_with_exponential/'
file_list_expo = sorted([file for file in os.listdir(directory_expo)])


set_complex = set(file_list_complex)
set_expo = set(file_list_expo)

# Step 2: Identify common elements
common_elements = list(set_complex.intersection(set_expo))




tau_list_complex = []
tau_list_expo = []


for file in common_elements:
    tau_1 = pd.read_parquet(f'{directory_complex}{file}')["tau"][0]
    if tau_1 <= 0 or tau_1 >= 3000:
        continue
    
    
    tau_2 = pd.read_parquet(f'{directory_expo}{file}')["tau"][0]
    # imputing values because the exponential function doesn't have a cutoff.
    if tau_2 <= 0 or tau_2 >= 3000:
        continue
    
    
    tau_list_complex.append(tau_1)
    tau_list_expo.append(tau_2)
    

correlation_matrix = np.corrcoef(tau_list_complex, tau_list_expo)
correlation_coefficient = correlation_matrix[0, 1]

print(correlation_coefficient)


plt.scatter(tau_list_complex, tau_list_expo, color='blue', marker='o', s=20, alpha = 0.25, edgecolors="none")

sns.regplot(x= tau_list_complex, y= tau_list_expo, scatter=False, color='red')

plt.xlabel("Tau values for f_complex")
plt.ylabel("Tau values for f_exponential_offset")

plt.suptitle("Correlating f_complex and f_exponential_offset, corrected for artefacts")
plt.title(f'r = {correlation_coefficient:.2f}', fontsize = 10)
plt.show()
    
plt.savefig('/local2/Vincent/graphs/correlation_complex_expo_1.png')


# %%
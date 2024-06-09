# %%

import matplotlib.pyplot as plt
import seaborn as sns
import glob
import pandas as pd
import numpy as np


def get_tau_and_weights(filepath):
    tau_values = []
    weights = []
    filenames = []
    
    for file in glob.glob(filepath):
        loaded = pd.read_parquet(file)
        tau_values.append(loaded["tau"][0])
        weights.append(loaded["num_neurons"][0])
        filenames.append(file)
    
    return tau_values, weights


def filter_artefacts(data, lower = 0, upper = 100000):
    
    for i in range(len(data)):
        data[i] = [x for x in data[i] if lower < x < upper]
    return data


def calculate_weighted_mean(values, weights):
    weights = np.log(weights)
    
    mean = np.sum(values * weights) / np.sum(weights)
    
    variance = np.sum(weights * (values - mean) ** 2) / np.sum(weights)
    std = np.sqrt(variance)
    
    return (mean, std)


def multiply_values_for_violin(data, weights):
    
    return_data = []
    for a,b in zip(data, weights):
        area_data =  []
        for c,d in zip(a,b):
            for i in range(int(round(np.log(d)))):
                area_data.append(c)
        
        return_data.append(area_data)
    
    return return_data        


def get_avg_windows(data):
    total = 0
    
    for element in data:
        total += len(element)
    
    return round(total/len(data) , 2)



def get_avg_weight(weights):
    total = 0
    n_weights = 0
    
    for element in weights:
        total += np.sum(element)
        n_weights += len(element)
        
    return round(total/n_weights , 2)



'''
ca1_wake_values, ca1_wake_weights = get_tau_and_weights("/local2/Vincent/mr_analysis_with_new_pipeline/*CA1_wake*.parquet")
ca1_sleep_values, ca1_sleep_weights = get_tau_and_weights("/local2/Vincent/mr_analysis_with_new_pipeline/*CA1_sleep*.parquet")

ca2_wake_values, ca2_wake_weights = get_tau_and_weights("/local2/Vincent/mr_analysis_with_new_pipeline/*CA2_wake*.parquet")
ca2_sleep_values, ca2_sleep_weights = get_tau_and_weights("/local2/Vincent/mr_analysis_with_new_pipeline/*CA2_sleep*.parquet")

ca3_wake_values, ca3_wake_weights = get_tau_and_weights("/local2/Vincent/mr_analysis_with_new_pipeline/*CA3_wake*.parquet")
ca3_sleep_values, ca3_sleep_weights = get_tau_and_weights("/local2/Vincent/mr_analysis_with_new_pipeline/*CA3_sleep*.parquet")

# Combine the lists into a single list
data = [ca1_wake_values, ca1_sleep_values, ca2_wake_values, ca2_sleep_values, ca3_wake_values, ca3_sleep_values]
weights = [ca1_wake_weights, ca1_sleep_weights, ca2_wake_weights, ca2_sleep_weights, ca3_wake_weights, ca3_sleep_weights]
'''

'''
ca1_values, ca1_weights = get_tau_and_weights("/local2/Vincent/mr_analysis_with_new_pipeline/*CA1*.parquet")
ca2_values, ca2_weights = get_tau_and_weights("/local2/Vincent/mr_analysis_with_new_pipeline/*CA2*.parquet")
ca3_values, ca3_weights = get_tau_and_weights("/local2/Vincent/mr_analysis_with_new_pipeline/*CA3*.parquet")

# Combine the lists into a single list
data = [ca1_values, ca2_values, ca3_values]
weights = [ca1_weights, ca2_weights, ca3_weights]
'''


act_0, weights_0 = get_tau_and_weights("/local2/Vincent/mr_analysis_with_new_pipeline/*_00.parquet")
act_1, weights_1 = get_tau_and_weights("/local2/Vincent/mr_analysis_with_new_pipeline/*_01.parquet")
act_2 , weights_2= get_tau_and_weights("/local2/Vincent/mr_analysis_with_new_pipeline/*_02.parquet")
act_3, weights_3 = get_tau_and_weights("/local2/Vincent/mr_analysis_with_new_pipeline/*_03.parquet")
act_4 , weights_4= get_tau_and_weights("/local2/Vincent/mr_analysis_with_new_pipeline/*_04.parquet")
act_5, weights_5 = get_tau_and_weights("/local2/Vincent/mr_analysis_with_new_pipeline/*_05.parquet")








'''

wake_values, wake_weights, filenames = get_tau_and_weights("/local2/Vincent/mr_analysis_with_exponential/*wake*.parquet")
# sleep_values, sleep_weights = get_tau_and_weights("/local2/Vincent/mr_analysis_with_exponential/*sleep*.parquet")



values_array = np.array(wake_values)
# Get the indices of the ten greatest values
top_ten_indices = np.argsort(values_array)[-10:]

for element in top_ten_indices:
    print(filenames[element], ":", values_array[element])

'''


# %%
# Combine the lists into a single list
data = [act_0, act_1, act_2, act_3, act_4, act_5]
weights = [weights_0, weights_1, weights_2, weights_3, weights_4, weights_5]









# %%

weighted_statistics = []
for v, w in zip(data, weights):
    weighted_statistics.append(calculate_weighted_mean(v,w))

'''
data = multiply_values_for_violin(data, weights)

'''
# Set the style
sns.set(style="whitegrid")

fig, ax = plt.subplots()
sns.violinplot(data=data, ax=ax)


# Set the labels for each list on the x-axis
plt.xticks(ticks=[0, 1,2,3,4,5], labels=["0", '1', "2", "3", "4", "5"])

# Add title and labels
plt.title(f'Comparing criticality')
plt.xlabel('')
plt.ylabel('Tau (ms)')



# Annotate mean and standard deviation for each list
for i, stat in enumerate(weighted_statistics):
    ax.text(i, stat[0] + stat[1], f'Mean: {stat[0]:.2f}\nStd: {stat[1]:.2f}', # also include n(animals), n(chunks) and median(n(neurons))
            horizontalalignment='center', 
            size='small', 
            color='black', 
            weight='semibold')
    
    
    
avg_windows = get_avg_windows(weights)
avg_weight = get_avg_weight(weights)
    
# Add an explanatory text at the bottom of the plot
plt.figtext(0.5, -0.05,
            f"For f_exp. 11 animals, each plot from on average of {avg_windows} chunks, consisting of an avg of {avg_weight} neurons. Each chunk is weighted with ln(n_neurons)", 
            wrap=True, horizontalalignment='center', fontsize=12)



plt.savefig('/local2/Vincent/graphs/time_plot.png')




# %%
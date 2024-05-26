# %%

import matplotlib.pyplot as plt
import seaborn as sns
import glob
import pandas as pd
import numpy as np



'''
ca1_wake = [pd.read_parquet(file)["tau"][0] for file in glob.glob("/local2/Vincent/mr_analysis_with_new_pipeline/*CA1_wake*.parquet")]
ca1_sleep = [pd.read_parquet(file)["tau"][0] for file in glob.glob("/local2/Vincent/mr_analysis_with_new_pipeline/*CA1_sleep*.parquet")]
ca3_wake = [pd.read_parquet(file)["tau"][0] for file in glob.glob("/local2/Vincent/mr_analysis_with_new_pipeline/*CA3_wake*.parquet")]
ca3_sleep = [pd.read_parquet(file)["tau"][0] for file in glob.glob("/local2/Vincent/mr_analysis_with_new_pipeline/*CA3_sleep*.parquet")]
'''


ca1_wake = []
for file in glob.glob("/local2/Vincent/mr_analysis_with_new_pipeline/*CA1_wake*.parquet"):
    loaded = pd.read_parquet(file)
    tau = loaded["tau"][0]
    
    for i in range(loaded["num_neurons"][0]):
        ca1_wake.append(tau)


ca1_sleep = []
for file in glob.glob("/local2/Vincent/mr_analysis_with_new_pipeline/*CA1_sleep*.parquet"):
    loaded = pd.read_parquet(file)
    tau = loaded["tau"][0]
    
    for i in range(loaded["num_neurons"][0]):
        ca1_sleep.append(tau)     



ca3_wake = []
for file in glob.glob("/local2/Vincent/mr_analysis_with_new_pipeline/*CA3_wake*.parquet"):
    loaded = pd.read_parquet(file)
    tau = loaded["tau"][0]
    
    for i in range(loaded["num_neurons"][0]):
        ca3_wake.append(tau)


ca3_sleep = []
for file in glob.glob("/local2/Vincent/mr_analysis_with_new_pipeline/*CA3_sleep*.parquet"):
    loaded = pd.read_parquet(file)
    tau = loaded["tau"][0]
    
    for i in range(loaded["num_neurons"][0]):
        ca3_sleep.append(tau) 


# Combine the lists into a single list
data = [ca1_wake, ca1_sleep, ca3_wake, ca3_sleep]


# filter artefacts
for i in range(len(data)):
    # print(len(data[i]))

    data[i] = [x for x in data[i] if 6 <= x <= 4999]




means = [np.mean(lst) for lst in data]
std_devs = [np.std(lst) for lst in data]




# Set the style
sns.set(style="whitegrid")

fig, ax = plt.subplots()
sns.violinplot(data=data, ax=ax)


# Set the labels for each list on the x-axis
plt.xticks(ticks=[0, 1, 2, 3], labels=['CA1_wake', 'CA1_sleep', 'CA3_wake', 'CA3_sleep'])

# Add title and labels
plt.title('Comparing criticality for different areals and states')
plt.xlabel('Area - State Combination')
plt.ylabel('Tau (ms)')



# Annotate mean and standard deviation for each list
for i, (mean, std) in enumerate(zip(means, std_devs)):
    ax.text(i, mean + std, f'Mean: {mean:.2f}\nStd: {std:.2f}', 
            horizontalalignment='center', 
            size='small', 
            color='black', 
            weight='semibold')
    
    
    


plt.savefig('/local2/Vincent/graphs/criticality_violin_plots_3.png')




# %%
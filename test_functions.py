# just a playground to test simple functionalites

import pynapple as nap
from scipy.io import loadmat
from collections import namedtuple

Animal = namedtuple('Animal', {'short_name', 'directory'})

animals_dict = {
           'fra' : Animal(short_name = 'fra', directory = '/local2/Jan/Frank/Frank/'),
           'gov' : Animal(short_name = 'gov', directory = '/local2/Jan/Government/Government/'),
           'egy' : Animal(short_name = 'egy', directory = '/local2/Jan/Egypt/Egypt/'), 
           'remy': Animal(short_name = 'remy', directory = '/local2/Jan/Remy/Remy/'),
           #"Fiv" : Animal(short_name = "Fiv", directory = "/home/dekorvyb/Downloads/Fiv"),
           "bon" : Animal(short_name = "bon", directory = "/home/dekorvyb/Downloads/Bon/"),
            "Cor" : Animal(short_name = "Cor", directory = "/home/dekorvyb/Downloads/Corriander/"),
            "con" : Animal(short_name = "con", directory = "/home/dekorvyb/Downloads/Con/"),
            #"ten" : Animal(short_name = "ten", directory = "/home/dekorvyb/Downloads/Ten/"),
            #"dud" : Animal(short_name = "dud", directory = "/home/dekorvyb/Downloads/Dudley/"),
            "cha" : Animal(short_name = "cha", directory = "/home/dekorvyb/Downloads/Chapati/"),
            #"Eig" : Animal(short_name = "Eig", directory = "/home/dekorvyb/Downloads/Eig/"),
            "dav" : Animal(short_name = "dav", directory = "/home/dekorvyb/Downloads/Dave/")
            }

animal = animals_dict["fra"]



neuron_key = ("bon", 1,1,1,1)
name, day, epoch, tetrode_number, neuron_number = neuron_key

### load the corresponding spikes-file
neuron_file = loadmat(f"{animal.directory}{animal.short_name}spikes0{day}.mat")
spike_time = neuron_file['spikes'][0, -1][0, epoch - 1][0, tetrode_number - 1][0, neuron_number - 1][0]['data'][0][:, 0]

### create a time series for each neuron
ts = nap.Ts(t=spike_time, time_units= "s")


# %%
import mrestimator as mre

bp = mre.simulate_branching(m=0.995, a=10, numtrials=15)

print(bp)

# %%


import pickle
import glob
import pandas as pd


def help_func(string):
    return int(string[-9])



former_filenames = glob.glob("/local2/Vincent/ts_90s/_fra_CA1_wake_4_2_*")
former_filenames.sort(key = help_func)
print(former_filenames)

former_values = []
for element in former_filenames:
    former_values.append(pd.read_parquet(element))
    

 
new_filenames = glob.glob("/home/dekorvyb/trash/fra_CA1_wake_04_02_*.parquet")
new_filenames.sort(key = help_func)
print(new_filenames)


new_values = []
for element in new_filenames:
    new_values.append(pd.read_parquet(element))


for i in range(len(former_values)): 
    print("######################################")
    print("######################################")
    print("FORMER")
    print(former_values[i])
    print("######################################")
    print("NEW")
    print(new_values[i])

# %%


import pynapple as nap
import numpy as np

ts = nap.Ts(t=np.sort(np.random.uniform(9000, 10000, 30)), time_units="s")


print(ts)

# %%
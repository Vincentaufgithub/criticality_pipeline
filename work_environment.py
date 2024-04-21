# %%

import pynapple as nap
from collections import namedtuple
from scipy.io import loadmat
import numpy as np
import pandas as pd
import mrestimator as mre
import matplotlib.pyplot as plt

import tools
# %%


### Creating dictionary with animal file paths
### to efficiently switch between animals and fetch the names of existing files
# ### Defining each animal via its short name and its directory
Animal = namedtuple('Animal', {'short_name', 'directory'})

# remy not working AT ALL
# so far, you also need to update the animals_dict in pipeline.lfp_data_to_dataframe. Workin on that
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



### define animal we want to look at
# so far, we'll only do one animal at once
# if we want, we can later iterate over a list of animals, but I would add this at the very end
animal = animals_dict["fra"]
areas = ["CA1", "CA3"]


### Create a dictionary with information on the recordings
# containing one pandas.df for each recorded area
# with the following column names:
# ['spikewidth', 'meanrate', 'numspikes', 'area', 'tetnum', 'neuron_id'


#cellinfo_dict_sorted_by_area = tools.create_sorted_dict_with_cellinfos(animal)

# we now have all the neuron keys and know which brain area the belong to.
# next, we need to find out in which epoch the animal was resting and in which epoch the animal was running
# as far as I understood, pynapple is not yet able to support us here
# that is because we are working with matlab files. Pynapple is written for nwb files. :(



taskinfo_dict_sorted_by_state = tools.create_sorted_dict_with_tasks(animal)


# %%

neuron_key = ("bon", 1,1,1,1)
name, day, epoch, tetrode_number, neuron_number = neuron_key

### load the corresponding spikes-file
neuron_file = loadmat(f"{animal.directory}{animal.short_name}spikes0{day}.mat")
spike_time = neuron_file['spikes'][0, -1][0, epoch - 1][0, tetrode_number - 1][0, neuron_number - 1][0]['data'][0][:, 0]

### create a time series for each neuron
ts = nap.Ts(t=spike_time, time_units= "s")
print(ts)


### just for fun, let's see if we can already run Mr. Estimator on this time series

# this gives a numpy.ndarray - exactly what we need for mrestimator!
values = ts.index.values
#print("values", values)
#print("type", type(values))

coefficients = mre.coefficients(values, dt=6.67, dtunit='ms', method = 'ts')
output_handler = mre.fit(coefficients.coefficients, fitfunc='f_complex')

       
plt.plot(coefficients.steps, coefficients.coefficients, label='data')
        
plt.plot(coefficients.steps, mre.f_complex(coefficients.steps, *output_handler.popt),
            label='complex m={:.5f}'.format(output_handler.mre))

plt.legend()
plt.savefig("/home/dekorvyb/trash/graphic.png")
print("saved succesfully")
# - Hoorray! It finally looks the way we want to


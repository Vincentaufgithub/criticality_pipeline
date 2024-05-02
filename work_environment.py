# %%

import pynapple as nap
import mrestimator as mre

from collections import namedtuple
from scipy.io import loadmat
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import tools


# Creating dictionary with animal file paths
# Defining each animal via its short name and its directory
Animal = namedtuple('Animal', {'short_name', 'directory'})

animals_dict = {
           'fra' : Animal(short_name = 'fra', directory = '/local2/Jan/Frank/Frank/'),
           'gov' : Animal(short_name = 'gov', directory = '/local2/Jan/Government/Government/'),
           'egy' : Animal(short_name = 'egy', directory = '/local2/Jan/Egypt/Egypt/'), 
           'remy': Animal(short_name = 'remy', directory = '/local2/Jan/Remy/Remy/'),
           "bon" : Animal(short_name = "bon", directory = "/home/dekorvyb/Downloads/Bon/"),
            "Cor" : Animal(short_name = "Cor", directory = "/home/dekorvyb/Downloads/Corriander/"),
            "con" : Animal(short_name = "con", directory = "/home/dekorvyb/Downloads/Con/"),
            "cha" : Animal(short_name = "cha", directory = "/home/dekorvyb/Downloads/Chapati/"),
            "dav" : Animal(short_name = "dav", directory = "/home/dekorvyb/Downloads/Dave/"),
            
            #"Fiv" : Animal(short_name = "Fiv", directory = "/home/dekorvyb/Downloads/Fiv"),
            #"ten" : Animal(short_name = "ten", directory = "/home/dekorvyb/Downloads/Ten/"),
            #"dud" : Animal(short_name = "dud", directory = "/home/dekorvyb/Downloads/Dudley/"),
            #"Eig" : Animal(short_name = "Eig", directory = "/home/dekorvyb/Downloads/Eig/")
            }


# might be useful to write a function which loads the cellinfo files for all animals in animals_dict.
# so we would get an overview of all the areas that were recorded for each animal.


# define animals and areas of interest
# if we want, we can later iterate over a list of animals, but I would add this at the very end
animal = animals_dict["fra"]
area_list = ["CA1"]


# print(cellinfo_dict_sorted_by_area.keys()) # shows all the areas that were recorded in given animal
cellinfo_dict_sorted_by_area = tools.create_sorted_dict_with_cellinfos(animal)

taskinfo_dict_sorted_by_state = tools.create_sorted_dict_with_tasks(animal)


for area in area_list:
    neuron_dict = tools.create_neuron_dicts_for_each_state(cellinfo_dict_sorted_by_area[(area,)], taskinfo_dict_sorted_by_state)
    spikes = tools.load_spikes(neuron_dict, animal)
    
    tools.run_mr_estimator_on_summed_activity()
    
    # in the code above, we converted the dataset with its specific structure into the desired format
    # the goal is to get to the same format with other datasets too, so the rest of the code will work universally

# %%
      
#print(spikes["wake"][4][4])

# this is great. Now we need to sum up all the neuron activity for each epoch. Then slice it. Then run mr.estimator. Then we should be finished.



epoch_ts_group = spikes["wake"][4][2]



# %%


overall_activity = np.sum(epoch_ts_group.values, axis=1)


coefficients = mre.coefficients(overall_activity, dt=5, dtunit='ms', method = 'ts')
output_handler = mre.fit(coefficients.coefficients, fitfunc='f_complex')

       
plt.plot(coefficients.steps, coefficients.coefficients, label='data')
        
plt.plot(coefficients.steps, mre.f_complex(coefficients.steps, *output_handler.popt),
            label='complex m={:.5f}'.format(output_handler.mre))

plt.legend()
plt.savefig("/home/dekorvyb/trash/graphic.png")
print("saved succesfully")
# - Hoorray! It finally looks the way we want to


# %%
# below is just experimental to understand the interplay of pynapple and mrestimator



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
print("test for github")

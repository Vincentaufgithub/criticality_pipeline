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



former_filenames = glob.glob("/home/dekorvyb/trash/_fra_CA3_wake_2_*")
# former_filenames.sort(key = help_func)
print(former_filenames)

former_values = []
for element in former_filenames:
    former_values.append((pd.read_parquet(element)["tau"], element))
    

 
new_filenames = glob.glob("/local2/Vincent/mr_analysis_with_new_pipeline/fra_CA3_wake_02_*")
# new_filenames.sort(key = help_func)
print(new_filenames)


new_values = []
for element in new_filenames:
    new_values.append((pd.read_parquet(element)["tau"], element))



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




###################################################
# Former code from work_environment.py
# looks like a mess, but keeping it here because I know it definitively works
###################################################





import pynapple as nap
import mrestimator as mre

from collections import namedtuple
from scipy.io import loadmat
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle

import tools
import loren_frank_helper_functions as lf_helper




epoch_ts_group = spikes["wake"][4][2]

for i in range(len(epoch_ts_group)):
    
    # plt.clf()
    
    overall_activity = epoch_ts_group[i]
    print(overall_activity)
    
    coefficients = mre.coefficients(overall_activity, dtunit='ms', dt = 5, method = 'ts')    
    
    output_handler = mre.fit(coefficients.coefficients, fitfunc='f_complex')
    
    data_to_store = {
            'popt': output_handler.popt,
            'ssres': output_handler.ssres,
            'pcov': [],
            'steps': output_handler.steps,
            'dt': output_handler.dt,
            'dtunit': output_handler.dtunit,
            'quantiles': output_handler.quantiles,
            'mrequantiles': output_handler.mrequantiles,
            'tauquantiles': output_handler.tauquantiles,
            'description': output_handler.description,
            'tau': output_handler.tau,
            'branching_factor': output_handler.mre,
        }

    
    data_to_store = pd.DataFrame([data_to_store])
    data_to_store.to_parquet(f"/home/dekorvyb/trash/{animal.short_name}_CA1_wake_04_02_{i}.parquet", index = True)
    
    
    '''

        
    plt.plot(coefficients.steps, coefficients.coefficients, label='data')
            
    plt.plot(coefficients.steps, mre.f_complex(coefficients.steps, *output_handler.popt),
                label='complex m={:.5f}'.format(output_handler.mre))

    plt.legend()
    plt.savefig(f"/home/dekorvyb/trash/graphic{i}.png")
    '''





# %%


overall_activity = np.sum(epoch_ts_group.values, axis=1)


coefficients = mre.coefficients(overall_activity, dtunit='steps', method = 'ts')
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
# %%

from collections import namedtuple

import tools
import loren_frank_helper_functions as lf_helper


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


animal_list = ["gov", "egy"] # done for: frank, bond
area_list = ["CA1", "CA3"]
bin_size = 5 # in ms
window_size = 90 # in seconds
dest_folder_binned_spike_trains = "/local2/Vincent/binned_spiking_data/"
dest_folder_mr_analysis = "/local2/Vincent/mr_analysis_with_new_pipeline/"


for animal_name in animal_list:
    animal = animals_dict[animal_name]
    
    # print(cellinfo_dict_sorted_by_area.keys()) # shows all the areas that were recorded in given animal
    cellinfo_dict_sorted_by_area = lf_helper.create_sorted_dict_with_cellinfos(animal)
    taskinfo_dict_sorted_by_state = lf_helper.create_sorted_dict_with_tasks(animal)

    for area in area_list:
        key = (animal.short_name, area)
        
        neuron_dict = lf_helper.create_neuron_dicts_for_each_state(cellinfo_dict_sorted_by_area[(area,)], taskinfo_dict_sorted_by_state)
        
        binned_spike_trains = lf_helper.load_spikes(neuron_dict, animal, bin_size = bin_size)

        tools.save_binned_spike_trains(binned_spike_trains, dest_folder_binned_spike_trains, key)
        
        tools.run_mr_estimator_on_summed_activity(binned_spike_trains, bin_size, window_size, dest_folder_mr_analysis, key)
        
        
        # in the code above, we converted the dataset with its specific structure into the desired format
        # the goal is to get to the same format with other datasets too, so the rest of the code will work universally

# %%

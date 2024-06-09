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
           'remy': Animal(short_name = 'remy', directory = '/local2/Jan/Remy/Remy/'), # doesn't work, sadly
            "bon" : Animal(short_name = "bon", directory = "/home/dekorvyb/Downloads/Bon/"),
            "Cor" : Animal(short_name = "Cor", directory = "/home/dekorvyb/Downloads/Corriander/"),
            "con" : Animal(short_name = "con", directory = "/home/dekorvyb/Downloads/Con/"),
            "cha" : Animal(short_name = "cha", directory = "/home/dekorvyb/Downloads/Chapati/"),
            "dav" : Animal(short_name = "dav", directory = "/home/dekorvyb/Downloads/Dave/"),   
            "Fiv" : Animal(short_name = "Fiv", directory = "/home/dekorvyb/Downloads/Fiv/"),
            "ten" : Animal(short_name = "ten", directory = "/home/dekorvyb/Downloads/Ten/"),
            "dud" : Animal(short_name = "dud", directory = "/home/dekorvyb/Downloads/Dudley/"),
            "Eig" : Animal(short_name = "Eig", directory = "/home/dekorvyb/Downloads/Eig/"),
            "mil" : Animal(short_name = "mil", directory = "/home/dekorvyb/Downloads/Mil/")
            }
# -> 11 animals in total (remy, Eig and Fiv don't work so far)

# might be useful to write a function which loads the cellinfo files for all animals in animals_dict.
# so we would get an overview of all the areas that were recorded for each animal.

# still missing for Fiv, ten, Mil, Eig
animal_list = ["ten", "mil"] # CA1 and CA3 done for: frank, bond, gov, egy, cha, con, cor, dav


bin_size = 5 # in ms
window_size = 90 # in seconds
dest_folder_binned_spike_trains = "/local2/Vincent/binned_spiking_data/"
dest_folder_mr_analysis = "/local2/Vincent/mr_analysis_with_new_pipeline/"


for animal_name in animal_list:
    
    animal = animals_dict[animal_name]

    try:
        cellinfo_dict_sorted_by_area, recorded_areas = lf_helper.create_sorted_dict_with_cellinfos(animal)
        taskinfo_dict_sorted_by_state = lf_helper.create_sorted_dict_with_tasks(animal)
        print(recorded_areas)
    
    except Exception as e:
        print(e)
        print("failed for animal", animal.short_name)
        continue
    
    # %%


    for area in recorded_areas:
            
        if area[0] == "???":
            continue # because I did them already
            
            
        try:
            print("analyzing for:", area)
                
            key = (animal.short_name, area[0])
                
            neuron_dict = lf_helper.create_neuron_dicts_for_each_state(cellinfo_dict_sorted_by_area[area], taskinfo_dict_sorted_by_state)
                
            binned_spike_trains = lf_helper.load_spikes(neuron_dict, animal, bin_size = bin_size)

            # we can now apply the universal functions
            # the functions themselves will iterate over the dict-structure of binned_spike_trains
            # maybe, it would be more elegant to implement the iteration here, in the work_env, to make the tools - functions independent of the dict structure
                
            tools.save_binned_spike_trains(binned_spike_trains, dest_folder_binned_spike_trains, key)
                
            tools.run_mr_estimator_on_summed_activity(binned_spike_trains, bin_size, window_size, dest_folder_mr_analysis, key)
            
        except Exception as e:
            print(e)
            

# %%

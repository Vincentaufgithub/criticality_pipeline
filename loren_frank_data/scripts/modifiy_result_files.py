# %%

from scipy.io import loadmat
from collections import namedtuple
import os

file = loadmat("/home/dekorvyb/Downloads/Bond/bonspikes03.mat")


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


def generate_info_filename(filename: str):
    global animals_dict
    
    file_infos: list = filename.split("_")
    animal_infos: tuple = animals_dict[file_infos[0]]
    
    return f"{animal_infos.directory}{animal_infos.short_name}spikes{file_infos[3]}.mat"



folder_old = "/local2/Vincent/loren_frank_MR_30s/"
files_old = [f for f in os.listdir(folder_old)]

folder_new = "/local2/Vincent/loren_frank/MR_30s_revised/"


for filename in folder_old:
    
    generate_info_filename(filename)
    extract_recording_start_time
    calculate_chunk_start_time
    append_to_result
    save_result_to_new_folder
    delete_result_from_old_folder
# %%
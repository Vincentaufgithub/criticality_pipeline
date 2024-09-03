# %%






#######################################
# I used this script to revise all the stored files and add the trial timings to each time chunk.
#######################################



from scipy.io import loadmat
from collections import namedtuple
import os
import pandas as pd



# Creating dictionary with animal file paths
# Defining each animal via its short name and its directory
Animal = namedtuple('Animal', {'short_name', 'directory'})

animals_dict = {
    "bon" : Animal(short_name = "bon", directory = "/home/dekorvyb/Downloads/Bond/"),
    "cha" : Animal(short_name = "cha", directory = "/home/dekorvyb/Downloads/Chapati/"),
    "Cor" : Animal(short_name = "Cor", directory = "/home/dekorvyb/Downloads/Corriander/"),
    "con" : Animal(short_name = "con", directory = "/home/dekorvyb/Downloads/Conley/"),
    'fra' : Animal(short_name = 'fra', directory = '/local2/Jan/Frank/Frank/'),
    'gov' : Animal(short_name = 'gov', directory = '/local2/Jan/Government/Government/'),
    'egy' : Animal(short_name = 'egy', directory = '/local2/Jan/Egypt/Egypt/'), 
           #'remy': Animal(short_name = 'remy', directory = '/local2/Jan/Remy/Remy/'), # doesn't work, sadly
    "dav" : Animal(short_name = "dav", directory = "/home/dekorvyb/Downloads/Dave/"),   
            #"Fiv" : Animal(short_name = "Fiv", directory = "/home/dekorvyb/Downloads/Fiv/"),
    "ten" : Animal(short_name = "ten", directory = "/home/dekorvyb/Downloads/Ten/"),
    "dud" : Animal(short_name = "dud", directory = "/home/dekorvyb/Downloads/Dudley/"),
            #"Eig" : Animal(short_name = "Eig", directory = "/home/dekorvyb/Downloads/Eig/"),
    "mil" : Animal(short_name = "mil", directory = "/home/dekorvyb/Downloads/Mil/")
            }

def filename_to_variables(filename):
    name, area, state, day, epoch, chunk = filename.split("_")
    epoch = int(epoch)
    chunk = int(chunk[0:3])
    return name, area, state, day, epoch, chunk




def generate_info_filename(name, day):
    global animals_dict

    animal_infos: tuple = animals_dict[name]
    
    return f"{animal_infos.directory}{animal_infos.short_name}spikes{day}.mat"



def get_recording_start_time(filename: str, epoch: int) -> int:
    
    df = loadmat(filename)['spikes'][0, -1][0, epoch-1]
    
    for tetrode in range(df.shape[1]):
        for neuron in range(df[0,tetrode].shape[1]):
            try:
                timerange = df[0, tetrode][0, neuron]["timerange"][0][0][0]
                # timerange is given in 10kHz unit. Convert to seconds.
                return int(timerange[0] /10000)
                
            except:
                continue
    

def append_to_result(folder: str, filename: str, chunk_start_time: int) -> dict:
    result_file = pd.read_parquet(f"{folder}{filename}")
    result_file["chunk_start_time"] = chunk_start_time
    result_file["chunk_end_time"] = chunk_start_time+30
    return result_file
    


def save_modified_result(folder, filename, dataframe):
    dataframe.to_parquet(f'{folder}{filename}')



def delete_old_file(folder, filename):
    os.remove(f"{folder_old}{filename}")



folder_old = "/local2/Vincent/loren_frank_MR_30s/"
files_old = [f for f in os.listdir(folder_old)]

folder_new = "/local2/Vincent/loren_frank/MR_30s_revised/"

key_list: list = list(animals_dict.keys())



for filename in files_old:
    
    try: 
        name, area, state, day, epoch, chunk = filename_to_variables(filename)
        
        if not name in key_list:
            continue
        
        info_filename: str = generate_info_filename(name, day)
        recording_start_time: int = get_recording_start_time(info_filename, epoch)
        chunk_start_time: int = recording_start_time + (chunk-1)*30 # e.g. second chunk starts after 30s
        modified_result: dict = append_to_result(folder_old, filename, chunk_start_time)
        save_modified_result(folder_new, filename, modified_result)
        delete_old_file(folder_old, filename)
    
    except:
        continue 
    
    
# %%
from scipy.io import loadmat
import loren_frank_data_processing.neurons as lf_neurons 
import pandas as pd
from glob import glob
import numpy as np




def create_sorted_dict_with_cellinfos(animal):
    '''
    loads the cellino file for the animal
    creates a pandas dataframe with relevant information
    sorts the dataframe according to recording area
    returns a dictionary. In the dictionary is one cellinfo_dataframe for each recorded area
    
    '''
    
    # load the cellinfo file of the animal
    cellinfo_filename = f"{animal.directory}{animal.short_name}cellinfo.mat"
    neuron_cellinfo = loadmat(cellinfo_filename)
    
    
    # using loren frank lab, we create a dataframe containing all neuron info for a given animal
    # please don't ask me how it works. It just does, somehow.
    # the function from loren frank lab also creates a unique neuron key for each recorded unit - pretty cool!
    neuron_info_dataframe = pd.concat([
        lf_neurons.convert_neuron_epoch_to_dataframe(epoch, animal.short_name, day_ind + 1, epoch_ind + 1)
        for day_ind, day in enumerate(neuron_cellinfo['cellinfo'].T)
        for epoch_ind, epoch in enumerate(day[0].T)
        ]).sort_index()
    
    neuron_info_dataframe = group_df_to_dict(neuron_info_dataframe, ["area"])
    
    return neuron_info_dataframe



def create_sorted_dict_with_tasks(animal):
    
    # find the names of all task files
    task_files = glob(f"{animal.directory}{animal.short_name}task*.mat"  )
    
    files = pd.concat( load_task(task_file, animal) for task_file in task_files)

    files = group_df_to_dict(files, "type")
    print(files.keys()
          )
    return files
   
   
def group_df_to_dict(df, label):
    dfs = {}
    for idx, group in df.groupby([label]):
        dfs[idx] = group.copy()
    return dfs

    
def load_task(file_name, animal):
    '''
    This function is mostly taken from loren frank lab.
    '''
    
    
    data = loadmat(file_name, variable_names=('task'))['task']
    #print(data.dtype.names)
    
    # data.shape returns a tuple (a,b), b being the number of days in the array
    n_days = data.shape[-1]
    
    epochs = data[0, -1][0]
    n_epochs = len(epochs)
    
    index = pd.MultiIndex.from_product(
        ([animal.short_name], [n_days], np.arange(n_epochs) + 1),
        names=['animal', 'day', 'epoch'])
    

    # Create a DataFrame from a list of dictionaries
    df_list = [
        {name: epoch[name].item().squeeze() 
         for name in epoch.dtype.names if name =='type'}
        for epoch in epochs]
    
    
    df = pd.DataFrame(df_list)

    # Set index and convert data types
    df = df.set_index(index).assign(
        type=lambda df: df.type.astype(str)
    )

    return df

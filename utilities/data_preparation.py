from scipy.io import loadmat
import pandas as pd
import numpy as np



def group_df_to_dict(df, label):
    dfs = {}
    for idx, group in df.groupby([label]):
        dfs[idx] = group.copy()
    return dfs

def load_task_file(file_name, animal):
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


def get_matching_pairs(dataframe, multiindex):
    valid_entries = [row_index[1:] for row_index in multiindex]
    print(valid_entries)
    df_entries = [(row_index[2],row_index[4]) for row_index in dataframe.index]
    
    matching_entries = [entry for entry in valid_entries if entry in df_entries]
    filtered_dataframe = pd.DataFrame()
    
    for matching_entry in matching_entries:
        temp_dataframe = dataframe.loc[(dataframe.index.get_level_values('day') == matching_entry[0]) & (dataframe.index.get_level_values('epoch') == matching_entry[1])]
        filtered_dataframe = pd.concat([filtered_dataframe, temp_dataframe])

    return filtered_dataframe